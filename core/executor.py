"""
core/executor.py

Responsável exclusivamente por encaminhar comandos já interpretados
pelo parser para o módulo de commands/ correto.

O executor não implementa lógica de negócio própria — apenas roteia.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

from rich.columns import Columns

from commands import apps, browser, info, system
from commands import history_cmd, update_cmd
from core import ui
from core.parser import Comando
from core.response import Resposta

if TYPE_CHECKING:
    from core.history import Historico


class Executor:
    """Encaminha comandos interpretados para os módulos responsáveis por executá-los."""

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
        self._comandos_simples: Dict[str, Callable[[], Resposta]] = {
            "hora": info.hora,
            "data": info.data,
            "cpu": system.cpu,
            "ram": system.ram,
            "disco": system.disco,
            "sistema": system.sistema,
            "google": browser.google,
            "youtube": browser.youtube,
            "github": browser.github,
        }

    def executar(self, comando: Comando) -> Resposta:
        """
        Executa um comando já interpretado e retorna a resposta correspondente.

        Args:
            comando: objeto Comando gerado pelo core/parser.py.

        Returns:
            Resposta: resultado padronizado da execução.
        """
        if comando.acao == "vazio":
            return Resposta(sucesso=False, mensagem="")

        if comando.acao == "abrir" and comando.alvo:
            return apps.abrir(comando.alvo, self.config)

        if comando.acao == "limpar":
            return system.limpar()

        if comando.acao in ("ajuda", "help"):
            return self._ajuda()

        if comando.acao in ("history", "historico"):
            return self._historico(comando.alvo)

        if comando.acao == "update":
            return update_cmd.executar_atualizacao(interativo=True)

        if comando.acao == "sair":
            return Resposta(sucesso=True, mensagem="Encerrando NEXUS...", encerrar=True)

        funcao = self._comandos_simples.get(comando.acao)
        if funcao:
            return funcao()

        return Resposta(sucesso=False, mensagem='Comando desconhecido.\nDigite "ajuda".')

    def _historico(self, alvo: Optional[str]) -> Resposta:
        """Roteia subcomandos do histórico."""
        if self.historico is None:
            return Resposta(sucesso=False, mensagem="Histórico não inicializado.")

        if alvo in ("limpar", "clear"):
            return history_cmd.limpar_historico(self.historico)

        return history_cmd.exibir_historico(self.historico)

    @staticmethod
    def _ajuda() -> Resposta:
        """Monta os painéis de ajuda com todos os comandos disponíveis."""
        comandos_sistema = [
            ("ajuda", "Exibe esta lista de comandos"),
            ("hora", "Exibe a hora atual"),
            ("data", "Exibe a data atual"),
            ("cpu", "Exibe o uso da CPU"),
            ("ram", "Exibe o uso da memória RAM"),
            ("disco", "Exibe o uso do disco"),
            ("sistema", "Exibe informações do sistema operacional"),
            ("history", "Exibe o histórico de comandos"),
            ("history limpar", "Limpa o histórico de comandos"),
            ("update", "Verifica e aplica atualizações seguras"),
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

        tabela_sistema = ui.tabela(
            "Sistema", ["Comando", "Descrição"], comandos_sistema, cor=ui.COR_PRIMARIA
        )
        tabela_apps = ui.tabela(
            "Aplicativos & Sites", ["Comando", "Descrição"], comandos_apps, cor=ui.COR_TECNOLOGICO
        )

        colunas = Columns([tabela_sistema, tabela_apps], equal=False, expand=False)
        return Resposta(sucesso=True, mensagem="Comandos disponíveis.", renderable=colunas)
