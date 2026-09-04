# Exemplos — `levantamento-requisitos`

## Sistema de Gestão de Tarefas Colaborativas (amostra aula 07)

### Riscos (resumo)

| Risco | Nota |
| --- | --- |
| Valor | Times precisam coordenar tarefas sem e-mail infinito? |
| Negócio | Alinha a produtividade interna; sem risco legal óbvio |
| Usabilidade | Onboarding deve ser curto |
| Técnico | Integração e-mail / notificações |

### Persona

Coordenador(a) de projeto que distribui tarefas e acompanha status.

### Problema

Solicitações se perdem em e-mail; falta visibilidade de status.

### Objetivos

Centralizar tarefas; status claro; notificações.

### Jornada (trecho CRM da aula 08 — orçamento)

1. Recebe solicitação de orçamento por e-mail  
2. Qualifica o lead  
3. Gera proposta  
4. Envia proposta ao cliente  

```plantuml
@startuml jornada-crm-orcamento
skinparam shadowing false
left to right direction

rectangle "Email recebido" as S1
rectangle "Lead qualificado" as S2
rectangle "Proposta gerada" as S3
rectangle "Proposta enviada" as S4
S1 --> S2
S2 --> S3
S3 --> S4
@enduml
```

### RF (amostra)

| ID | Requisito |
| --- | --- |
| RF-01 | Criar tarefa a partir de e-mail |
| RF-02 | Atribuir responsável |
| RF-03 | Gerar proposta a partir do orçamento |
