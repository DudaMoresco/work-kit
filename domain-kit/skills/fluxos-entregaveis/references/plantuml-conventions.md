# Convenções PlantUML — fluxos entregáveis

Validar com MCP **`user-plantuml`**: `check_syntax` → corrigir.
Não usar plantuml.com.

---

## Comum

```plantuml
@startuml nome-unico-kebab
skinparam shadowing false
' ...
@enduml
```

- Um diagrama por bloco ` ```plantuml `
- Preferir ASCII em labels se acentos gerarem warning
- `autonumber` em toda sequência

---

## Sequência — participantes

```plantuml
@startuml seq-exemplo
skinparam shadowing false
autonumber

actor "Cliente" as Cli

box "Application"
  participant "DecidirOrcamentoService" as App
end box

participant "Orcamento" as Orc
participant "OrdemDeServico" as OS
participant "ItemEstoque" as Est
participant "DomainEvents" as Ev

Cli -> App : aprovar(orcamentoId, documento)
App -> Orc : aprovar()
note over Orc : ENVIADO -> APROVADO
App -> Ev : publish OrcamentoAprovado
Ev --> App : on OrcamentoAprovado
App -> OS : iniciarExecucao()
note over OS : AguardandoAprovacao -> EmExecucao
App -> Ev : publish ExecucaoIniciada
App -> Est : reservar(osId, orcamentoId, qtd)
note over Est : cria Reserva ATIVA
App -> Ev : publish ItensReservados
App --> Cli : aprovado
@enduml
```

| Elemento | Uso |
| --- | --- |
| `box "Application"` | Só services de orquestração |
| Agregados fora do box | Fronteira de BC / domínio |
| `DomainEvents` / `Events` | **Obrigatório** — publish e on |
| `note over X : A -> B` | Troca de status (obrigatória quando houver) |
| `note over X : status inalterado: S` | Quando o fluxo não muda status |
| `publish Evento` / `on Evento` | Produção / consumo |
| `alt` / `else` | Só no diagrama de alternativos (ou ramos que mudam regra) |

---

## Status

- Sempre `De -> Para` no note (ou mensagem de retorno com o status novo).
- Incluir status de **todos** os agregados afetados no mesmo diagrama
  (ex.: Orcamento **e** OS).
- Status de entidade interna (ex. `Reserva ATIVA -> CONSUMIDA`) também conta.

---

## Eventos

- Nome no passado; preferir linguagem do Event Storming.
- `App -> Ev : publish X` = produção.
- `Ev --> App : on X` = consumo neste fluxo (reação síncrona ok no monolito).
- Se o consumidor for **outro** fluxo:  
  `note over Ev : X consumido em: 05 - Aguardando item`
- Sem evento de domínio:  
  `note over Ev : sem publish neste fluxo`  
  e linha correspondente na tabela Eventos do MD.

Não inventar Event Bus / SNS/SQS se o design for monolito in-process —
`DomainEvents` representa o **contrato lógico**.

---

## Mapa (README)

```plantuml
@startuml mapa-exemplo
skinparam shadowing false
left to right direction
rectangle "Gatilhos" {
  (Gatilho A) as A
}
(01 Fluxo) as F1
A --> F1
@enduml
```

---

## Anti-padrões

- Sequência sem participante `DomainEvents` e sem nota explicando ausência
- `save` sem note de status quando o método de domínio muda status
- Evento no infinitivo (`AprovarOrcamento`) — usar passado (`OrcamentoAprovado`)
- Mermaid no lugar de PlantUML nesta pasta
