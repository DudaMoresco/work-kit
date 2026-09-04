# Exemplos — `event-storming`

## Escola — entrega e correção de atividade

### Brainstorm (amostra)

- Atividade publicada
- Prazo definido
- Entrega submetida
- Entrega recebida
- Correcao iniciada
- Nota atribuida
- Feedback enviado
- Entrega rejeitada por prazo
- Entrega reaberta

### Timeline ideal

1. Atividade publicada  
2. Prazo definido  
3. Entrega submetida  
4. Correcao iniciada  
5. Nota atribuida  
6. Feedback enviado  

### Alternativa

Após “Entrega submetida”: se fora do prazo → “Entrega rejeitada por prazo”.

### PlantUML

```plantuml
@startuml es-timeline-entrega-escola
skinparam shadowing false
left to right direction

rectangle "Atividade publicada" as E1 #Orange
rectangle "Prazo definido" as E2 #Orange
rectangle "Entrega submetida" as E3 #Orange
rectangle "Correcao iniciada" as E4 #Orange
rectangle "Nota atribuida" as E5 #Orange
rectangle "Feedback enviado" as E6 #Orange
rectangle "Entrega rejeitada por prazo" as EX #Pink

E1 --> E2
E2 --> E3
E3 --> E4
E4 --> E5
E5 --> E6
E3 --> EX : fora do prazo
@enduml
```
