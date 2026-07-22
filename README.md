<p align="center">
  <img src="assets/branding/logo_with_background.png" alt="NEXUS Logo" width="160" height="160" />
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
  <img alt="version" src="https://img.shields.io/badge/version-v0.2.2.1%20Alpha-00A8FF?style=for-the-badge&labelColor=001B44" />
  <img alt="codename" src="https://img.shields.io/badge/codename-Kernel%20Identity-00FFFF?style=for-the-badge&labelColor=001B44" />
  <img alt="theme" src="https://img.shields.io/badge/theme-NEXUS%20Blue-0077FF?style=for-the-badge&labelColor=001B44" />
  <img alt="python" src="https://img.shields.io/badge/python-3.10+-0077FF?style=for-the-badge&logo=python&logoColor=E8F4FF&labelColor=001B44" />
  <img alt="license" src="https://img.shields.io/badge/license-MIT-E8F4FF?style=for-the-badge&labelColor=001B44" />
</p>

<p align="center">
  <b>Assistente pessoal de terminal</b> com marca própria.<br/>
  Tecnologia · inteligência · futuro · precisão · elegância.
</p>

---

## Visão geral

O **NEXUS** é um assistente de terminal para Linux Mint, escrito em **Python 3**.
A versão **v0.2.2.1 Alpha — Kernel Identity** consolida a **primeira identidade visual oficial**:
logo com e sem fundo, tema **NEXUS Blue**, comando `about` e documentação no padrão de um projeto open source real.

> **Version:** `v0.2.2.1 Alpha` · **Codename:** `Kernel Identity`  
> *"Identity module loaded."*

---

## Demonstração

```text
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

     Networked Executive Intelligence System

╭────────────────────────────╮
│          NEXUS             │
│ Networked Executive System │
├────────────────────────────┤
│ Version: v0.2.2.1 Alpha    │
│ Codename: Kernel Identity  │
│ Status: ONLINE             │
╰────────────────────────────╯

NEXUS ❯ about
NEXUS ❯ help
NEXUS ❯ version
```

---

## NEXUS Identity

![NEXUS Logo](assets/branding/logo_with_background.png)

### Significado da logo

A marca é um **N** geométrico em gradiente — do neon ao azul tecnológico —
sobre fundo escuro. Representa o **nó central** de um sistema em rede:
conexão, inteligência e precisão.

| Variante | Arquivo | Uso |
|----------|---------|-----|
| Com fundo | `assets/branding/logo_with_background.png` | README, docs, apresentações |
| Sem fundo | `assets/branding/logo.png` | Ícone, UI futura, mobile |
| ASCII | `assets/branding/logo_ascii.txt` | Terminal (boot, about, help) |

### Filosofia visual

- **Tecnologia** — linhas limpas, tipografia de sistema
- **Inteligência** — contraste alto, hierarquia clara
- **Futuro** — neon + azul escuro
- **Precisão** — painéis alinhados, status explícitos
- **Elegância** — minimalismo, sem ruído visual

### Paleta — NEXUS Blue Theme

| Nome | Hex | Papel |
|------|-----|-------|
| Azul Neon | `#00FFFF` | Acento, status, prompt |
| Azul tecnológico | `#0077FF` | Gradiente da marca |
| Azul principal | `#00A8FF` | Bordas, títulos |
| Azul escuro | `#001B44` | Fundo de painéis |
| Branco | `#E8F4FF` | Texto principal |

Tema carregado de `assets/themes/nexus_blue.json` via `core/theme.py`.

---

## Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| Identidade visual | Logo, tema NEXUS Blue, painéis de marca |
| `about` | Tela oficial de identidade + módulos |
| CLI Rich | Banner ASCII, painéis, tabelas |
| Config XDG | `~/.config/nexus/` |
| Logs / History | Persistentes |
| Update seguro | Backup + rollback |
| Roteador interno | Comandos NEXUS ≠ SO |
| `shell <cmd>` | SO apenas quando explícito |

---

## Instalação

```bash
git clone https://github.com/<seu-usuario>/NEXUS.git
cd NEXUS
chmod +x install.sh && ./install.sh
```

```bash
# local
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 nexus.py
```

---

## Uso

```bash
nexus                 # interativo
nexus about           # identidade oficial
nexus version         # versão + build
nexus history
nexus update
nexus help
```

| Comando | Ação |
|---------|------|
| `about` | Logo + versão + módulos |
| `help` | Catálogo com marca |
| `version` | Painel de identidade |
| `update` | Atualizador interno |
| `shell ls` | Comando no SO |
| `sair` | Encerra |

---

## Estrutura

```text
NEXUS/
├── nexus.py
├── version.json
├── assets/
│   ├── branding/
│   │   ├── logo.png
│   │   ├── logo_with_background.png
│   │   ├── logo_ascii.txt
│   │   ├── banner.txt
│   │   └── colors.json
│   └── themes/
│       └── nexus_blue.json
├── core/
│   ├── theme.py          # NEXUS Blue Theme
│   ├── banner.py         # Boot Identity
│   └── …
├── commands/
│   ├── about_cmd.py
│   └── …
├── plugins/              # (futuro)
└── modules/              # voice · ai · hud · mobile
```

---

## Roadmap

| Versão | Codename | Status |
|--------|----------|--------|
| v0.1 Alpha | Boot | ✔ |
| v0.1.5 Alpha | Launch | ✔ |
| v0.2 Alpha | Kernel | ✔ |
| v0.2.1 Alpha | Kernel Patch | ✔ |
| v0.2.2 Alpha | Kernel Identity | ✔ |
| **v0.2.2.1 Alpha** | **Kernel Identity** | ✔ |
| v0.5 Beta | Core | ◻ |
| v1.0 Stable | Genesis | ◻ |

---

## Histórico de versões

| Versão | Codename | Marco |
|--------|----------|-------|
| **v0.1 Alpha** | Boot | Nascimento do sistema |
| **v0.1.5 Alpha** | Launch | Instalação global e experiência CLI |
| **v0.2 Alpha** | Kernel | Núcleo do sistema |
| **v0.2.1 Alpha** | Kernel Patch | Correções do sistema de atualização |
| **v0.2.2 Alpha** | Kernel Identity | Primeira identidade visual oficial |
| **v0.2.2.1 Alpha** | Kernel Identity | Revisão da identidade e branding |

Detalhes em [`CHANGELOG.md`](./CHANGELOG.md).

---

## Créditos

| | |
|--|--|
| **Projeto** | NEXUS — Networked Executive Intelligence System |
| **Autor** | Tiago |
| **Tema** | NEXUS Blue Theme |
| **Stack** | Python 3 · Rich · psutil |
| **Plataforma** | Linux Mint Cinnamon |

---

## Licença

MIT

---

<p align="center">
  <img src="assets/branding/logo_with_background.png" alt="NEXUS" width="64" /><br/>
  <code>#00FFFF</code> · <code>#00A8FF</code> · <code>#001B44</code><br/>
  <b>NEXUS</b> — Identity module loaded.
</p>
