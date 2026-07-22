"""
commands/history_cmd.py

Comandos relacionados ao histórico de comandos do NEXUS.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from core import ui
from core.response import Resposta

if TYPE_CHECKING:
    from core.history import Historico


def exibir_historico(historico: "Historico", limite: Optional[int] = 30) -> Resposta:
    """
    Monta uma tabela com os comandos anteriores.

    Args:
        historico: instância de Historico.
        limite: quantidade máxima de entradas a exibir (mais recentes).
    """
    entradas = historico.listar(limite=limite)
    if not entradas:
        return Resposta(
            sucesso=True,
            mensagem="Nenhum comando no histórico ainda.",
            renderable=ui.painel(
                "HISTORY",
                [f"[{ui.COR_TEXTO_SECUNDARIO}]Histórico vazio.[/{ui.COR_TEXTO_SECUNDARIO}]"],
                cor=ui.COR_PRIMARIA,
            ),
        )

    linhas = []
    total = len(entradas)
    # Numeração crescente; a última linha é a mais recente
    offset = max(0, len(historico.listar()) - total)
    for indice, comando in enumerate(entradas, start=1):
        numero = offset + indice
        linhas.append((str(numero), comando))

    tabela = ui.tabela(
        f"Histórico — {total} comando(s)",
        ["#", "Comando"],
        linhas,
        cor=ui.COR_PRIMARIA,
    )
    return Resposta(
        sucesso=True,
        mensagem=f"{total} comando(s) no histórico.",
        renderable=tabela,
    )


def limpar_historico(historico: "Historico") -> Resposta:
    """Remove todas as entradas do histórico."""
    historico.limpar()
    return Resposta(sucesso=True, mensagem="Histórico limpo.")
