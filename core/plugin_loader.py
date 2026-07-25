"""
core/plugin_loader.py

Descobre e carrega plugins do diretório plugins/.

Um plugin válido é um arquivo .py em plugins/ que:
    1. Possui um dicionário PLUGIN_INFO com 'nome', 'versao' e 'descricao'.
    2. Define uma função registrar(executor) para registrar comandos.
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List

from core.config import PROJECT_ROOT
from core.logger import logger

if TYPE_CHECKING:
    from core.executor import Executor

PLUGINS_DIR = PROJECT_ROOT / "plugins"


def carregar_plugins(executor: "Executor") -> List[Dict[str, Any]]:
    """
    Descobre e carrega todos os plugins válidos.

    Args:
        executor: instância do executor onde os comandos serão registrados.

    Returns:
        Lista de dicionários PLUGIN_INFO dos plugins carregados.
    """
    carregados: List[Dict[str, Any]] = []

    if not PLUGINS_DIR.is_dir():
        return carregados

    # Ensure plugins/ is importable
    plugins_parent = str(PLUGINS_DIR.parent)
    if plugins_parent not in sys.path:
        sys.path.insert(0, plugins_parent)

    for arquivo in sorted(PLUGINS_DIR.glob("*.py")):
        if arquivo.name.startswith("_"):
            continue  # skip __init__.py etc.

        nome_modulo = f"plugins.{arquivo.stem}"
        try:
            modulo = importlib.import_module(nome_modulo)
        except Exception as erro:
            logger.aviso(f"Plugin '{arquivo.name}': falha ao importar — {erro}")
            continue

        info = getattr(modulo, "PLUGIN_INFO", None)
        if not isinstance(info, dict):
            logger.aviso(f"Plugin '{arquivo.name}': PLUGIN_INFO ausente ou inválido.")
            continue

        campos = ("nome", "versao", "descricao")
        if not all(campo in info for campo in campos):
            logger.aviso(f"Plugin '{arquivo.name}': PLUGIN_INFO incompleto (faltam: {', '.join(c for c in campos if c not in info)}).")
            continue

        registrar = getattr(modulo, "registrar", None)
        if not callable(registrar):
            logger.aviso(f"Plugin '{arquivo.name}': função registrar() ausente.")
            continue

        try:
            registrar(executor)
            carregados.append(dict(info))
            logger.info(f"Plugin carregado: {info['nome']} v{info['versao']}")
        except Exception as erro:
            logger.erro(f"Plugin '{info.get('nome', arquivo.name)}': falha ao registrar — {erro}")

    return carregados
