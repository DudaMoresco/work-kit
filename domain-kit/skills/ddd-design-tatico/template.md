# Design Tático — <BC / recorte>

> Gerado com `ddd-design-tatico`.

## Sumário

| Campo | Valor |
| --- | --- |
| Bounded Context | … |
| Data | YYYY-MM-DD |
| Fontes | ES, UL, stories… |

---

## 1. Camadas

| Camada | Conteúdo neste BC |
| --- | --- |
| Interface | … |
| Aplicação | … (gatilhos / casos de uso sem regra) |
| Domínio | … |
| Infraestrutura | … |

---

## 2. Blocos de construção

### Agregados

| Raiz | Membros | Invariantes |
| --- | --- | --- |
| … | … | … |

### Entidades

| Nome | Identidade | Notas |
| --- | --- | --- |
| … | … | … |

### Value Objects

| Nome | Atributos | Notas |
| --- | --- | --- |
| … | … | … |

---

## 3. PlantUML — camadas

```plantuml
@startuml camadas-<slug>
skinparam shadowing false
top to bottom direction

package "Interface" as UI {
  [API / UI]
}
package "Aplicacao" as APP {
  [Casos de uso / jobs]
}
package "Dominio" as DOM {
  [Agregados / regras]
}
package "Infraestrutura" as INF {
  [Persistencia / mensageria]
}

UI --> APP
APP --> DOM
DOM ..> INF : portas
APP --> INF
@enduml
```

## 4. PlantUML — agregados

```plantuml
@startuml agregados-<slug>
skinparam shadowing false

package "Agregado Entrega" {
  class Entrega <<Entity Root>>
  class StatusEntrega <<VO>>
  class Anexo <<VO>>
  Entrega *-- StatusEntrega
  Entrega *-- Anexo
}
@enduml
```

---

## 5. Decisões tecnológicas (hipóteses)

| Tema | Hipótese | Abrir spike? |
| --- | --- | --- |
| Persistência | … | … |

## 6. Abertos

- [ ] …
