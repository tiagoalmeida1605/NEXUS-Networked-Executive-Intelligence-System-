"""
core/system.py

Informações do sistema operacional e identificação do operador.

Módulo leve e reutilizável, sem dependências externas além da stdlib.
Fornece funções para detectar o usuário logado e o hostname da máquina,
usadas por toda a aplicação para exibir a identidade do operador.
"""

from __future__ import annotations

import getpass
import platform
from typing import Optional

# Usuário desenvolvedor oficial do NEXUS
_DEV_USER = "tiago"
_DEV_LABEL = "Tiago/dev"


def get_system_user() -> str:
    """
    Retorna o nome do usuário logado no sistema operacional.

    Uses:
        getpass.getuser() — funciona em Linux, macOS e Windows.

    Returns:
        str: nome do usuário do sistema, ou "unknown" em caso de erro.
    """
    try:
        return getpass.getuser()
    except Exception:  # noqa: BLE001
        return "unknown"


def get_operator_name() -> str:
    """
    Retorna o nome de exibição do operador do NEXUS.

    Se o usuário for o desenvolvedor oficial (tiago), exibe "Tiago/dev".
    Caso contrário, exibe o nome do usuário do sistema.

    Returns:
        str: nome formatado do operador.
    """
    usuario = get_system_user()
    if usuario.lower() == _DEV_USER.lower():
        return _DEV_LABEL
    return usuario


def get_hostname() -> str:
    """
    Retorna o hostname da máquina.

    Returns:
        str: nome do host, ou "unknown" em caso de erro.
    """
    try:
        return platform.node()
    except Exception:  # noqa: BLE001
        return "unknown"
