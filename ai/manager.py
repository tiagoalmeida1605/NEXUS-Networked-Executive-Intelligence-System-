"""
ai/manager.py

Gerenciador de ciclo de vida dos modelos de IA do NEXUS.

Controla qual modelo está ativo, alterna entre modelos e
gerencia o modo dynamic (apenas um modelo carregado por vez).

Os modelos NÃO ficam carregados simultaneamente — são ativados
sob demanda e "liberados" após o uso.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from ai.ollama import (
    enviar_prompt,
    listar_modelos_config,
    listar_modelos_ollama,
    modelo_instalado,
    modelo_padrao,
    modelo_por_role,
    verificar_ollama,
)
from ai.router import selecionar_modelo
from ai.memory import ler_config_ai, salvar_config_ai

# Estado global do modelo ativo
_modelo_ativo: Optional[Dict[str, Any]] = None


def status_ollama() -> Dict[str, Any]:
    """
    Verifica o status completo do Ollama e dos modelos.

    Returns:
        dict com: ollama_online, modelos_instalados, modelos_config, ativo.
    """
    online = verificar_ollama()
    instalados = listar_modelos_ollama() if online else []
    config = listar_modelos_config()

    return {
        "ollama_online": online,
        "modelos_instalados": instalados,
        "modelos_config": [
            {
                "id": m["id"],
                "name": m["name"],
                "role": m["role"],
                "instalado": m["id"] in instalados,
            }
            for m in config
        ],
        "modelo_ativo": _modelo_ativo["name"] if _modelo_ativo else None,
    }


def obter_modelo_ativo() -> Optional[Dict[str, Any]]:
    """Retorna o modelo atualmente ativo."""
    return _modelo_ativo


def ativar_modelo(modelo_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Ativa um modelo específico ou o padrão.

    Args:
        modelo_id: ID do modelo (ex.: "phi3:mini"). Se None, ativa o padrão.

    Returns:
        dict do modelo ativado, ou None se não disponível.
    """
    global _modelo_ativo

    if not verificar_ollama():
        _modelo_ativo = None
        return None

    if modelo_id:
        for m in listar_modelos_config():
            if m["id"] == modelo_id:
                if not modelo_instalado(modelo_id):
                    return None
                _modelo_ativo = m
                salvar_config_ai("ultimo_modelo", modelo_id)
                return m
        return None

    # Ativa o modelo padrão
    padrao = modelo_padrao()
    if padrao and (not padrao["id"] or modelo_instalado(padrao["id"])):
        _modelo_ativo = padrao
        salvar_config_ai("ultimo_modelo", padrao["id"])
        return padrao

    # Fallback: primeiro modelo instalado
    instalados = listar_modelos_ollama()
    for m in listar_modelos_config():
        if m["id"] in instalados:
            _modelo_ativo = m
            salvar_config_ai("ultimo_modelo", m["id"])
            return m

    _modelo_ativo = None
    return None


def liberar_modelo() -> None:
    """
    Libera o modelo ativo (simulação de descarregamento).

    Na prática, marca que nenhum modelo está ativo.
    O Ollama gerencia a memória dos modelos automaticamente.
    """
    global _modelo_ativo
    _modelo_ativo = None


def processar(entrada: str) -> Dict[str, Any]:
    """
    Processa uma entrada do usuário com o modelo adequado.

    Fluxo:
        1. Detecta intenção
        2. Seleciona modelo
        3. Ativa o modelo (se necessário)
        4. Envia prompt
        5. Libera o modelo (modo dynamic)

    Args:
        entrada: texto do usuário.

    Returns:
        dict com: sucesso, resposta, modelo_usado, role_detectada.
    """
    if not verificar_ollama():
        return {
            "sucesso": False,
            "resposta": "Ollama não está disponível.",
            "modelo_usado": None,
            "role_detectada": None,
        }

    modelo_selecionado, role = selecionar_modelo(entrada)

    if not modelo_selecionado:
        return {
            "sucesso": False,
            "resposta": "Nenhum modelo disponível.",
            "modelo_usado": None,
            "role_detectada": role,
        }

    # Verifica se o modelo está instalado
    if not modelo_instalado(modelo_selecionado["id"]):
        return {
            "sucesso": False,
            "resposta": (
                f"Modelo '{modelo_selecionado['name']}' não está instalado.\n"
                f"Instale com: ollama pull {modelo_selecionado['id']}"
            ),
            "modelo_usado": modelo_selecionado["id"],
            "role_detectada": role,
        }

    # Ativa o modelo
    ativado = ativar_modelo(modelo_selecionado["id"])
    if not ativado:
        return {
            "sucesso": False,
            "resposta": "Falha ao ativar o modelo.",
            "modelo_usado": modelo_selecionado["id"],
            "role_detectada": role,
        }

    # Envia o prompt
    from ai.prompts.system import get_system_prompt

    sistema = get_system_prompt(role)
    resposta = enviar_prompt(modelo_selecionado["id"], entrada, sistema)

    # Libera o modelo (modo dynamic)
    modo = ler_config_ai("ai_mode", "dynamic")
    if modo == "dynamic":
        liberar_modelo()

    if resposta is None:
        return {
            "sucesso": False,
            "resposta": "Erro ao obter resposta do modelo.",
            "modelo_usado": modelo_selecionado["id"],
            "role_detectada": role,
        }

    return {
        "sucesso": True,
        "resposta": resposta,
        "modelo_usado": modelo_selecionado["id"],
        "role_detectada": role,
    }
