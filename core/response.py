"""
core/response.py

Responsável por padronizar as respostas geradas pelos comandos e exibi-las
no terminal com a identidade visual do NEXUS.

Um comando pode retornar apenas uma `mensagem` de texto (para confirmações
rápidas, como "Abrindo Brave...") ou também um `renderable` Rich (Panel,
Table, Columns...) para saídas mais elaboradas, como os painéis de
CPU/RAM/disco. Nenhum outro módulo deve imprimir diretamente no terminal —
toda saída passa por aqui, o que preserva compatibilidade: comandos antigos
que só definem `mensagem` continuam funcionando exatamente como antes.
"""

from dataclasses import dataclass
from typing import Optional

from rich.console import Console, RenderableType

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

    icone = "[bold green]✔[/bold green]" if resposta.sucesso else "[bold red]✗[/bold red]"
    linhas = resposta.mensagem.split("\n")
    console.print(f"{icone} {linhas[0]}")
    for linha in linhas[1:]:
        console.print(f"   {linha}")
    console.print()
