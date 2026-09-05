---
name: event-storming
description: >-
  Conduz e documenta sessão de Event Storming: time, brainstorm de eventos
  (verbo no passado), linha do tempo (caminho ideal + alternativas); gera MD com
  PlantUML. Acione apenas pelo nome `event-storming` (não auto-invocar).
disable-model-invocation: true
---

# Event Storming

## Purpose

Tempestade de eventos: modelagem colaborativa do processo com **eventos de
domínio**, timeline e alternativas. Artefato Markdown + **PlantUML** em
`01-product/03-discovery/01-event-storming/`.

Idioma: **pt-BR**. Para converter diagrama visual (SVG/Miro) em tabelas, use
`event-storming-to-scenario-tables` **depois**.

Relacionadas:

- `domain-storytelling` — narrativa pictográfica (complementar)
- `ddd-linguagem-e-contextos` — BCs/UL (antes ou após ES)
- `event-storming-to-scenario-tables` — tabelas por funcionalidade
- Design tático / agregados a partir dos eventos — **fora do escopo do domain-kit**

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`event-storming`**
- Pedir tempestade de eventos, timeline de domínio, brainstorm de eventos

**Não usar** se a entrada já for SVG/diagrama pronto para tabelas →
`event-storming-to-scenario-tables`.

---

## Why decisions

- Eventos no **passado** forçam fatos de domínio, não intenções técnicas.
- Brainstorm **sem ordem** primeiro evita ancorar cedo demais no caminho feliz.
- Timeline ideal → alternativas depois reduz ruído e facilita revisão com experts.
- Foco desta skill é **eventos + timeline**; comandos/políticas/hotspots só se
  o usuário trouxer ou pedir — senão próximo passo (`to-scenario-tables`).
- Agregados, camadas e design de solução ficam **fora do escopo do domain-kit**.
- PlantUML validado via MCP evita diagrama ilegível no hub.
- Path canônico sob discovery separa exploração de fluxos operacionais to-be.

---

## Conceitos (obrigatório)

### Time da sessão

| Papel | Função |
| --- | --- |
| Domain Experts | Contam a história (quantos forem necessários) |
| Ouvintes | Aprendem (dev e agregados) |
| Facilitador | Perguntas, alinhamento ao objetivo |

Material: post-its / Miro / FigJam — ou narrativa no chat (agente = modelador).

### Evento de domínio

Algo que **ocorreu** no domínio. Escrita: **verbo no passado** (ex.: “Atividade
publicada”). No brainstorm: post-its “laranja”; **sem ordem** até esgotar ideias.

### Linha do tempo

Organizar o “caminho ideal”; depois alternativas/exceções; remover duplicatas;
corrigir/adicionar eventos esquecidos.

Nesta skill o foco é **eventos + timeline**. Comandos, políticas, hotspots:
incluir se o usuário trouxer ou pedir; senão marcar como próximo passo
(`event-storming-to-scenario-tables`). Modelagem tática (agregados, ACL) é
**fora do escopo do domain-kit**.

---

## Outputs canônicos

Mapa: [references/hub-paths.md](../../references/hub-paths.md). Em comando
`domain-*`, o **wrapper vence** se houver conflito.

1. Path explícito do usuário (se houver).
2. Hub:

```text
products/{produto}/01-product/03-discovery/01-event-storming/
├── README.md
└── 01-<cenario>.md
```

3. Fora do hub: `docs/event-storming-<slug>.md`.

Confirmar `{produto}` antes da 1ª gravação. Usar [template.md](template.md).

---

## Workflow

```
Progresso:
- [ ] 1. Intake (recorte, participantes, path)
- [ ] 2. Brainstorm de eventos (passado, sem ordem)
- [ ] 3. Timeline caminho ideal
- [ ] 4. Alternativas / exceções
- [ ] 5. PlantUML + validar MCP
- [ ] 6. Abertos + sugerir to-scenario-tables se couber
```

Validar com MCP **`user-plantuml`**.

---

## Anti-patterns

- Eventos no infinitivo ou futuro (“criar conta”, “vai notificar”).
- Ordenar a timeline antes de esgotar o brainstorm.
- Misturar serviços, filas e payloads no MD de discovery.
- Exigir BCs/agregados nesta etapa (tático / fora do escopo).
- Converter SVG em tabelas nesta skill (usar `to-scenario-tables`).
- Gravar sob `04-operacional/fluxos/` — isso é fluxo to-be, não ES.

---

## Exit

Saída no chat:

1. Path gravado  
2. Contagem de eventos + timeline resumida  
3. Alternativas e abertos  
4. Próximo passo sugerido (`to-scenario-tables` / UL / story) se couber  

Exemplo: [examples.md](examples.md).
