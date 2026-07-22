"""
commands/info.py

Responsável pelos comandos relacionados a data, hora e versão do NEXUS.
"""

from __future__ import annotations

from datetime import datetime

from core import ui
from core.config import carregar_versao
from core.response import Resposta


def hora() -> Resposta:
    """Retorna a hora atual do sistema."""
    agora = datetime.now().strftime("%H:%M:%S")
    return Resposta(sucesso=True, mensagem=f"Hora atual: {agora}")


def data() -> Resposta:
    """Retorna a data atual do sistema."""
    hoje = datetime.now().strftime("%d/%m/%Y")
    return Resposta(sucesso=True, mensagem=f"Data atual: {hoje}")


def versao() -> Resposta:
    """Retorna a versão e o codename atuais do NEXUS."""
    meta = carregar_versao()
    label = str(meta.get("label", "desconhecida"))
    codename = str(meta.get("codename", "—"))
    numero = str(meta.get("version", "—"))

    painel = ui.painel(
        "VERSION",
        [
            f"[{ui.COR_TEXTO_SECUNDARIO}]Versão:[/{ui.COR_TEXTO_SECUNDARIO}] "
            f"[bold {ui.COR_PRIMARIA}]{label}[/bold {ui.COR_PRIMARIA}]",
            f"[{ui.COR_TEXTO_SECUNDARIO}]Codename:[/{ui.COR_TEXTO_SECUNDARIO}] "
            f"[bold {ui.COR_NEON}]{codename}[/bold {ui.COR_NEON}]",
            f"[{ui.COR_TEXTO_SECUNDARIO}]SemVer:[/{ui.COR_TEXTO_SECUNDARIO}] "
            f"[{ui.COR_BRANCO}]{numero}[/{ui.COR_BRANCO}]",
        ],
        cor=ui.COR_PRIMARIA,
    )
    return Resposta(
        sucesso=True,
        mensagem=f"{label} ({codename})",
        renderable=painel,
    )
