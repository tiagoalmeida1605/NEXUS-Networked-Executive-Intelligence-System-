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
from commands import history_cmd, update_cmd, doctor_cmd
from commands import banner_cmd, credits_cmd, motd_cmd, theme_cmd, reload_cmd
from commands import ai_cmd
from core import ui
from core.logger import logger
from core.parser import Comando
from core.response import Resposta

if TYPE_CHECKING:
    from core.history import Historico

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
        self.config = config
        self.historico = historico

        # Catálogo de comandos internos sem alvo
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
            "doctor": doctor_cmd.doctor,
            "history": lambda: self._historico(None),
            "historico": lambda: self._historico(None),
            "sair": self._sair,
            "exit": self._sair,
            "quit": self._sair,
            "banner": banner_cmd.banner,
            "credits": credits_cmd.credits,
            "motd": motd_cmd.motd,
            "theme": self._theme,
            "reload": reload_cmd.reload_config,
            "cls": system.limpar,
            "models": lambda: self._models(),
        }

        # Plugins registrados dinamicamente (com suporte a alvo)
        self._plugins: Dict[str, Callable[[Optional[str]], Resposta]] = {}

        # Rastreamento de plugins para o comando de ajuda
        self._plugin_help: list[tuple[str, str]] = []

    def registrar_plugin(
        self, comando: str, handler: Callable[[str | None], Resposta], descricao: str
    ) -> None:
        """Permite que plugins adicionem novos comandos no NEXUS."""
        cmd_lower = comando.lower().strip()
        if cmd_lower in self._internos or cmd_lower in self._plugins:
            logger.aviso(
                f"Plugin tentou sobrescrever o comando interno '{cmd_lower}'. Ignorado."
            )
            return

        self._plugins[cmd_lower] = handler
        self._plugin_help.append((cmd_lower, f"[Plugin] {descricao}"))

    def executar(self, comando: Comando) -> Resposta:
        """
        Executa um comando ja interpretado e retorna a resposta.

        Args:
            comando: objeto Comando gerado pelo core/parser.py.

        Returns:
            Resposta: resultado padronizado da execucao.
        """
        try:
            return self._rotear(comando)
        except Exception as erro:  # noqa: BLE001
            logger.erro(f"Falha ao executar '{comando.bruto}': {erro}")
            return Resposta(
                sucesso=False,
                mensagem=(
                    f"Erro ao executar o comando interno: {erro}\n"
                    "O NEXUS continua em execucao."
                ),
            )

    def _rotear(self, comando: Comando) -> Resposta:
        """Roteia para handler interno; nunca envia texto cru ao SO."""
        if comando.acao == "vazio":
            return Resposta(sucesso=False, mensagem="")

        if comando.acao == "abrir":
            if not comando.alvo:
                return Resposta(
                    sucesso=False,
                    mensagem="Uso: abrir <alvo>\nExemplo: abrir brave",
                )
            return apps.abrir(comando.alvo, self.config)

        if comando.acao == "shell":
            return shell_cmd.executar(comando.alvo)

        if comando.acao in ("history", "historico") and comando.alvo:
            return self._historico(comando.alvo)

        if comando.acao == "theme" and comando.alvo == "list":
            from commands.theme_cmd import theme_list
            return theme_list()

        if comando.acao == "theme":
            from commands.theme_cmd import theme_info
            return theme_info()

        # AI command with alvo support (ai, ai status)
        if comando.acao == "ai":
            return ai_cmd.ai_mode(comando.alvo)

        # Plugins dinâmicos (com suporte a alvo)
        plugin_handler = self._plugins.get(comando.acao)
        if plugin_handler is not None:
            return plugin_handler(comando.alvo)

        # Catálogo de comandos internos sem alvo
        handler = self._internos.get(comando.acao)
        if handler is not None:
            return handler()

        return Resposta(sucesso=False, mensagem=MSG_NAO_ENCONTRADO)

    def _update(self) -> Resposta:
        """Handler interno do atualizador."""
        return update_cmd.executar_atualizacao(interativo=True)

    def _theme(self) -> Resposta:
        """Handler interno do comando theme."""
        from commands.theme_cmd import theme_info
        return theme_info()

    @staticmethod
    def _about() -> Resposta:
        """Handler interno do comando about."""
        from commands import about_cmd
        return about_cmd.about()

    @staticmethod
    def _sair() -> Resposta:
        return Resposta(sucesso=True, mensagem="Encerrando NEXUS...", encerrar=True)

    @staticmethod
    def _models() -> Resposta:
        """Handler interno do comando models."""
        return ai_cmd.listar_modelos()

    def _historico(self, alvo: Optional[str]) -> Resposta:
        """Roteia subcomandos do historico."""
        if self.historico is None:
            return Resposta(sucesso=False, mensagem="Historico nao inicializado.")
        if alvo in ("limpar", "clear"):
            return history_cmd.limpar_historico(self.historico)
        return history_cmd.exibir_historico(self.historico)

    def _ajuda(self) -> Resposta:
        """Monta os paineis de ajuda alinhados ao catalogo do roteador."""
        from rich.console import Group
        from core.config import carregar_versao

        meta = carregar_versao()
        versao = str(meta.get("label", "v0.5 Alpha"))
        codename = str(meta.get("codename", "AI Framework"))

        comandos_nexus = [
            ("help / ajuda", "Exibe esta lista de comandos"),
            ("about", "Identidade oficial do NEXUS"),
            ("version / versao", "Exibe a versao do NEXUS"),
            ("hora", "Exibe a hora atual"),
            ("data", "Exibe a data atual"),
            ("cpu", "Exibe o uso da CPU"),
            ("ram", "Exibe o uso da memoria RAM"),
            ("disco", "Exibe o uso do disco"),
            ("sistema", "Exibe informacoes do sistema operacional"),
            ("history", "Exibe o historico de comandos"),
            ("history limpar", "Limpa o historico de comandos"),
            ("update", "Atualizador interno do NEXUS"),
            ("doctor", "Diagnostico completo do sistema"),
            ("shell <cmd>", "Executa um comando no sistema (explicito)"),
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

        comandos_ai = [
            ("ai", "Modo conversa com IA"),
            ("ai status", "Status do sistema de IA"),
            ("models", "Lista modelos de IA disponiveis"),
        ]

        comandos_novos = [
            ("banner", "Exibe o banner do NEXUS"),
            ("credits", "Creditos do NEXUS"),
            ("motd", "Mensagem do dia"),
            ("theme", "Informacoes do tema atual"),
            ("theme list", "Lista temas disponiveis"),
            ("reload", "Recarrega configuracoes"),
            ("cls", "Limpa a tela (alias)"),
        ]

        tabela_nexus = ui.tabela(
            "NEXUS (internos)",
            ["Comando", "Descricao"],
            comandos_nexus,
            cor=ui.COR_PRIMARIA,
        )
        tabela_apps = ui.tabela(
            "Aplicativos & Sites",
            ["Comando", "Descricao"],
            comandos_apps,
            cor=ui.COR_TECNOLOGICO,
        )

        tabelas = [tabela_nexus, tabela_apps]

        if comandos_ai:
            tabela_ai = ui.tabela(
                "Inteligencia Artificial",
                ["Comando", "Descricao"],
                comandos_ai,
                cor=ui.COR_NEON,
            )
            tabelas.append(tabela_ai)

        if comandos_novos:
            tabela_novos = ui.tabela(
                "Extras",
                ["Comando", "Descricao"],
                comandos_novos,
                cor=ui.COR_SUCESSO,
            )
            tabelas.append(tabela_novos)

        if self._plugin_help:
            tabela_plugins = ui.tabela(
                "Plugins (Modulos)",
                ["Comando", "Descricao"],
                self._plugin_help,
                cor=ui.COR_SUCESSO,
            )
            tabelas.append(tabela_plugins)

        colunas = Columns(tabelas, equal=False, expand=False)
        return Resposta(
            sucesso=True,
            mensagem="Comandos disponiveis.",
            renderable=Group(ui.cabecalho_ajuda(versao, codename), colunas),
        )
