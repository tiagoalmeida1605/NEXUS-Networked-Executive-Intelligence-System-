# Plugins no NEXUS

O NEXUS possui um sistema de extensibilidade que permite aos usuários criar e gerenciar plugins. Plugins podem adicionar novas funcionalidades e comandos ao sistema. 

## Como Criar um Plugin

Para criar um plugin no NEXUS, basta adicionar um arquivo `.py` no diretório `plugins/`. 

Todo plugin precisa definir as seguintes propriedades:

1. **`PLUGIN_INFO`**: Um dicionário contendo metadados do plugin (`nome`, `versao` e `descricao`).
2. **`registrar(executor)`**: Uma função que aceita a instância do executor como argumento. Essa função é usada para registrar os novos comandos.

### Regras de Ouro
- Funções de comandos dos plugins devem retornar um objeto `Resposta` da classe `core.response`.
- Plugins **não** devem usar funções de `print` diretamente. Todo output visual (interface) deve ser passado via o campo `renderable` da `Resposta` ou usar logs (`core.logger`).

### Código de Exemplo

```python
"""
plugins/exemplo_plugin.py
"""
from __future__ import annotations
from core.response import Resposta

PLUGIN_INFO = {
    "nome": "Exemplo",
    "versao": "1.0",
    "descricao": "Plugin de demonstração do NEXUS.",
}

def _ping() -> Resposta:
    """Responde com um PONG para testar o sistema de plugins."""
    return Resposta(sucesso=True, mensagem="NEXUS PONG ✓")

def registrar(executor) -> None:
    """Registra os comandos deste plugin no executor."""
    executor.registrar_plugin("ping", _ping, "Testa o sistema de plugins (PONG)")
```

## Como Instalar e Remover Plugins

- **Instalar**: Basta copiar (ou mover) o arquivo `.py` do seu plugin para a pasta `plugins/`.
- **Remover**: Apague (ou mova) o arquivo `.py` do diretório `plugins/`.

Ao iniciar o NEXUS, o sistema (via `core.plugin_loader`) descobrirá automaticamente e carregará todos os plugins válidos presentes nesse diretório.
