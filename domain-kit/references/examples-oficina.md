# Walkthrough — domain-kit na oficina-mecanica

Exemplo concreto de como o pipeline se materializou no hub real.

**Produto:** `oficina-mecanica`  
**Iniciativa:** `tech-challenge-fase1`

---

## Entrada

Enunciado FIAP: back-end monolítico, OS + orçamento + estoque + cadastros + JWT.

Path: `initiatives/tech-challenge-fase1/01-enunciado.md`

---

## `/domain.discover` — o que foi produzido

### 1. Design estratégico

**Arquivo:** `01-product/01-vision/01-design-estrategico.md`

Decisões-chave:
- Subdomínio **principal:** ciclo da ordem de serviço (diagnóstico → entrega)
- **Suporte:** estoque, cadastros
- **Genérico:** autenticação admin (JWT)

### 2. Domain Storytelling (6 histórias)

**Pasta:** `01-product/03-discovery/02-domain-storytelling/`

| # | História | Insight de negócio |
| --- | --- | --- |
| 01 | Identificação e abertura OS | Cliente + veículo antes da OS |
| 02 | Análise e orçamento inicial | Diagnóstico gera orçamento separado |
| 03 | Aprovação, reserva, execução | Reserva ≠ baixa física |
| 04 | Estoque virtual e físico | Saldo disponível = físico − reservas |
| 05 | Orçamento complementar | Acréscimo durante execução |
| 06 | Cliente acompanha OS | API pública sem JWT admin (→ D-06, D-27) |

### 3. Event Storming (5 workshops)

**Pasta:** `01-product/03-discovery/01-event-storming/`

Workshops separados por recorte — não um ES único infinito:
- 01 identificação e cadastro
- 02 criação/análise/orçamento
- 03 reserva e execução
- 04 orçamento complementar
- 05 exceções estoque

Origem de decisões como D-13 (orçar só disponível; resto via complementar).

### 4. Linguagem ubíqua + BCs

**Pasta:** `01-product/02-domain/`

| Arquivo | Conteúdo |
| --- | --- |
| `desafio-negocio.md` | Planilhas vs realidade operacional |
| `linguagem-ubiqua.md` | OS, Orçamento, Reserva, Baixa, Item… |
| `bounded-contexts.md` | 5 BCs nomeados |

**Gate G1:** passou — BCs fechados, discovery rico.

---

## `/domain.model` — o que foi produzido

### 1. Integração entre BCs

**Arquivo:** `01-product/04-integration/01-contextos.md`

Decisão estrutural **D-16:**

```text
Orçamento NÃO chama Estoque diretamente.
OS orquestra: aprovação → Reservar → retirada → Baixar → Liberar.
```

Sem este doc, o design tático de cada BC fica inconsistente.

### 2. Requisitos

**Arquivo:** `04-platform/01-non-functional/01-requisitos.md`

RF/RNF derivados dos fluxos e enunciado (inclui D-36 observabilidade depois).

Owned pelo domain-kit na fase model; arch-kit **linka**, não reescreve.

### 3. Design tático por BC

**Pasta:** `02-capabilities/{bc}/design-tatico.md`

| BC | Agregado raiz | Decisões ligadas |
| --- | --- | --- |
| ordem-de-servico | OrdemDeServico | D-01…D-08, D-16, D-32 |
| orcamento | Orcamento | D-02, D-07, D-10, D-11 |
| estoque | ItemEstoque | D-09, D-12, D-14 |
| cadastros | (entidades CRUD) | D-20 packaging |
| acesso | — | D-06, D-27 |

### 4. Fluxos entregáveis (7)

Distribuídos por BC, numerados **01–07** para rastreio:

| fluxo | BC principal | Arquivo |
| --- | --- | --- |
| 01 | ordem-de-servico | `fluxos/01-identificacao-e-abertura-os.md` |
| 02 | orcamento | `fluxos/02-orcamento-inicial.md` |
| 03 | orcamento | `fluxos/03-decisao-orcamento.md` |
| 04 | estoque | `fluxos/04-retirada-e-baixa.md` |
| 05 | ordem-de-servico | `fluxos/05-aguardando-item.md` |
| 06 | orcamento | `fluxos/06-orcamento-complementar.md` |
| 07 | ordem-de-servico | `fluxos/07-finalizar-e-entregar.md` |

Estes 7 fluxos viraram, depois, **stories #11–#17** na delivery-kit (1:1).

### 5. Orquestração

**Arquivo:** `02-capabilities/ordem-de-servico/fluxos-aplicacao.md`

Use cases que **coordenam** BCs (application layer) — ex.: “Abrir OS”, “Executar fluxo 02”.

### 6. Registry produto

**Arquivo:** `03-registry/produto.md`

33 decisões D-01…D-33, cada uma com:
- capability
- status (`aceita`)
- texto da decisão
- **link** para evidência (fluxo, ES, tático)

Exemplo **D-03** (bloquear OS duplicada para mesmo veículo):
- Evidência: `02-capabilities/ordem-de-servico/`
- Impacto: invariante no agregado OrdemDeServico

**Gate G2:** passou em 2026-08-23 → arch-kit iniciou (`rota-decisao.md`).

---

## Diagrama do que o domain-kit cobriu

```text
ENUNCIADO
    │
    ├─ discover ─────────────────────────────────────┐
    │   design-estrategico                           │
    │   domain-stories (×6)                          │
    │   event-storming (×5)                          │
    │   UL + BCs (×5)                                │
    │                    G1 ✓                        │
    ├─ model ────────────────────────────────────────┤
    │   integração (D-16 ACL)                        │
    │   requisitos RF/RNF                            │
    │   design-tatico (×5 BC)                        │
    │   fluxos 01–07                                 │
    │   fluxos-aplicacao                             │
    │   registry D-01…33                             │
    │                    G2 ✓                        │
    └────────────────────────────────────────────────┘
                         │
                         ▼
                    arch-kit (estilo, C4, ADR…)
```

---

## Lições para replicar

1. **ES em workshops pequenos** — mais fácil de manter que 1 diagrama gigante.
2. **D-n cedo** — toda regra polêmica vira linha no registry com link.
3. **Integração antes do tático** — D-16 evitou acoplamento Orçamento↔Estoque no código.
4. **Numerar fluxos 01–NN** — IDs estáveis até spec-kit (`fluxo-01` → story-11 → spec-011).
5. **Requisitos em platform/** — ok; domain-kit “entrega” lá na fase model.

---

## Se refizesse com domain-kit desde o zero

Ordem sugerida pelo framework (igual ao que aconteceu na prática):

```bash
/domain.install oficina-mecanica
/domain.init oficina-mecanica --initiative tech-challenge-fase1
/domain.discover oficina-mecanica
/domain.model oficina-mecanica
# → H2 → /arch.route
```

Tempo estimado humano+agente: 2–4 sessões de chat para MVP rico como a oficina.
