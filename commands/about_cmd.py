"""
commands/about_cmd.py

Comando ``about`` — identidade oficial do NEXUS.

Exibe logo ASCII, versão, codename, descrição e status dos módulos.
"""

from __future__ import annotations

from rich.align import Align
from rich.console import Group
from rich.text import Text

from core import theme
from core.config import carregar_versao
from core.response import Resposta


def about() -> Resposta:
    """Monta a tela oficial About do NEXUS."""
    meta = carregar_versao()
    label = str(meta.get("label", "v0.2.2.1 Alpha"))
    codename = str(meta.get("codename", "Kernel Identity"))
    tema = theme.meta_tema()

    modulos = [
        ("Core", True),
        ("Parser", True),
        ("Executor", True),
        ("Update System", True),
        ("Identity System", True),
        ("Logger", True),
        ("History", True),
        ("Theme (NEXUS Blue)", tema.get("theme_file", False)),
        ("Logo PNG", tema.get("logo_png", False)),
        ("Logo (com fundo)", tema.get("logo_with_background", False)),
    ]

    linhas_modulos = []
    for nome, ativo in modulos:
        marca = "✓" if ativo else "✗"
        cor = theme.COR_SUCESSO if ativo else theme.COR_ERRO
        linhas_modulos.append(f"[{cor}]{marca}[/] {nome}")

    identidade = theme.painel(
        "ABOUT",
        [
            f"[bold {theme.COR_PRIMARIA}]NEXUS[/]",
            "",
            f"[{theme.COR_TEXTO_SECUNDARIO}]Version:[/]  [bold {theme.COR_NEON}]{label}[/]",
            f"[{theme.COR_TEXTO_SECUNDARIO}]Codename:[/] [bold {theme.COR_PRIMARIA}]{codename}[/]",
            "",
            f"[{theme.COR_TEXTO_SECUNDARIO}]Descrição:[/]",
            f"[{theme.COR_BRANCO}]Networked Executive Intelligence System[/]",
            "",
            f"[{theme.COR_TEXTO_SECUNDARIO}]Tema:[/] [bold {theme.COR_NEON}]{theme.nome_tema()}[/]",
        ],
        cor=theme.COR_PRIMARIA,
    )

    status = theme.painel(
        "MODULES",
        linhas_modulos,
        cor=theme.COR_TECNOLOGICO,
    )

    return Resposta(
        sucesso=True,
        mensagem=f"NEXUS {label} — {codename}",
        renderable=Group(
            theme.render_logo_ascii(),
            Text(""),
            Align.center(Text("NEXUS", style=f"bold {theme.COR_PRIMARIA}")),
            Align.center(
                Text(
                    "Networked Executive Intelligence System",
                    style=theme.COR_BRANCO,
                )
            ),
            Text(""),
            identidade,
            status,
        ),
    )
