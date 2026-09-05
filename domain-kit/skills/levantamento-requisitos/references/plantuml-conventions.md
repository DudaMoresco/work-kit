> Preâmbulo compartilhado: [plantuml-preamble.md](../../../references/plantuml-preamble.md)

# Convenções PlantUML — Levantamento de Requisitos

Validar com MCP **`user-plantuml`**: `check_syntax`.

## Jornada

```plantuml
@startuml jornada-exemplo
skinparam shadowing false
left to right direction
rectangle "Passo A" as A
rectangle "Passo B" as B
A --> B
@enduml
```

- Um retângulo por passo da jornada
- Ramos para caminhos alternativos se necessário
- Sem PII; preferir ASCII se acentos gerarem warning
