"""
commands/reload_cmd.py

Comando ``reload`` — recarrega as configurações do NEXUS.
"""

from __future__ import annotations

from core.config import carregar_config
from core.response import Resposta


def reload_config() -> Resposta:
    """Recarrega as configurações do arquivo ~/.config/nexus/config.json."""
    carregar_config()
    return Resposta(
        sucesso=True,
        mensagem="Configurações recarregadas com sucesso.",
    )
