"""
commands/update_cmd.py

Interface de terminal para o sistema de atualização seguro do NEXUS.
"""

from __future__ import annotations

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

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
        Text("Verificando atualizações...", style=f"bold {ui.COR_PRIMARIA}"),
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
                Text.assemble(
                    ("\nDeseja atualizar? ", ui.COR_BRANCO),
                    ("[S/N] ", f"bold {ui.COR_NEON}"),
                )
            ).strip().lower()
        except (KeyboardInterrupt, EOFError):
            console.print()
            return Resposta(sucesso=False, mensagem="Atualização cancelada.")

        if resposta not in ("s", "sim", "y", "yes"):
            return Resposta(sucesso=True, mensagem="Atualização cancelada pelo usuário.")

    with console.status(
        Text("Aplicando atualização segura...", style=f"bold {ui.COR_PRIMARIA}"),
        spinner="dots12",
        spinner_style=ui.COR_NEON,
    ):
        resultado = aplicar_atualizacao(info)

    if resultado.sucesso:
        linhas = [f"✔ {resultado.mensagem}"]
        if resultado.backup:
            linhas.append(f"Backup: {resultado.backup}")
        painel = ui.painel("UPDATE OK", linhas, cor=ui.COR_SUCESSO)
        return Resposta(sucesso=True, mensagem=resultado.mensagem, renderable=painel)

    painel = ui.painel(
        "UPDATE FAILED",
        [f"✗ {resultado.mensagem}"],
        cor=ui.COR_ERRO,
    )
    return Resposta(sucesso=False, mensagem=resultado.mensagem, renderable=painel)


def _exibir_painel_update(info: InfoAtualizacao) -> None:
    """Renderiza o painel [NEXUS UPDATE] no estilo solicitado."""
    texto = Text()
    texto.append("Versão atual:\n", style=f"bold {ui.COR_TEXTO_SECUNDARIO}")
    texto.append(f"{info.atual_label}\n\n", style=f"bold {ui.COR_PRIMARIA}")
    texto.append("Nova versão:\n", style=f"bold {ui.COR_TEXTO_SECUNDARIO}")
    texto.append(f"{info.nova_label}\n\n", style=f"bold {ui.COR_NEON}")
    texto.append("Alterações:\n", style=f"bold {ui.COR_TEXTO_SECUNDARIO}")

    if info.alteracoes:
        for item in info.alteracoes:
            texto.append("+ ", style=f"bold {ui.COR_NEON}")
            texto.append(f"{item}\n", style=ui.COR_BRANCO)
    else:
        texto.append("Sem notas de alteração.\n", style=ui.COR_TEXTO_SECUNDARIO)

    texto.append(f"\n{info.mensagem}", style=ui.COR_MUTED)

    painel = Panel(
        texto,
        title=Text("NEXUS UPDATE", style=f"bold {ui.COR_BRANCO}"),
        border_style=ui.COR_PRIMARIA,
        padding=(1, 2),
    )
    console.print()
    console.print(Align.center(painel))
    console.print()
