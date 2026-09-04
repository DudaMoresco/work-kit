# Domain Story — <título do cenário>

> Gerado com a skill `domain-storytelling`. Validar com Domain Experts.

## Sumário

| Campo | Valor |
| --- | --- |
| Domínio / subdomínio | … |
| Cenário | … (exemplo concreto) |
| Granularidade | Grossa / Média / Fina |
| Momento | As-is / To-be |
| Pureza | Puro / Digitalizado |
| Data | YYYY-MM-DD |
| Fontes | narrativa, workshop, notas… |

**Limites desta história:** o que **não** cobre.

---

## 1. Escopo

Justificar em 2–4 bullets por que este recorte (granularidade / momento /
pureza) serve ao objetivo atual (entender domínio, requisitos, fronteiras…).

---

## 2. Atores

| Ator (papel) | Tipo | Notas |
| --- | --- | --- |
| … | Pessoa / Grupo / Sistema | … |

---

## 3. Objetos de trabalho

| Objeto | Tipo (físico / doc / digital / info) | Notas |
| --- | --- | --- |
| … | … | … |

---

## 4. História (frases numeradas)

1. **\<Ator\>** \<verbo\> **\<objeto\>** \[para/com **\<Ator\>**\].
2. …
3. …

### Premissas

- …

### Anotações / variações

- No passo N: se … então … (ou ver cenário `NN-…`)
- …

---

## 5. Diagrama PlantUML

```plantuml
@startuml story-<slug>
skinparam shadowing false
left to right direction

actor "Ator A" as A
actor "Ator B" as B
collections "Grupo C" as C
rectangle "Sistema X" as X
artifact "Objeto 1" as O1
artifact "Objeto 2" as O2

A --> O1 : 1. verbo
A --> B : 2. verbo
B --> O2 : 3. verbo
B --> X : 4. verbo
note right of O1
  Anotação / premissa
end note
@enduml
```

---

## 6. Glossário (linguagem ubíqua)

| Termo | Significado neste domínio |
| --- | --- |
| … | … |

---

## 7. Equipe / validação

| Papel | Quem (papel org., sem PII desnecessária) | Status |
| --- | --- | --- |
| Contador | … | … |
| Modelador | … | … |
| Validador | … | Pendente / Ok |

---

## 8. Hipóteses e abertos

- [ ] …
- [ ] …

## 9. Relação com outras histórias

| História | Relação |
| --- | --- |
| `01-…` | antecede / continua / variação de |
