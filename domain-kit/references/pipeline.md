# Pipeline do domain-kit

Fases **Evidências → Estratégico → Descoberta → Operacional** → handoff arch-kit.

Placeholders: `{produto}`, `{bc}`, `{iniciativa}`.

Guia: [`../COMMAND-GUIDE.md`](../COMMAND-GUIDE.md) · Estágios: [`discovery-workflow.md`](discovery-workflow.md) · Critérios: [`gates.yml`](gates.yml)

---

## Camadas de comandos

| Camada | Comandos |
| --- | --- |
| Hub | `domain.install` |
| Meta | `domain.init`, `domain.scan`, `domain.status`, `domain.change` |
| Macro | `domain.discover`, `domain.model` |
| Micro | `domain.flow`, `domain.decision` |

~~`domain.capability`~~ → arch-kit.

---

## Ingestão de fontes (Evidências)

Ver [`../wrappers/scan-github.md`](../wrappers/scan-github.md). Saída: `01-product/00-scan/`.

Primeiro scan em **`/domain.init`**. Re-sync: **`/domain.scan`**.

---

## Visão

```mermaid
flowchart TB
  subgraph hub [Hub]
    INS[domain.install]
  end
  subgraph meta [Meta]
    INIT[domain.init]
    SCAN[domain.scan]
    CHG[domain.change]
  end
  subgraph discover ["/domain.discover"]
    S1[Estratégico]
    S2[Stories]
    S5[Event Storming]
    S3[UL + BCs]
  end
  subgraph operacional ["/domain.flow + model"]
    FL[Fluxos 03-operacional]
    NFR[NFRs produto]
    REG[Registry D-n]
  end
  INS --> INIT
  INIT --> EV[Evidências PASS]
  SCAN -.-> EV
  EV --> DISC[domain.discover]
  CHG --> DISC
  CHG --> FL
  DISC --> S1
  S1 --> S3
  S1 --> S2
  S2 --> S5
  S3 --> FL
  S5 --> FL
  FL --> NFR
  NFR --> REG
  REG --> OP[Operacional PASS]
  OP --> ARCH["/arch.route"]
```

---

## Mapa fase → artefatos

| Fase | Artefatos |
| --- | --- |
| Evidências | `sources.yml`, `00-scan/`, `sintese-evidencias.md`, `product-README.md` (stub) |
| Estratégico | `01-design-estrategico.md`, `desafio-negocio.md`, `bounded-contexts.md`, `linguagem-ubiqua.md` |
| Descoberta | `03-discovery/01-event-storming/`, `02-domain-storytelling/`, `abertos.md` |
| Operacional | `03-operacional/fluxos/`, `flows-registry.yml`, `01-requisitos.md`, `03-registry/produto.md` |
| Arch (fora) | `arch/{bc}/design-tatico.md`, `arch/01-integration/`, `arch/fluxos/` |

---

## Paths de fluxo

| Camada | Path |
| --- | --- |
| **Negócio (domain-kit)** | `products/{p}/01-product/03-operacional/fluxos/{NN}-{slug}.md` |
| **Técnica (arch-kit)** | `products/{p}/arch/fluxos/{NN}-{slug}-tecnico.md` |
| Legado | `02-capabilities/{bc}/fluxos/` — só adopt/migração |

Wrapper autoridade: [`../wrappers/fluxos-entregaveis.md`](../wrappers/fluxos-entregaveis.md).

---

## Validação

```bash
.domain/scripts/validate_gate.py --phase evidencias --product {p}
.domain/scripts/validate_gate.py --phase operacional --product {p} --suggest
# aliases: --gate G0|G1|G2
```
