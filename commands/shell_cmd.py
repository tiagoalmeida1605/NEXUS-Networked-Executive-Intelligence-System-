"""
commands/shell_cmd.py

Execução explícita de comandos do sistema operacional.

Nenhum comando digitado no prompt do NEXUS é enviado ao SO automaticamente.
Somente entradas no formato:

    shell <comando>

são encaminhadas ao shell do sistema.
"""

from __future__ import annotations

import shlex
import subprocess
from typing import Optional

from core import ui
from core.response import Resposta


def executar(comando_sistema: Optional[str]) -> Resposta:
    """
    Executa um comando no shell do sistema operacional.

    Args:
        comando_sistema: texto após a palavra-chave ``shell``.
    """
    if not comando_sistema or not comando_sistema.strip():
        return Resposta(
            sucesso=False,
            mensagem=(
                "Uso: shell <comando>\n"
                "Exemplo: shell ls -la"
            ),
        )

    texto = comando_sistema.strip()

    try:
        partes = shlex.split(texto)
    except ValueError as erro:
        return Resposta(
            sucesso=False,
            mensagem=f"Comando de shell inválido: {erro}",
        )

    if not partes:
        return Resposta(sucesso=False, mensagem="Uso: shell <comando>")

    try:
        resultado = subprocess.run(
            partes,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return Resposta(
            sucesso=False,
            mensagem=f'Programa não encontrado no sistema: "{partes[0]}".',
        )
    except OSError as erro:
        return Resposta(
            sucesso=False,
            mensagem=f"Falha ao executar no sistema: {erro}",
        )

    saida = (resultado.stdout or "").rstrip()
    erros = (resultado.stderr or "").rstrip()
    linhas = []

    if saida:
        linhas.append(saida)
    if erros:
        linhas.append(erros)

    corpo = "\n".join(linhas) if linhas else "(sem saída)"
    sucesso = resultado.returncode == 0

    painel = ui.painel(
        f"SHELL · exit {resultado.returncode}",
        [corpo],
        cor=ui.COR_SUCESSO if sucesso else ui.COR_ERRO,
    )

    return Resposta(
        sucesso=sucesso,
        mensagem=f"shell: {texto} (código {resultado.returncode})",
        renderable=painel,
    )
