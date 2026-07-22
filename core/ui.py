"""
core/ui.py

Camada de apresentação do NEXUS — reexporta o tema oficial.

A partir de v0.2.2 (Kernel Identity), cores e componentes vivem em
``core/theme.py``. Este módulo mantém a API antiga para não quebrar
imports existentes (``from core import ui``).
"""

from __future__ import annotations

from core.theme import (  # noqa: F401
    COR_ACENTO,
    COR_ALERTA,
    COR_BRANCO,
    COR_ERRO,
    COR_ESCURO,
    COR_MUTED,
    COR_NEON,
    COR_PRIMARIA,
    COR_SUCESSO,
    COR_TECNOLOGICO,
    COR_TEXTO_SECUNDARIO,
    PROMPT,
    barra_progresso,
    cabecalho_ajuda,
    carregar_banner_ascii,
    carregar_logo_ascii,
    caminho_logo_png,
    console,
    detectar_distro,
    painel,
    painel_identidade,
    paleta,
    regra,
    render_banner_ascii,
    render_logo_ascii,
    status_indicador,
    tabela,
)

__all__ = [
    "COR_ACENTO",
    "COR_ALERTA",
    "COR_BRANCO",
    "COR_ERRO",
    "COR_ESCURO",
    "COR_MUTED",
    "COR_NEON",
    "COR_PRIMARIA",
    "COR_SUCESSO",
    "COR_TECNOLOGICO",
    "COR_TEXTO_SECUNDARIO",
    "PROMPT",
    "barra_progresso",
    "cabecalho_ajuda",
    "carregar_banner_ascii",
    "carregar_logo_ascii",
    "caminho_logo_png",
    "console",
    "detectar_distro",
    "painel",
    "painel_identidade",
    "paleta",
    "regra",
    "render_banner_ascii",
    "render_logo_ascii",
    "status_indicador",
    "tabela",
]
