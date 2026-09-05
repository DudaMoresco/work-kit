> Preâmbulo compartilhado: [plantuml-preamble.md](../../../references/plantuml-preamble.md)

# Convenções PlantUML — Design Estratégico DDD

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir → (opcional)
`render_diagram`. Não usar `https://www.plantuml.com/plantuml`.

---

## Comum

```plantuml
@startuml nome-unico-kebab
skinparam shadowing false
' ...
@enduml
```

- Um diagrama por bloco fenced ` ```plantuml `
- Nome do `@startuml` único no arquivo
- Preferir ASCII nos labels se acentos gerarem warning no MCP
- Sem PII, credenciais ou dados sensíveis

---

## Mapa domínio → subdomínios

Cores fixas por tipo:

| Tipo | Cor PlantUML |
| --- | --- |
| Principal | `#LightGreen` |
| Suporte | `#LightBlue` |
| Genérico | `#LightGray` |

```plantuml
@startuml mapa-dominio-exemplo
skinparam shadowing false
skinparam packageStyle rectangle
left to right direction

package "Dominio: Nome" {
  package "Principal" #LightGreen {
    [Core A]
  }
  package "Suporte" #LightBlue {
    [Suporte B]
  }
  package "Generico" #LightGray {
    [Generico C]
  }
}

[Core A] ..> [Suporte B] : apoia
[Core A] ..> [Generico C] : usa
@enduml
```

- `left to right direction`
- Relacionamentos só quando úteis (`apoia`, `usa`, `alimenta`)
- Não misturar componentes técnicos (API, DB) neste mapa

---

## Fluxograma de classificação (activity)

```plantuml
@startuml classificar-subdominio
skinparam shadowing false
start
:Candidato a subdominio;
if (Diferencia o negocio\nno mercado?) then (sim)
  :Principal;
  stop
else (nao)
  if (Capacidade comum\nde mercado?) then (sim)
    :Generico;
    stop
  else (nao)
    if (Apoia o principal\n(CRUD / cadastro /\nintegracao auxiliar)?) then (sim)
      :Suporte;
      stop
    else (ambiguo)
      :Hipótese +\nvalidar com Domain Expert;
      stop
    endif
  endif
endif
@enduml
```

Ordem das perguntas é **obrigatória** (Principal → Genérico → Suporte →
ambíguo).

---

## Opcional: visão por investimento

Só se o usuário pedir priorização (buy/build/focus):

```plantuml
@startuml investimento-subdominios
skinparam shadowing false
left to right direction

rectangle "Foco interno\n(Principal)" #LightGreen
rectangle "Manter simples\n(Suporte)" #LightBlue
rectangle "Comprar / reusar\n(Generico)" #LightGray
@enduml
```
