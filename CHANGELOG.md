# Changelog — NEXUS

Todas as mudanças relevantes deste projeto são documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere a [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
