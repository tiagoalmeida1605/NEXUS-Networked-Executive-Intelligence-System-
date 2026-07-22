"""
core/update.py

Sistema de atualização seguro do NEXUS.

Fluxo:
    1. Verifica versão atual (version.json)
    2. Consulta o remoto Git (tags / branch tracking)
    3. Exibe alterações
    4. Pede confirmação
    5. Cria backup em ~/.config/nexus/cache/backups/
    6. Aplica a atualização
    7. Restaura o backup caso algo dê errado
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

from core.config import CACHE_DIR, PROJECT_ROOT, carregar_versao, garantir_estrutura
from core.logger import logger


@dataclass
class InfoAtualizacao:
    """Resultado da verificação de atualização."""

    atual_label: str
    atual_versao: str
    nova_label: str
    nova_versao: str
    disponivel: bool
    alteracoes: List[str] = field(default_factory=list)
    origem: str = ""
    mensagem: str = ""


@dataclass
class ResultadoAtualizacao:
    """Resultado da aplicação de uma atualização."""

    sucesso: bool
    mensagem: str
    backup: Optional[Path] = None
    restaurado: bool = False


def verificar_atualizacao() -> InfoAtualizacao:
    """
    Compara a versão local com a do remoto Git (quando disponível).

    Returns:
        InfoAtualizacao: estado da verificação.
    """
    meta = carregar_versao()
    atual_versao = str(meta.get("version", "0.0.0"))
    atual_label = str(meta.get("label", f"v{atual_versao}"))
    alteracoes_locais = [str(item) for item in meta.get("changelog", [])]

    if not (PROJECT_ROOT / ".git").exists():
        return InfoAtualizacao(
            atual_label=atual_label,
            atual_versao=atual_versao,
            nova_label=atual_label,
            nova_versao=atual_versao,
            disponivel=False,
            alteracoes=alteracoes_locais,
            mensagem="Repositório Git não detectado. Atualização automática indisponível.",
        )

    fetch = _rodar(["git", "fetch", "--tags", "--quiet"], cwd=PROJECT_ROOT)
    if fetch.returncode != 0:
        return InfoAtualizacao(
            atual_label=atual_label,
            atual_versao=atual_versao,
            nova_label=atual_label,
            nova_versao=atual_versao,
            disponivel=False,
            alteracoes=alteracoes_locais,
            mensagem=(
                "Não foi possível consultar o remoto.\n"
                f"{(fetch.stderr or fetch.stdout).strip()}"
            ),
        )

    remoto = _descobrir_remoto()
    if not remoto:
        return InfoAtualizacao(
            atual_label=atual_label,
            atual_versao=atual_versao,
            nova_label=atual_label,
            nova_versao=atual_versao,
            disponivel=False,
            alteracoes=alteracoes_locais,
            mensagem="Nenhum branch de tracking remoto encontrado.",
        )

    remota_meta = _ler_version_remota(remoto)
    if remota_meta is None:
        # Fallback: commits à frente no remoto
        ahead = _commits_a_frente(remoto)
        if ahead <= 0:
            return InfoAtualizacao(
                atual_label=atual_label,
                atual_versao=atual_versao,
                nova_label=atual_label,
                nova_versao=atual_versao,
                disponivel=False,
                alteracoes=alteracoes_locais,
                origem=remoto,
                mensagem="NEXUS já está na versão mais recente.",
            )
        return InfoAtualizacao(
            atual_label=atual_label,
            atual_versao=atual_versao,
            nova_label=f"remoto ({remoto})",
            nova_versao=atual_versao,
            disponivel=True,
            alteracoes=_listar_commits(remoto) or [f"{ahead} commit(s) novo(s) no remoto"],
            origem=remoto,
            mensagem=f"{ahead} commit(s) disponível(is) em {remoto}.",
        )

    nova_versao = str(remota_meta.get("version", atual_versao))
    nova_label = str(remota_meta.get("label", f"v{nova_versao}"))
    alteracoes = [str(item) for item in remota_meta.get("changelog", [])] or alteracoes_locais
    disponivel = _comparar_versoes(nova_versao, atual_versao) > 0

    return InfoAtualizacao(
        atual_label=atual_label,
        atual_versao=atual_versao,
        nova_label=nova_label,
        nova_versao=nova_versao,
        disponivel=disponivel,
        alteracoes=alteracoes,
        origem=remoto,
        mensagem=(
            "Nova versão disponível."
            if disponivel
            else "NEXUS já está na versão mais recente."
        ),
    )


def aplicar_atualizacao(info: InfoAtualizacao) -> ResultadoAtualizacao:
    """
    Aplica a atualização com backup e rollback automático em caso de falha.

    Args:
        info: resultado prévio de verificar_atualizacao().

    Returns:
        ResultadoAtualizacao: status da operação.
    """
    if not info.disponivel:
        return ResultadoAtualizacao(sucesso=False, mensagem=info.mensagem or "Nada a atualizar.")

    if not info.origem:
        return ResultadoAtualizacao(
            sucesso=False,
            mensagem="Origem remota desconhecida. Atualização abortada.",
        )

    logger.atualizacao(f"Iniciando atualização: {info.atual_label} → {info.nova_label}")
    backup = criar_backup()
    logger.atualizacao(f"Backup criado em {backup}")

    pull = _rodar(["git", "pull", "--ff-only"], cwd=PROJECT_ROOT)
    if pull.returncode != 0:
        logger.falha(f"Falha no git pull: {(pull.stderr or pull.stdout).strip()}")
        restaurado = restaurar_backup(backup)
        return ResultadoAtualizacao(
            sucesso=False,
            mensagem=(
                "Falha ao aplicar a atualização.\n"
                f"{(pull.stderr or pull.stdout).strip()}\n"
                + ("Backup restaurado." if restaurado else "Não foi possível restaurar o backup.")
            ),
            backup=backup,
            restaurado=restaurado,
        )

    # Reinstala dependências se requirements.txt existir
    requirements = PROJECT_ROOT / "requirements.txt"
    if requirements.exists():
        venv_python = PROJECT_ROOT / "venv" / "bin" / "python"
        python_bin = str(venv_python) if venv_python.exists() else "python3"
        deps = _rodar(
            [python_bin, "-m", "pip", "install", "-r", str(requirements), "-q"],
            cwd=PROJECT_ROOT,
        )
        if deps.returncode != 0:
            logger.falha("Falha ao atualizar dependências — iniciando rollback.")
            restaurado = restaurar_backup(backup)
            return ResultadoAtualizacao(
                sucesso=False,
                mensagem=(
                    "Atualização do código ok, mas as dependências falharam.\n"
                    + ("Backup restaurado." if restaurado else "Rollback falhou.")
                ),
                backup=backup,
                restaurado=restaurado,
            )

    logger.sucesso(f"Atualizado para {info.nova_label}")
    return ResultadoAtualizacao(
        sucesso=True,
        mensagem=f"NEXUS atualizado com sucesso para {info.nova_label}.",
        backup=backup,
    )


def criar_backup() -> Path:
    """
    Cria um backup compactado do projeto em ~/.config/nexus/cache/backups/.

    Returns:
        Path: caminho do arquivo .tar.gz gerado.
    """
    garantir_estrutura()
    destino_dir = CACHE_DIR / "backups"
    destino_dir.mkdir(parents=True, exist_ok=True)

    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S")
    meta = carregar_versao()
    versao = str(meta.get("version", "unknown")).replace(".", "_")
    arquivo = destino_dir / f"nexus_{versao}_{carimbo}"

    # Exclui ambientes virtuais e metadados Git do backup de código
    ignore = shutil.ignore_patterns(
        "venv",
        ".venv",
        "__pycache__",
        "*.pyc",
        ".git",
        ".idea",
        "*.egg-info",
    )
    staging = destino_dir / f".staging_{carimbo}"
    try:
        shutil.copytree(PROJECT_ROOT, staging, ignore=ignore, dirs_exist_ok=False)
        arquivo_final = Path(shutil.make_archive(str(arquivo), "gztar", root_dir=staging))
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)

    _limpar_backups_antigos(destino_dir, manter=5)
    return arquivo_final


def restaurar_backup(backup: Path) -> bool:
    """
    Restaura o projeto a partir de um arquivo de backup .tar.gz.

    Args:
        backup: caminho do arquivo gerado por criar_backup().

    Returns:
        bool: True se a restauração foi bem-sucedida.
    """
    if not backup.exists():
        logger.falha(f"Backup inexistente: {backup}")
        return False

    staging = CACHE_DIR / "backups" / f".restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        staging.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(str(backup), extract_dir=staging)

        # O archive contém a pasta raiz do projeto
        conteudo = [p for p in staging.iterdir() if p.is_dir()]
        origem = conteudo[0] if len(conteudo) == 1 else staging

        for item in origem.iterdir():
            destino = PROJECT_ROOT / item.name
            if destino.exists():
                if destino.is_dir():
                    shutil.rmtree(destino)
                else:
                    destino.unlink()
            shutil.move(str(item), str(destino))

        logger.atualizacao(f"Backup restaurado a partir de {backup.name}")
        return True
    except Exception as erro:  # noqa: BLE001
        logger.falha(f"Erro ao restaurar backup: {erro}")
        return False
    finally:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)


def _rodar(comando: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    """Executa um comando de subprocesso capturando stdout/stderr."""
    try:
        return subprocess.run(
            list(comando),
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as erro:
        return subprocess.CompletedProcess(
            args=list(comando),
            returncode=127,
            stdout="",
            stderr=str(erro),
        )


def _descobrir_remoto() -> Optional[str]:
    """Descobre o ref de tracking do branch atual (ex.: origin/main)."""
    resultado = _rodar(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        cwd=PROJECT_ROOT,
    )
    if resultado.returncode == 0:
        return resultado.stdout.strip() or None

    # Fallback comum
    for candidato in ("origin/main", "origin/master"):
        checagem = _rodar(["git", "rev-parse", "--verify", candidato], cwd=PROJECT_ROOT)
        if checagem.returncode == 0:
            return candidato
    return None


def _ler_version_remota(remoto: str) -> Optional[dict]:
    """Lê version.json do tip do remoto sem fazer checkout."""
    resultado = _rodar(["git", "show", f"{remoto}:version.json"], cwd=PROJECT_ROOT)
    if resultado.returncode != 0:
        return None
    try:
        dados = json.loads(resultado.stdout)
        return dados if isinstance(dados, dict) else None
    except json.JSONDecodeError:
        return None


def _commits_a_frente(remoto: str) -> int:
    """Conta commits no remoto que ainda não estão no HEAD local."""
    resultado = _rodar(["git", "rev-list", "--count", f"HEAD..{remoto}"], cwd=PROJECT_ROOT)
    if resultado.returncode != 0:
        return 0
    try:
        return int(resultado.stdout.strip() or "0")
    except ValueError:
        return 0


def _listar_commits(remoto: str, limite: int = 8) -> List[str]:
    """Lista mensagens de commit disponíveis no remoto."""
    resultado = _rodar(
        ["git", "log", f"HEAD..{remoto}", f"--pretty=format:%s", f"-n{limite}"],
        cwd=PROJECT_ROOT,
    )
    if resultado.returncode != 0 or not resultado.stdout.strip():
        return []
    return [linha.strip() for linha in resultado.stdout.splitlines() if linha.strip()]


def _comparar_versoes(a: str, b: str) -> int:
    """
    Compara duas versões semânticas simplificadas (X.Y.Z).

    Returns:
        int: >0 se a > b, 0 se iguais, <0 se a < b.
    """

    def partes(valor: str) -> List[int]:
        numeros = [int(n) for n in re.findall(r"\d+", valor)]
        while len(numeros) < 3:
            numeros.append(0)
        return numeros[:3]

    pa, pb = partes(a), partes(b)
    return (pa > pb) - (pa < pb)


def _limpar_backups_antigos(diretorio: Path, manter: int = 5) -> None:
    """Mantém apenas os N backups mais recentes."""
    arquivos = sorted(
        diretorio.glob("nexus_*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for antigo in arquivos[manter:]:
        try:
            antigo.unlink()
        except OSError:
            pass
