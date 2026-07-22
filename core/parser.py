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


# Ações internas do NEXUS que aceitam complemento (alvo / subcomando).
# "shell" preserva o restante da linha como comando do SO (sem lower no alvo útil
# — o lower é aplicado na linha toda; comandos de shell costumam ser case-sensitive
# em argumentos, mas a ação em si é normalizada).
_ACOES_COM_ALVO = frozenset(
    {
        "abrir",
        "history",
        "historico",
        "shell",
    }
)


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

        # Ação sempre em minúsculas; o alvo de "shell" preserva o original
        # (após o primeiro token) para não alterar argumentos do SO.
        partes_originais = texto.split(maxsplit=1)
        acao = partes_originais[0].lower()
        alvo_original = partes_originais[1] if len(partes_originais) > 1 else None

        if acao == "shell":
            return Comando(acao="shell", alvo=alvo_original, bruto=bruto)

        texto_lower = texto.lower()
        partes = texto_lower.split(maxsplit=1)
        acao = partes[0]
        alvo = partes[1].strip() if len(partes) > 1 else None

        if acao in _ACOES_COM_ALVO:
            return Comando(acao=acao, alvo=alvo, bruto=bruto)

        # Comandos internos de uma palavra (ou frases exatas já lowercased)
        return Comando(acao=texto_lower, alvo=None, bruto=bruto)
