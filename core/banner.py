"""
core/banner.py

Responsável exclusivamente pela experiência de abertura do NEXUS:
a animação de inicialização e o banner principal, usando Rich.

Nenhuma lógica de comandos vive aqui — apenas apresentação.
"""

import time
from typing import Any, Dict

from rich.align import Align
from rich.console import Console

from core import ui

console = Console()

VERSAO = "v0.1.5 Alpha"
CODENAME = "Launch"

_CARACTERE_REGRA = "═"


def _regra() -> None:
    """Desenha uma linha divisória dupla, no estilo visual do NEXUS."""
    console.rule(style=ui.COR_PRIMARIA, characters=_CARACTERE_REGRA)


def exibir_banner(config: Dict[str, Any]) -> None:
    """
    Exibe a animação de inicialização seguida do banner principal do NEXUS.

    Args:
        config: dicionário de configuração carregado de config/config.json,
            usado para personalizar a saudação com o nome do usuário.
    """
    usuario = config.get("user", "usuário")
    distro = ui.detectar_distro()

    etapas = (
        "Core Online",
        "Parser Online",
        "Executor Online",
        "Configuração carregada",
        f"{distro} detectado",
    )

    with console.status(
        f"[bold {ui.COR_PRIMARIA}]Inicializando NEXUS...[/bold {ui.COR_PRIMARIA}]",
        spinner="dots",
    ):
        time.sleep(0.7)

    console.print()
    _regra()
    console.print()
    console.print(Align.center(f"[bold {ui.COR_PRIMARIA}]N E X U S[/bold {ui.COR_PRIMARIA}]"))
    console.print(Align.center("[white]Networked Executive Intelligence System[/white]"))
    console.print()
    console.print(Align.center(f"[{ui.COR_TEXTO_SECUNDARIO}]Version:  {VERSAO}[/{ui.COR_TEXTO_SECUNDARIO}]"))
    console.print(Align.center(f"[{ui.COR_TEXTO_SECUNDARIO}]Codename: {CODENAME}[/{ui.COR_TEXTO_SECUNDARIO}]"))
    console.print()
    _regra()
    console.print()
    console.print(Align.center("[bold]STATUS[/bold]"))
    console.print()

    for etapa in etapas:
        console.print(Align.center(f"[bold {ui.COR_SUCESSO}]✔[/bold {ui.COR_SUCESSO}] {etapa}"))
        time.sleep(0.12)

    console.print()
    _regra()
    console.print()
    console.print(Align.center(f"[bold]Olá, {usuario}.[/bold]"))
    console.print(Align.center("Sistema inicializado com sucesso."))
    console.print(Align.center('Digite "ajuda" para visualizar os comandos.'))
    console.print()
    _regra()
    console.print()
