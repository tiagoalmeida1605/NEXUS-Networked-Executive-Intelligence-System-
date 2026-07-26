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
  <img alt="version" src="https://img.shields.io/badge/version-v0.3.1%20Alpha-00A8FF?style=for-the-badge&labelColor=001B44" />
  <img alt="codename" src="https://img.shields.io/badge/codename-Developer%20Identity-00FFFF?style=for-the-badge&labelColor=001B44" />
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
A versão **v0.3.1 Alpha — Developer Identity** representa uma atualização incremental focada na identificação automática do operador e na consolidação da arquitetura interna, sem alterar o comportamento principal do NEXUS.

> **Version:** `v0.3.1 Alpha` · **Codename:** `Developer Identity`  
> *"Developer Identity active."*

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

╭────────────────────────────────╮
│          NEXUS                 │
│ Networked Executive System     │
├────────────────────────────────┤
│ Version: v0.3.1 Alpha          │
│ Codename: Developer Identity   │
│ Operator: Tiago/dev            │
│ Host: tiago-mint-linux         │
│ Status: ONLINE                 │
╰────────────────────────────────╯

NEXUS ❯ doctor
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
| `doctor` | Diagnóstico completo de saúde do sistema |
| Identificação do operador | Detecção automática via `getpass.getuser()` |
| Core modular | Arquitetura desacoplada e evolutiva |
| Sistema de plugins | Suporte e carregamento dinâmico de extensões |
| Gestão de config & logs | Rotação automática de logs (1 MB) e merge de preferências |
| Base para IA futura | Estrutura preparada para integração inteligente (roadmap) |
| CLI Rich | Banner ASCII, painéis, tabelas |
| Config XDG | `~/.config/nexus/` |
| Logs / History | Persistentes |
| Update seguro | Backup + rollback |
| Roteador interno | Comandos NEXUS ≠ SO |
| `shell <cmd>` | SO apenas quando explícito |

---

## Instalação

```bash
git clone https://github.com/tiagoalmeida1605/NEXUS-Networked-Executive-Intelligence-System-.git
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
nexus doctor          # diagnóstico do sistema
nexus version         # versão + build
nexus history
nexus update
nexus help
```

| Comando | Ação |
|---------|------|
| `about` | Logo + versão + módulos |
| `doctor` | Diagnóstico completo do sistema |
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
│   ├── plugin_loader.py  # Carregador de plugins
│   ├── logger.py         # Logs com rotação
│   ├── system.py         # Identificação do operador
│   └── …
├── commands/
│   ├── about_cmd.py
│   ├── doctor_cmd.py     # Diagnóstico do sistema
│   └── …
├── plugins/              # Sistema de plugins (.py)
└── modules/              # voice · ai (futuro) · hud · mobile
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
| v0.2.2.1 Alpha | Kernel Identity | ✔ |
| **v0.3 Alpha** | **Core Evolution** | ✔ |
| **v0.3.1 Alpha** | **Developer Identity** | ✔ |
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
| **v0.3 Alpha** | Core Evolution | Evolução do núcleo e preparação arquitetural |
| **v0.3.1 Alpha** | Developer Identity | Identificação automática do operador e consolidação |

Detalhes em [`CHANGELOG.md`](./CHANGELOG.md).

---

## Créditos

| |                                                 |
|--|-------------------------------------------------|
| **Projeto** | NEXUS — Networked Executive Intelligence System |
| **Autor** | Tiago Silvestre                                 |
| **Tema** | NEXUS Blue Theme                                |
| **Stack** | Python 3 · Rich · psutil                        |
| **Plataforma** | Linux Mint 22.3 Cinnamon                        |

---

## Licença

MIT

---

<p align="center">
  <img src="assets/branding/logo_with_background.png" alt="NEXUS" width="64" /><br/>
  <code>#00FFFF</code> · <code>#00A8FF</code> · <code>#001B44</code><br/>
  <b>NEXUS</b> — Developer Identity active.
</p>
