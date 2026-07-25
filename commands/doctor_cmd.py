"""
commands/doctor_cmd.py

Comando para diagnóstico completo do sistema NEXUS.
"""

from __future__ import annotations

import os
import sys
import platform
from pathlib import Path

from rich.console import Group
from rich.text import Text

from core import ui
from core.response import Resposta
from core.config import (
    CONFIG_HOME,
    LOGS_DIR,
    HISTORY_DIR,
    CACHE_DIR,
    VERSION_FILE,
    PROJECT_ROOT
)

def doctor() -> Resposta:
    """Executa um diagnóstico do sistema e retorna os resultados."""
    checks = []
    passed = 0
    total = 15

    def add_check(name: str, success: bool, details: str):
        nonlocal passed
        if success:
            status = f'[{ui.COR_SUCESSO}]✓[/{ui.COR_SUCESSO}]'
            passed += 1
        else:
            status = f'[{ui.COR_ERRO}]✗[/{ui.COR_ERRO}]'
        checks.append((name, status, details))

    # 1. Python version
    py_version = sys.version_info
    py_ok = py_version >= (3, 10)
    py_details = f"{sys.version.split()[0]}"
    add_check("Python versão >= 3.10", py_ok, py_details)

    # 2. rich installed
    try:
        import rich
        add_check("Biblioteca 'rich'", True, "Instalada")
    except ImportError:
        add_check("Biblioteca 'rich'", False, "Não instalada")

    # 3. psutil installed
    try:
        import psutil
        add_check("Biblioteca 'psutil'", True, f"v{psutil.__version__}")
    except ImportError:
        add_check("Biblioteca 'psutil'", False, "Não instalada")

    # 4. Config directory
    add_check("Diretório Config", CONFIG_HOME.is_dir(), str(CONFIG_HOME))

    # 5. Logs directory
    add_check("Diretório Logs", LOGS_DIR.is_dir(), str(LOGS_DIR))

    # 6. History directory
    add_check("Diretório Histórico", HISTORY_DIR.is_dir(), str(HISTORY_DIR))

    # 7. Cache directory
    add_check("Diretório Cache", CACHE_DIR.is_dir(), str(CACHE_DIR))

    # 8. Config file
    config_file = CONFIG_HOME / 'config.json'
    add_check("Arquivo de Configuração", config_file.is_file(), str(config_file))

    # 9. Config writable
    writable = os.access(CONFIG_HOME, os.W_OK)
    add_check("Permissão de Escrita Config", writable, "Sim" if writable else "Não")

    # 10. version.json
    add_check("Arquivo version.json", VERSION_FILE.is_file(), str(VERSION_FILE))

    # 11. Logo ASCII
    logo_file = PROJECT_ROOT / 'assets' / 'branding' / 'logo_ascii.txt'
    add_check("Logo ASCII", logo_file.is_file(), str(logo_file))

    # 12. Banner ASCII
    banner_file = PROJECT_ROOT / 'assets' / 'branding' / 'banner.txt'
    add_check("Banner ASCII", banner_file.is_file(), str(banner_file))

    # 13. Theme file
    theme_file = PROJECT_ROOT / 'assets' / 'themes' / 'nexus_blue.json'
    add_check("Arquivo de Tema", theme_file.is_file(), str(theme_file))

    # 14. Colors file
    colors_file = PROJECT_ROOT / 'assets' / 'branding' / 'colors.json'
    add_check("Arquivo de Cores", colors_file.is_file(), str(colors_file))

    # 15. Git repository
    git_dir = PROJECT_ROOT / '.git'
    add_check("Repositório Git", git_dir.is_dir(), str(git_dir))

    # Create output
    tabela = ui.tabela("Verificações de Sistema", ["Check", "Status", "Detalhe"], checks)

    header = Text("NEXUS DOCTOR", style=f"bold {ui.COR_NEON}", justify="center")
    group = Group(header, tabela)

    all_passed = passed == total
    if all_passed:
        color = ui.COR_SUCESSO
    elif passed > total / 2:
        color = ui.COR_ALERTA
    else:
        color = ui.COR_ERRO

    summary = f"[{color}]{passed} de {total} verificações OK[/{color}]"

    return Resposta(sucesso=all_passed, mensagem=summary, renderable=group)
