"""
core/logger.py

Sistema de registro profissional do NEXUS.

Grava eventos em ~/.config/nexus/logs/nexus.log no formato:

    [NEXUS LOG]

    2026-07-21 20:30

    INFO:
    Sistema iniciado.

    COMMAND:
    abrir brave

    SUCCESS:
    Aplicação aberta.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Optional

from core.config import LOGS_DIR, garantir_estrutura


class NivelLog(str, Enum):
    """Níveis de severidade suportados pelo logger."""

    INFO = "INFO"
    COMMAND = "COMMAND"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    WARNING = "WARNING"
    UPDATE = "UPDATE"
    FAILURE = "FAILURE"


class NexusLogger:
    """
    Logger estruturado do NEXUS.

    Thread-safe para escrita sequencial no arquivo de log diário/único.
    """

    def __init__(self, arquivo: Optional[Path] = None) -> None:
        """
        Args:
            arquivo: caminho do arquivo de log. Padrão: ~/.config/nexus/logs/nexus.log
        """
        garantir_estrutura()
        self.arquivo = arquivo or (LOGS_DIR / "nexus.log")
        self._lock = Lock()
        self._cabecalho_garantido = False

    def info(self, mensagem: str) -> None:
        """Registra uma mensagem informativa."""
        self._escrever(NivelLog.INFO, mensagem)

    def comando(self, mensagem: str) -> None:
        """Registra um comando digitado pelo usuário."""
        self._escrever(NivelLog.COMMAND, mensagem)

    def sucesso(self, mensagem: str) -> None:
        """Registra o sucesso de uma operação."""
        self._escrever(NivelLog.SUCCESS, mensagem)

    def erro(self, mensagem: str) -> None:
        """Registra um erro."""
        self._escrever(NivelLog.ERROR, mensagem)

    def aviso(self, mensagem: str) -> None:
        """Registra um aviso."""
        self._escrever(NivelLog.WARNING, mensagem)

    def atualizacao(self, mensagem: str) -> None:
        """Registra um evento relacionado a atualização."""
        self._escrever(NivelLog.UPDATE, mensagem)

    def falha(self, mensagem: str) -> None:
        """Registra uma falha crítica."""
        self._escrever(NivelLog.FAILURE, mensagem)

    def _escrever(self, nivel: NivelLog, mensagem: str) -> None:
        """Persiste uma entrada formatada no arquivo de log."""
        agora = datetime.now().strftime("%Y-%m-%d %H:%M")
        bloco = (
            f"{agora}\n\n"
            f"{nivel.value}:\n"
            f"{mensagem.strip()}\n\n"
            f"{'─' * 40}\n\n"
        )

        with self._lock:
            try:
                self._rotacionar()
                self._garantir_cabecalho()
                with open(self.arquivo, "a", encoding="utf-8") as destino:
                    destino.write(bloco)
            except OSError:
                # Logger nunca deve derrubar o sistema principal.
                pass

    def _rotacionar(self) -> None:
        """Rotaciona o arquivo de log se exceder 1 MB."""
        if not self.arquivo.exists():
            return
        if self.arquivo.stat().st_size >= 1_048_576:
            backup = self.arquivo.with_name(f"{self.arquivo.name}.1")
            try:
                if backup.exists():
                    backup.unlink()
                self.arquivo.rename(backup)
                self._cabecalho_garantido = False
            except OSError:
                pass

    def _garantir_cabecalho(self) -> None:
        """Escreve o cabeçalho [NEXUS LOG] na primeira utilização do arquivo."""
        if self._cabecalho_garantido:
            return
        if not self.arquivo.exists() or self.arquivo.stat().st_size == 0:
            self.arquivo.parent.mkdir(parents=True, exist_ok=True)
            with open(self.arquivo, "a", encoding="utf-8") as destino:
                destino.write("[NEXUS LOG]\n\n")
        self._cabecalho_garantido = True


# Instância global compartilhada pelo sistema
logger = NexusLogger()
