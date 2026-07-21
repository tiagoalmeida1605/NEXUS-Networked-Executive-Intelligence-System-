"""
commands/apps.py

Responsável exclusivamente pela abertura de aplicativos e pastas do
sistema, com base nos caminhos e comandos definidos em config/config.json.

Nenhum caminho ou comando é fixado diretamente no código.
"""

import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from core.response import Resposta


def abrir(alvo: str, config: Dict[str, Any]) -> Resposta:
    """
    Abre um aplicativo ou uma pasta com base no alvo informado.

    Args:
        alvo: nome do aplicativo ou pasta (ex.: "brave", "downloads").
        config: dicionário de configuração carregado de config/config.json.

    Returns:
        Resposta: resultado da operação solicitada.
    """
    mapa_apps = {
        "brave": config.get("browser", "brave-browser"),
        "firefox": "firefox",
        "terminal": config.get("terminal", "gnome-terminal"),
        "pycharm": config.get("editor", "pycharm"),
        "webstorm": config.get("webstorm", "webstorm"),
        "vscode": config.get("vscode", "code"),
    }

    mapa_pastas = {
        "downloads": config.get("downloads"),
        "documentos": config.get("documents"),
    }

    if alvo in mapa_apps:
        return _executar_comando(mapa_apps[alvo], alvo)

    if alvo in mapa_pastas:
        return _abrir_pasta(mapa_pastas[alvo], alvo)

    return Resposta(sucesso=False, mensagem=f'Não sei como abrir "{alvo}".\nDigite "ajuda".')


def _executar_comando(comando: Optional[str], nome_exibicao: str) -> Resposta:
    """Executa o comando de sistema associado a um aplicativo."""
    if not comando:
        return Resposta(
            sucesso=False, mensagem=f"Nenhum comando configurado para {nome_exibicao}."
        )
    try:
        subprocess.Popen(
            [comando], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return Resposta(sucesso=True, mensagem=f"Abrindo {nome_exibicao.capitalize()}...")
    except FileNotFoundError:
        return Resposta(
            sucesso=False,
            mensagem=f'Aplicativo "{comando}" não encontrado no sistema.',
        )
    except Exception as erro:  # noqa: BLE001
        return Resposta(sucesso=False, mensagem=f"Erro ao abrir {nome_exibicao}: {erro}")


def _abrir_pasta(caminho: Optional[str], nome_exibicao: str) -> Resposta:
    """Abre uma pasta do sistema utilizando o gerenciador de arquivos padrão."""
    if not caminho:
        return Resposta(
            sucesso=False, mensagem=f"Nenhum caminho configurado para {nome_exibicao}."
        )

    pasta = Path(caminho).expanduser()
    if not pasta.exists():
        return Resposta(sucesso=False, mensagem=f'A pasta "{pasta}" não existe.')

    try:
        subprocess.Popen(
            ["xdg-open", str(pasta)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        return Resposta(sucesso=True, mensagem=f"Abrindo {nome_exibicao}...")
    except Exception as erro:  # noqa: BLE001
        return Resposta(sucesso=False, mensagem=f"Erro ao abrir {nome_exibicao}: {erro}")
