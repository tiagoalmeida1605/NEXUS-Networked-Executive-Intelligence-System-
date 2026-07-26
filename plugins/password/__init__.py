"""
plugins/password/

Plugin de geração de senhas para o NEXUS.
Comando: password [tamanho]
"""

from __future__ import annotations

import secrets
import string
from typing import Optional

from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Password Generator",
    "versao": "1.0",
    "descricao": "Gera senhas fortes aleatórias.",
}

_TAMANHO_PADRAO = 16
_TAMANHO_MAXIMO = 128
_CARACTERES = string.ascii_letters + string.digits + "!@#$%&*"


def _password(tamanho: Optional[str] = None) -> Resposta:
    """Gera uma senha forte com o tamanho especificado."""
    try:
        tam = int(tamanho) if tamanho and tamanho.strip().isdigit() else _TAMANHO_PADRAO
    except (ValueError, TypeError):
        tam = _TAMANHO_PADRAO

    if tam < 4:
        return Resposta(sucesso=False, mensagem="Tamanho mínimo: 4 caracteres.")
    if tam > _TAMANHO_MAXIMO:
        tam = _TAMANHO_MAXIMO

    senha = "".join(secrets.choice(_CARACTERES) for _ in range(tam))
    return Resposta(
        sucesso=True,
        mensagem=f"Senha gerada ({tam} caracteres): {senha}",
    )


def registrar(executor) -> None:
    """Registra o comando password."""
    executor.registrar_plugin("password", _password, "Gera senha forte (password [tamanho])")
