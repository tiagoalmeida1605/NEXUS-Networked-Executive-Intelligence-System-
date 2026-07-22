"""
commands/info.py

Responsável pelos comandos relacionados a data, hora e versão do NEXUS.
"""

from __future__ import annotations

from datetime import datetime

from rich.console import Group

from core import theme
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
    """Retorna a versão, codename e identidade visual do NEXUS."""
    meta = carregar_versao()
    label = str(meta.get("label", "desconhecida"))
    codename = str(meta.get("codename", "—"))
    numero = str(meta.get("version", "—"))
    tema_meta = theme.meta_tema()

    identidade = theme.painel_identidade(
        versao=label,
        codename=codename,
        online=True,
    )

    detalhes = theme.painel(
        "BUILD",
        [
            f"SemVer: {numero}",
            f"Logo PNG: {'✔' if tema_meta['logo_png'] else '✗'}",
            f"Logo ASCII: {'✔' if tema_meta['logo_ascii'] else '✗'}",
            f"Theme: Kernel Identity",
        ],
        cor=theme.COR_TECNOLOGICO,
    )

    return Resposta(
        sucesso=True,
        mensagem=f"{label} ({codename})",
        renderable=Group(
            theme.render_logo_ascii(),
            identidade,
            detalhes,
        ),
    )
