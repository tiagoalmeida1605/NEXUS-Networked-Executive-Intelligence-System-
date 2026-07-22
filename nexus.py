#!/usr/bin/env python3
"""
nexus.py

Ponto de entrada do NEXUS - Networked Executive Intelligence System.

Responsável apenas por:
    - garantir a estrutura de configuração (~/.config/nexus/);
    - carregar a configuração do usuário;
    - inicializar logger, histórico, parser e executor;
    - tratar subcomandos CLI (history, update);
    - exibir o banner inicial;
    - manter o loop principal de leitura e execução de comandos.

Nenhuma lógica de negócio deve ser implementada aqui.
"""

from __future__ import annotations

import sys
from typing import List, Optional

from rich.console import Console

from commands import history_cmd, update_cmd
from core import ui
from core.banner import exibir_banner
from core.config import carregar_config, garantir_estrutura
from core.executor import Executor
from core.history import Historico
from core.logger import logger
from core.parser import Parser
from core.response import exibir

console = Console()


def _tratar_argv(argv: List[str], historico: Historico) -> Optional[int]:
    """
    Processa subcomandos invocados diretamente pela CLI.

    Exemplos:
        nexus history
        nexus update

    Args:
        argv: argumentos de sys.argv (sem o nome do script).
        historico: instância do histórico.

    Returns:
        Optional[int]: código de saída se um subcomando foi tratado;
            None para entrar no modo interativo.
    """
    if not argv:
        return None

    acao = argv[0].lower()

    if acao in ("history", "historico"):
        sub = argv[1].lower() if len(argv) > 1 else None
        if sub in ("limpar", "clear"):
            resposta = history_cmd.limpar_historico(historico)
        else:
            resposta = history_cmd.exibir_historico(historico)
        exibir(resposta)
        return 0 if resposta.sucesso else 1

    if acao == "update":
        resposta = update_cmd.executar_atualizacao(interativo=True)
        exibir(resposta)
        return 0 if resposta.sucesso else 1

    if acao in ("-h", "--help", "help", "ajuda"):
        console.print(
            f"[bold {ui.COR_PRIMARIA}]NEXUS[/bold {ui.COR_PRIMARIA}] — "
            f"[{ui.COR_BRANCO}]Networked Executive Intelligence System[/{ui.COR_BRANCO}]\n\n"
            f"  [{ui.COR_NEON}]nexus[/{ui.COR_NEON}]              Inicia o modo interativo\n"
            f"  [{ui.COR_NEON}]nexus history[/{ui.COR_NEON}]      Exibe o histórico de comandos\n"
            f"  [{ui.COR_NEON}]nexus update[/{ui.COR_NEON}]       Verifica e aplica atualizações\n"
            f"  [{ui.COR_NEON}]nexus help[/{ui.COR_NEON}]         Exibe esta ajuda\n"
        )
        return 0

    console.print(
        f"[bold {ui.COR_ERRO}]✗[/bold {ui.COR_ERRO}] "
        f'Argumento desconhecido: "{acao}". Use [bold]nexus help[/bold].'
    )
    return 1


def main(argv: Optional[List[str]] = None) -> int:
    """
    Inicializa o NEXUS e mantém o loop principal de comandos.

    Args:
        argv: lista de argumentos CLI (padrão: sys.argv[1:]).

    Returns:
        int: código de saída do processo.
    """
    args = list(sys.argv[1:] if argv is None else argv)

    try:
        garantir_estrutura()
        config = carregar_config()
        historico = Historico()
        historico.habilitar_readline()

        codigo = _tratar_argv(args, historico)
        if codigo is not None:
            return codigo

        parser = Parser()
        executor = Executor(config, historico=historico)

        logger.info("Sistema iniciado.")
        exibir_banner(config)

        while True:
            try:
                entrada = console.input(ui.PROMPT)
            except (KeyboardInterrupt, EOFError):
                console.print(
                    f"\n[bold {ui.COR_PRIMARIA}][NEXUS][/bold {ui.COR_PRIMARIA}] "
                    f"[{ui.COR_BRANCO}]Encerrando NEXUS...[/{ui.COR_BRANCO}]"
                )
                logger.info("Sistema encerrado pelo usuário (SIGINT/EOF).")
                break

            if entrada.strip():
                historico.adicionar(entrada)
                logger.comando(entrada.strip())

            comando = parser.interpretar(entrada)
            resposta = executor.executar(comando)
            exibir(resposta)

            if comando.acao != "vazio":
                if resposta.sucesso:
                    logger.sucesso(resposta.mensagem or "OK")
                else:
                    logger.erro(resposta.mensagem or "Falha")

            if resposta.encerrar:
                logger.info("Sistema encerrado.")
                break

        return 0

    except Exception as erro:  # noqa: BLE001
        logger.falha(f"Falha crítica: {erro}")
        console.print(
            f"[bold {ui.COR_ERRO}][NEXUS][/bold {ui.COR_ERRO}] "
            f"Falha crítica: {erro}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
