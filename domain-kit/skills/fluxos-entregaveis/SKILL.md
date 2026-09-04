---
name: fluxos-entregaveis
description: >-
  Know-how de fluxos to-be (cenários ponta a ponta, status e eventos).
  No domain-kit, paths canônicos vêm do wrapper: products/{produto}/01-product/03-operacional/fluxos/.
  Detalhe técnico (serviços/filas) → arch-kit. Use with /domain.flow or when documenting operational flows.
---

# Fluxos operacionais / entregáveis

Documenta **cenários to-be** derivados de Event Storming, domain stories e decisões.

No **domain-kit**, a camada obrigatória é **negócio** (linguagem ubíqua). Sequências técnicas
(application services, filas) ficam no **arch-kit**.

**Diferença de `fluxogramas-decisao`:** aquele é as-is + árvore de decisão. Este é to-be.

**Paths — autoridade do wrapper:**  
[`../../wrappers/fluxos-entregaveis.md`](../../wrappers/fluxos-entregaveis.md)  
Ignore paths legados `02-capabilities/{bc}/fluxos/` ao gravar artefatos novos.

Templates: [references/templates.md](references/templates.md) ·  
PlantUML: [references/plantuml-conventions.md](references/plantuml-conventions.md) ·  
Template domain-kit: [`../../templates/fluxo-operacional.md`](../../templates/fluxo-operacional.md)

---

## Quando usar

- `/domain.flow {NN}` (via wrapper domain-kit)
- Montar/atualizar fluxos operacionais de negócio
- Explicitar status e eventos de domínio antes do arch-kit

**Não usar** para fluxogramas as-is (`fluxogramas-decisao`), tabelas ES
(`event-storming-to-scenario-tables`), ou C4 puro.

---

## Artefato (obrigatório) — domain-kit

```text
products/{produto}/01-product/03-operacional/fluxos/
├── {NN}-{slug}.md          ← um fluxo por arquivo
└── …                       ← registry: products/{produto}/flows-registry.yml
```

Template preferido: `templates/fluxo-operacional.md` (camada negócio).

### Camada técnica (arch-kit — opcional)

```text
products/{produto}/arch/fluxos/{NN}-{slug}-tecnico.md
```

### Legado (somente migração)

```text
products/{produto}/02-capabilities/{bc}/fluxos/   ← não usar para fluxos novos
```

Confirmar `{produto}` e deps (`flow_deps.py`) antes da 1ª gravação.

Fontes típicas (ler o que existir; não inventar regra fechada):

| Prioridade | Fonte |
| --- | --- |
| 1 | `03-discovery/01-event-storming/` |
| 2 | `03-discovery/02-domain-storytelling/` |
| 3 | `02-domain/bounded-contexts.md` + `linguagem-ubiqua.md` |
| 4 | `03-registry/produto.md` (D-n) |
| 5 | design-tático / integração (só se já existir no arch — não bloquear fluxo negócio) |

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
gravar sob `03-operacional/` no domain-kit (ou `arch/fluxos/` se for técnico).

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
- [ ] Path = `03-operacional/fluxos/` (domain) ou `arch/fluxos/` (técnico)

---

## Anti-padrões

- Gravar fluxo novo em `02-capabilities/.../fluxos/`
- Misturar ACL/filas/payloads no MD de negócio (isso é arch)
- Sequência só com `save`/`find` sem status nem eventos
- Inventar eventos fora do ES sem marcar hipótese
- Um MD gigante com todos os fluxos

---

## Exemplos de pedido

| Pedido | Ação |
| --- | --- |
| `/domain.flow 01` | Wrapper → draft operacional → registry |
| “Fluxo técnico com filas” | arch-kit / `arch/fluxos/` |
| “Só o mapa de jornadas” | índice no registry + MDs operacionais |
