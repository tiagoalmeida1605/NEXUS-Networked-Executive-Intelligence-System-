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
  <img alt="version" src="https://img.shields.io/badge/version-v0.2%20Alpha-00A8FF?style=for-the-badge&labelColor=001B44" />
  <img alt="codename" src="https://img.shields.io/badge/codename-Kernel-00FFFF?style=for-the-badge&labelColor=001B44" />
  <img alt="python" src="https://img.shields.io/badge/python-3.10+-0077FF?style=for-the-badge&logo=python&logoColor=E8F4FF&labelColor=001B44" />
  <img alt="platform" src="https://img.shields.io/badge/platform-Linux%20Mint-00A8FF?style=for-the-badge&labelColor=001B44" />
  <img alt="license" src="https://img.shields.io/badge/license-MIT-E8F4FF?style=for-the-badge&labelColor=001B44" />
</p>

<p align="center">
  <b>Assistente pessoal de terminal</b> — futurista, modular e profissional.<br/>
  Inspirado em ferramentas como <code>btop</code>, <code>fastfetch</code> e <code>lazygit</code>.
</p>

---

## Visão geral

O **NEXUS** é um assistente de terminal para Linux Mint (Cinnamon) escrito em **Python 3**.
Ele transforma o shell em um cockpit limpo: painéis Rich, histórico persistente,
logs estruturados, configuração XDG e atualização segura com backup/rollback.

> **Versão atual:** `v0.2 Alpha` · **Codename:** `Kernel`  
> Foco desta versão: estabilidade do núcleo, organização e gerenciamento do sistema.

---

## Demonstração (terminal)

```text
════════════════════════════════════════════════════
███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

     Networked Executive Intelligence System

                   v0.2 Alpha
               Codename: Kernel

                   ● ONLINE
════════════════════════════════════════════════════

┌─ BOOT SEQUENCE ──────────────────────────┐
│ ✔ Kernel   Núcleo carregado              │
│ ✔ Config   Configuração em ~/.config/…   │
│ ✔ Logger   Sistema de logs online        │
│ ✔ History  Histórico de comandos pronto  │
└──────────────────────────────────────────┘

NEXUS ❯ abrir brave
✔ Abrindo Brave...

NEXUS ❯ history
┌─ Histórico ──────────────────────────────┐
│ #  │ Comando                             │
│ 1  │ cpu                                 │
│ 2  │ abrir brave                         │
└──────────────────────────────────────────┘
```

---

## Paleta de cores

| Nome              | Hex       | Uso                          |
|-------------------|-----------|------------------------------|
| Azul principal    | `#00A8FF` | Títulos, bordas, marca       |
| Azul tecnológico  | `#0077FF` | Painéis secundários          |
| Azul escuro       | `#001B44` | Fundo de painéis             |
| Azul neon         | `#00FFFF` | Acentos, status, prompt      |
| Branco            | `#E8F4FF` | Texto principal              |

Sensação desejada: **futurista · tecnológica · limpa · profissional**.

---

## Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| CLI moderna | Painéis, tabelas, barras e animação de boot com Rich |
| Config XDG | `~/.config/nexus/` criado automaticamente |
| Logs | Registro de init, comandos, sucessos, erros e updates |
| Histórico | `history` + navegação com setas `↑` `↓` |
| Update seguro | `update` com confirmação, backup e rollback |
| Sistema | CPU, RAM, disco, distro/kernel |
| Apps & web | Abre navegadores, IDEs, pastas e sites |
| Instalação global | Comando `nexus` em qualquer diretório |

---

## Instalação

### Requisitos

- Linux Mint (ou distro Linux compatível)
- Python 3.10+
- `python3-venv`
- Git (para `nexus update`)

### Instalação rápida (recomendado)

```bash
git clone https://github.com/<seu-usuario>/NEXUS.git
cd NEXUS
chmod +x install.sh
./install.sh
```

O instalador:

1. Cria/ativa um `venv` local
2. Instala `rich` e `psutil`
3. Publica o comando global `nexus` em `~/.local/bin`
4. Cria um launcher `.desktop` no menu do Linux Mint

### Instalação local (sem comando global)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 nexus.py
```

### Desinstalação global

```bash
chmod +x uninstall.sh
./uninstall.sh
```

> Os scripts **não movem** o projeto. O launcher aponta para a pasta
> onde o `install.sh` foi executado — mantenha-a no lugar.

---

## Como executar

```bash
nexus                 # modo interativo
nexus history         # histórico de comandos
nexus update          # atualização segura
nexus help            # ajuda da CLI
```

Ou, sem instalação global:

```bash
python3 nexus.py
python3 nexus.py history
python3 nexus.py update
```

---

## Configuração

Na primeira execução o NEXUS cria:

```text
~/.config/nexus/
├── config.json
├── logs/
│   └── nexus.log
├── history/
│   └── commands.txt
└── cache/
    └── backups/
