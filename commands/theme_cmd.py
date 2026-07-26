"""
commands/theme_cmd.py

Comandos ``theme`` e ``theme list``.
Exibe informações do tema atual e lista temas disponíveis.
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Group
from rich.text import Text

from core import theme
from core.response import Resposta


def theme_info() -> Resposta:
    """Exibe informações do tema ativo."""
    meta = theme.meta_tema()
    paleta = theme.paleta()

    cores = [
        f"[bold {paleta['neon']}]■[/] Neon:       {paleta['neon']}",
        f"[bold {paleta['tech']}]■[/] Tech:       {paleta['tech']}",
        f"[bold {paleta['primary']}]■[/] Primary:    {paleta['primary']}",
        f"[bold {paleta['white']}]■[/] Text:       {paleta['white']}",
        f"[bold {paleta['success']}]■[/] Success:    {paleta['success']}",
        f"[bold {paleta['error']}]■[/] Error:      {paleta['error']}",
        f"[bold {paleta['warning']}]■[/] Warning:    {paleta['warning']}",
    ]

    info = [
        f"[bold {theme.COR_NEON}]{meta.get('theme', 'NEXUS Blue')}[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]ID:[/] {meta.get('theme_id', 'nexus_blue')}",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Assets disponíveis:[/]",
        f"  Logo PNG:    {'✔' if meta.get('logo_png') else '✗'}",
        f"  Logo fundo:  {'✔' if meta.get('logo_with_background') else '✗'}",
        f"  Logo ASCII:  {'✔' if meta.get('logo_ascii') else '✗'}",
        f"  Banner:      {'✔' if meta.get('banner') else '✗'}",
        f"  Cores:       {'✔' if meta.get('colors_file') else '✗'}",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Paleta:[/]",
        *cores,
    ]

    return Resposta(
        sucesso=True,
        mensagem="Tema ativo: NEXUS Blue Theme.",
        renderable=theme.painel("THEME", info, cor=theme.COR_PRIMARIA),
    )


def theme_list() -> Resposta:
    """Lista temas disponíveis no diretório assets/themes/."""
    from core.theme import THEMES_DIR

    temas_encontrados = []
    if THEMES_DIR.is_dir():
        for arquivo in sorted(THEMES_DIR.glob("*.json")):
            temas_encontrados.append(arquivo.stem)

    if not temas_encontrados:
        return Resposta(
            sucesso=False,
            mensagem="Nenhum tema encontrado em assets/themes/.",
        )

    linhas = [
        f"[{theme.COR_TEXTO_SECUNDARIO}]Temas disponíveis:[/]",
        *[f"  • [bold {theme.COR_NEON}]{t}[/]" for t in temas_encontrados],
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Ativo:[/] [bold {theme.COR_PRIMARIA}]{theme.nome_tema()}[/]",
    ]

    return Resposta(
        sucesso=True,
        mensagem=f"{len(temas_encontrados)} tema(s) encontrado(s).",
        renderable=theme.painel("THEME LIST", linhas, cor=theme.COR_TECNOLOGICO),
    )
