"""
core/parser.py

Responsável exclusivamente por interpretar a entrada de texto do usuário
e transformá-la em uma estrutura de comando (ação + alvo).

O parser NUNCA executa nada — apenas interpreta.
Quem executa é o core/executor.py.
"""

from __future__ import annotations

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


# Ações internas do NEXUS onde o alvo preserva maiúsculas/minúsculas.
# "shell" preserva o restante da linha como comando do SO.
_ACOES_CASE_SENSITIVE = frozenset({"shell"})


class Parser:
    """Interpreta strings digitadas pelo usuário e gera objetos Comando."""

    def interpretar(self, entrada: str) -> Comando:
        """
        Interpreta a entrada bruta do usuário.

        Exemplo:
            entrada: "abrir brave"
            resultado: Comando(acao="abrir", alvo="brave")

            entrada: "shell ls -la"
            resultado: Comando(acao="shell", alvo="ls -la")

        Args:
            entrada: texto digitado pelo usuário no prompt.

        Returns:
            Comando: objeto contendo a ação e o alvo identificados.
        """
        bruto = entrada
        texto = entrada.strip()

        if not texto:
            return Comando(acao="vazio", bruto=bruto)

        partes_originais = texto.split(maxsplit=1)
        acao = partes_originais[0].lower()
        alvo_original = partes_originais[1] if len(partes_originais) > 1 else None

        if acao in _ACOES_CASE_SENSITIVE:
            return Comando(acao=acao, alvo=alvo_original, bruto=bruto)

        texto_lower = texto.lower()
        partes = texto_lower.split(maxsplit=1)
        alvo = partes[1].strip() if len(partes) > 1 else None

        return Comando(acao=acao, alvo=alvo, bruto=bruto)
