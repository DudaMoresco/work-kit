# Convenções PlantUML — Event Storming

Validar com MCP **`user-plantuml`**: `check_syntax`.

## Timeline

- Eventos: `rectangle "Verbo no passado" as En #Orange`
- Alternativas: `#Pink` ou note
- `left to right direction`
- Setas na ordem temporal (uma seta por par: `En --> En1`); ramo para exceção
- Evitar cadeia `A --> B --> C` numa única linha (pode falhar no MCP)
