"""
commands/update_cmd.py

Interface de terminal para o sistema de atualização seguro do NEXUS.
"""

from __future__ import annotations

from rich.align import Align
from rich.console import Console
from rich.panel import Panel

from core import ui
from core.response import Resposta
from core.update import InfoAtualizacao, aplicar_atualizacao, verificar_atualizacao

console = Console()


def executar_atualizacao(interativo: bool = True) -> Resposta:
    """
    Verifica e, se confirmado, aplica uma atualização segura.

    Args:
        interativo: quando True, solicita confirmação [S/N] ao usuário.
    """
    with console.status(
        f"[bold {ui.COR_PRIMARIA}]Verificando atualizações...[/bold {ui.COR_PRIMARIA}]",
        spinner="dots12",
        spinner_style=ui.COR_NEON,
    ):
        info = verificar_atualizacao()

    _exibir_painel_update(info)

    if not info.disponivel:
        return Resposta(sucesso=True, mensagem=info.mensagem)

    if interativo:
        try:
            resposta = console.input(
                f"\n[{ui.COR_BRANCO}]Deseja atualizar?[/] "
                f"[bold {ui.COR_NEON}]\\[S/N][/bold {ui.COR_NEON}] "
            ).strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print()
            return Resposta(sucesso=False, mensagem="Atualização cancelada.")

        if resposta not in ("s", "sim", "y", "yes"):
            return Resposta(sucesso=True, mensagem="Atualização cancelada pelo usuário.")

    with console.status(
        f"[bold {ui.COR_PRIMARIA}]Aplicando atualização segura...[/bold {ui.COR_PRIMARIA}]",
        spinner="dots12",
        spinner_style=ui.COR_NEON,
    ):
        resultado = aplicar_atualizacao(info)

    if resultado.sucesso:
        painel = ui.painel(
            "UPDATE OK",
            [
                f"[{ui.COR_SUCESSO}]✔ {resultado.mensagem}[/{ui.COR_SUCESSO}]",
                f"[{ui.COR_TEXTO_SECUNDARIO}]Backup: {resultado.backup}[/{ui.COR_TEXTO_SECUNDARIO}]"
                if resultado.backup
                else "",
            ],
            cor=ui.COR_SUCESSO,
        )
        return Resposta(sucesso=True, mensagem=resultado.mensagem, renderable=painel)

    painel = ui.painel(
        "UPDATE FAILED",
        [
            f"[{ui.COR_ERRO}]✗ {resultado.mensagem}[/{ui.COR_ERRO}]",
        ],
        cor=ui.COR_ERRO,
    )
    return Resposta(sucesso=False, mensagem=resultado.mensagem, renderable=painel)


def _exibir_painel_update(info: InfoAtualizacao) -> None:
    """Renderiza o painel [NEXUS UPDATE] no estilo solicitado."""
    linhas_alt = []
    if info.alteracoes:
        for item in info.alteracoes:
            linhas_alt.append(f"[bold {ui.COR_NEON}]+[/bold {ui.COR_NEON}] {item}")
    else:
        linhas_alt.append(f"[{ui.COR_TEXTO_SECUNDARIO}]Sem notas de alteração.[/{ui.COR_TEXTO_SECUNDARIO}]")

    corpo = "\n".join(
        [
            f"[bold {ui.COR_TEXTO_SECUNDARIO}]Versão atual:[/{ui.COR_TEXTO_SECUNDARIO}]",
            f"[bold {ui.COR_PRIMARIA}]{info.atual_label}[/bold {ui.COR_PRIMARIA}]",
            "",
            f"[bold {ui.COR_TEXTO_SECUNDARIO}]Nova versão:[/{ui.COR_TEXTO_SECUNDARIO}]",
            f"[bold {ui.COR_NEON}]{info.nova_label}[/bold {ui.COR_NEON}]",
            "",
            f"[bold {ui.COR_TEXTO_SECUNDARIO}]Alterações:[/{ui.COR_TEXTO_SECUNDARIO}]",
            *linhas_alt,
            "",
            f"[{ui.COR_MUTED}]{info.mensagem}[/{ui.COR_MUTED}]",
        ]
    )

    painel = Panel(
        corpo,
        title=f"[bold {ui.COR_BRANCO}]NEXUS UPDATE[/bold {ui.COR_BRANCO}]",
        border_style=ui.COR_PRIMARIA,
        padding=(1, 2),
    )
    console.print()
    console.print(Align.center(painel))
    console.print()
