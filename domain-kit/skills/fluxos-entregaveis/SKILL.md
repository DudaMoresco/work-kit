---
name: fluxos-entregaveis
description: >-
  Gera ou atualiza documentação to-be de fluxos entregáveis (MVP/código)
  em products/{produto}/02-capabilities/{bc}/fluxos/: README com mapa, um MD por fluxo com
  diagramas de sequência PlantUML de sucesso e alternativos. Cada sequência
  deve explicitar troca de status e produção/consumo de eventos de domínio.
  Use when the user asks for fluxos entregáveis, sequências to-be do MVP,
  fluxos de aplicação a partir de design-tático/event-storming, ou pasta
  fluxos-entregaveis.
---

# Fluxos entregáveis (to-be MVP)

Documenta **fluxos que entram no código** (to-be), derivados de design
tático + Event Storming (+ decisões fechadas). Não é as-is de legado.

**Diferença de `fluxogramas-decisao`:** aquele é as-is + árvore de decisão + C4.
Este é to-be + application services + **par sucesso/alternativos**, com
**status e eventos obrigatórios** na sequência.

Referência de exemplo: `products/oficina-mecanica/02-capabilities/*/fluxos/`.

Templates: [references/templates.md](references/templates.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Montar/atualizar pasta `fluxos-entregaveis/` (ou `NN-fluxos-entregaveis/`)
- Sequências de application layer a partir de design-tático + ES
- Explicitar máquina de status e eventos lógicos antes do bootstrap

**Não usar** para fluxogramas as-is de produção (`fluxogramas-decisao`),
tabelas de cenário ES (`event-storming-to-scenario-tables`), ou C4 puro.

---

## Artefato (obrigatório)

Escrever no disco — não só no chat.

```text
products/{produto}/02-capabilities/{bc}/fluxos/
├── README.md
├── 01-<slug>.md
├── 02-<slug>.md
└── …
```

Mapa de paths: `work-hub/skills/references/hub-paths.md`. Confirmar `{produto}` e `{bc}` antes da 1ª gravação.

Fontes típicas (ler o que existir; não inventar regra fechada):

| Prioridade | Fonte |
| --- | --- |
| 1 | `snapshots-decisao/` (se houver) |
| 2 | `design-tatico/` (agregados + `*-fluxos-aplicacao*`) |
| 3 | `event-storming/` |
| 4 | Domain Stories / integração ACL |

Se decisão aberta: marcar **hipótese** no MD; não inventar como fechada.

---

## Fluxo de trabalho

```
Progresso:
- [ ] 1. Intake
- [ ] 2. Inventário (gatilho = 1 MD)
- [ ] 3. README (mapa + índice)
- [ ] 4. Um MD por fluxo (sucesso + alternativos)
- [ ] 5. Validar PlantUML (MCP user-plantuml)
- [ ] 6. Cross-links + atualizar snapshots se houver
```

### 1. Intake

Máx. 3–5 perguntas se faltar:

| Campo | Default |
| --- | --- |
| Path | `…/fluxos-entregaveis/` ou numerado no pipeline |
| Escopo | Todos os fluxos de application **no código MVP** |
| Fora de código | Só nota / não criar MD dedicado (ex. D-17) |

### 2. Inventário

Um MD = um gatilho coerente (abrir OS, montar orçamento, decidir, retirar…).
Numerar `01-`, `02-`… kebab-case. Classificar núcleo vs suporte no README.

### 3–4. README e MDs

Seguir [references/templates.md](references/templates.md).

### 5. Validar PlantUML

MCP `user-plantuml` → `check_syntax` em cada `@startuml`…`@enduml` até `valid: true`.
Convenções: [references/plantuml-conventions.md](references/plantuml-conventions.md).

### 6. Snapshots

Se o projeto tiver `snapshots-decisao/`, atualizar conforme a matriz do README
de lá (artefato novo → `estado-projeto.md` + `proximos.md`).

---

## Regra obrigatória — status e eventos na sequência

Toda sequência (sucesso **e** cada ramo relevante dos alternativos) deve
deixar explícito:

### 1. Troca de status

- Qual agregado/entidade muda de status (`OrdemDeServico`, `Orcamento`,
  `Reserva`, etc.).
- Transição no formato `De -> Para` (ex.: `EmExecucao -> AguardandoAprovacao`).
- Se **não** houver mudança de status no fluxo: `note` dizendo
  `status inalterado: <StatusAtual>`.

Formas aceitas (combináveis):

- Mensagem no agregado: `OS.aguardarAprovacao()` + `note over OS: EmDiagnostico -> AguardandoAprovacao`
- Retorno: `OS --> App : status AguardandoAprovacao`

### 2. Produção / consumo de eventos

Eventos de domínio **lógicos** (mesmo sem Event Bus no monolito).

| Papel | Como mostrar |
| --- | --- |
| **Produz** | Agregado ou App → `Events` : `publish <EventoNoPassado>` |
| **Consome** | `Events` → App (ou outro handler) : `on <Evento>` → reação |

- Participante obrigatório: `DomainEvents` (ou `Events`) — in-process ok.
- Nomes no **passado**, alinhados ao ES quando existir
  (`OrcamentoAprovado`, `ItensReservados`, `OSAguardandoItem`).
- Se o fluxo só orquestra comandos sem evento de domínio nomeado: declarar
  na tabela **Eventos** do MD `nenhum evento de dominio` e na sequência
  `note over Events: sem publish neste fluxo` — não omitir o participante
  sem explicar.

### Checklist por diagrama

- [ ] Toda transição de status aparece (`De -> Para` ou “inalterado”)
- [ ] Todo `publish` tem consumidor no mesmo fluxo **ou** nota
      `consumido em: NN — <fluxo>` / `consumidor futuro / fora MVP`
- [ ] Alternativos que mudam status/evento mostram a diferença no `alt`
- [ ] Tabela **Eventos** do MD bate com os `publish`/`on` do PlantUML

---

## Anti-padrões

- Sequência só com `save`/`find` sem status nem eventos
- Orçamento chamando Estoque direto (se a decisão do domínio proíbe — ACL na App)
- Misturar as-is C4 com este pacote no mesmo MD
- Inventar eventos que não existem no ES/tático sem marcar hipótese
- Um MD gigante com todos os fluxos

---

## Exemplos de pedido

| Pedido | Ação |
| --- | --- |
| “Cria fluxos entregáveis a partir do tático/ES” | Intake → inventário → README + N MDs |
| “Atualiza o 03 com status e eventos” | Reescrever sequências do MD + tabela Eventos |
| “Só o mapa” | README com mapa + índice |
