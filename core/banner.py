"""
core/banner.py

Responsável exclusivamente por exibir a tela inicial do NEXUS,
com o status de carregamento dos módulos principais.
"""

import platform

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

console = Console()

VERSAO = "v0.1 Alpha"
CODENAME = "Boot"


def exibir_banner() -> None:
    """Exibe o banner inicial do sistema e o status de carregamento dos módulos."""
    titulo = (
        "[bold cyan]NEXUS[/bold cyan]\n"
        "[white]Networked Executive Intelligence System[/white]\n"
        f"[dim]{VERSAO}  •  Codename: {CODENAME}[/dim]"
    )
    console.print()
    console.print(Panel(Align.center(titulo), border_style="cyan", padding=(1, 6)))
    console.print()

    console.print("  [bold green]✔[/bold green] Core carregado")
    console.print("  [bold green]✔[/bold green] Parser iniciado")
    console.print("  [bold green]✔[/bold green] Executor iniciado")
    console.print(
        f"  [bold green]✔[/bold green] Sistema operacional detectado: [bold]{platform.system()}[/bold]"
    )
    console.print()
    console.print("[bold]Sistema inicializado com sucesso.[/bold]")
    console.print("Todos os módulos estão operacionais.")
    console.print('Digite "ajuda" para visualizar os comandos.')
    console.print()
