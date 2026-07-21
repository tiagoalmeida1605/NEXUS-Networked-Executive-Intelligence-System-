# NEXUS — Networked Executive Intelligence System

**Versão atual: v0.1.5 Alpha — Codename: Launch**

## Descrição

NEXUS é um assistente pessoal para Linux, executado via terminal, com uma
interface CLI moderna construída inteiramente com [Rich](https://github.com/Textualize/rich):
painéis arredondados, tabelas, barras de progresso coloridas, animação de
inicialização e um prompt personalizado. O objetivo desta versão é
transformar a base do v0.1 em um aplicativo realmente agradável de usar —
sem ainda introduzir IA, interface gráfica, voz, plugins ou automações
complexas.

## Objetivo

- Elevar a experiência de terminal a um padrão profissional (inspirado em
  ferramentas como lazygit, btop, fastfetch e gh CLI);
- Instalação global, para rodar `nexus` em qualquer diretório;
- Manter a arquitetura modular e 100% compatível com o v0.1 Alpha.

## Instalação

```bash
git clone https://github.com/<seu-usuario>/NEXUS-Networked-Executive-Intelligence-System-.git
cd NEXUS-Networked-Executive-Intelligence-System-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 nexus.py
```

## Instalação Global

Para poder digitar apenas `nexus` em qualquer diretório do Linux Mint:

```bash
chmod +x install.sh
./install.sh
```

O `install.sh`:
1. Verifica se o Python 3 está instalado;
2. Instala as dependências (`rich`, `psutil`);
3. Cria o comando global `nexus` em `~/.local/bin/nexus`;
4. Cria um launcher `.desktop` no menu de aplicativos do Linux Mint.

Para remover a instalação global (sem apagar os arquivos do projeto):

```bash
chmod +x uninstall.sh
./uninstall.sh
```

> Os scripts não movem o projeto — o comando global aponta para a pasta
> onde o `install.sh` foi executado, então mantenha-a no lugar.

## Dependências

- [rich](https://github.com/Textualize/rich) — toda a interface de terminal (painéis, tabelas, regras, animações)
- [psutil](https://github.com/giampaolo/psutil) — informações de CPU, RAM e disco

As demais bibliotecas (`platform`, `datetime`, `os`, `subprocess`, `json`,
`pathlib`, `webbrowser`, `sys`) fazem parte da biblioteca padrão do Python 3.

## Estrutura do projeto

```
Nexus/
│
├── nexus.py
│
├── core/
│   ├── banner.py       → animação de boot + banner principal
│   ├── parser.py       → interpreta a entrada do usuário
│   ├── executor.py     → encaminha comandos para commands/
│   ├── response.py     → padroniza e exibe as respostas
│   └── ui.py           → identidade visual: painéis, tabelas, barras, cores
│
├── commands/
│   ├── system.py       → CPU, RAM, disco, sistema, limpar
│   ├── info.py         → hora, data
│   ├── apps.py         → abertura de aplicativos e pastas
│   └── browser.py      → abertura de sites
│
├── config/
│   └── config.json
│
├── assets/
│
├── install.sh          → instalação global (comando "nexus" + launcher)
├── uninstall.sh        → remove a instalação global
├── requirements.txt
└── README.md
```

`core/ui.py` é a única fonte de painéis, tabelas e cores do sistema — nenhum
outro módulo monta componentes Rich diretamente, o que mantém uma
identidade visual única em todo o NEXUS.

## Comandos

| Comando            | Descrição                              |
|--------------------|-----------------------------------------|
| `ajuda`            | Exibe as tabelas de comandos            |
| `hora`             | Exibe a hora atual                      |
| `data`             | Exibe a data atual                      |
| `cpu`              | Painel de uso da CPU (com barra e núcleos)|
| `ram`              | Painel de uso da memória RAM            |
| `disco`            | Painel de uso do disco                  |
| `sistema`          | Painel com distribuição, kernel e Python|
| `limpar`           | Limpa a tela                            |
| `sair`             | Encerra o NEXUS                         |
| `abrir brave`      | Abre o navegador Brave                  |
| `abrir firefox`    | Abre o navegador Firefox                |
| `abrir terminal`   | Abre o terminal                         |
| `abrir pycharm`    | Abre o PyCharm                          |
| `abrir webstorm`   | Abre o WebStorm                         |
| `abrir vscode`     | Abre o VSCode                           |
| `abrir downloads`  | Abre a pasta Downloads                  |
| `abrir documentos` | Abre a pasta Documentos                 |
| `google`           | Abre o Google                           |
| `youtube`          | Abre o YouTube                          |
| `github`           | Abre o GitHub                           |

## Como executar

```bash
python3 nexus.py
```

ou, após a instalação global:

```bash
nexus
```

Antes de executar, ajuste `config/config.json` com os comandos e caminhos
reais do seu sistema (usuário, navegador, terminal, editor e pastas).

## Roadmap

**NEXUS v0.1 Alpha — Codename: Boot**
- ✔ Estrutura inicial
- ✔ Parser
- ✔ Executor
- ✔ Comandos básicos

---

**NEXUS v0.1.5 Alpha — Codename: Launch**
- ✔ Instalação global (`install.sh` / `uninstall.sh`)
- ✔ Terminal profissional (`core/ui.py`)
- ✔ Interface CLI moderna (painéis, tabelas, prompt personalizado)
- ✔ Melhor experiência visual (animação de boot, barras de progresso)

---

**NEXUS v0.2 Alpha — Codename: Kernel** *(planejado)*
- Histórico de comandos
- Logs
- Sistema de aliases
- Parser aprimorado

---

**NEXUS v0.5 Beta — Codename: Core** *(planejado)*
- Sistema modular completo
- Primeiras automações
- Configuração dinâmica

---

**NEXUS v1.0 Stable — Codename: Genesis** *(planejado)*
- Primeira versão considerada estável
- Interface CLI completa
- Sistema totalmente modular

---

**Versões futuras**

A arquitetura foi pensada para receber, sem necessidade de reescrever a base
do projeto: reconhecimento de voz, resposta por voz, HUD futurista,
interface gráfica, IA, sistema de plugins, sistema de automações, aplicativo
para celular e integração Desktop + Mobile.

## Licença

Este projeto está licenciado sob os termos da licença MIT.
