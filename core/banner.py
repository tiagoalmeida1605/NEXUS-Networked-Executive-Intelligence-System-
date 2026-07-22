"""
core/banner.py

Experiência de abertura do NEXUS (v0.2.2 — Kernel Identity).

Exibe a logo ASCII oficial, identidade de versão e boot sequence
com o Identity System.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from core import theme
from core.config import carregar_versao

console = Console()


def exibir_banner(config: Dict[str, Any]) -> None:
    """
    Exibe a animação de inicialização e o painel de identidade.

    Args:
        config: configuração do usuário (saudação com o nome).
    """
    usuario = str(config.get("user", "usuário"))
    meta = carregar_versao()
    versao = str(meta.get("label", "v0.2.2 Alpha"))
    codename = str(meta.get("codename", "Kernel Identity"))

    etapas = (
        ("Core", "Core Online"),
        ("Parser", "Parser Online"),
        ("Executor", "Executor Online"),
        ("Update", "Update System Online"),
        ("Identity", "Identity System Online"),
    )

    console.print()
    with console.status(
        Text("Carregando Identity module...", style=f"bold {theme.COR_PRIMARIA}"),
        spinner="dots12",
        spinner_style=theme.COR_NEON,
    ):
        time.sleep(0.4)

    # ── Logo ASCII com revelação linha a linha ────────────────────────────
    logo_linhas = theme.carregar_logo_ascii().splitlines()
    cores = (theme.COR_NEON, theme.COR_PRIMARIA, theme.COR_TECNOLOGICO)

    with Live(console=console, refresh_per_second=18, transient=False) as live:
        acumulado: list = []
        for indice, linha in enumerate(logo_linhas):
            cor = cores[min(indice * len(cores) // max(len(logo_linhas), 1), len(cores) - 1)]
            acumulado.append(Align.center(Text(linha, style=f"bold {cor}")))
            live.update(Group(*acumulado))
            time.sleep(0.06)

    console.print()
    console.print(Align.center(Text("NEXUS", style=f"bold {theme.COR_PRIMARIA}")))
    console.print(
        Align.center(
            Text(
                "Networked Executive Intelligence System",
                style=theme.COR_BRANCO,
            )
        )
    )
    console.print()
    console.print(Align.center(Text(f"Version:  {versao}", style=theme.COR_NEON)))
    console.print(
        Align.center(Text(f"Codename: {codename}", style=theme.COR_TEXTO_SECUNDARIO))
    )
    console.print()
    theme.regra()
    console.print()

    # ── Boot sequence ─────────────────────────────────────────────────────
    linhas_status: list[str] = []
    with Live(console=console, refresh_per_second=12, transient=False) as live:
        for nome, descricao in etapas:
            linhas_status.append(
                f"[bold {theme.COR_SUCESSO}]✓[/] "
                f"[bold {theme.COR_NEON}]{nome:<10}[/] "
                f"[{theme.COR_BRANCO}]{descricao}[/]"
            )
            painel_boot = Panel(
                "\n".join(linhas_status),
                title=Text("STATUS", style=f"bold {theme.COR_BRANCO}"),
                border_style=theme.COR_TECNOLOGICO,
                padding=(0, 2),
                style=f"on {theme.COR_ESCURO}",
            )
            live.update(Align.center(painel_boot))
            time.sleep(0.11)

    console.print()
    console.print(
        Align.center(
            Text("Identity module loaded.", style=f"bold {theme.COR_NEON}")
        )
    )
    console.print()

    # ── Painel de identidade oficial ──────────────────────────────────────
    console.print(
        Align.center(
            theme.painel_identidade(
                versao=versao,
                codename=codename,
                usuario=usuario,
                online=True,
            )
        )
    )
    console.print()
    console.print(
        Align.center(
            Text(
                'Digite "help" para visualizar os comandos.',
                style=theme.COR_TEXTO_SECUNDARIO,
            )
        )
    )
    console.print(
        Align.center(
            Text(
                "↑ ↓ histórico  ·  update  ·  version  ·  shell",
                style=theme.COR_MUTED,
            )
        )
    )
    console.print()
    theme.regra()
    console.print()
