"""
commands/system.py

Responsável pelos comandos que consultam ou controlam o sistema
operacional: uso de CPU, RAM, disco, informações gerais e limpeza de tela.
"""

import os
import platform

import psutil

from core.response import Resposta


def cpu() -> Resposta:
    """Retorna o percentual de uso atual da CPU."""
    uso = psutil.cpu_percent(interval=0.5)
    return Resposta(sucesso=True, mensagem=f"Uso de CPU: {uso}%")


def ram() -> Resposta:
    """Retorna o percentual e a quantidade de memória RAM em uso."""
    memoria = psutil.virtual_memory()
    usado_mb = memoria.used // (1024 ** 2)
    total_mb = memoria.total // (1024 ** 2)
    return Resposta(
        sucesso=True,
        mensagem=f"Memória RAM: {memoria.percent}% utilizada ({usado_mb} MB / {total_mb} MB)",
    )


def disco() -> Resposta:
    """Retorna o percentual e a quantidade de espaço em disco em uso."""
    uso = psutil.disk_usage("/")
    usado_gb = uso.used // (1024 ** 3)
    total_gb = uso.total // (1024 ** 3)
    return Resposta(
        sucesso=True,
        mensagem=f"Disco: {uso.percent}% utilizado ({usado_gb} GB / {total_gb} GB)",
    )


def sistema() -> Resposta:
    """Retorna informações gerais sobre o sistema operacional."""
    info = (
        f"Sistema: {platform.system()}\n"
        f"Versão: {platform.version()}\n"
        f"Distribuição: {platform.platform()}\n"
        f"Arquitetura: {platform.machine()}\n"
        f"Processador: {platform.processor() or 'Não identificado'}"
    )
    return Resposta(sucesso=True, mensagem=info)


def limpar() -> Resposta:
    """Limpa a tela do terminal."""
    os.system("cls" if platform.system() == "Windows" else "clear")
    return Resposta(sucesso=True, mensagem="")
