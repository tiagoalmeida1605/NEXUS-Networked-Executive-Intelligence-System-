"""
ai/router.py

Roteador de intenção do NEXUS AI.

Analisa a entrada do usuário para detectar o tipo de tarefa
e seleciona o modelo mais adequado com base nas capacidades.

Estratégia:
    - Palavras-chave associadas a cada role (developer, assistant, analyst)
    - Fallback para o modelo padrão quando não há correspondência clara
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from ai.ollama import listar_modelos_config, modelo_por_role, modelo_padrao

# Palavras-chave para detecção de intenção
_INTENT_KEYWORDS: Dict[str, List[str]] = {
    "developer": [
        "programa", "código", "script", "python", "bash", "função",
        "classe", "método", "algoritmo", "bug", "erro", "debug",
        "arquivo", "criar", "implementar", "desenvolver", "corrigir",
        "código fonte", "função", "api", "biblioteca", "import",
        "programming", "code", "function", "class", "script",
    ],
    "assistant": [
        "comando", "terminal", "shell", "linux", "sistema",
        "abrir", "executar", "instalar", "atualizar", "remover",
        "cpu", "ram", "disco", "memória", "processo",
        "rápido", "ajuda", "comando", "dica", "sugestão",
        "command", "run", "execute", "system", "quick",
    ],
    "analyst": [
        "analisar", "explicar", "planejar", "estratégia",
        "comparar", "avaliar", "recomendar", "por que",
        "qual a diferença", "como funciona", "benefício",
        "análise", "relatório", "proposta", "arquitetura",
        "analyze", "explain", "plan", "strategy", "compare",
        "recommend", "why", "how", "architecture",
    ],
}


def detectar_intencao(entrada: str) -> str:
    """
    Detecta a intenção do usuário com base em palavras-chave.

    Args:
        entrada: texto digitado pelo usuário.

    Returns:
        str: role detectada ("developer", "assistant", "analyst").
    """
    if not entrada:
        return "assistant"

    texto = entrada.lower().strip()

    # Pontua cada role com base em palavras-chave encontradas
    pontuacao: Dict[str, int] = {"developer": 0, "assistant": 0, "analyst": 0}

    for role, keywords in _INTENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in texto)
        pontuacao[role] += score

    # Se houver um vencedor claro, retorna
    max_score = max(pontuacao.values())
    if max_score > 0:
        # Empate entre developer e analyst: prefere developer (mais específico)
        if pontuacao["developer"] == pontuacao["analyst"] and pontuacao["developer"] > 0:
            return "developer"
        return max(pontuacao, key=pontuacao.get)

    return "assistant"


def selecionar_modelo(entrada: str) -> Tuple[Optional[Dict], str]:
    """
    Seleciona o modelo ideal para a entrada do usuário.

    Args:
        entrada: texto digitado pelo usuário.

    Returns:
        tuple: (dict do modelo selecionado ou None, role detectada).
    """
    role = detectar_intencao(entrada)
    modelo = modelo_por_role(role)

    if modelo is None:
        modelo = modelo_padrao()
        if modelo is None:
            modelos = listar_modelos_config()
            if modelos:
                modelo = modelos[0]

    return modelo, role


def role_para_descricao(role: str) -> str:
    """Converte role para descrição amigável."""
    descricoes = {
        "developer": "Programming",
        "assistant": "System information",
        "analyst": "Analysis",
    }
    return descricoes.get(role, "General")