```

O template do repositório (`config/config.json`) é copiado automaticamente
para `~/.config/nexus/config.json`. Edite a cópia do usuário:

```json
{
    "user": "Tiago",
    "browser": "brave-browser",
    "terminal": "gnome-terminal",
    "editor": "pycharm",
    "vscode": "code",
    "webstorm": "webstorm",
    "downloads": "/home/tiago/Downloads",
    "documents": "/home/tiago/Documents",
    "projects": "/home/tiago/Documents"
}
```

---

## Comandos disponíveis

### Sistema

| Comando | Descrição |
|---------|-----------|
| `ajuda` | Lista de comandos |
| `hora` / `data` | Hora e data atuais |
| `cpu` / `ram` / `disco` | Painéis de recursos |
| `sistema` | Distro, kernel e Python |
| `history` | Histórico de comandos |
| `history limpar` | Limpa o histórico |
| `update` | Atualização segura |
| `limpar` | Limpa a tela |
| `sair` | Encerra o NEXUS |

### Aplicativos & web

| Comando | Descrição |
|---------|-----------|
| `abrir brave` | Navegador Brave |
| `abrir firefox` | Firefox |
| `abrir terminal` | Terminal |
| `abrir pycharm` / `webstorm` / `vscode` | IDEs |
| `abrir downloads` / `documentos` | Pastas |
| `google` / `youtube` / `github` | Sites |

### CLI (fora do prompt)

| Comando | Descrição |
|---------|-----------|
| `nexus history` | Exibe o histórico |
| `nexus update` | Fluxo de atualização |
| `↑` / `↓` | Repete comandos recentes |

---

## Atualização segura

```text
[NEXUS UPDATE]

Versão atual:
v0.2 Alpha Kernel

Nova versão:
v0.2.1 Alpha

Alterações:
+ Melhor parser
+ Correções de bugs
+ Melhor desempenho

Deseja atualizar? [S/N]
```

O fluxo:

1. Lê `version.json`
2. Consulta o remoto Git
3. Exibe alterações
4. Pede confirmação
5. Gera backup em `~/.config/nexus/cache/backups/`
6. Aplica `git pull --ff-only` + dependências
7. Restaura o backup se algo falhar

---

## Estrutura do projeto

```text
NEXUS/
├── nexus.py                 # Ponto de entrada
├── version.json             # Metadados de versão
├── CHANGELOG.md
├── requirements.txt
├── install.sh / uninstall.sh
│
├── core/                    # Núcleo do sistema
│   ├── banner.py            # ASCII + animação de boot
│   ├── parser.py            # Interpretação de comandos
│   ├── executor.py          # Roteamento
│   ├── response.py          # Saída padronizada
│   ├── ui.py                # Identidade visual Rich
│   ├── config.py            # ~/.config/nexus/
│   ├── logger.py            # Sistema de logs
│   ├── history.py           # Histórico + readline
│   └── update.py            # Update com backup/rollback
│
├── commands/                # Comandos de usuário
│   ├── system.py
│   ├── info.py
│   ├── apps.py
│   ├── browser.py
│   ├── history_cmd.py
│   └── update_cmd.py
│
├── config/
│   └── config.json          # Template (migrado no 1º boot)
│
├── plugins/                 # (futuro) sistema de plugins
├── modules/                 # (futuro) voz · IA · HUD · mobile
│   ├── voice/
│   ├── ai/
│   ├── hud/
│   └── mobile/
│
└── assets/
```

---

## Dependências

| Pacote | Função |
|--------|--------|
| [rich](https://github.com/Textualize/rich) | Interface de terminal |
| [psutil](https://github.com/giampaolo/psutil) | CPU, RAM e disco |

Demais módulos usados (`json`, `pathlib`, `subprocess`, `readline`, `webbrowser`…)
fazem parte da biblioteca padrão do Python 3.

---

## Roadmap

| Versão | Codename | Status | Destaques |
|--------|----------|--------|-----------|
| **v0.1 Alpha** | Boot | ✔ | Parser, executor, comandos básicos |
| **v0.1.5 Alpha** | Launch | ✔ | Instalação global, CLI Rich |
| **v0.2 Alpha** | Kernel | ✔ | Config XDG, logs, history, update |
| **v0.5 Beta** | Core | ◻ | Automações, config dinâmica |
| **v1.0 Stable** | Genesis | ◻ | CLI estável e modular completa |

### Futuro (arquitetura já preparada)

- Reconhecimento e resposta por voz (`modules/voice/`)
- Inteligência artificial (`modules/ai/`)
- Interface gráfica HUD (`modules/hud/`)
- App mobile + sync Desktop (`modules/mobile/`)
- Sistema de plugins (`plugins/`)
- Automações avançadas

---

## Histórico de versões

### v0.2 Alpha — Kernel *(atual)*
- Configuração profissional em `~/.config/nexus/`
- Logs estruturados
- Histórico com `↑` `↓`
- Update seguro com backup/rollback
- Banner ASCII + paleta azul tecnológica

### v0.1.5 Alpha — Launch
- `install.sh` / `uninstall.sh`
- Comando global `nexus`
- Interface CLI moderna com Rich

### v0.1 Alpha — Boot
- Estrutura modular inicial
- Parser + executor
- Comandos de sistema, apps e browser

Detalhes completos em [`CHANGELOG.md`](./CHANGELOG.md).

---

## Créditos

| | |
|--|--|
| **Projeto** | NEXUS — Networked Executive Intelligence System |
| **Autor** | Tiago |
| **Stack** | Python 3 · Rich · psutil |
| **Plataforma alvo** | Linux Mint Cinnamon |
| **IDE** | JetBrains PyCharm |

Inspiração visual e de UX: `btop`, `fastfetch`, `lazygit` e CLIs modernas.

---

## Licença

Este projeto está licenciado sob os termos da licença **MIT**.

---

<p align="center">
  <code>#00A8FF</code> · Built for the terminal · <b>NEXUS Kernel</b>
</p>
