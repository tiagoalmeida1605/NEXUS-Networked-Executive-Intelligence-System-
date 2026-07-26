"""
core/banner.py

Experiência de abertura do NEXUS.

Delega a exibição do splash animado para core/theme.py.exibir_splash().
Mantido como módulo separado para preservar a arquitetura existente.
"""

from __future__ import annotations

from typing import Any, Dict

from core import theme


def exibir_banner(config: Dict[str, Any]) -> None:
    """
    Exibe a splash screen completa com animação de módulos.

    Args:
        config: configuração do usuário (mantido por compatibilidade).
    """
    theme.exibir_splash()
