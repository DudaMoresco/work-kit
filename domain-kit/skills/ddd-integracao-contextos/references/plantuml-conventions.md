# Convenções PlantUML — Integração de Contextos

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir.

## Mapa U → D

```plantuml
@startuml integracao-exemplo
skinparam shadowing false
left to right direction

rectangle "Upstream (U)" as U #LightGray
rectangle "Downstream (D)" as D #LightGreen
rectangle "ACL" as ACL #Wheat

U --> D : Conformista
U --> ACL : protocolo
ACL --> D : modelo D
@enduml
```

| Elemento | Cor sugerida |
| --- | --- |
| Fornecedor externo / U | `#LightGray` |
| BC interno | `#LightBlue` ou `#LightGreen` |
| ACL | `#Wheat` |

- Rótulo da seta = padrão (`Conformista`, `ACL`, `Customer-Supplier`)
- Preferir ASCII nos labels se acentos gerarem warning
- Sem PII
