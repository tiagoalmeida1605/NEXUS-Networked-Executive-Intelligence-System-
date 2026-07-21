# NEXUS — Networked Executive Intelligence System

**Versão atual: v0.1 Alpha — Codename: Boot**

## Descrição

NEXUS é um assistente pessoal para Linux, executado via terminal, criado para
evoluir ao longo do tempo em uma arquitetura modular. Nesta primeira versão,
o NEXUS interpreta comandos digitados pelo usuário, executa ações no sistema
operacional (abrir aplicativos, pastas e sites, consultar informações do
sistema) e responde de forma elegante utilizando a biblioteca `rich`.

## Objetivo

Construir uma base sólida, limpa e escalável para um assistente pessoal,
sem qualquer forma de IA, interface gráfica, reconhecimento de voz ou
automações complexas nesta versão. O foco do v0.1 Alpha é exclusivamente:

- Estrutura modular bem definida;
- Separação clara de responsabilidades (parser, executor, comandos);
- Configuração externa, sem caminhos fixos no código;
- Comandos básicos de terminal.

## Instalação

```bash
git clone https://github.com/<seu-usuario>/NEXUS-Networked-Executive-Intelligence-System-.git
cd NEXUS-Networked-Executive-Intelligence-System-
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Dependências

- [rich](https://github.com/Textualize/rich) — interface de terminal
- [psutil](https://github.com/giampaolo/psutil) — informações de CPU, RAM e disco

As demais bibliotecas utilizadas (`platform`, `datetime`, `os`, `subprocess`,
`json`, `pathlib`, `webbrowser`) fazem parte da biblioteca padrão do Python 3
e não exigem instalação.

## Estrutura do projeto

```
Nexus/
│
├── nexus.py
│
├── core/
│   ├── banner.py
│   ├── parser.py
│   ├── executor.py
│   └── response.py
│
├── commands/
│   ├── system.py
│   ├── info.py
│   ├── apps.py
│   └── browser.py
│
├── config/
│   └── config.json
│
├── assets/
│
├── requirements.txt
│
└── README.md
```

- **core/banner.py** — exibe a tela inicial do sistema.
- **core/parser.py** — interpreta a entrada do usuário (ação + alvo). Nunca executa nada.
- **core/executor.py** — encaminha os comandos interpretados ao módulo correto.
- **core/response.py** — padroniza e exibe as respostas do sistema.
- **commands/system.py** — comandos de CPU, RAM, disco, informações do SO e limpeza de tela.
- **commands/info.py** — comandos de hora e data.
- **commands/apps.py** — abertura de aplicativos e pastas configurados em `config.json`.
- **commands/browser.py** — abertura de sites (Google, YouTube, GitHub).
- **config/config.json** — configurações do usuário (navegador, editor, terminal, pastas).

## Comandos

| Comando            | Descrição                              |
|--------------------|-----------------------------------------|
| `ajuda`            | Exibe a lista de comandos               |
| `hora`             | Exibe a hora atual                      |
| `data`             | Exibe a data atual                      |
| `cpu`              | Exibe o uso da CPU                      |
| `ram`              | Exibe o uso da memória RAM              |
| `disco`            | Exibe o uso do disco                    |
| `sistema`          | Exibe informações do sistema operacional|
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

Antes de executar, ajuste `config/config.json` com os comandos e caminhos
reais do seu sistema (usuário, navegador, terminal, editor e pastas).

## Roadmap

**NEXUS v0.1 Alpha — Codename: Boot**
- ✔ Base do sistema
- ✔ Parser
- ✔ Executor
- ✔ Comandos básicos

---

**NEXUS v0.2 Alpha — Codename: Kernel** *(planejado)*
- Histórico de comandos
- Arquivo de configuração expandido
- Sistema de aliases
- Melhor tratamento de erros
- Logs

---

**NEXUS v0.5 Beta — Codename: Core** *(planejado)*
- Arquitetura de módulos
- Primeiras automações
- Configuração dinâmica
- Melhor parser

---

**NEXUS v1.0 Stable — Codename: Genesis** *(planejado)*
- Primeira versão considerada estável
- Interface CLI completa
- Sistema totalmente modular

---

**Versões futuras**

A arquitetura foi pensada para receber, sem necessidade de reescrever a base
do projeto:
- Reconhecimento de voz
- Resposta por voz
- HUD futurista
- Interface gráfica
- IA
- Sistema de plugins
- Sistema de automações
- Aplicativo para celular
- Integração Desktop + Mobile

## Licença

Este projeto está licenciado sob os termos da licença MIT.
# NEXUS-Networked-Executive-Intelligence-System-
