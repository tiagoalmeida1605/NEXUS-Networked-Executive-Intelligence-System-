"""
commands/info.py

Responsável pelos comandos relacionados a data e hora do sistema.
"""

from datetime import datetime

from core.response import Resposta


def hora() -> Resposta:
    """Retorna a hora atual do sistema."""
    agora = datetime.now().strftime("%H:%M:%S")
    return Resposta(sucesso=True, mensagem=f"Hora atual: {agora}")


def data() -> Resposta:
    """Retorna a data atual do sistema."""
    hoje = datetime.now().strftime("%d/%m/%Y")
    return Resposta(sucesso=True, mensagem=f"Data atual: {hoje}")
