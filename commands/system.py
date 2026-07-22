"""
commands/system.py

Responsável pelos comandos que consultam ou controlam o sistema
operacional: uso de CPU, RAM, disco, informações gerais e limpeza de tela.

As saídas são montadas como painéis Rich através de core/ui.py.
"""

import os
import platform
import sys
from typing import Optional

import psutil

from core import ui
from core.response import Resposta


def cpu() -> Resposta:
    """Retorna um painel com o uso atual da CPU."""
    uso = psutil.cpu_percent(interval=0.5)
    nucleos = psutil.cpu_count(logical=True) or 0

    conteudo = [
        f"Uso: {ui.barra_progresso(uso)}",
        f"Núcleos: {nucleos}",
    ]

    temperatura = _temperatura_cpu()
    if temperatura is not None:
        conteudo.append(f"Temperatura: {temperatura:.0f}°C")

    painel = ui.painel("CPU", conteudo, cor=ui.COR_PRIMARIA)
    return Resposta(sucesso=True, mensagem=f"Uso de CPU: {uso}%", renderable=painel)


def ram() -> Resposta:
    """Retorna um painel com o uso atual de memória RAM."""
    memoria = psutil.virtual_memory()
    usado_mb = memoria.used // (1024 ** 2)
    total_mb = memoria.total // (1024 ** 2)

    conteudo = [
        f"Uso: {ui.barra_progresso(memoria.percent)}",
        f"{usado_mb} MB / {total_mb} MB",
    ]

    painel = ui.painel("RAM", conteudo, cor=ui.COR_PRIMARIA)
    return Resposta(
        sucesso=True,
        mensagem=f"Memória RAM: {memoria.percent}% utilizada ({usado_mb} MB / {total_mb} MB)",
        renderable=painel,
    )


def disco() -> Resposta:
    """Retorna um painel com o uso atual de disco."""
    uso = psutil.disk_usage("/")
    usado_gb = uso.used // (1024 ** 3)
    total_gb = uso.total // (1024 ** 3)

    conteudo = [
        f"Uso: {ui.barra_progresso(uso.percent)}",
        f"{usado_gb} GB / {total_gb} GB",
    ]

    painel = ui.painel("Disco", conteudo, cor=ui.COR_PRIMARIA)
    return Resposta(
        sucesso=True,
        mensagem=f"Disco: {uso.percent}% utilizado ({usado_gb} GB / {total_gb} GB)",
        renderable=painel,
    )


def sistema() -> Resposta:
    """Retorna um painel com informações gerais do sistema operacional."""
    from rich.console import Group

    from core.config import carregar_versao

    distro = ui.detectar_distro()
    meta = carregar_versao()

    conteudo = [
        distro,
        f"Kernel {platform.release()}",
        f"Python {sys.version.split()[0]}",
        f"Arquitetura: {platform.machine()}",
    ]

    painel_host = ui.painel("Sistema", conteudo, cor=ui.COR_ACENTO)
    identidade = ui.painel_identidade(
        versao=str(meta.get("label", "v0.2.2.1 Alpha")),
        codename=str(meta.get("codename", "Kernel Identity")),
        online=True,
    )
    return Resposta(
        sucesso=True,
        mensagem=f"Sistema: {distro}",
        renderable=Group(ui.render_logo_ascii(), identidade, painel_host),
    )


def limpar() -> Resposta:
    """Limpa a tela do terminal."""
    os.system("cls" if platform.system() == "Windows" else "clear")
    return Resposta(sucesso=True, mensagem="")


def _temperatura_cpu() -> Optional[float]:
    """
    Tenta ler a temperatura atual da CPU via psutil.

    Retorna None quando a plataforma não expõe sensores de temperatura
    (comum fora do Linux, ou em ambientes virtualizados/contêineres).
    """
    leitor = getattr(psutil, "sensors_temperatures", None)
    if leitor is None:
        return None

    try:
        sensores = leitor()
    except Exception:  # noqa: BLE001
        return None

    for leituras in sensores.values():
        for leitura in leituras:
            if leitura.current:
                return leitura.current
    return None
