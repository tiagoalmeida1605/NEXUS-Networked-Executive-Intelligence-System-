"""
core/executor.py

Responsável exclusivamente por encaminhar comandos já interpretados
pelo parser para o módulo de commands/ correto.

O executor não implementa lógica de negócio própria — apenas roteia.
"""

from typing import Any, Callable, Dict

from commands import apps, browser, info, system
from core.parser import Comando
from core.response import Resposta


class Executor:
    """Encaminha comandos interpretados para os módulos responsáveis por executá-los."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Args:
            config: dicionário de configuração carregado de config/config.json.
        """
        self.config = config
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

        if comando.acao == "sair":
            return Resposta(sucesso=True, mensagem="Encerrando NEXUS...", encerrar=True)

        funcao = self._comandos_simples.get(comando.acao)
        if funcao:
            return funcao()

        return Resposta(sucesso=False, mensagem='Comando desconhecido.\nDigite "ajuda".')

    @staticmethod
    def _ajuda() -> Resposta:
        """Monta a mensagem de ajuda com todos os comandos disponíveis."""
        texto = (
            "Comandos disponíveis:\n"
            "\n"
            "  ajuda             exibe esta lista de comandos\n"
            "  hora              exibe a hora atual\n"
            "  data              exibe a data atual\n"
            "  cpu               exibe o uso da CPU\n"
            "  ram               exibe o uso da memória RAM\n"
            "  disco             exibe o uso do disco\n"
            "  sistema           exibe informações do sistema operacional\n"
            "  limpar            limpa a tela\n"
            "  sair              encerra o NEXUS\n"
            "\n"
            "  abrir brave       abre o navegador Brave\n"
            "  abrir firefox     abre o navegador Firefox\n"
            "  abrir terminal    abre o terminal\n"
            "  abrir pycharm     abre o PyCharm\n"
            "  abrir webstorm    abre o WebStorm\n"
            "  abrir vscode      abre o VSCode\n"
            "  abrir downloads   abre a pasta Downloads\n"
            "  abrir documentos  abre a pasta Documentos\n"
            "\n"
            "  google            abre o Google\n"
            "  youtube           abre o YouTube\n"
            "  github            abre o GitHub"
        )
        return Resposta(sucesso=True, mensagem=texto)
