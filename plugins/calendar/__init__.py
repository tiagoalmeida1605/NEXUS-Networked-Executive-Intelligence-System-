"""
plugins/calendar/

Plugin de calendario para o NEXUS.
Comando: calendar
Mostra o calendario do mes atual.
"""

from __future__ import annotations

import calendar
from datetime import datetime
from typing import Optional

from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Calendar",
    "versao": "1.0",
    "descricao": "Exibe o calendario mensal.",
}


def _calendar(alvo: Optional[str] = None) -> Resposta:
    """Exibe o calendario do mes atual.

    Args:
        alvo: ignorado (compatibilidade com a API de plugins).
    """
    agora = datetime.now()
    cal = calendar.TextCalendar()
    texto_cal = cal.formatmonth(agora.year, agora.month)

    return Resposta(
        sucesso=True,
        mensagem=f"Calendario de {agora.strftime('%B/%Y')}\n\n{texto_cal}",
    )


def registrar(executor) -> None:
    """Registra o comando calendar."""
    executor.registrar_plugin("calendar", _calendar, "Exibe o calendario mensal")
