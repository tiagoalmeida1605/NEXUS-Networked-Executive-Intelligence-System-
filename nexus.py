#!/usr/bin/env python3
"""
nexus.py

Ponto de entrada do NEXUS - Networked Executive Intelligence System.

Responsável apenas por:
    - carregar a configuração;
    - inicializar parser e executor;
    - exibir o banner inicial;
    - manter o loop principal de leitura e execução de comandos.

Nenhuma lógica de negócio deve ser implementada aqui.
"""

import json
from pathlib import Path
from typing import Any, Dict

from rich.console import Console

from core import ui
from core.banner import exibir_banner
from core.executor import Executor
from core.parser import Parser
from core.response import exibir

console = Console()

CONFIG_PATH = Path(__file__).resolve().parent / "config" / "config.json"


def carregar_config(caminho: Path) -> Dict[str, Any]:
    """
    Carrega o arquivo de configuração do NEXUS.

    Args:
        caminho: caminho para o arquivo config.json.

    Returns:
        Dict[str, Any]: dicionário com as configurações carregadas.
        Retorna um dicionário vazio caso o arquivo não exista ou esteja inválido.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        console.print(
            f"[bold red][NEXUS][/bold red] Arquivo de configuração não encontrado: {caminho}"
        )
    except json.JSONDecodeError as erro:
        console.print(f"[bold red][NEXUS][/bold red] Configuração inválida: {erro}")
    return {}


def main() -> None:
    """Inicializa o NEXUS e mantém o loop principal de comandos."""
    config = carregar_config(CONFIG_PATH)
    parser = Parser()
    executor = Executor(config)

    exibir_banner(config)

    while True:
        try:
            entrada = console.input(ui.PROMPT)
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold cyan][NEXUS][/bold cyan] Encerrando NEXUS...")
            break

        comando = parser.interpretar(entrada)
        resposta = executor.executar(comando)
        exibir(resposta)

        if resposta.encerrar:
            break


if __name__ == "__main__":
    main()
