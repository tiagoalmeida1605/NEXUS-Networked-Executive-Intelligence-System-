# Changelog — NEXUS

Todas as mudanças relevantes deste projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.5.0] — 2026-07-26 — AI Framework

### Adicionado
- NEXUS AI Framework: módulo `ai/` com arquitetura modular completa
- `ai/ollama.py`: integração com API local do Ollama (detecção, listagem, prompts)
- `ai/router.py`: roteador de intenção por palavras-chave (developer/assistant/analyst)
- `ai/manager.py`: gerenciador de ciclo de vida com modo dynamic (carrega/libera)
- `ai/memory.py`: memória persistente em `~/.config/nexus/ai_memory.json`
- `ai/prompts/system.py`: prompts de sistema específicos para cada role
- `ai/models.json`: definição dos 3 modelos (Qwen Coder, Phi Mini, Gemma)
- Comandos: `ai` (modo conversa), `ai status` (status do sistema), `models` (lista modelos)

### Alterado
- `core/executor.py`: registrados comandos `ai` (com suporte a alvo) e `models`
- `commands/ai_cmd.py`: interface CLI para IA com detecção de disponibilidade
- `version.json` atualizado para v0.5 com codename AI Framework
- `CHANGELOG.md` e README atualizados

### Segurança
- Sistema resistente: NEXUS funciona normalmente sem Ollama
- IA atua apenas como módulo adicional, não substitui o Core
- Ações requerem confirmação quando necessário

---

## [0.4.0] — 2026-07-26 — Interface

### Adicionado
- Splash screen animada com carregamento por módulos (✓ Core, Commands, Theme, Config, Plugins)
- Prompt visual redesenhado: `╭─ NEXUS` / `╰─▶`
- Comandos: `banner`, `credits`, `motd`, `theme`, `theme list`, `reload`, `cls`
- Sistema de informação completo: CPU, RAM, Disco, Kernel, Python, Hostname, Operador, Uptime, Arch
- Plugin loader expandido: suporte a plugins em subdiretórios com `__init__.py`
- Plugins: calculator (`calc`), clock (`clock`), calendar (`calendar`), password (`password`), notes (`note add/list/remove`), todo (`todo add/list/done/remove`)

### Alterado
- `core/theme.py`: splash animado via `Live`, prompt moderno, novos helpers visuais
- `core/banner.py`: simplificado, delega para `theme.exibir_splash()`
- `core/system.py`: adicionado `get_uptime()`, `format_uptime()`, `get_architecture()`, `get_kernel()`
- `commands/system.py`: `sistema` agora exibe uptime, hostname, operador, arch
- `core/plugin_loader.py`: suporta arquivos `.py` e subdiretórios com `__init__.py`
- `core/executor.py`: novos comandos registrados (banner, credits, motd, theme, reload, cls)
- `core/parser.py`: aliases de comandos mantidos
- Todos os painéis: bordas consistentes, ícones discretos, alinhamento

---

## [0.3.1] — 2026-07-26 — Developer Identity

### Adicionado
- Sistema de identificação automática do operador via `getpass.getuser()`
- Novo módulo `core/system.py` com `get_system_user()`, `get_operator_name()`, `get_hostname()`
- Operador exibido em painéis de identidade (banner, about, version, sistema)
- Identificador especial `Tiago/dev` para o usuário oficial (tiago)

### Alterado
- `core/theme.py`: `painel_identidade()` agora mostra Operator e Host automaticamente
- `core/banner.py`: identificação do operador substitui leitura estática do config
- `commands/about_cmd.py`: painel ABOUT exibe Operator e Host
- `version.json` atualizado para v0.3.1 com codename Developer Identity
- `CHANGELOG.md` e README atualizados para refletir nova versão

---

## [0.3.0] — 2026-07-25 — Core Evolution

### Adicionado
- Melhorias estruturais do core e reorganização interna
- Comando de diagnóstico completo do sistema (`doctor` / `nexus doctor`)
- Sistema dinâmico de descoberta e carregamento de plugins (`core/plugin_loader.py`)
- Rotação automática de arquivos de log (limite de 1 MB)
- Configuração estruturada com suporte a deep-merge (`preferences` e `modules`)

### Alterado
- Melhorias na arquitetura e desacoplamento do executor de comandos
- Parser aprimorado com captura e tratamento de alvos generalizados
- Refinamento da experiência CLI e catálogo de ajuda expandido
- Organização do projeto para maior escalabilidade

### Preparado
- Base padronizada para ecossistema e desenvolvimento de plugins
- Estrutura modular preparada para futuras integrações com Inteligência Artificial
- Arquitetura expansível para novos módulos do ecossistema NEXUS

---

## [0.2.2.1] — 2026-07-21 — Kernel Identity

### Alterado
- Versão atual marcada como **v0.2.2.1 Alpha**
- Revisão da identidade visual e organização de branding

---

## [0.2.2] — 2026-07-21 — Kernel Identity

### Adicionado
- Estrutura `assets/branding/` e `assets/themes/`
- Logo oficial com fundo e sem fundo
- Tema **NEXUS Blue** (`nexus_blue.json`)
- Comando `about` / `nexus about`
- Sistema de tema centralizado (`core/theme.py`)
- Painel de identidade no boot
- Seção **NEXUS Identity** no README

### Alterado
- Banner de inicialização: ASCII + painel de identidade
- Assets de marca reorganizados profissionalmente
- `core/ui.py` reexporta o tema (compatibilidade preservada)

---

## [0.2.1] — 2026-07-21 — Kernel Patch

### Corrigido
- Roteamento explícito de comandos internos vs. sistema
- `update` isolado como comando interno do NEXUS
- Porta explícita `shell <comando>` para o SO
- Comandos desconhecidos não derrubam o NEXUS
- Markup Rich no painel de update

---

## [0.2.0] — 2026-07-21 — Kernel

### Adicionado
- Configuração profissional em `~/.config/nexus/`
- Logs, histórico e update seguro com backup/rollback
- Banner ASCII e paleta azul tecnológica

---

## [0.1.5] — 2026-07-21 — Launch

### Adicionado
- Instalação global (`install.sh` / `uninstall.sh`)
- Interface CLI moderna com Rich

---

## [0.1.0] — 2026-07-20 — Boot

### Adicionado
- Estrutura modular inicial
- Parser, executor e comandos básicos
