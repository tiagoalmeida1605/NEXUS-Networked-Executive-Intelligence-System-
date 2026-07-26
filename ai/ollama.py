"""
ai/ollama.py

Integração com a API local do Ollama (http://localhost:11434).

Fornece funções para verificar disponibilidade, listar modelos
e enviar prompts para inferência. Usa apenas urllib (stdlib)
para evitar dependências externas.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib import request as urllib_request
from urllib.error import URLError

AI_DIR = Path(__file__).resolve().parent
MODELS_FILE = AI_DIR / "models.json"

# Cache de modelos detectados no Ollama
_modelos_ollama_cache: Optional[List[str]] = None


def _carregar_settings() -> Dict[str, Any]:
    """Carrega as configurações do arquivo models.json."""
    try:
        dados = json.loads(MODELS_FILE.read_text(encoding="utf-8"))
        return dados.get("settings", {})
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {
            "ollama_host": "http://localhost:11434",
            "timeout": 30,
            "max_tokens": 2048,
        }


def _ollama_host() -> str:
    """Retorna o host do Ollama (compatível com env OLLAMA_HOST)."""
    settings = _carregar_settings()
    return settings.get("ollama_host", "http://localhost:11434")


def _api_url(path: str) -> str:
    """Monta URL completa para a API do Ollama."""
    host = _ollama_host().rstrip("/")
    return f"{host}{path}"


def _requisicao_api(method: str, path: str, dados: Optional[dict] = None) -> Optional[dict]:
    """Faz requisição HTTP para a API do Ollama."""
    url = _api_url(path)
    try:
        data_bytes = json.dumps(dados).encode("utf-8") if dados else None
        req = urllib_request.Request(url, data=data_bytes, method=method)
        req.add_header("Content-Type", "application/json")
        with urllib_request.urlopen(req, timeout=_carregar_settings().get("timeout", 30)) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (URLError, OSError, json.JSONDecodeError):
        return None


def verificar_ollama() -> bool:
    """
    Verifica se o Ollama está instalado e o serviço está ativo.

    Returns:
        bool: True se Ollama está disponível.
    """
    # Verifica se o binário existe
    try:
        subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False

    # Verifica se o serviço está respondendo
    resultado = _requisicao_api("GET", "/api/tags")
    return resultado is not None


def listar_modelos_ollama() -> List[str]:
    """
    Lista os nomes dos modelos instalados no Ollama.

    Returns:
        List[str]: lista de tags de modelos (ex.: ["qwen2.5-coder:3b"]).
    """
    global _modelos_ollama_cache
    if _modelos_ollama_cache is not None:
        return _modelos_ollama_cache

    resultado = _requisicao_api("GET", "/api/tags")
    if not resultado:
        return []

    _modelos_ollama_cache = [
        m["name"] for m in resultado.get("models", []) if "name" in m
    ]
    return _modelos_ollama_cache


def modelo_instalado(modelo_id: str) -> bool:
    """
    Verifica se um modelo específico está instalado no Ollama.

    Args:
        modelo_id: identificador do modelo (ex.: "phi3:mini").

    Returns:
        bool: True se o modelo está disponível.
    """
    return modelo_id in listar_modelos_ollama()


def listar_modelos_config() -> List[Dict[str, Any]]:
    """Carrega a lista de modelos definidos em models.json."""
    try:
        dados = json.loads(MODELS_FILE.read_text(encoding="utf-8"))
        return dados.get("models", [])
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def modelo_por_role(role: str) -> Optional[Dict[str, Any]]:
    """
    Retorna o primeiro modelo configurado que corresponde a uma role.

    Args:
        role: "developer", "assistant" ou "analyst".

    Returns:
        dict com dados do modelo, ou None.
    """
    for m in listar_modelos_config():
        if m.get("role") == role:
            return m
    return None


def modelo_padrao() -> Optional[Dict[str, Any]]:
    """Retorna o modelo padrão definido em models.json."""
    try:
        dados = json.loads(MODELS_FILE.read_text(encoding="utf-8"))
        default_id = dados.get("default_model", "phi3:mini")
        for m in dados.get("models", []):
            if m.get("id") == default_id:
                return m
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return None


def enviar_prompt(modelo_id: str, prompt: str, sistema: str = "") -> Optional[str]:
    """
    Envia um prompt para o modelo e retorna a resposta.

    Args:
        modelo_id: identificador do modelo (ex.: "phi3:mini").
        prompt: texto do prompt do usuário.
        sistema: prompt de sistema opcional.

    Returns:
        str: resposta do modelo, ou None em caso de erro.
    """
    dados: Dict[str, Any] = {
        "model": modelo_id,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": _carregar_settings().get("max_tokens", 2048),
        },
    }
    if sistema:
        dados["system"] = sistema

    resultado = _requisicao_api("POST", "/api/generate", dados)
    if resultado and "response" in resultado:
        return resultado["response"].strip()
    return None
