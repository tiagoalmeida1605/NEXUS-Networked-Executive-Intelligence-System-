#!/usr/bin/env bash
#
# install.sh
#
# Instala o NEXUS globalmente no sistema, permitindo executá-lo
# digitando apenas "nexus" em qualquer diretório do Linux Mint.
#
# O que este script faz:
#   1. Verifica se o Python 3 está disponível.
#   2. Verifica se o módulo venv está disponível.
#   3. Cria um ambiente virtual (venv), caso não exista.
#   4. Instala as dependências dentro da venv.
#   5. Cria um comando global "nexus" em ~/.local/bin.
#   6. Cria um launcher (.desktop) para o menu de aplicativos.
#
# Este script NÃO move nem copia os arquivos do projeto: o launcher
# aponta diretamente para esta pasta, então ela deve permanecer no lugar.

set -e

PROJETO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/nexus"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/nexus.desktop"
VENV_DIR="$PROJETO_DIR/venv"

echo "══════════════════════════════════════════"
echo " NEXUS — Instalação Global"
echo "══════════════════════════════════════════"
echo ""

echo "→ Verificando Python 3..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "✗ Python 3 não encontrado."
    echo "Instale o Python 3 antes de continuar."
    exit 1
fi

echo "✔ Python encontrado: $(python3 --version)"
echo ""

echo "→ Verificando suporte a ambientes virtuais..."

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "✗ O módulo venv não está instalado."
    echo ""
    echo "Instale com:"
    echo "sudo apt install python3.12-venv"
    echo ""
    exit 1
fi

echo "✔ Ambiente virtual suportado."
echo ""

echo "→ Preparando ambiente virtual..."

if [ ! -d "$VENV_DIR" ]; then
    echo "→ Criando ambiente virtual..."
    python3 -m venv "$VENV_DIR"
    echo "✔ Ambiente virtual criado."
else
    echo "✔ Ambiente virtual já existe."
fi

echo ""

echo "→ Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate"

echo "✔ Ambiente ativado."
echo ""

echo "→ Atualizando pip..."
python -m pip install --upgrade pip

echo ""

echo "→ Instalando dependências..."

python -m pip install -r "$PROJETO_DIR/requirements.txt"

echo "✔ Dependências instaladas."
echo ""

echo "→ Preparando configuração em ~/.config/nexus/..."
mkdir -p "$HOME/.config/nexus/logs"
mkdir -p "$HOME/.config/nexus/history"
mkdir -p "$HOME/.config/nexus/cache"
if [ ! -f "$HOME/.config/nexus/config.json" ] && [ -f "$PROJETO_DIR/config/config.json" ]; then
    cp "$PROJETO_DIR/config/config.json" "$HOME/.config/nexus/config.json"
    echo "✔ config.json criado a partir do template."
else
    echo "✔ Estrutura de configuração pronta."
fi
echo ""

echo "→ Criando comando global 'nexus'..."

mkdir -p "$BIN_DIR"

cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
# Launcher gerado automaticamente pelo install.sh do NEXUS.

exec "$VENV_DIR/bin/python" "$PROJETO_DIR/nexus.py" "\$@"
EOF

chmod +x "$LAUNCHER"

echo "✔ Comando 'nexus' criado em:"
echo "  $LAUNCHER"
echo ""

echo "→ Criando launcher do menu do Linux Mint..."

mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=NEXUS
Comment=Networked Executive Intelligence System
Exec=$LAUNCHER
Icon=utilities-terminal
Terminal=true
Categories=Utility;System;Development;
EOF

chmod +x "$DESKTOP_FILE"

echo "✔ Launcher criado em:"
echo "  $DESKTOP_FILE"
echo ""

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then

    echo "→ Adicionando ~/.local/bin ao PATH..."

    SHELL_RC="$HOME/.bashrc"

    if [ -n "$ZSH_VERSION" ]; then
        SHELL_RC="$HOME/.zshrc"
    fi

    if ! grep -q 'HOME/.local/bin' "$SHELL_RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo "✔ PATH atualizado em $SHELL_RC"
    else
        echo "✔ PATH já configurado."
    fi

    echo ""
    echo "⚠ Reinicie o terminal ou execute:"
    echo ""
    echo "source $SHELL_RC"
    echo ""

fi

if command -v nexus >/dev/null 2>&1; then
    echo "✔ Comando nexus funcionando!"
else
    echo "⚠ O comando foi criado, mas será necessário reiniciar o terminal."
fi

echo "══════════════════════════════════════════"
echo "           Instalação concluída"
echo "══════════════════════════════════════════"
echo ""
echo "Agora basta abrir um novo terminal e executar:"
echo ""
echo "    nexus"
echo ""
echo "O NEXUS utilizará automaticamente o ambiente virtual criado."
echo ""
echo "══════════════════════════════════════════"