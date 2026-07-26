"""
commands/banner_cmd.py

Comando ``banner`` — exibe o banner ASCII do NEXUS.
"""

from __future__ import annotations

from rich.align import Align
from rich.console import Group
from rich.text import Text

from core import theme
from core.config import carregar_versao
from core.response import Resposta


def banner() -> Resposta:
    """Exibe o banner completo com identidade do NEXUS."""
    meta = carregar_versao()
    label = str(meta.get("label", "v0.4 Alpha"))
    codename = str(meta.get("codename", "Interface"))

    return Resposta(
        sucesso=True,
        mensagem="Banner exibido.",
        renderable=Group(
            theme.render_banner_ascii(),
            Text(""),
            Align.center(
                Text(
                    "Networked Executive Intelligence System",
                    style=theme.COR_BRANCO,
                )
            ),
            Text(""),
            Align.center(
                theme.painel_identidade(
                    versao=label,
                    codename=codename,
                    online=True,
                )
            ),
        ),
    )
