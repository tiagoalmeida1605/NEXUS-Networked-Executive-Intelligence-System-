<p align="center">
  <img src="assets/logo.png" alt="NEXUS Logo" width="128" height="128" />
</p>

```
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
```

# NEXUS

### Networked Executive Intelligence System

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-v0.2.2%20Alpha-00A8FF?style=for-the-badge&labelColor=001B44" />
  <img alt="codename" src="https://img.shields.io/badge/codename-Kernel%20Identity-00FFFF?style=for-the-badge&labelColor=001B44" />
  <img alt="python" src="https://img.shields.io/badge/python-3.10+-0077FF?style=for-the-badge&logo=python&logoColor=E8F4FF&labelColor=001B44" />
  <img alt="platform" src="https://img.shields.io/badge/platform-Linux%20Mint-00A8FF?style=for-the-badge&labelColor=001B44" />
  <img alt="license" src="https://img.shields.io/badge/license-MIT-E8F4FF?style=for-the-badge&labelColor=001B44" />
</p>

<p align="center">
  <b>Assistente pessoal de terminal</b> com marca própria.<br/>
  Futurista · tecnológico · minimalista · profissional.
</p>

---

## Visão geral

O **NEXUS** é um assistente de terminal para Linux Mint, escrito em **Python 3**.
A versão **v0.2.2 Alpha — Kernel Identity** inaugura a **primeira identidade visual oficial**:
logo, tema centralizado, painéis de marca e documentação no padrão de um projeto open source real.

> **Version:** `v0.2.2 Alpha` · **Codename:** `Kernel Identity`  
> *"Identity module loaded."*

---

## Demonstração

```text
███╗   ██╗
████╗  ██║
██╔██╗ ██║
██║╚██╗██║
██║ ╚████║
╚═╝  ╚═══╝

              NEXUS
 Networked Executive Intelligence System

 Version:  v0.2.2 Alpha
 Codename: Kernel Identity

╭─ STATUS ─────────────────────────────╮
│ ✓ Core       Core Online             │
│ ✓ Parser     Parser Online           │
│ ✓ Executor   Executor Online         │
│ ✓ Update     Update System Online    │
│ ✓ Identity   Identity System Online  │
╰──────────────────────────────────────╯

        Identity module loaded.

╭──────────────────────────────╮
│          NEXUS               │
│ Networked Executive System   │
├──────────────────────────────┤
│ Version: v0.2.2 Alpha        │
│ Codename: Kernel Identity    │
│ Status: ONLINE               │
│ User: Tiago                  │
╰──────────────────────────────╯

NEXUS ❯
```

---

## Identidade visual

### Logo oficial

| Asset | Caminho | Uso |
|-------|---------|-----|
| Logo PNG | `assets/logo.png` | README, ícones, marca |
| Logo ASCII | `assets/logo_ascii.txt` | Boot, help, version |
| Banner | `assets/banner.txt` | Letreiro tipográfico |
| Cores | `assets/colors.json` | Tema oficial |

### Paleta

| Nome | Hex | Papel |
|------|-----|-------|
| Azul Neon | `#00FFFF` | Acento, status, prompt |
| Azul tecnológico | `#0077FF` | Gradiente da marca |
| Azul principal | `#00A8FF` | Bordas, títulos |
| Azul escuro | `#001B44` | Fundo de painéis |
| Branco | `#E8F4FF` | Texto principal |

Sensação: **tecnologia · inteligência · futuro · precisão**.

O tema vive em `core/theme.py` — cores não ficam espalhadas pelo código.

---

## Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| Identidade visual | Logo, tema, painéis de marca |
| CLI Rich | Painéis, tabelas, barras, boot animado |
| Config XDG | `~/.config/nexus/` |
| Logs | Init, comandos, erros, updates |
| Histórico | `history` + setas `↑` `↓` |
| Update seguro | Backup + rollback |
| Roteador interno | Comandos NEXUS ≠ SO |
| Shell explícito | `shell <comando>` |
| Apps & web | Navegadores, IDEs, pastas, sites |

---

## Instalação

```bash
git clone https://github.com/<seu-usuario>/NEXUS.git
cd NEXUS
chmod +x install.sh
./install.sh
```

Ou localmente:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 nexus.py
```

Desinstalação global:

```bash
./uninstall.sh
```

---

## Uso

```bash
nexus                 # modo interativo
nexus version         # identidade + build
nexus history         # histórico
nexus update          # atualizador interno
nexus help            # ajuda CLI
```

### No prompt

| Comando | Ação |
|---------|------|
| `help` | Catálogo com logo |
| `version` | Painel de identidade |
| `update` | Update interno do NEXUS |
| `shell ls` | Comando no SO (explícito) |
| `sistema` | Host + identidade |
| `sair` | Encerra |

---

## Estrutura

```text
NEXUS/
├── nexus.py
├── version.json
├── CHANGELOG.md
├── assets/
│   ├── logo.png              # Logo oficial
│   ├── logo_ascii.txt        # N geométrico
│   ├── banner.txt            # Letreiro NEXUS
│   └── colors.json           # Paleta oficial
├── core/
│   ├── theme.py              # Tema & componentes
│   ├── ui.py                 # Reexport (compat)
│   ├── banner.py             # Boot Identity
│   ├── parser.py / executor.py / …
├── commands/
├── config/config.json        # Template
├── plugins/                  # (futuro)
└── modules/                  # voice · ai · hud · mobile
```

---

## Roadmap

| Versão | Codename | Status |
|--------|----------|--------|
| v0.1 Alpha | Boot | ✔ |
| v0.1.5 Alpha | Launch | ✔ |
| v0.2 Alpha | Kernel | ✔ |
| v0.2.1 Alpha | Kernel Patch | ✔ |
| **v0.2.2 Alpha** | **Kernel Identity** | ✔ |
| v0.5 Beta | Core | ◻ |
| v1.0 Stable | Genesis | ◻ |

### Preparado para o futuro

HUD · mobile · IA · voz · plugins · automações · sync entre dispositivos  
*(estrutura em `modules/` e `plugins/` — ainda não implementado)*

---

## Histórico de versões

| Versão | Codename | Marco |
|--------|----------|-------|
| **v0.1 Alpha** | Boot | Nascimento do sistema |
| **v0.1.5 Alpha** | Launch | Instalação global e CLI Rich |
| **v0.2 Alpha** | Kernel | Núcleo, logs, histórico e updates |
| **v0.2.1 Alpha** | Kernel Patch | Correção do sistema de atualização |
| **v0.2.2 Alpha** | Kernel Identity | Primeira identidade visual oficial |

Detalhes em [`CHANGELOG.md`](./CHANGELOG.md).

---

## Créditos

| | |
|--|--|
| **Projeto** | NEXUS — Networked Executive Intelligence System |
| **Autor** | Tiago |
| **Stack** | Python 3 · Rich · psutil |
| **Plataforma** | Linux Mint Cinnamon |
| **Marca** | Kernel Identity (v0.2.2) |

---

## Licença

MIT

---

<p align="center">
  <img src="assets/logo.png" alt="N" width="48" /><br/>
  <code>#00FFFF</code> · <code>#00A8FF</code> · <code>#001B44</code><br/>
  <b>NEXUS</b> — Identity module loaded.
</p>
