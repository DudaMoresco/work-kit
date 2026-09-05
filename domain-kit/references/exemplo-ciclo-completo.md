# Exemplo — ciclo completo (produto novo + evolução)

Narrativa ponta a ponta com o produto fictício **Biblioteca Comunitária**, cobrindo os comandos do domain-kit do zero até evolução e problema em produção.

Contrato: [plan-mode.md](plan-mode.md) · Comandos: [COMMAND-GUIDE.md](../COMMAND-GUIDE.md)

Paths relativos a `products/biblioteca-comunitaria/` (salvo quando indicado).

---

## 1. Hub novo

```text
/domain.install
```

Instala o kit no hub (skills, wrappers, scripts, comandos). **Não** cria artefato de produto.

Próximo: `/domain.init`.

---

## 2. Produto novo — Evidências

```text
/domain.init biblioteca-comunitaria --initiative demo-iniciativa
```

Cria índices (`sources.yml`, `flows-registry.yml`, `domain-status.json`, `product-README.md`, `CHANGELOG.md`, registry stub), condução do **primeiro scan**, curadoria e `01-product/00-scan/sintese-evidencias.md`.

Checagem:

```text
/domain.status biblioteca-comunitaria
```

Sugestão típica: `/domain.discover`.

---

## 3. Estratégico + Descoberta

```text
/domain.discover biblioteca-comunitaria
# lacunas (0b) + --stage auto

/domain.discover --stage strategic
# 01-product/01-vision/01-design-estrategico.md

/domain.discover --stage contexts
# desafio-negocio, linguagem-ubiqua, bounded-contexts + refresh product-README

/domain.discover --stage stories
# 03-discovery/02-domain-storytelling/… (empréstimo, reserva, multa)

/domain.discover --stage event-storming
# 03-discovery/01-event-storming/ (ciclo reserva → devolução)
```

`/domain.status` → Estratégico e Descoberta PASS → próximo: `/domain.flow`.

---

## 4. Operacional — fluxos e decisões

```text
/domain.flow 01
# Empréstimo de exemplar → 04-operacional/fluxos/01-….md + flows-registry

/domain.decision
# D-01: multa só após X dias → 05-decisoes/produto.md

/domain.flow 02
# Reserva de título indisponível
```

---

## 5. Fechar Operacional (MVP)

```text
/domain.model biblioteca-comunitaria
# rascunho NFRs de produto

/domain.model biblioteca-comunitaria --finalize
# 01-product/04-operacional/requisitos.md + validação da fase
```

`/domain.status` → todas as fases PASS → **fim do pipeline domain-kit** para o MVP.

A próxima etapa técnica (design de solução, tático, implementação) fica **fora do escopo do domain-kit**.

**Não** usar `/domain.capability` neste fluxo.

---

## 6. Fonte externa mudou

O enunciado da iniciativa foi atualizado (ex.: novo canal WhatsApp).

```text
/domain.scan biblioteca-comunitaria
```

Atualiza manifest / `sources.yml`, refresh de `sintese-evidencias.md` e `CHANGELOG.md`.

Lacunas de negócio **não** são reabertas aqui — isso fica para `/domain.discover` ou `/domain.change`.

---

## 7. Evolução intencional (E-n)

Negócio quer **renovação de empréstimo pelo membro**.

```text
/domain.change biblioteca-comunitaria \
  --kind evolution \
  --title "Renovação de empréstimo pelo membro" \
  --phases descoberta,operacional \
  --handoff discover
```

Registra **E-01** em `01-product/02-domain/evolucoes.md` e preenche `activeChange` em `domain-status.json`.

```text
/domain.discover --stage stories
# story da renovação (sessão vinculada a E-01)

/domain.flow 03
# fluxo operacional Renovação

/domain.decision
# D-02: no máximo 2 renovações se não houver reserva

/domain.model --finalize
# revalida Operacional se NFRs/fluxos mudaram

/domain.change --close
# encerra activeChange; E-01 concluída
```

---

## 8. Problema em produção (P-n)

Multa aplicada em feriado municipal — negócio discorda.

```text
/domain.change \
  --kind problem-new \
  --title "Multa cobrada em feriado municipal" \
  --handoff discover

/domain.discover --stage contexts
# ajusta UL / regra no BC Empréstimo

/domain.flow 01
# atualiza fluxo Empréstimo (ou fluxo dedicado)

/domain.decision
# D-03: feriados municipais não contam atraso

/domain.change --close
```

---

## 9. Produto já no hub sem domain-kit (paralelo)

```text
/domain.init biblioteca-antiga --adopt
/domain.status biblioteca-antiga
```

Só índices faltantes + inventário de gaps — **não** recria conteúdo. Depois preencher pelos gaps (`discover` → `flow` → `model --finalize`).

---

## Mapa — comandos neste exemplo

| Comando | Quando aparece |
| --- | --- |
| `/domain.install` | Hub zerado |
| `/domain.init` | Bootstrap + 1º scan |
| `/domain.init --adopt` | Produto já no hub (§9) |
| `/domain.status` | Entre fases e no fim |
| `/domain.discover` | Estratégico / Descoberta (+ evolução) |
| `/domain.flow` | Fluxos 01, 02, 03 |
| `/domain.decision` | D-01 … D-03 |
| `/domain.model` / `--finalize` | Fechar Operacional (MVP e pós E-01) |
| `/domain.scan` | Fonte/enunciado mudou |
| `/domain.change` / `--close` | E-01 renovação + P-n multa |
| `/domain.capability` | **Não** entra no fluxo feliz (fora do escopo) |
| `/domain.clarify` | **Não** entra — perguntas ficam inline nos comandos |

---

## Pipeline mental

```text
install → init → discover* → flow* → decision* → model --finalize
                 ↑________________|  (retrabalho de fase)

scan                          # fonte externa mudou
change → discover|flow|model|decision → change --close
```

Sandbox local: `bash domain-kit/scripts/bootstrap-test-hub.sh` (produto `demo-produto`).
