# Convenções PlantUML — Domain Storytelling

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir → (opcional)
`render_diagram`. Não usar `https://www.plantuml.com/plantuml`.

---

## Comum

```plantuml
@startuml story-nome-kebab
skinparam shadowing false
left to right direction
' ...
@enduml
```

- Um diagrama por bloco ` ```plantuml `
- Preferir ASCII nos labels se acentos gerarem warning
- Sem PII (usar papéis: `Responsavel`, não nome completo)

---

## Mapeamento pictográfico → PlantUML

| Elemento DST | PlantUML sugerido |
| --- | --- |
| Ator pessoa | `actor "Papel" as X` |
| Ator grupo | `collections "Papel" as X` |
| Ator sistema | `rectangle "Sistema" as X` |
| Objeto de trabalho | `artifact "Termo" as Y` |
| Atividade | seta com rótulo `N. verbo` |
| Anotação | `note left/right/bottom of …` |

Frase: **Ator → Objeto** ou **Ator → Ator** com verbo numerado.

---

## Exemplo mínimo

```plantuml
@startuml story-exemplo-minimo
skinparam shadowing false
left to right direction

actor "Professor" as Prof
collections "Alunos" as Alunos
artifact "Plano de aula" as Plano

Prof --> Plano : 1. elabora
Prof --> Alunos : 2. apresenta plano
note right of Plano
  Premissa: calendario letivo ok
end note
@enduml
```

---

## Sequência alternativa (quando o mapa fica denso)

Se houver muitos passos, complementar (não substituir) com sequence:

```plantuml
@startuml story-exemplo-seq
skinparam shadowing false

actor Professor
participant "Plano de aula" as Plano
collections Alunos

Professor -> Plano : 1. elabora
Professor -> Alunos : 2. apresenta
@enduml
```

Manter os **mesmos números** da lista de frases do MD.

---

## README índice (várias histórias)

```plantuml
@startuml indice-historias-escola
skinparam shadowing false
left to right direction

rectangle "Projeto Escola" {
  (01 matricula) as H1
  (02 aula tipica) as H2
  (03 boletim) as H3
}

H1 -down-> H2 : depois
H2 -down-> H3 : depois
@enduml
```
