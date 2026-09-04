---
name: event-storming
description: >-
  Conduz e documenta sessão de Event Storming: time, brainstorm de eventos
  (verbo no passado), linha do tempo (caminho ideal + alternativas); gera MD com
  PlantUML. Acione apenas pelo nome `event-storming` (não auto-invocar).
disable-model-invocation: true
---

# Event Storming

Tempestade de eventos: modelagem colaborativa do processo com **eventos de
domínio**, timeline e alternativas. Artefato Markdown + **PlantUML**.

Idioma: **pt-BR**. Para converter diagrama visual (SVG/Miro) em tabelas, use
`event-storming-to-scenario-tables` **depois**.

Relacionadas:

- `domain-storytelling` — narrativa pictográfica (complementar)
- `ddd-linguagem-e-contextos` — BCs/UL (antes ou após ES)
- `event-storming-to-scenario-tables` — tabelas por funcionalidade
- `ddd-design-tatico` — agregados a partir dos eventos

Templates: [template.md](template.md) · Exemplos: [examples.md](examples.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md)

---

## Quando usar

- Usuário citar **`event-storming`**
- Pedir tempestade de eventos, timeline de domínio, brainstorm de eventos

**Não usar** se a entrada já for SVG/diagrama pronto para tabelas →
`event-storming-to-scenario-tables`.

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

Nesta skill o foco é **eventos + timeline**. Comandos, políticas, agregados
hotspots: incluir se o usuário trouxer ou pedir; senão marcar como próximo passo
(`event-storming-to-scenario-tables` / `ddd-design-tatico`).

---

## Artefato (obrigatório)

### Onde salvar

1. Path do usuário.
2. Hub: `products/{produto}/01-product/03-discovery/01-event-storming/`  
   `README.md` + `01-<cenario>.md`
3. Senão: `docs/event-storming-<slug>.md`.

Mapa de paths: [references/hub-paths.md](../references/hub-paths.md). Confirmar `{produto}` (e `{bc}` ou `{iniciativa}` quando aplicável) antes da 1ª gravação.

---

## Fluxo

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

## Saída no chat

1. Path  
2. Contagem de eventos + timeline resumida  
3. Alternativas e abertos  

Exemplo: [examples.md](examples.md).
