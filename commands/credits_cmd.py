"""
commands/credits_cmd.py

Comando ``credits`` — exibe os créditos do NEXUS.
"""

from __future__ import annotations

from rich.console import Group
from rich.text import Text

from core import theme
from core.response import Resposta


def credits() -> Resposta:
    """Exibe os créditos oficiais do NEXUS."""
    conteudo = [
        f"[bold {theme.COR_PRIMARIA}]NEXUS[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Networked Executive Intelligence System[/]",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Autor:[/]  [bold {theme.COR_BRANCO}]Tiago Silvestre[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Tema:[/]   [bold {theme.COR_NEON}]{theme.nome_tema()}[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Stack:[/]   Python 3 · Rich · psutil",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Plataforma:[/] Linux Mint",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Licença:[/] MIT",
    ]

    painel = theme.painel("CREDITS", conteudo, cor=theme.COR_PRIMARIA)
    return Resposta(
        sucesso=True,
        mensagem="Créditos do NEXUS.",
        renderable=Group(
            theme.render_logo_ascii(),
            Text(""),
            painel,
        ),
    )
