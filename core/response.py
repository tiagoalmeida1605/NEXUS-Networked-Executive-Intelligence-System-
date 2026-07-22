"""
core/response.py

Responsável por padronizar as respostas geradas pelos comandos e exibi-las
no terminal com a identidade visual do NEXUS.

Um comando pode retornar apenas uma `mensagem` de texto (para confirmações
rápidas, como "Abrindo Brave...") ou também um `renderable` Rich (Panel,
Table, Columns...) para saídas mais elaboradas. Nenhum outro módulo deve
imprimir diretamente no terminal — toda saída passa por aqui.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rich.console import Console, RenderableType

from core import ui

console = Console()


@dataclass
class Resposta:
    """
    Representa o resultado padronizado da execução de um comando.

    Attributes:
        sucesso: indica se o comando foi executado com êxito.
        mensagem: texto simples para confirmações rápidas e para o
            fallback textual quando não há `renderable`.
        renderable: componente Rich opcional (Panel, Table, Columns...)
            usado para saídas mais elaboradas.
        encerrar: quando True, sinaliza ao loop principal que o NEXUS
            deve ser encerrado após esta resposta ser exibida.
    """

    sucesso: bool
    mensagem: str = ""
    renderable: Optional[RenderableType] = None
    encerrar: bool = False


def exibir(resposta: Resposta) -> None:
    """Exibe uma Resposta no terminal, seguindo a identidade visual do NEXUS."""
    if resposta.renderable is not None:
        console.print(resposta.renderable)
        console.print()
        return

    if not resposta.mensagem:
        return

    if resposta.sucesso:
        icone = f"[bold {ui.COR_SUCESSO}]✔[/bold {ui.COR_SUCESSO}]"
    else:
        icone = f"[bold {ui.COR_ERRO}]✗[/bold {ui.COR_ERRO}]"

    linhas = resposta.mensagem.split("\n")
    console.print(f"{icone} [{ui.COR_BRANCO}]{linhas[0]}[/{ui.COR_BRANCO}]")
    for linha in linhas[1:]:
        console.print(f"   [{ui.COR_TEXTO_SECUNDARIO}]{linha}[/{ui.COR_TEXTO_SECUNDARIO}]")
    console.print()
