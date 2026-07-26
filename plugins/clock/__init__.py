"""
plugins/clock/

Plugin de relogio para o NEXUS.
Comando: clock
Mostra hora, data e timezone atuais.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Clock",
    "versao": "1.0",
    "descricao": "Exibe hora, data e timezone atuais.",
}


def _clock(alvo: Optional[str] = None) -> Resposta:
    """Exibe a hora, data e timezone atuais.

    Args:
        alvo: ignorado (compatibilidade com a API de plugins).
    """
    agora = datetime.now()
    tz = timezone.utc
    try:
        tz = datetime.now().astimezone().tzinfo or timezone.utc
    except Exception:
        pass

    return Resposta(
        sucesso=True,
        mensagem=(
            f"Hora:     {agora.strftime('%H:%M:%S')}\n"
            f"Data:     {agora.strftime('%d/%m/%Y')}\n"
            f"Timezone: {tz}"
        ),
    )


def registrar(executor) -> None:
    """Registra o comando clock."""
    executor.registrar_plugin("clock", _clock, "Exibe hora, data e timezone")
