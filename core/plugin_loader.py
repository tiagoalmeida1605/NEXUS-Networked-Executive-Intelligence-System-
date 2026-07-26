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


def _carregar_modulo(nome_modulo: str, caminho: Path, executor: "Executor") -> None:
    """Tenta importar e registrar um plugin a partir de um módulo."""
    try:
        modulo = importlib.import_module(nome_modulo)
    except Exception as erro:
        logger.aviso(f"Plugin '{caminho.name}': falha ao importar — {erro}")
        return

    info = getattr(modulo, "PLUGIN_INFO", None)
    if not isinstance(info, dict):
        logger.aviso(f"Plugin '{caminho.name}': PLUGIN_INFO ausente ou inválido.")
        return

    campos = ("nome", "versao", "descricao")
    if not all(campo in info for campo in campos):
        logger.aviso(
            f"Plugin '{caminho.name}': PLUGIN_INFO incompleto "
            f"(faltam: {', '.join(c for c in campos if c not in info)})."
        )
        return

    registrar = getattr(modulo, "registrar", None)
    if not callable(registrar):
        logger.aviso(f"Plugin '{caminho.name}': função registrar() ausente.")
        return

    try:
        registrar(executor)
        logger.info(f"Plugin carregado: {info['nome']} v{info['versao']}")
    except Exception as erro:
        logger.erro(f"Plugin '{info.get('nome', caminho.name)}': falha ao registrar — {erro}")


def carregar_plugins(executor: "Executor") -> None:
    """
    Descobre e carrega todos os plugins válidos.

    Suporta dois formatos:
    1. Arquivos .py em plugins/ (ex.: exemplo_plugin.py)
    2. Subdiretórios com __init__.py (ex.: calculator/)

    Args:
        executor: instância do executor onde os comandos serão registrados.
    """
    if not PLUGINS_DIR.is_dir():
        return

    plugins_parent = str(PLUGINS_DIR.parent)
    if plugins_parent not in sys.path:
        sys.path.insert(0, plugins_parent)

    # 1) Arquivos .py na raiz de plugins/
    for arquivo in sorted(PLUGINS_DIR.glob("*.py")):
        if arquivo.name.startswith("_"):
            continue
        nome_modulo = f"plugins.{arquivo.stem}"
        _carregar_modulo(nome_modulo, arquivo, executor)

    # 2) Subdiretórios com __init__.py
    for subdir in sorted(PLUGINS_DIR.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("__"):
            continue
        init_file = subdir / "__init__.py"
        if not init_file.exists():
            continue
        nome_modulo = f"plugins.{subdir.name}"
        _carregar_modulo(nome_modulo, subdir, executor)
