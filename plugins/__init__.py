"""
plugins/

Sistema de plugins do NEXUS (v0.3 Alpha — Core Expansion).

Cada arquivo .py neste diretório é carregado automaticamente se:
    1. Contém um dicionário PLUGIN_INFO com 'nome', 'versao' e 'descricao'.
    2. Define uma função registrar(executor) que registra comandos.

Veja exemplo_plugin.py e README.md para detalhes.
"""
