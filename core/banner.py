"""
core/banner.py

Experiência de abertura do NEXUS (v0.2.2.1 — Kernel Identity).

Fluxo:
    1. Banner ASCII (letreiro NEXUS)
    2. Painel de identidade oficial
"""

from __future__ import annotations

import time
from typing import Any, Dict

from rich.align import Align
from rich.console import Console
from rich.text import Text

from core import theme
from core.config import carregar_versao

console = Console()


def exibir_banner(config: Dict[str, Any]) -> None:
    """
    Exibe o banner ASCII e o painel de identidade.

    Args:
        config: configuração do usuário (saudação / nome).
    """
    usuario = str(config.get("user", "usuário"))
    meta = carregar_versao()
    versao = str(meta.get("label", "v0.2.2.1 Alpha"))
    codename = str(meta.get("codename", "Kernel Identity"))

    console.print()
    with console.status(
        Text("Carregando NEXUS Identity...", style=f"bold {theme.COR_PRIMARIA}"),
        spinner="dots12",
        spinner_style=theme.COR_NEON,
    ):
        time.sleep(0.35)

    # 1) Banner ASCII completo
    console.print(theme.render_banner_ascii())
    console.print()
    console.print(
        Align.center(
            Text(
                "Networked Executive Intelligence System",
                style=theme.COR_BRANCO,
            )
        )
    )
    console.print()
    theme.regra()
    console.print()

    # 2) Painel de identidade
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
            Text("Identity module loaded.", style=f"bold {theme.COR_NEON}")
        )
    )
    console.print(
        Align.center(
            Text(
                'Digite "help" ou "about" para saber mais.',
                style=theme.COR_TEXTO_SECUNDARIO,
            )
        )
    )
    console.print()
    theme.regra()
    console.print()
