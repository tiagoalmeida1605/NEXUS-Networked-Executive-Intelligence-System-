"""
core/history.py

Histórico persistente de comandos do NEXUS.

Armazena entradas em ~/.config/nexus/history/commands.txt e integra-se
ao readline para permitir repetir comandos recentes com as setas ↑ ↓.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from core.config import HISTORY_DIR, garantir_estrutura

HISTORY_FILE = HISTORY_DIR / "commands.txt"
MAX_ENTRADAS = 500


class Historico:
    """Gerencia leitura, escrita e navegação do histórico de comandos."""

    def __init__(self, arquivo: Optional[Path] = None, limite: int = MAX_ENTRADAS) -> None:
        """
        Args:
            arquivo: caminho do arquivo de histórico.
            limite: quantidade máxima de entradas persistidas.
        """
        garantir_estrutura()
        self.arquivo = arquivo or HISTORY_FILE
        self.limite = limite
        self._entradas: List[str] = []
        self._carregar()

    def _carregar(self) -> None:
        """Carrega o histórico do disco para a memória."""
        if not self.arquivo.exists():
            self._entradas = []
            return
        try:
            texto = self.arquivo.read_text(encoding="utf-8")
            self._entradas = [linha.strip() for linha in texto.splitlines() if linha.strip()]
        except OSError:
            self._entradas = []

    def adicionar(self, comando: str) -> None:
        """
        Adiciona um comando ao histórico (ignora vazios e duplicatas consecutivas).

        Args:
            comando: texto digitado pelo usuário.
        """
        texto = comando.strip()
        if not texto:
            return
        if self._entradas and self._entradas[-1] == texto:
            return

        self._entradas.append(texto)
        if len(self._entradas) > self.limite:
            self._entradas = self._entradas[-self.limite :]
        self._salvar()
        # O readline já registra a linha digitada via input();
        # não chamar add_history aqui evita duplicatas no ↑ ↓.

    def listar(self, limite: Optional[int] = None) -> List[str]:
        """
        Retorna os comandos do histórico, do mais antigo ao mais recente.

        Args:
            limite: se informado, retorna apenas as N entradas mais recentes.
        """
        if limite is None or limite <= 0:
            return list(self._entradas)
        return self._entradas[-limite:]

    def limpar(self) -> None:
        """Remove todo o histórico em memória e no disco."""
        self._entradas = []
        self._salvar()
        try:
            import readline

            readline.clear_history()
        except Exception:  # noqa: BLE001
            pass

    def _salvar(self) -> None:
        """Persiste o histórico atual no disco."""
        try:
            self.arquivo.parent.mkdir(parents=True, exist_ok=True)
            conteudo = "\n".join(self._entradas)
            if self._entradas:
                conteudo += "\n"
            self.arquivo.write_text(conteudo, encoding="utf-8")
        except OSError:
            pass

    def habilitar_readline(self) -> bool:
        """
        Integra o histórico ao módulo readline para navegação com ↑ ↓.

        Returns:
            bool: True se o readline foi configurado com sucesso.
        """
        try:
            import readline
        except ImportError:
            return False

        try:
            readline.clear_history()
            for entrada in self._entradas:
                readline.add_history(entrada)
            readline.set_history_length(self.limite)
            return True
        except Exception:  # noqa: BLE001
            return False
