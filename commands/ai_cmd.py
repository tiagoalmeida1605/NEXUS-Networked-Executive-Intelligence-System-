"""
commands/ai_cmd.py

Comandos de Inteligência Artificial do NEXUS v0.4.1.

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
from core.theme import COR_NEON, COR_BRANCO, COR_TEXTO_SECUNDARIO
from core.theme import console as _console

COMANDOS_SAIDA = frozenset({"sair", "exit", "quit"})


def _chat_cabecalho(modelo: str) -> None:
    """Exibe o cabeçalho do chat AI."""
    _console.print(f"[bold {COR_NEON}]✔ NEXUS AI ONLINE[/bold {COR_NEON}]")
    _console.print()
    _console.print(f"[{COR_TEXTO_SECUNDARIO}]Model:[/] {modelo}")
    _console.print()
    _console.print(f"[{COR_BRANCO}]Digite sua mensagem (ou 'sair' para encerrar):[/{COR_BRANCO}]")
    _console.print()


def _chat_loop() -> None:
    """
    Loop interativo do chat de IA.

    Permite que o usuário digite mensagens continuamente até digitar
    'sair', 'exit' ou 'quit'. A função lida com interrupções e erros
    sem nunca derrubar o NEXUS.
    """
    while True:
        try:
            entrada = _console.input(f"[bold {COR_NEON}]>[/bold {COR_NEON}] ")
        except (KeyboardInterrupt, EOFError):
            _console.print(f"\n   [{COR_BRANCO}]Saindo do modo AI...[/{COR_BRANCO}]")
            _console.print()
            return

        texto = entrada.strip()

        if not texto:
            continue

        if texto.lower() in COMANDOS_SAIDA:
            _console.print(f"   [{COR_BRANCO}]Saindo do modo AI...[/{COR_BRANCO}]")
            _console.print()
            return

        _console.print(f"[{COR_TEXTO_SECUNDARIO}]Usuário:[/{COR_TEXTO_SECUNDARIO}]")
        _console.print(f"{texto}")
        _console.print()

        try:
            if not verificar_ollama() or not listar_modelos_ollama():
                _console.print(f"[{COR_NEON}]NEXUS:[/{COR_NEON}]")
                _console.print(f"[{COR_BRANCO}]Nenhum modelo configurado.[/{COR_BRANCO}]")
                _console.print()
                continue

            resultado = processar(texto)

            if resultado.get("sucesso"):
                resposta = resultado.get("resposta", "")
                _console.print(f"[{COR_NEON}]NEXUS:[/{COR_NEON}]")
                _console.print(f"[{COR_BRANCO}]{resposta}[/{COR_BRANCO}]")
            else:
                mensagem = resultado.get("resposta", "Nenhum modelo configurado.")
                _console.print(f"[{COR_NEON}]NEXUS:[/{COR_NEON}]")
                _console.print(f"[{COR_BRANCO}]{mensagem}[/{COR_BRANCO}]")
        except Exception:  # noqa: BLE001
            _console.print(f"[{COR_NEON}]NEXUS:[/{COR_NEON}]")
            _console.print(f"[{COR_BRANCO}]Nenhum modelo configurado.[/{COR_BRANCO}]")

        _console.print()


def ai_mode(alvo: Optional[str] = None) -> Resposta:
    """Modo conversa com IA ou ai status."""
    if alvo and alvo.strip().lower() == "status":
        return ai_status()

    if verificar_ollama() and listar_modelos_ollama():
        modelo = obter_modelo_ativo()
        nome_modelo = modelo["name"] if modelo else "Nenhum"
    else:
        nome_modelo = "Nenhum"

    _chat_cabecalho(nome_modelo)
    _chat_loop()

    return Resposta(sucesso=True, mensagem="Modo AI encerrado.")


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
