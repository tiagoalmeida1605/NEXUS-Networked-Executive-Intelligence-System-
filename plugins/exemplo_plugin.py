"""
plugins/exemplo_plugin.py

Plugin de exemplo do NEXUS — demonstra a API de plugins.

Todo plugin precisa de:
    1. PLUGIN_INFO: dicionário com 'nome', 'versao' e 'descricao'
    2. registrar(executor): função que registra comandos no executor
"""

from __future__ import annotations

from typing import Optional

from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Exemplo",
    "versao": "1.0",
    "descricao": "Plugin de demonstração do NEXUS.",
}


def _ping(alvo: Optional[str] = None) -> Resposta:
    """Responde com um PONG para testar o sistema de plugins.

    Args:
        alvo: ignorado (compatibilidade com a API de plugins).
    """
    return Resposta(sucesso=True, mensagem="NEXUS PONG ✓")


def registrar(executor) -> None:
    """Registra os comandos deste plugin no executor."""
    executor.registrar_plugin("ping", _ping, "Testa o sistema de plugins (PONG)")
