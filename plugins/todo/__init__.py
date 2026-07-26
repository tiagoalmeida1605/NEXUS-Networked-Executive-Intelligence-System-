"""
plugins/todo/

Plugin de lista de tarefas para o NEXUS.
Comandos: todo add <texto>, todo list, todo done <id>, todo remove <id>
Salva em ~/.config/nexus/todo.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from core.config import CONFIG_HOME
from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Todo",
    "versao": "1.0",
    "descricao": "Lista de tarefas (todo add/list/done/remove).",
}

TODO_FILE = CONFIG_HOME / "todo.json"


def _carregar_tarefas() -> list[dict]:
    """Carrega as tarefas do arquivo JSON."""
    if not TODO_FILE.exists():
        return []
    try:
        dados = json.loads(TODO_FILE.read_text(encoding="utf-8"))
        return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _salvar_tarefas(tarefas: list[dict]) -> None:
    """Persiste as tarefas no arquivo JSON."""
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    TODO_FILE.write_text(
        json.dumps(tarefas, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _todo_add(texto: Optional[str]) -> Resposta:
    """Adiciona uma nova tarefa."""
    if not texto or not texto.strip():
        return Resposta(sucesso=False, mensagem="Uso: todo add <tarefa>")
    tarefas = _carregar_tarefas()
    tarefas.append({"id": len(tarefas) + 1, "texto": texto.strip(), "done": False})
    _salvar_tarefas(tarefas)
    return Resposta(sucesso=True, mensagem=f"Tarefa adicionada: {texto.strip()}")


def _todo_list() -> Resposta:
    """Lista todas as tarefas."""
    tarefas = _carregar_tarefas()
    if not tarefas:
        return Resposta(sucesso=True, mensagem="Nenhuma tarefa na lista.")
    linhas = []
    for t in tarefas:
        status = "✓" if t["done"] else "○"
        linhas.append(f"{t['id']:2d}. [{status}] {t['texto']}")
    return Resposta(sucesso=True, mensagem="\n".join(linhas))


def _todo_done(id_str: Optional[str]) -> Resposta:
    """Marca uma tarefa como concluída."""
    if not id_str or not id_str.strip().isdigit():
        return Resposta(sucesso=False, mensagem="Uso: todo done <id>")
    tarefas = _carregar_tarefas()
    idx = int(id_str.strip()) - 1
    if idx < 0 or idx >= len(tarefas):
        return Resposta(sucesso=False, mensagem=f"Tarefa #{id_str} não encontrada.")
    tarefas[idx]["done"] = True
    _salvar_tarefas(tarefas)
    return Resposta(sucesso=True, mensagem=f"Tarefa concluída: {tarefas[idx]['texto']}")


def _todo_remove(id_str: Optional[str]) -> Resposta:
    """Remove uma tarefa pelo ID."""
    if not id_str or not id_str.strip().isdigit():
        return Resposta(sucesso=False, mensagem="Uso: todo remove <id>")
    tarefas = _carregar_tarefas()
    idx = int(id_str.strip()) - 1
    if idx < 0 or idx >= len(tarefas):
        return Resposta(sucesso=False, mensagem=f"Tarefa #{id_str} não encontrada.")
    removida = tarefas.pop(idx)
    for i, t in enumerate(tarefas):
        t["id"] = i + 1
    _salvar_tarefas(tarefas)
    return Resposta(sucesso=True, mensagem=f"Tarefa removida: {removida['texto']}")


def _todo_handler(alvo: Optional[str]) -> Resposta:
    """Roteia subcomandos do todo."""
    if not alvo:
        return _todo_list()
    partes = alvo.split(maxsplit=1)
    sub = partes[0].lower()
    resto = partes[1] if len(partes) > 1 else None
    if sub == "add":
        return _todo_add(resto)
    if sub == "list":
        return _todo_list()
    if sub == "done":
        return _todo_done(resto)
    if sub in ("remove", "rm", "del"):
        return _todo_remove(resto)
    return Resposta(sucesso=False, mensagem="Uso: todo add/list/done/remove")


def registrar(executor) -> None:
    """Registra o comando todo."""
    executor.registrar_plugin("todo", _todo_handler, "Tarefas: todo add/list/done/remove")
