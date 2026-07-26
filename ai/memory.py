"""
ai/memory.py

Memória simples da IA do NEXUS.

Armazena preferências, configurações e informações importantes
em ~/.config/nexus/ai_memory.json.

Não implementa memória conversacional complexa — apenas
persistência de dados estruturados para uso da IA.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from core.config import CONFIG_HOME

MEMORY_FILE = CONFIG_HOME / "ai_memory.json"


def _garantir_arquivo() -> None:
    """Garante que o arquivo de memória existe."""
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not MEMORY_FILE.exists():
        dados_iniciais = {
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "preferences": {},
            "config": {},
            "notes": [],
        }
        MEMORY_FILE.write_text(
            json.dumps(dados_iniciais, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )


def _carregar() -> Dict[str, Any]:
    """Carrega os dados da memória do disco."""
    _garantir_arquivo()
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"preferences": {}, "config": {}, "notes": []}


def _salvar(dados: Dict[str, Any]) -> None:
    """Persiste os dados no disco."""
    dados["updated"] = datetime.now().isoformat()
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(
        json.dumps(dados, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def salvar_preferencia(chave: str, valor: Any) -> None:
    """
    Salva uma preferência.

    Args:
        chave: nome da preferência.
        valor: valor a ser armazenado.
    """
    dados = _carregar()
    dados["preferences"][chave] = valor
    _salvar(dados)


def ler_preferencia(chave: str, padrao: Any = None) -> Any:
    """
    Lê uma preferência salva.

    Args:
        chave: nome da preferência.
        padrao: valor padrão caso não exista.

    Returns:
        valor armazenado ou padrao.
    """
    dados = _carregar()
    return dados.get("preferences", {}).get(chave, padrao)


def salvar_config_ai(chave: str, valor: Any) -> None:
    """Salva uma configuração da IA."""
    dados = _carregar()
    dados["config"][chave] = valor
    _salvar(dados)


def ler_config_ai(chave: str, padrao: Any = None) -> Any:
    """Lê uma configuração da IA."""
    dados = _carregar()
    return dados.get("config", {}).get(chave, padrao)


def adicionar_nota(texto: str) -> None:
    """Adiciona uma nota à memória."""
    dados = _carregar()
    dados["notes"].append({
        "text": texto,
        "timestamp": datetime.now().isoformat(),
    })
    _salvar(dados)


def listar_notas(limite: int = 10) -> list[Dict[str, str]]:
    """Lista as últimas notas da memória."""
    dados = _carregar()
    return dados.get("notes", [])[-limite:]


def obter_resumo() -> Dict[str, Any]:
    """Retorna um resumo dos dados armazenados."""
    dados = _carregar()
    return {
        "preferences": len(dados.get("preferences", {})),
        "config_keys": list(dados.get("config", {}).keys()),
        "notes_count": len(dados.get("notes", [])),
        "updated": dados.get("updated", "unknown"),
    }
