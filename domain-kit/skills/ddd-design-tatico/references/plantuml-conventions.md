# Convenções PlantUML — Design Tático

Validar com MCP **`user-plantuml`**: `check_syntax`.

## Camadas

- `top to bottom direction` ou packages empilhados
- Domínio no centro; Infra só via dependência técnica (tracejada se porta)

## Agregados

- Raiz: `<<Entity Root>>` ou estereótipo claro
- VO: `<<VO>>`
- Composição `*--` da raiz para membros do agregado
- Não misturar dois agregados no mesmo package sem necessidade

Preferir ASCII nos labels se acentos gerarem warning.
