"""
core/response.py

Responsável por padronizar as respostas geradas pelos comandos e exibi-las
no terminal de forma elegante, utilizando a biblioteca rich.

Nenhum outro módulo deve imprimir diretamente no terminal:
toda saída de texto para o usuário passa por este módulo.
"""

from dataclasses import dataclass

from rich.console import Console

console = Console()


@dataclass
class Resposta:
    """
    Representa o resultado padronizado da execução de um comando.

    Attributes:
        sucesso: indica se o comando foi executado com êxito.
        mensagem: texto a ser exibido ao usuário (pode ter múltiplas linhas).
        encerrar: quando True, sinaliza ao loop principal que o NEXUS deve
            ser encerrado após esta resposta ser exibida.
    """

    sucesso: bool
    mensagem: str
    encerrar: bool = False


def exibir(resposta: Resposta) -> None:
    """
    Exibe uma Resposta no terminal, no padrão visual do NEXUS.

    Args:
        resposta: objeto Resposta a ser exibido.
    """
    if not resposta.mensagem:
        return

    cor = "cyan" if resposta.sucesso else "red"
    console.print(f"[bold {cor}][NEXUS][/bold {cor}]")
    for linha in resposta.mensagem.split("\n"):
        console.print(linha)
    console.print()
