"""
core/theme.py

Sistema oficial de tema do NEXUS (v0.2.2 — Kernel Identity).

Única fonte de verdade para:
    - paleta de cores (assets/colors.json)
    - estilos Rich
    - componentes visuais reutilizáveis
    - carregamento de assets de marca (logo ASCII, banner)

Demais módulos devem importar cores e componentes daqui
(ou via core.ui, que reexporta esta API por compatibilidade).
"""

from __future__ import annotations

import json
import platform
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Sequence

from rich.align import Align
from rich.box import ROUNDED
from rich.console import Console, Group, RenderableType
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

# ── Paths ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
COLORS_FILE = ASSETS_DIR / "colors.json"
LOGO_ASCII_FILE = ASSETS_DIR / "logo_ascii.txt"
BANNER_FILE = ASSETS_DIR / "banner.txt"
LOGO_PNG_FILE = ASSETS_DIR / "logo.png"

console = Console()

# ── Paleta padrão (fallback se colors.json estiver ausente) ───────────────────

_DEFAULT_PALETTE: Dict[str, str] = {
    "neon": "#00FFFF",
    "tech": "#0077FF",
    "primary": "#00A8FF",
    "dark": "#001B44",
    "white": "#E8F4FF",
    "success": "#00E5A0",
    "error": "#FF4D6D",
    "warning": "#FFC857",
    "secondary": "#7BA3C9",
    "muted": "#4A6A8A",
    "black": "#000000",
}


