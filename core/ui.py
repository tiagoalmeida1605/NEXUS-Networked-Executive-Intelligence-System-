"""
core/ui.py

Camada de apresentação do NEXUS. Concentra toda a identidade visual do
projeto — cores, painéis, tabelas, regras e barras de progresso — para
que os demais módulos nunca precisem montar componentes Rich diretamente.

Paleta oficial (tons de azul tecnológico):
    Azul principal .... #00A8FF
    Azul tecnológico .. #0077FF
    Azul escuro ....... #001B44
    Azul neon ......... #00FFFF
    Branco ............ #E8F4FF
"""

from __future__ import annotations

import platform
from typing import Iterable, Sequence

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Paleta oficial do NEXUS
COR_PRIMARIA = "#00A8FF"
COR_TECNOLOGICO = "#0077FF"
COR_ESCURO = "#001B44"
COR_NEON = "#00FFFF"
COR_BRANCO = "#E8F4FF"

# Semântica
COR_ACENTO = COR_NEON
COR_SUCESSO = "#00E5A0"
COR_ERRO = "#FF4D6D"
COR_ALERTA = "#FFC857"
COR_TEXTO_SECUNDARIO = "#7BA3C9"
COR_MUTED = "#4A6A8A"

# Prompt personalizado exibido a cada iteração do loop principal
PROMPT = (
    f"[bold {COR_PRIMARIA}]NEXUS[/bold {COR_PRIMARIA}] "
    f"[bold {COR_NEON}]❯[/bold {COR_NEON}] "
)


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
        title=f"[bold {COR_BRANCO}]{titulo}[/bold {COR_BRANCO}]",
        border_style=cor,
        box=ROUNDED,
        padding=(1, 2),
        style=f"on {COR_ESCURO}",
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
        title=f"[bold {COR_BRANCO}]{titulo}[/bold {COR_BRANCO}]",
        box=ROUNDED,
        border_style=cor,
        header_style=f"bold {COR_NEON}",
        title_style=f"bold {COR_PRIMARIA}",
        expand=False,
    )
    for coluna in colunas:
        tabela_rich.add_column(coluna, style=COR_BRANCO)
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
    return f"[{cor}]{barra}[/{cor}] [{COR_BRANCO}]{percentual:.0f}%[/{COR_BRANCO}]"


def status_indicador(ativo: bool = True) -> str:
    """
    Retorna um indicador de status compacto.

    Args:
        ativo: se True, exibe online (neon); caso contrário, offline.
    """
    if ativo:
        return f"[bold {COR_NEON}]● ONLINE[/bold {COR_NEON}]"
    return f"[bold {COR_ERRO}]● OFFLINE[/bold {COR_ERRO}]"


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
