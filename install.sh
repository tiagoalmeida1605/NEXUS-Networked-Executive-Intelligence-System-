#!/usr/bin/env bash
#
# install.sh
#
# Instala o NEXUS globalmente no sistema, permitindo executá-lo
# digitando apenas "nexus" em qualquer diretório do Linux Mint.
#
# O que este script faz:
#   1. Verifica se o Python 3 está disponível.
#   2. Instala as dependências listadas em requirements.txt.
#   3. Cria um comando global "nexus" em ~/.local/bin.
#   4. Cria um launcher (.desktop) para o menu de aplicativos.
#
# Este script NÃO move nem copia os arquivos do projeto: o launcher
# aponta diretamente para esta pasta, então ela deve permanecer no lugar.

set -e

PROJETO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/nexus"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/nexus.desktop"

echo "══════════════════════════════════════════"
echo " NEXUS — Instalação Global"
echo "══════════════════════════════════════════"
echo ""

echo "→ Verificando Python 3..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "✗ Python 3 não encontrado. Instale o Python 3 antes de continuar."
    exit 1
fi
echo "✔ Python 3 encontrado: $(python3 --version)"
echo ""

echo "→ Instalando dependências..."
python3 -m pip install --user -r "$PROJETO_DIR/requirements.txt"
echo ""

echo "→ Criando comando global 'nexus'..."
mkdir -p "$BIN_DIR"
cat > "$LAUNCHER" <<EOF
#!/usr/bin/env bash
# Launcher gerado automaticamente pelo install.sh do NEXUS.
exec python3 "$PROJETO_DIR/nexus.py" "\$@"
EOF
chmod +x "$LAUNCHER"
echo "✔ Comando 'nexus' criado em $LAUNCHER"
echo ""

echo "→ Criando launcher para o menu do Linux Mint..."
mkdir -p "$DESKTOP_DIR"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=NEXUS
Comment=Networked Executive Intelligence System
Exec=$LAUNCHER
Icon=utilities-terminal
Terminal=true
Categories=Utility;System;
EOF
echo "✔ Launcher de menu criado em $DESKTOP_FILE"
echo ""

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠ Atenção: $BIN_DIR não está no seu PATH."
    echo "  Adicione a linha abaixo ao seu ~/.bashrc (ou ~/.zshrc) e reabra o terminal:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo "══════════════════════════════════════════"
echo " ✔ NEXUS instalado com sucesso."
echo "   Abra um novo terminal e digite: nexus"
echo "══════════════════════════════════════════"
