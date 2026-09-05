---
name: fluxos-entregaveis
description: >-
  Know-how de fluxos to-be (cenários ponta a ponta, status e eventos).
  No domain-kit, paths canônicos vêm do wrapper: products/{produto}/01-product/04-operacional/fluxos/.
  Detalhe técnico (serviços/filas) fica fora do escopo do domain-kit.
  Use with /domain.flow or when documenting operational flows.
---

# Fluxos operacionais / entregáveis

Documenta **cenários to-be** derivados de Event Storming, domain stories e decisões.

No **domain-kit**, a camada obrigatória é **negócio** (linguagem ubíqua). Sequências técnicas
(application services, filas) ficam **fora do escopo do domain-kit**.

**Diferença de `fluxogramas-decisao`:** aquele é as-is em `03-discovery/00-as-is/`. Este é to-be em `04-operacional/fluxos/`.

**Paths — autoridade do wrapper:**  
[`../../wrappers/fluxos-entregaveis.md`](../../wrappers/fluxos-entregaveis.md)  

Não inventar path fora de [hub-paths.md](../../references/hub-paths.md).

Templates: [references/templates.md](references/templates.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md) ·  
Template domain-kit: [`../../templates/fluxo-operacional.md`](../../templates/fluxo-operacional.md) ·  
Mapa: [references/hub-paths.md](../../references/hub-paths.md)

---

## Quando usar

- `/domain.flow {NN}` (via wrapper domain-kit)
- Montar/atualizar fluxos operacionais de negócio
- Explicitar status e eventos de domínio antes do detalhe técnico

**Não usar** para fluxogramas as-is (`fluxogramas-decisao` → `00-as-is/`), tabelas ES
(`event-storming-to-scenario-tables`), ou C4 puro.

---

## Why decisions

- Transições de status explícitas (`De -> Para` ou inalterado) evitam sequência
  só com `save`/`find` sem significado de domínio.
- Um fluxo por arquivo + deps em `flows-registry.yml` mantêm ordem, ownership e
  review legíveis.
- Camada **negócio** (UL) é obrigatória no domain-kit; detalhe técnico
  (serviços/filas) vai para `arch/fluxos/` se existir — não polui o MD operacional.
- Path canônico `01-product/04-operacional/fluxos/` alinha hub-paths e o wrapper.
- Fontes ES / stories / UL / `05-decisoes` antes de inventar regra fechada.
- Separação as-is (`00-as-is/`) vs to-be (`04-operacional/`) evita misturar
  comportamento atual com entregável.

---

## Artefato (obrigatório) — domain-kit

```text
products/{produto}/01-product/04-operacional/fluxos/
├── {NN}-{slug}.md          ← um fluxo por arquivo
└── …                       ← registry: products/{produto}/flows-registry.yml
```

Template preferido: `templates/fluxo-operacional.md` (camada negócio).

### Camada técnica (fora do escopo do domain-kit — opcional)

```text
products/{produto}/arch/fluxos/{NN}-{slug}-tecnico.md
```

Confirmar `{produto}` e deps (`flow_deps.py`) antes da 1ª gravação.

Fontes típicas (ler o que existir; não inventar regra fechada):

| Prioridade | Fonte |
| --- | --- |
| 1 | `03-discovery/01-event-storming/` |
| 2 | `03-discovery/02-domain-storytelling/` |
| 3 | `02-domain/bounded-contexts.md` + `linguagem-ubiqua.md` |
| 4 | `05-decisoes/produto.md` (D-n) |
| 5 | design-tático / integração (só se já existir sob `arch/` — não bloquear fluxo negócio) |

Se decisão aberta: marcar **hipótese** no MD; não inventar como fechada.

---

## Fluxo de trabalho

```
Progresso:
- [ ] 1. Intake (produto, NN, BC, deps)
- [ ] 2. Draft em .draft/ (plan mode)
- [ ] 3. MD do fluxo (cenário + exceções + eventos)
- [ ] 4. Atualizar flows-registry.yml
- [ ] 5. Validar PlantUML se houver diagrama
- [ ] 6. OK do usuário → promote
```

### 1. Intake

Máx. 3 perguntas se faltar: título, ator, métrica de sucesso, deps.

### 2–3. Conteúdo

Preferir estrutura de `fluxo-operacional.md`. Se o time pedir sequência PlantUML
detalhada, seguir [references/templates.md](references/templates.md) — ainda assim
gravar sob `04-operacional/` no domain-kit (ou `arch/fluxos/` se for técnico).

### 5. Validar PlantUML

MCP `user-plantuml` → `check_syntax` até `valid: true`.

---

## Regra — status e eventos

Toda sequência relevante (sucesso e alternativos) deve deixar explícito:

### 1. Troca de status

- Qual conceito de domínio muda (`Pedido`, `Notificacao`, …)
- Transição `De -> Para`, ou `status inalterado: …`

### 2. Produção / consumo de eventos

Eventos de domínio **lógicos** (linguagem ubíqua), alinhados ao ES quando existir.

| Papel | Como mostrar |
| --- | --- |
| **Produz** | publish / emite `<EventoNoPassado>` |
| **Consome** | on `<Evento>` → reação |

Se não houver evento: declarar `nenhum evento de dominio` — não omitir sem explicar.

### Checklist

- [ ] Transições de status explícitas
- [ ] Eventos batem com a tabela do MD / ES
- [ ] Alternativos que mudam status/evento mostram a diferença
- [ ] Path = `04-operacional/fluxos/` (domain) ou `arch/fluxos/` (técnico)

---

## Anti-patterns

- Inventar path fora de [hub-paths.md](../../references/hub-paths.md).
- Detalhe técnico (ACL, filas, payloads, application services) como conteúdo
  principal do MD de negócio — isso fica em `arch/fluxos/` se necessário.
- Sequência só com `save`/`find` sem status nem eventos.
- Inventar eventos fora do ES sem marcar hipótese.
- Um MD gigante com todos os fluxos.
- Documentar as-is sob `04-operacional/` (usar `03-discovery/00-as-is/`).

---

## Exemplos de pedido

| Pedido | Ação |
| --- | --- |
| `/domain.flow 01` | Wrapper → draft operacional → registry |
| “Fluxo técnico com filas” | Fora do escopo → `arch/fluxos/` |
| “Só o mapa de jornadas” | índice no registry + MDs operacionais |
