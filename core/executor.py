"""
core/executor.py

Roteador de comandos internos do NEXUS.

Regra de ouro:
    1. Verificar se a ação está no catálogo interno do NEXUS.
    2. Se sim, executar a função correspondente (nunca o SO).
    3. Comandos do sistema operacional só via ``shell <comando>``.
    4. Comando desconhecido → mensagem amigável, sem crash e sem shell.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from rich.columns import Columns

from commands import apps, browser, info, shell_cmd, system
from commands import history_cmd, update_cmd
from core import ui
from core.logger import logger
from core.parser import Comando
from core.response import Resposta

if TYPE_CHECKING:
    from core.history import Historico

# Mensagem padrão para comandos que não existem no catálogo interno
MSG_NAO_ENCONTRADO = (
    "Comando não encontrado. Use 'help' para ver os comandos disponíveis."
)


class Executor:
    """
    Encaminha comandos interpretados apenas para handlers internos do NEXUS.

    Nenhum texto digitado é repassado automaticamente ao sistema operacional.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        historico: Optional["Historico"] = None,
    ) -> None:
        """
        Args:
            config: dicionário de configuração do usuário.
            historico: instância opcional do gerenciador de histórico.
        """
        self.config = config
        self.historico = historico

        # Catálogo explícito de comandos internos (ação → handler).
        # Handlers sem alvo: Callable[[], Resposta]
        self._internos: Dict[str, Callable[[], Resposta]] = {
            "hora": info.hora,
            "data": info.data,
            "cpu": system.cpu,
            "ram": system.ram,
            "disco": system.disco,
            "sistema": system.sistema,
            "google": browser.google,
            "youtube": browser.youtube,
            "github": browser.github,
            "limpar": system.limpar,
            "clear": system.limpar,
            "ajuda": self._ajuda,
            "help": self._ajuda,
            "version": info.versao,
            "versao": info.versao,
            "about": self._about,
            "update": self._update,
            "history": lambda: self._historico(None),
            "historico": lambda: self._historico(None),
            "sair": self._sair,
            "exit": self._sair,
            "quit": self._sair,
        }

    def executar(self, comando: Comando) -> Resposta:
        """
        Executa um comando já interpretado e retorna a resposta correspondente.

        Args:
            comando: objeto Comando gerado pelo core/parser.py.

        Returns:
            Resposta: resultado padronizado da execução.
        """
        try:
            return self._rotear(comando)
        except Exception as erro:  # noqa: BLE001
            logger.erro(f"Falha ao executar '{comando.bruto}': {erro}")
            return Resposta(
                sucesso=False,
                mensagem=(
                    f"Erro ao executar o comando interno: {erro}\n"
                    "O NEXUS continua em execução."
                ),
            )

    def _rotear(self, comando: Comando) -> Resposta:
        """Roteia para handler interno; nunca envia texto cru ao SO."""
        if comando.acao == "vazio":
            return Resposta(sucesso=False, mensagem="")

        # --- Comandos com alvo (ainda 100% internos) ---
        if comando.acao == "abrir":
            if not comando.alvo:
                return Resposta(
                    sucesso=False,
                    mensagem='Uso: abrir <alvo>\nExemplo: abrir brave',
                )
            return apps.abrir(comando.alvo, self.config)

        if comando.acao == "shell":
            # Única porta explícita para o sistema operacional
            return shell_cmd.executar(comando.alvo)

        if comando.acao in ("history", "historico") and comando.alvo:
            return self._historico(comando.alvo)

        # --- Catálogo de comandos internos sem alvo ---
        handler = self._internos.get(comando.acao)
        if handler is not None:
            return handler()

        # Desconhecido: NÃO executar no SO
        return Resposta(sucesso=False, mensagem=MSG_NAO_ENCONTRADO)

    def _update(self) -> Resposta:
        """Handler interno do atualizador do NEXUS (não é o 'update' do SO)."""
        return update_cmd.executar_atualizacao(interativo=True)

    @staticmethod
    def _about() -> Resposta:
        """Handler interno da tela About / identidade."""
        from commands import about_cmd

        return about_cmd.about()

    @staticmethod
    def _sair() -> Resposta:
        return Resposta(sucesso=True, mensagem="Encerrando NEXUS...", encerrar=True)

    def _historico(self, alvo: Optional[str]) -> Resposta:
        """Roteia subcomandos do histórico."""
        if self.historico is None:
            return Resposta(sucesso=False, mensagem="Histórico não inicializado.")

        if alvo in ("limpar", "clear"):
            return history_cmd.limpar_historico(self.historico)

        return history_cmd.exibir_historico(self.historico)

    def _ajuda(self) -> Resposta:
        """Monta os painéis de ajuda alinhados ao catálogo do roteador."""
        from rich.console import Group

        from core.config import carregar_versao

        meta = carregar_versao()
        versao = str(meta.get("label", "v0.2.2.1 Alpha"))
        codename = str(meta.get("codename", "Kernel Identity"))

        comandos_nexus = [
            ("help / ajuda", "Exibe esta lista de comandos"),
            ("about", "Identidade oficial do NEXUS"),
            ("version / versao", "Exibe a versão do NEXUS"),
            ("hora", "Exibe a hora atual"),
            ("data", "Exibe a data atual"),
            ("cpu", "Exibe o uso da CPU"),
            ("ram", "Exibe o uso da memória RAM"),
            ("disco", "Exibe o uso do disco"),
            ("sistema", "Exibe informações do sistema operacional"),
            ("history", "Exibe o histórico de comandos"),
            ("history limpar", "Limpa o histórico de comandos"),
            ("update", "Atualizador interno do NEXUS"),
            ("shell <cmd>", "Executa um comando no sistema (explícito)"),
            ("limpar", "Limpa a tela"),
            ("sair", "Encerra o NEXUS"),
        ]

        comandos_apps = [
            ("abrir brave", "Abre o navegador Brave"),
            ("abrir firefox", "Abre o navegador Firefox"),
            ("abrir terminal", "Abre o terminal"),
            ("abrir pycharm", "Abre o PyCharm"),
            ("abrir webstorm", "Abre o WebStorm"),
            ("abrir vscode", "Abre o VSCode"),
            ("abrir downloads", "Abre a pasta Downloads"),
            ("abrir documentos", "Abre a pasta Documentos"),
            ("google", "Abre o Google"),
            ("youtube", "Abre o YouTube"),
            ("github", "Abre o GitHub"),
        ]

        tabela_nexus = ui.tabela(
            "NEXUS (internos)",
            ["Comando", "Descrição"],
            comandos_nexus,
            cor=ui.COR_PRIMARIA,
        )
        tabela_apps = ui.tabela(
            "Aplicativos & Sites",
            ["Comando", "Descrição"],
            comandos_apps,
            cor=ui.COR_TECNOLOGICO,
        )

        colunas = Columns([tabela_nexus, tabela_apps], equal=False, expand=False)
        return Resposta(
            sucesso=True,
            mensagem="Comandos disponíveis.",
            renderable=Group(
                ui.cabecalho_ajuda(versao, codename),
                colunas,
            ),
        )
