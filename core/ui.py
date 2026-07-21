"""
core/ui.py

Camada de apresentação do NEXUS. Concentra toda a identidade visual do
projeto — cores, painéis, tabelas, regras e barras de progresso — para
que os demais módulos nunca precisem montar componentes Rich diretamente.

Isso garante uma identidade visual única e consistente em todo o sistema.
"""

import platform
from typing import Iterable, Sequence

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Paleta de cores da identidade visual do NEXUS
COR_PRIMARIA = "bright_cyan"
COR_ACENTO = "magenta"
COR_SUCESSO = "green"
COR_ERRO = "red"
COR_ALERTA = "yellow"
COR_TEXTO_SECUNDARIO = "grey62"

# Prompt personalizado exibido a cada iteração do loop principal
PROMPT = "[bold bright_cyan]NEXUS[/bold bright_cyan] [bold magenta]❯[/bold magenta] "


def painel(titulo: str, conteudo: Iterable[str], cor: str = COR_PRIMARIA) -> Panel:
    """
    Monta um painel padronizado do NEXUS a partir de linhas de texto.

    Args:
        titulo: título exibido na borda superior do painel.
        conteudo: linhas de texto (já com markup Rich, se necessário).
        cor: cor da borda do painel.

    Returns:
        Panel: painel Rich pronto para ser exibido ou embutido em uma Resposta.
    """
    corpo = "\n".join(conteudo)
    return Panel(
        corpo,
        title=f"[bold]{titulo}[/bold]",
        border_style=cor,
        box=ROUNDED,
        padding=(1, 2),
    )


def tabela(
    titulo: str,
    colunas: Sequence[str],
    linhas: Sequence[Sequence[str]],
    cor: str = COR_PRIMARIA,
) -> Table:
    """
    Monta uma tabela padronizada do NEXUS.

    Args:
        titulo: título exibido acima da tabela.
        colunas: nomes das colunas.
        linhas: uma sequência de linhas, cada uma com um valor por coluna.
        cor: cor da borda e do cabeçalho da tabela.

    Returns:
        Table: tabela Rich pronta para ser exibida ou embutida em uma Resposta.
    """
    tabela_rich = Table(
        title=titulo,
        box=ROUNDED,
        border_style=cor,
        header_style=f"bold {cor}",
        expand=False,
    )
    for coluna in colunas:
        tabela_rich.add_column(coluna)
    for linha in linhas:
        tabela_rich.add_row(*linha)
    return tabela_rich


def barra_progresso(percentual: float, largura: int = 24) -> str:
    """
    Gera uma barra de progresso textual colorida conforme o percentual.

    A cor muda automaticamente: verde (uso baixo), amarelo (uso moderado)
    e vermelho (uso alto), dando um retorno visual imediato.

    Args:
        percentual: valor entre 0 e 100.
        largura: largura da barra em caracteres.

    Returns:
        str: string com markup Rich pronta para impressão.
    """
    percentual = max(0.0, min(100.0, percentual))
    preenchido = int((percentual / 100) * largura)
    vazio = largura - preenchido

    if percentual < 60:
        cor = COR_SUCESSO
    elif percentual < 85:
        cor = COR_ALERTA
    else:
        cor = COR_ERRO

    barra = "█" * preenchido + "░" * vazio
    return f"[{cor}]{barra}[/{cor}] {percentual:.0f}%"


def detectar_distro() -> str:
    """
    Detecta um nome amigável para o sistema operacional em execução.

    Usa as informações do /etc/os-release quando disponíveis (Linux),
    recorrendo a platform.system() em qualquer outro caso.

    Returns:
        str: nome amigável do sistema operacional (ex.: "Linux Mint 21.3").
    """
    try:
        info = platform.freedesktop_os_release()
        return info.get("PRETTY_NAME", platform.system())
    except (AttributeError, OSError):
        return platform.system()