def _carregar_paleta() -> Dict[str, str]:
    """Carrega a paleta de assets/colors.json com fallback seguro."""
    try:
        with open(COLORS_FILE, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        paleta = dados.get("palette", {})
        if isinstance(paleta, dict) and paleta:
            return {**_DEFAULT_PALETTE, **{k: str(v) for k, v in paleta.items()}}
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    return dict(_DEFAULT_PALETTE)


_PALETTE = _carregar_paleta()

# API pública de cores (nomes estáveis usados em todo o projeto)
COR_NEON = _PALETTE["neon"]
COR_TECNOLOGICO = _PALETTE["tech"]
COR_PRIMARIA = _PALETTE["primary"]
COR_ESCURO = _PALETTE["dark"]
COR_BRANCO = _PALETTE["white"]
COR_SUCESSO = _PALETTE["success"]
COR_ERRO = _PALETTE["error"]
COR_ALERTA = _PALETTE["warning"]
COR_TEXTO_SECUNDARIO = _PALETTE["secondary"]
COR_MUTED = _PALETTE["muted"]
COR_ACENTO = COR_NEON

PROMPT = (
    f"[bold {COR_PRIMARIA}]NEXUS[/bold {COR_PRIMARIA}] "
    f"[bold {COR_NEON}]❯[/bold {COR_NEON}] "
)

_CARACTERE_REGRA = "═"


# ── Assets de marca ───────────────────────────────────────────────────────────


def carregar_logo_ascii() -> str:
    """
    Carrega a logo ASCII oficial (letra N geométrica).

    Returns:
        str: arte ASCII da marca; fallback embutido se o arquivo faltar.
    """
    fallback = (
        "███╗   ██╗\n"
        "████╗  ██║\n"
        "██╔██╗ ██║\n"
        "██║╚██╗██║\n"
        "██║ ╚████║\n"
        "╚═╝  ╚═══╝"
    )
    try:
        texto = LOGO_ASCII_FILE.read_text(encoding="utf-8").rstrip("\n")
        return texto if texto.strip() else fallback
    except OSError:
        return fallback


def carregar_banner_ascii() -> str:
    """
    Carrega o letreiro ASCII completo (palavra NEXUS).

    Returns:
        str: banner ASCII; fallback embutido se o arquivo faltar.
    """
    fallback = (
        "███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗\n"
        "████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝\n"
        "██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗\n"
        "██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║\n"
        "██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║\n"
        "╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
    )
    try:
        texto = BANNER_FILE.read_text(encoding="utf-8").rstrip("\n")
        return texto if texto.strip() else fallback
    except OSError:
        return fallback


def caminho_logo_png() -> Optional[Path]:
    """Retorna o caminho de assets/logo.png se existir."""
    return LOGO_PNG_FILE if LOGO_PNG_FILE.is_file() else None


def paleta() -> Dict[str, str]:
    """Retorna uma cópia da paleta oficial carregada."""
    return dict(_PALETTE)


# ── Componentes visuais ───────────────────────────────────────────────────────


def regra(estilo: Optional[str] = None) -> None:
    """Imprime um separador horizontal no estilo NEXUS."""
    console.rule(style=estilo or COR_PRIMARIA, characters=_CARACTERE_REGRA)


def render_logo_ascii(gradiente: bool = True) -> Group:
    """
    Renderiza a logo ASCII (N) centralizada, com gradiente neon → tech.

    Args:
        gradiente: se True, aplica transição de cor nas linhas.
    """
    linhas = carregar_logo_ascii().splitlines()
    cores = (COR_NEON, COR_PRIMARIA, COR_TECNOLOGICO)
    renderizaveis = []
    total = max(len(linhas), 1)
    for indice, linha in enumerate(linhas):
        if gradiente:
            cor = cores[min(indice * len(cores) // total, len(cores) - 1)]
        else:
            cor = COR_PRIMARIA
        renderizaveis.append(Align.center(Text(linha, style=f"bold {cor}")))
    return Group(*renderizaveis)


def render_banner_ascii() -> Group:
    """Renderiza o letreiro ASCII completo centralizado."""
    linhas = carregar_banner_ascii().splitlines()
    return Group(
        *[Align.center(Text(linha, style=f"bold {COR_PRIMARIA}")) for linha in linhas]
    )


def painel(
    titulo: str,
    conteudo: Iterable[str],
    cor: str = COR_PRIMARIA,
) -> Panel:
    """Monta um painel padronizado do NEXUS."""
    corpo = "\n".join(linha for linha in conteudo if linha is not None)
    return Panel(
        corpo,
        title=Text(titulo, style=f"bold {COR_BRANCO}"),
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
    """Monta uma tabela padronizada do NEXUS."""
    tabela_rich = Table(
        title=Text(titulo, style=f"bold {COR_BRANCO}"),
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
    """Gera uma barra de progresso textual colorida."""
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
    return f"[{cor}]{barra}[/] [{COR_BRANCO}]{percentual:.0f}%[/]"


def status_indicador(ativo: bool = True) -> Text:
    """Indicador compacto ONLINE / OFFLINE."""
    if ativo:
        return Text("● ONLINE", style=f"bold {COR_NEON}")
    return Text("● OFFLINE", style=f"bold {COR_ERRO}")


def painel_identidade(
    versao: str,
    codename: str,
    usuario: Optional[str] = None,
    online: bool = True,
) -> Panel:
    """
    Painel oficial de identidade do NEXUS.

    Exemplo visual::

        ╭──────────────────────────────╮
        │          NEXUS               │
        │ Networked Executive System   │
        ├──────────────────────────────┤
        │ Version: v0.2.2 Alpha        │
        │ Codename: Kernel Identity    │
        │ Status: ONLINE               │
        ╰──────────────────────────────╯
    """
    cabecalho = Text(justify="center")
    cabecalho.append("NEXUS\n", style=f"bold {COR_PRIMARIA}")
    cabecalho.append(
        "Networked Executive Intelligence System\n",
        style=COR_BRANCO,
    )

    corpo = Text()
    corpo.append("Version:  ", style=COR_TEXTO_SECUNDARIO)
    corpo.append(f"{versao}\n", style=f"bold {COR_NEON}")
    corpo.append("Codename: ", style=COR_TEXTO_SECUNDARIO)
    corpo.append(f"{codename}\n", style=f"bold {COR_PRIMARIA}")
    corpo.append("Status:   ", style=COR_TEXTO_SECUNDARIO)
    corpo.append(
        "ONLINE\n" if online else "OFFLINE\n",
        style=f"bold {COR_NEON if online else COR_ERRO}",
    )
    if usuario:
        corpo.append("User:     ", style=COR_TEXTO_SECUNDARIO)
        corpo.append(f"{usuario}\n", style=f"bold {COR_BRANCO}")

    return Panel(
        Group(cabecalho, Rule(style=COR_TECNOLOGICO), corpo),
        border_style=COR_PRIMARIA,
        box=ROUNDED,
        padding=(1, 2),
        style=f"on {COR_ESCURO}",
    )


def cabecalho_ajuda(versao: str, codename: str) -> RenderableType:
    """Cabeçalho com logo + identidade para a tela de ajuda."""
    return Group(
        render_logo_ascii(),
        Text(""),
        Align.center(Text("NEXUS", style=f"bold {COR_PRIMARIA}")),
        Align.center(
            Text(
                "Networked Executive Intelligence System",
                style=COR_BRANCO,
            )
        ),
        Align.center(Text(f"{versao} · {codename}", style=COR_TEXTO_SECUNDARIO)),
        Text(""),
    )


def detectar_distro() -> str:
    """Detecta um nome amigável para o sistema operacional."""
    try:
        info = platform.freedesktop_os_release()
        return info.get("PRETTY_NAME", platform.system())
    except (AttributeError, OSError):
        return platform.system()


def meta_tema() -> Dict[str, Any]:
    """Metadados do tema carregado (útil para debug / version)."""
    return {
        "palette": paleta(),
        "logo_ascii": LOGO_ASCII_FILE.exists(),
        "banner": BANNER_FILE.exists(),
        "logo_png": LOGO_PNG_FILE.exists(),
        "colors_file": COLORS_FILE.exists(),
    }
