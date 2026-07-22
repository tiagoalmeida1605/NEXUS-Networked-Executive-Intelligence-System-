"""
core/banner.py

Responsável exclusivamente pela experiência de abertura do NEXUS:
a animação de inicialização e o banner ASCII principal, usando Rich.

Nenhuma lógica de comandos vive aqui — apenas apresentação.
"""

from __future__ import annotations

import time
from typing import Any, Dict

from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel
from rich.text import Text

from core import ui
from core.config import carregar_versao

console = Console()

_CARACTERE_REGRA = "═"

# Letreiro ASCII oficial do NEXUS (fonte ANSI Shadow)
ASCII_LOGO = r"""
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
""".strip(
    "\n"
)


def _regra() -> None:
    """Desenha uma linha divisória dupla, no estilo visual do NEXUS."""
    console.rule(style=ui.COR_PRIMARIA, characters=_CARACTERE_REGRA)


def _montar_cabecalho(versao: str, codename: str, linhas_logo: int) -> Group:
    """Monta o bloco superior (logo parcial + identidade)."""
    logo_linhas = ASCII_LOGO.splitlines()[:linhas_logo]
    logo_render = Group(
        *[
            Align.center(f"[bold {ui.COR_PRIMARIA}]{linha}[/bold {ui.COR_PRIMARIA}]")
            for linha in logo_linhas
        ]
    )

    elementos = [
        Align.center(Text(_CARACTERE_REGRA * 52, style=ui.COR_PRIMARIA)),
        Text(""),
        logo_render,
    ]

    if linhas_logo >= len(ASCII_LOGO.splitlines()):
        elementos.extend(
            [
                Text(""),
                Align.center(
                    f"[bold {ui.COR_BRANCO}]Networked Executive Intelligence System[/bold {ui.COR_BRANCO}]"
                ),
                Text(""),
                Align.center(f"[{ui.COR_NEON}]{versao}[/{ui.COR_NEON}]"),
                Align.center(
                    f"[{ui.COR_TEXTO_SECUNDARIO}]Codename: {codename}[/{ui.COR_TEXTO_SECUNDARIO}]"
                ),
                Text(""),
                Align.center(ui.status_indicador(True)),
                Text(""),
                Align.center(Text(_CARACTERE_REGRA * 52, style=ui.COR_PRIMARIA)),
            ]
        )

    return Group(*elementos)


def exibir_banner(config: Dict[str, Any]) -> None:
    """
    Exibe a animação de inicialização seguida do banner principal do NEXUS.

    Args:
        config: dicionário de configuração do usuário,
            usado para personalizar a saudação com o nome.
    """
    usuario = config.get("user", "usuário")
    distro = ui.detectar_distro()
    meta = carregar_versao()
    versao = str(meta.get("label", "v0.2 Alpha"))
    codename = str(meta.get("codename", "Kernel"))

    etapas = (
        ("Kernel", "Núcleo carregado"),
        ("Config", "Configuração em ~/.config/nexus/"),
        ("Logger", "Sistema de logs online"),
        ("History", "Histórico de comandos pronto"),
        ("Parser", "Interpretador online"),
        ("Executor", "Roteador de comandos online"),
        ("Host", f"{distro} detectado"),
    )

    console.print()
    with console.status(
        f"[bold {ui.COR_PRIMARIA}]Inicializando NEXUS Kernel...[/bold {ui.COR_PRIMARIA}]",
        spinner="dots12",
        spinner_style=ui.COR_NEON,
    ):
        time.sleep(0.45)

    # Animação 1: revela o logo linha a linha
    total_linhas = len(ASCII_LOGO.splitlines())
    with Live(console=console, refresh_per_second=20, transient=False) as live:
        for n in range(1, total_linhas + 1):
            live.update(_montar_cabecalho(versao, codename, n))
            time.sleep(0.05)

    console.print()

    # Animação 2: boot sequence com painel progressivo
    linhas_status: list[str] = []
    with Live(console=console, refresh_per_second=12, transient=False) as live:
        for nome, descricao in etapas:
            linhas_status.append(
                f"[bold {ui.COR_SUCESSO}]✔[/bold {ui.COR_SUCESSO}] "
                f"[bold {ui.COR_NEON}]{nome:<8}[/bold {ui.COR_NEON}] "
                f"[{ui.COR_BRANCO}]{descricao}[/{ui.COR_BRANCO}]"
            )
            painel_boot = Panel(
                "\n".join(linhas_status),
                title=f"[bold {ui.COR_BRANCO}]BOOT SEQUENCE[/bold {ui.COR_BRANCO}]",
                border_style=ui.COR_TECNOLOGICO,
                padding=(0, 2),
            )
            live.update(Align.center(painel_boot))
            time.sleep(0.12)

    console.print()
    saudacao = Text.assemble(
        ("Olá, ", ui.COR_BRANCO),
        (f"{usuario}", f"bold {ui.COR_PRIMARIA}"),
        (".", ui.COR_BRANCO),
    )
    console.print(Align.center(saudacao))
    console.print(
        Align.center(
            f"[{ui.COR_TEXTO_SECUNDARIO}]Sistema inicializado com sucesso.[/{ui.COR_TEXTO_SECUNDARIO}]"
        )
    )
    console.print(
        Align.center(
            f'[{ui.COR_TEXTO_SECUNDARIO}]Digite "ajuda" para visualizar os comandos.[/{ui.COR_TEXTO_SECUNDARIO}]'
        )
    )
    console.print(
        Align.center(
            f"[{ui.COR_MUTED}]↑ ↓ navega o histórico  ·  history  ·  update[/{ui.COR_MUTED}]"
        )
    )
    console.print()
    _regra()
    console.print()
