# Event Storming — <cenário>

> Gerado com `event-storming`.

## Sumário

| Campo | Valor |
| --- | --- |
| Recorte / BC | … |
| Tipo | Brainstorm + timeline |
| Data | YYYY-MM-DD |
| Facilitador / Experts | papéis |

---

## 1. Participantes

| Papel | Quem (papel org.) |
| --- | --- |
| Domain Expert | … |
| Ouvinte | … |
| Facilitador | … |

---

## 2. Brainstorm — eventos (sem ordem)

- Atividade publicada
- …
- …

*(verbo no passado)*

---

## 3. Timeline — caminho ideal

1. …
2. …
3. …

## 4. Alternativas / exceções

| Após evento | Alternativa | Evento(s) |
| --- | --- | --- |
| … | … | … |

---

## 5. PlantUML — linha do tempo

```plantuml
@startuml es-timeline-<slug>
skinparam shadowing false
left to right direction

rectangle "Atividade publicada" as E1 #Orange
rectangle "Entrega submetida" as E2 #Orange
rectangle "Entrega corrigida" as E3 #Orange
rectangle "Nota registrada" as E4 #Orange

E1 --> E2
E2 --> E3
E3 --> E4

rectangle "Entrega rejeitada" as EX #Pink
E2 --> EX : alternativa
@enduml
```

---

## 6. Próximos passos

- [ ] `event-storming-to-scenario-tables` (comandos/políticas/tabelas)
- [ ] `ddd-design-tatico` (agregados)
- [ ] Abertos: …
