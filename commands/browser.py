"""
commands/browser.py

Responsável exclusivamente pelos comandos que abrem sites
no navegador padrão do sistema.
"""

import webbrowser

from core.response import Resposta

_SITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://www.github.com",
}


def _abrir_site(nome: str) -> Resposta:
    """Abre o site correspondente ao nome informado."""
    url = _SITES[nome]
    try:
        webbrowser.open(url)
        return Resposta(sucesso=True, mensagem=f"Abrindo {nome.capitalize()}...")
    except Exception as erro:  # noqa: BLE001
        return Resposta(sucesso=False, mensagem=f"Erro ao abrir {nome.capitalize()}: {erro}")


def google() -> Resposta:
    """Abre o Google no navegador padrão."""
    return _abrir_site("google")


def youtube() -> Resposta:
    """Abre o YouTube no navegador padrão."""
    return _abrir_site("youtube")


def github() -> Resposta:
    """Abre o GitHub no navegador padrão."""
    return _abrir_site("github")
