"""
core/theme.py

Sistema oficial de tema do NEXUS (v0.2.2.1 — Kernel Identity).

Tema: NEXUS Blue Theme (assets/themes/nexus_blue.json)

Assets de marca:
    assets/branding/logo.png
    assets/branding/logo_with_background.png
    assets/branding/logo_ascii.txt
    assets/branding/banner.txt
    assets/branding/colors.json
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
BRANDING_DIR = ASSETS_DIR / "branding"
THEMES_DIR = ASSETS_DIR / "themes"

THEME_FILE = THEMES_DIR / "nexus_blue.json"
COLORS_FILE = BRANDING_DIR / "colors.json"
LOGO_ASCII_FILE = BRANDING_DIR / "logo_ascii.txt"
BANNER_FILE = BRANDING_DIR / "banner.txt"
LOGO_PNG_FILE = BRANDING_DIR / "logo.png"
LOGO_BG_PNG_FILE = BRANDING_DIR / "logo_with_background.png"

# Fallbacks legados (assets/ na raiz) — compatibilidade
_LEGACY_COLORS = ASSETS_DIR / "colors.json"
_LEGACY_LOGO_ASCII = ASSETS_DIR / "logo_ascii.txt"
_LEGACY_BANNER = ASSETS_DIR / "banner.txt"
_LEGACY_LOGO = ASSETS_DIR / "logo.png"

console = Console()

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

_THEME_META: Dict[str, Any] = {
    "name": "NEXUS Blue Theme",
    "id": "nexus_blue",
}


def _ler_json(caminho: Path) -> Optional[Dict[str, Any]]:
    """Lê um JSON de forma segura."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        return dados if isinstance(dados, dict) else None
    except (OSError, json.JSONDecodeError, TypeError):
        return None


def _carregar_paleta() -> Dict[str, str]:
    """
    Carrega a paleta do NEXUS Blue Theme.

    Ordem: themes/nexus_blue.json → branding/colors.json → legado → default.
    """
    for caminho in (THEME_FILE, COLORS_FILE, _LEGACY_COLORS):
        dados = _ler_json(caminho)
        if not dados:
            continue
        if caminho == THEME_FILE:
            _THEME_META["name"] = str(dados.get("name", _THEME_META["name"]))
            _THEME_META["id"] = str(dados.get("id", _THEME_META["id"]))
        paleta = dados.get("palette", {})
        if isinstance(paleta, dict) and paleta:
            return {**_DEFAULT_PALETTE, **{k: str(v) for k, v in paleta.items()}}
    return dict(_DEFAULT_PALETTE)


def _resolver_arquivo(*candidatos: Path) -> Path:
    """Retorna o primeiro caminho existente, ou o primeiro candidato."""
    for caminho in candidatos:
        if caminho.is_file():
            return caminho
    return candidatos[0]


_PALETTE = _carregar_paleta()

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

_LOGO_ASCII_PATH = _resolver_arquivo(LOGO_ASCII_FILE, _LEGACY_LOGO_ASCII)
_BANNER_PATH = _resolver_arquivo(BANNER_FILE, _LEGACY_BANNER)
_LOGO_PNG_PATH = _resolver_arquivo(LOGO_PNG_FILE, _LEGACY_LOGO)


def carregar_logo_ascii() -> str:
    """Carrega a logo ASCII oficial (letra N)."""
    fallback = (
        "███╗   ██╗\n"
        "████╗  ██║\n"
        "██╔██╗ ██║\n"
        "██║╚██╗██║\n"
        "██║ ╚████║\n"
        "╚═╝  ╚═══╝"
    )
    try:
        texto = _LOGO_ASCII_PATH.read_text(encoding="utf-8").rstrip("\n")
        return texto if texto.strip() else fallback
    except OSError:
        return fallback


def carregar_banner_ascii() -> str:
    """Carrega o letreiro ASCII completo (palavra NEXUS)."""
    fallback = (
        "███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗\n"
        "████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝\n"
        "██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗\n"
        "██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║\n"
        "██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║\n"
        "╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝"
    )
    try:
        texto = _BANNER_PATH.read_text(encoding="utf-8").rstrip("\n")
        return texto if texto.strip() else fallback
    except OSError:
        return fallback


def caminho_logo_png() -> Optional[Path]:
    """Logo sem fundo — ícone / UI futura / mobile."""
    return _LOGO_PNG_PATH if _LOGO_PNG_PATH.is_file() else None


def caminho_logo_com_fundo() -> Optional[Path]:
    """Logo com fundo — README, docs e apresentações."""
    return LOGO_BG_PNG_FILE if LOGO_BG_PNG_FILE.is_file() else None


def nome_tema() -> str:
    """Nome do tema ativo."""
    return str(_THEME_META.get("name", "NEXUS Blue Theme"))


def paleta() -> Dict[str, str]:
    """Cópia da paleta oficial carregada."""
    return dict(_PALETTE)


def regra(estilo: Optional[str] = None) -> None:
    """Separador horizontal no estilo NEXUS."""
    console.rule(style=estilo or COR_PRIMARIA, characters=_CARACTERE_REGRA)


def render_logo_ascii(gradiente: bool = True) -> Group:
    """Renderiza a logo ASCII (N) com gradiente neon → tech."""
    linhas = carregar_logo_ascii().splitlines()
    cores = (COR_NEON, COR_PRIMARIA, COR_TECNOLOGICO)
    renderizaveis = []
    total = max(len(linhas), 1)
    for indice, linha in enumerate(linhas):
        cor = (
            cores[min(indice * len(cores) // total, len(cores) - 1)]
            if gradiente
            else COR_PRIMARIA
        )
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
    """Painel padronizado do NEXUS."""
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
    """Tabela padronizada do NEXUS."""
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
    """Barra de progresso textual colorida."""
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
    """Indicador ONLINE / OFFLINE."""
    if ativo:
        return Text("● ONLINE", style=f"bold {COR_NEON}")
    return Text("● OFFLINE", style=f"bold {COR_ERRO}")


def painel_identidade(
    versao: str,
    codename: str,
    usuario: Optional[str] = None,
    online: bool = True,
) -> Panel:
    """Painel oficial de identidade do NEXUS."""
    cabecalho = Text(justify="center")
    cabecalho.append("NEXUS\n", style=f"bold {COR_PRIMARIA}")
    cabecalho.append("Networked Executive System\n", style=COR_BRANCO)

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
            Text("Networked Executive Intelligence System", style=COR_BRANCO)
        ),
        Align.center(Text(f"{versao} · {codename}", style=COR_TEXTO_SECUNDARIO)),
        Text(""),
    )


def detectar_distro() -> str:
    """Nome amigável do sistema operacional."""
    try:
        info = platform.freedesktop_os_release()
        return info.get("PRETTY_NAME", platform.system())
    except (AttributeError, OSError):
        return platform.system()


def meta_tema() -> Dict[str, Any]:
    """Metadados do tema e assets de marca."""
    return {
        "theme": nome_tema(),
        "theme_id": _THEME_META.get("id", "nexus_blue"),
        "palette": paleta(),
        "logo_ascii": _LOGO_ASCII_PATH.is_file(),
        "banner": _BANNER_PATH.is_file(),
        "logo_png": caminho_logo_png() is not None,
        "logo_with_background": caminho_logo_com_fundo() is not None,
        "colors_file": COLORS_FILE.exists() or _LEGACY_COLORS.exists(),
        "theme_file": THEME_FILE.exists(),
    }
