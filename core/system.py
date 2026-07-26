"""
core/system.py

Informações do sistema operacional e identificação do operador.

Módulo leve e reutilizável, sem dependências externas além da stdlib.
Fornece funções para detectar o usuário logado, hostname, tempo ligado
earquitetura da máquina, usadas por toda a aplicação.
"""

from __future__ import annotations

import getpass
import os
import platform
import time
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


def get_uptime() -> float:
    """
    Retorna o tempo de atividade do sistema em segundos.

    No Linux, lê de /proc/uptime. Em outros sistemas, retorna 0.

    Returns:
        float: segundos desde a inicialização do sistema.
    """
    try:
        with open("/proc/uptime", "r") as f:
            return float(f.readline().split()[0])
    except (OSError, IndexError, ValueError):
        return 0.0


def format_uptime(segundos: Optional[float] = None) -> str:
    """
    Formata o uptime em formato legível (dias, horas, minutos).

    Args:
        segundos: tempo em segundos. Se None, obtém automaticamente.

    Returns:
        str: ex.: "2d 14h 32m"
    """
    if segundos is None:
        segundos = get_uptime()
    dias, resto = divmod(int(segundos), 86400)
    horas, resto = divmod(resto, 3600)
    minutos = resto // 60
    partes = []
    if dias:
        partes.append(f"{dias}d")
    if horas:
        partes.append(f"{horas}h")
    if minutos or not partes:
        partes.append(f"{minutos}m")
    return " ".join(partes)


def get_architecture() -> str:
    """
    Retorna a arquitetura da máquina.

    Returns:
        str: ex.: "x86_64"
    """
    return platform.machine()


def get_kernel() -> str:
    """
    Retorna a versão do kernel.

    Returns:
        str: ex.: "6.8.0"
    """
    return platform.release()
