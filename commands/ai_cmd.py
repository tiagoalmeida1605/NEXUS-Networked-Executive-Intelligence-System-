"""
commands/ai_cmd.py

Comandos de Inteligência Artificial do NEXUS v0.5.

Comandos:
    ai              — Abre modo de conversa com IA
    ai status       — Mostra status do sistema de IA
    models          — Lista modelos disponíveis
"""

from __future__ import annotations

from typing import Optional

from rich.align import Align
from rich.console import Group
from rich.text import Text

from core import theme
from core.response import Resposta
from ai.manager import obter_modelo_ativo, processar, status_ollama
from ai.ollama import (
    listar_modelos_config,
    listar_modelos_ollama,
    verificar_ollama,
)
from ai.router import detectar_intencao, role_para_descricao


def ai_mode(alvo: Optional[str] = None) -> Resposta:
    """Modo conversa com IA ou ai status."""
    if alvo and alvo.strip().lower() == "status":
        return ai_status()

    if not verificar_ollama():
        return Resposta(
            sucesso=False,
            mensagem=(
                "NEXUS AI\n\n"
                "Ollama não encontrado.\n"
                "O sistema continuará funcionando sem inteligência artificial."
            ),
        )

    if not listar_modelos_ollama():
        return Resposta(
            sucesso=False,
            mensagem=(
                "NEXUS AI\n\n"
                "Nenhum modelo instalado.\n"
                "Instale um modelo com: ollama pull <modelo>"
            ),
        )

    modelo = obter_modelo_ativo()
    nome_modelo = modelo["name"] if modelo else "Nenhum"

    return Resposta(
        sucesso=True,
        mensagem=(
            f"NEXUS AI ONLINE\n\n"
            f"Model: {nome_modelo}\n\n"
            "Digite sua mensagem (ou 'sair' para encerrar):\n"
            "> "
        ),
    )


def ai_status() -> Resposta:
    """Exibe o status completo do sistema de IA."""
    if not verificar_ollama():
        return Resposta(
            sucesso=False,
            mensagem="NEXUS AI STATUS\n\nOllama: OFFLINE",
        )

    status = status_ollama()
    modelo = obter_modelo_ativo()
    instalados = status.get("modelos_instalados", [])
    config = status.get("modelos_config", [])

    linhas = [
        f"[bold {theme.COR_NEON}]NEXUS AI STATUS[/]",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Ollama:[/]     [bold {theme.COR_SUCESSO}]ONLINE[/]",
    ]

    if modelo:
        linhas.append(
            f"[{theme.COR_TEXTO_SECUNDARIO}]Active model:[/] [bold {theme.COR_BRANCO}]{modelo['name']}[/]"
        )
    else:
        linhas.append(
            f"[{theme.COR_TEXTO_SECUNDARIO}]Active model:[/] [{theme.COR_TEXTO_SECUNDARIO}]Nenhum[/]"
        )

    linhas.extend([
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Installed models:[/]",
    ])

    if instalados:
        for m in instalados:
            linhas.append(f"  [bold {theme.COR_SUCESSO}]✓[/] {m}")
    else:
        linhas.append(f"  [{theme.COR_TEXTO_SECUNDARIO}]Nenhum modelo instalado[/]")

    linhas.extend([
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Configured models:[/]",
    ])

    for m in config:
        status_icone = "✓" if m["instalado"] else "✗"
        cor = theme.COR_SUCESSO if m["instalado"] else theme.COR_ERRO
        linhas.append(
            f"  [{cor}]{status_icone}[/] {m['name']}  "
            f"[{theme.COR_TEXTO_SECUNDARIO}]({m['role']})[/]"
        )

    return Resposta(
        sucesso=True,
        mensagem="AI Status exibido.",
        renderable=theme.painel("AI STATUS", linhas, cor=theme.COR_NEON),
    )


def listar_modelos() -> Resposta:
    """Lista os modelos disponíveis (configurados e instalados)."""
    if not verificar_ollama():
        return Resposta(
            sucesso=False,
            mensagem="NEXUS AI MODELS\n\nOllama não está disponível.",
        )

    config = listar_modelos_config()
    instalados = listar_modelos_ollama()
    ativo = obter_modelo_ativo()
    nome_ativo = ativo["name"].lower() if ativo else None

    if not config:
        return Resposta(
            sucesso=True,
            mensagem="Nenhum modelo configurado em ai/models.json.",
        )

    linhas = [
        f"[bold {theme.COR_NEON}]NEXUS AI MODELS[/]",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Available models:[/]",
    ]

    for m in config:
        instalado = m["id"] in instalados
        is_ativo = nome_ativo and nome_ativo == m["name"].lower()
        icone = "ACTIVE" if is_ativo else ("✓" if instalado else "✗")
        cor = theme.COR_NEON if is_ativo else (
            theme.COR_SUCESSO if instalado else theme.COR_ERRO
        )
        linhas.append(
            f"  [{cor}]{icone}[/] {m['name']}"
        )
        linhas.append(
            f"     [{theme.COR_TEXTO_SECUNDARIO}]Role:[/] {m['role']}"
        )
        linhas.append(
            f"     [{theme.COR_TEXTO_SECUNDARIO}]{m['description']}[/]"
        )

    return Resposta(
        sucesso=True,
        mensagem="Modelos listados.",
        renderable=theme.painel("MODELS", linhas, cor=theme.COR_NEON),
    )
