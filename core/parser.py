"""
core/parser.py

Responsável exclusivamente por interpretar a entrada de texto do usuário
e transformá-la em uma estrutura de comando (ação + alvo).

O parser NUNCA executa nada — apenas interpreta.
Quem executa é o core/executor.py.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Comando:
    """
    Representa um comando já interpretado, pronto para ser executado.

    Attributes:
        acao: a ação principal reconhecida (ex.: "abrir", "cpu", "sair").
        alvo: o complemento da ação, quando existir (ex.: "brave").
        bruto: o texto original digitado pelo usuário.
    """

    acao: str
    alvo: Optional[str] = None
    bruto: str = ""


class Parser:
    """Interpreta strings digitadas pelo usuário e gera objetos Comando."""

    def interpretar(self, entrada: str) -> Comando:
        """
        Interpreta a entrada bruta do usuário.

        Exemplo:
            entrada: "abrir brave"
            resultado: Comando(acao="abrir", alvo="brave")

        Args:
            entrada: texto digitado pelo usuário no prompt.

        Returns:
            Comando: objeto contendo a ação e o alvo identificados.
        """
        texto = entrada.strip().lower()

        if not texto:
            return Comando(acao="vazio", bruto=entrada)

        partes = texto.split(maxsplit=1)
        acao = partes[0]
        alvo = partes[1].strip() if len(partes) > 1 else None

        if acao == "abrir" and alvo:
            return Comando(acao="abrir", alvo=alvo, bruto=entrada)

        return Comando(acao=texto, alvo=None, bruto=entrada)
