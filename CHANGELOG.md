# Changelog — NEXUS

Todas as mudanças relevantes deste projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.2.0] — 2026-07-21 — Kernel

### Adicionado
- Sistema de configuração profissional em `~/.config/nexus/`
- Diretórios automáticos: `logs/`, `history/`, `cache/`
- Sistema de logs estruturado (inicialização, comandos, erros, atualizações)
- Comando `history` / `nexus history`
- Navegação de histórico com setas ↑ ↓
- Comando `update` / `nexus update` com backup e rollback
- Banner ASCII art com animação de boot
- Paleta visual azul tecnológica (#00A8FF, #0077FF, #001B44, #00FFFF)
- Estrutura preparatória para plugins, voz, IA, HUD e mobile

### Alterado
- Migrada a configuração do usuário para `~/.config/nexus/config.json`
- Identidade visual unificada em tons de azul
- README reescrito como documentação open source profissional

---

## [0.1.5] — 2026-07-21 — Launch

### Adicionado
- Instalação global (`install.sh` / `uninstall.sh`)
- Comando `nexus` em qualquer diretório
- Launcher `.desktop` para Linux Mint
- Interface CLI moderna com Rich (painéis, tabelas, barras)
- Animação de inicialização

---

## [0.1.0] — 2026-07-20 — Boot

### Adicionado
- Estrutura inicial modular
- Parser e executor
- Comandos básicos (sistema, apps, browser, info)
- Configuração local em `config/config.json`
