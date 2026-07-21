#!/usr/bin/env bash
#
# uninstall.sh
#
# Remove a instalação global do NEXUS (o comando "nexus" e o launcher
# do menu de aplicativos), sem apagar os arquivos do projeto.

BIN_DIR="$HOME/.local/bin"
LAUNCHER="$BIN_DIR/nexus"
DESKTOP_FILE="$HOME/.local/share/applications/nexus.desktop"

echo "══════════════════════════════════════════"
echo " NEXUS — Desinstalação Global"
echo "══════════════════════════════════════════"
echo ""

if [[ -f "$LAUNCHER" ]]; then
    rm -f "$LAUNCHER"
    echo "✔ Comando global 'nexus' removido."
else
    echo "→ Comando global 'nexus' não estava instalado."
fi

if [[ -f "$DESKTOP_FILE" ]]; then
    rm -f "$DESKTOP_FILE"
    echo "✔ Launcher do menu removido."
else
    echo "→ Launcher do menu não estava instalado."
fi

echo ""
echo "══════════════════════════════════════════"
echo " ✔ Desinstalação concluída."
echo "   Os arquivos do projeto foram mantidos intactos."
echo "══════════════════════════════════════════"
