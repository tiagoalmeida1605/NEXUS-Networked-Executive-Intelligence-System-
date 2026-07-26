"""
plugins/notes/

Plugin de notas para o NEXUS.
Comandos: note add <texto>, note list, note remove <id>
Salva em ~/.config/nexus/notes.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from core.config import CONFIG_HOME
from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Notes",
    "versao": "1.0",
    "descricao": "Sistema de notas simples (note add, note list, note remove).",
}

NOTES_FILE = CONFIG_HOME / "notes.json"


def _carregar_notas() -> list[dict]:
    """Carrega as notas do arquivo JSON."""
    if not NOTES_FILE.exists():
        return []
    try:
        dados = json.loads(NOTES_FILE.read_text(encoding="utf-8"))
        return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _salvar_notas(notas: list[dict]) -> None:
    """Persiste as notas no arquivo JSON."""
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.write_text(
        json.dumps(notas, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _note_add(texto: Optional[str]) -> Resposta:
    """Adiciona uma nova nota."""
    if not texto or not texto.strip():
        return Resposta(sucesso=False, mensagem="Uso: note add <texto>")
    notas = _carregar_notas()
    notas.append({"id": len(notas) + 1, "texto": texto.strip()})
    _salvar_notas(notas)
    return Resposta(sucesso=True, mensagem=f"Nota adicionada: {texto.strip()}")


def _note_list() -> Resposta:
    """Lista todas as notas."""
    notas = _carregar_notas()
    if not notas:
        return Resposta(sucesso=True, mensagem="Nenhuma nota salva.")
    linhas = [f"{n['id']}: {n['texto']}" for n in notas]
    return Resposta(sucesso=True, mensagem="\n".join(linhas))


def _note_remove(id_str: Optional[str]) -> Resposta:
    """Remove uma nota pelo ID."""
    if not id_str or not id_str.strip().isdigit():
        return Resposta(sucesso=False, mensagem="Uso: note remove <id>")
    notas = _carregar_notas()
    idx = int(id_str.strip()) - 1
    if idx < 0 or idx >= len(notas):
        return Resposta(sucesso=False, mensagem=f"Nota #{id_str} não encontrada.")
    removida = notas.pop(idx)
    # Reindexa
    for i, n in enumerate(notas):
        n["id"] = i + 1
    _salvar_notas(notas)
    return Resposta(sucesso=True, mensagem=f"Nota removida: {removida['texto']}")


def _note_handler(alvo: Optional[str]) -> Resposta:
    """Roteia subcomandos do note."""
    if not alvo:
        return _note_list()
    partes = alvo.split(maxsplit=1)
    sub = partes[0].lower()
    resto = partes[1] if len(partes) > 1 else None
    if sub == "add":
        return _note_add(resto)
    if sub == "list":
        return _note_list()
    if sub in ("remove", "rm", "del"):
        return _note_remove(resto)
    return Resposta(sucesso=False, mensagem="Uso: note add/list/remove")


def registrar(executor) -> None:
    """Registra o comando note."""
    executor.registrar_plugin("note", _note_handler, "Notas: note add/list/remove")
