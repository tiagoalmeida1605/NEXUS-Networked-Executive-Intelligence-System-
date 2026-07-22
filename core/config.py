"""
core/config.py

Gerencia a configuração profissional do NEXUS em ~/.config/nexus/.

Estrutura criada automaticamente:
    ~/.config/nexus/
    ├── config.json
    ├── logs/
    ├── history/
    └── cache/

Se o arquivo do usuário ainda não existir, migra o template do projeto
(config/config.json) como ponto de partida.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict

# Diretório raiz do projeto (pai de core/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Diretório XDG de configuração do usuário
CONFIG_HOME = Path.home() / ".config" / "nexus"
CONFIG_FILE = CONFIG_HOME / "config.json"
LOGS_DIR = CONFIG_HOME / "logs"
HISTORY_DIR = CONFIG_HOME / "history"
CACHE_DIR = CONFIG_HOME / "cache"

# Template embutido no repositório
TEMPLATE_CONFIG = PROJECT_ROOT / "config" / "config.json"
VERSION_FILE = PROJECT_ROOT / "version.json"

_DEFAULT_CONFIG: Dict[str, Any] = {
    "user": "usuário",
    "browser": "brave-browser",
    "terminal": "gnome-terminal",
    "editor": "pycharm",
    "vscode": "code",
    "webstorm": "webstorm",
    "downloads": str(Path.home() / "Downloads"),
    "documents": str(Path.home() / "Documents"),
    "projects": str(Path.home() / "Documents"),
}


def garantir_estrutura() -> Path:
    """
    Garante que ~/.config/nexus/ e seus subdiretórios existam.

    Returns:
        Path: caminho do diretório de configuração do usuário.
    """
    for pasta in (CONFIG_HOME, LOGS_DIR, HISTORY_DIR, CACHE_DIR):
        pasta.mkdir(parents=True, exist_ok=True)
    return CONFIG_HOME


def carregar_versao() -> Dict[str, Any]:
    """
    Carrega os metadados de versão a partir de version.json.

    Returns:
        Dict[str, Any]: dados de versão (version, label, codename, changelog...).
    """
    fallback = {
        "version": "0.2.0",
        "label": "v0.2 Alpha",
        "codename": "Kernel",
        "released": "2026-07-21",
        "changelog": [],
    }
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return {**fallback, **dados}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return fallback


def carregar_config() -> Dict[str, Any]:
    """
    Carrega a configuração do usuário, criando a estrutura se necessário.

    Na primeira execução, copia o template do projeto para ~/.config/nexus/.

    Returns:
        Dict[str, Any]: dicionário de configuração do usuário.
    """
    garantir_estrutura()

    if not CONFIG_FILE.exists():
        _migrar_template()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            if not isinstance(dados, dict):
                return dict(_DEFAULT_CONFIG)
            return {**_DEFAULT_CONFIG, **dados}
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULT_CONFIG)


def salvar_config(config: Dict[str, Any]) -> None:
    """
    Persiste a configuração do usuário em ~/.config/nexus/config.json.

    Args:
        config: dicionário completo de configuração a ser salvo.
    """
    garantir_estrutura()
    with open(CONFIG_FILE, "w", encoding="utf-8") as arquivo:
        json.dump(config, arquivo, indent=4, ensure_ascii=False)
        arquivo.write("\n")


def _migrar_template() -> None:
    """Copia o template do projeto ou grava o padrão embutido."""
    garantir_estrutura()
    if TEMPLATE_CONFIG.exists():
        shutil.copy2(TEMPLATE_CONFIG, CONFIG_FILE)
        return
    salvar_config(dict(_DEFAULT_CONFIG))
