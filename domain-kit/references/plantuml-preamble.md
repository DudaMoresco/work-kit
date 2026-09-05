# PlantUML — preâmbulo compartilhado (domain-kit)

Usado por skills com diagramas. Validar com MCP **`user-plantuml`**: `check_syntax` antes de gravar no hub.

## Regras gerais

- Idioma dos rótulos: **pt-BR**
- Preferir `left to right direction` ou `top to bottom` explícito
- Evitar cadeias `A --> B --> C` numa única linha (pode falhar no MCP) — uma seta por par
- Cores só quando a skill definir semântica (ex.: eventos laranja no ES)
- Não colocar secrets / PII real nos diagramas

## Ciclo mínimo

1. Escrever bloco `@startuml` … `@enduml`
2. `check_syntax` via MCP
3. Incluir no MD do artefato canônico (ver [hub-paths.md](hub-paths.md))

Detalhes de formas/cores ficam no `references/plantuml-conventions.md` de cada skill.
