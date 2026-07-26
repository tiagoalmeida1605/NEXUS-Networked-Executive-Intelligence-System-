"""
plugins/calculator/

Plugin de calculadora para o NEXUS.
Comando: calc <expressão>
"""

from __future__ import annotations

from typing import Optional

from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Calculator",
    "versao": "1.0",
    "descricao": "Calculadora aritmética simples (calc 10+20).",
}

# Operações permitidas para eval
_SEGURO = {"__builtins__": {}}, {
    "abs": abs, "round": round, "min": min, "max": max,
    "int": int, "float": float, "pow": pow,
}


def _calc(expressao: Optional[str]) -> Resposta:
    """Avalia uma expressão matemática simples."""
    if not expressao or not expressao.strip():
        return Resposta(
            sucesso=False,
            mensagem='Uso: calc <expressão>\nExemplo: calc (15*8)/2',
        )

    try:
        # Remove espaços e avalia expressão aritmética
        expr = expressao.strip()
        # Valida caracteres permitidos
        if not all(c in "0123456789+-*/().,% " for c in expr):
            return Resposta(sucesso=False, mensagem="Expressão contém caracteres inválidos.")

        resultado = eval(expr, _SEGURO[0], _SEGURO[1])  # noqa: PGH001
        return Resposta(
            sucesso=True,
            mensagem=f"{expr} = {resultado}",
        )
    except ZeroDivisionError:
        return Resposta(sucesso=False, mensagem="Erro: divisão por zero.")
    except (SyntaxError, NameError, TypeError, ValueError) as erro:
        return Resposta(sucesso=False, mensagem=f"Erro na expressão: {erro}")


def registrar(executor) -> None:
    """Registra o comando calc."""
    executor.registrar_plugin("calc", _calc, "Calculadora aritmética (calc 10+20)")
