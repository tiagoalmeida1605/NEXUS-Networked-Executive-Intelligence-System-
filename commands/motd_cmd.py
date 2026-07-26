"""
commands/motd_cmd.py

Comando ``motd`` — Mensagem do Dia do NEXUS.
Exibe informações rápidas do sistema e boas-vindas.
"""

from __future__ import annotations

from datetime import datetime

from rich.align import Align
from rich.console import Group
from rich.text import Text

from core import theme
from core.config import carregar_versao
from core.response import Resposta
from core.system import get_hostname, get_operator_name, format_uptime


def motd() -> Resposta:
    """Exibe a Mensagem do Dia com informações do sistema."""
    meta = carregar_versao()
    label = str(meta.get("label", "v0.4 Alpha"))
    codename = str(meta.get("codename", "Interface"))
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    linhas = [
        f"[bold {theme.COR_PRIMARIA}]NEXUS[/] — {label} ({codename})",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Operator:[/]  [bold {theme.COR_BRANCO}]{get_operator_name()}[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Host:[/]      [bold {theme.COR_BRANCO}]{get_hostname()}[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Uptime:[/]    [bold {theme.COR_BRANCO}]{format_uptime()}[/]",
        f"[{theme.COR_TEXTO_SECUNDARIO}]Data:[/]      [bold {theme.COR_BRANCO}]{agora}[/]",
        "",
        f"[{theme.COR_TEXTO_SECUNDARIO}]\"A tecnologia é a ponte entre o presente e o futuro.\"[/]",
    ]

    painel = theme.painel("MOTD", linhas, cor=theme.COR_NEON)

    return Resposta(
        sucesso=True,
        mensagem="Mensagem do dia exibida.",
        renderable=Group(
            Align.center(Text("MESSAGE OF THE DAY", style=f"bold {theme.COR_NEON}")),
            Text(""),
            painel,
        ),
    )
