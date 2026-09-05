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

**Fase Estratégico + Descoberta:** PASS — BCs fechados, discovery rico.

---

## `/domain.model` — o que foi produzido

### 1. Integração entre BCs (mapa de negócio)

Decisão estrutural **D-16:**

```text
Orçamento NÃO chama Estoque diretamente.
OS orquestra: aprovação → Reservar → retirada → Baixar → Liberar.
```

Sem este alinhamento, o design de cada BC fica inconsistente. Detalhe técnico de ACL/protocolos fica **fora do escopo do domain-kit**.

### 2. Requisitos

**Arquivo:** `01-product/04-operacional/requisitos.md`

RF/RNF derivados dos fluxos e enunciado (inclui D-36 observabilidade depois).

Owned pelo domain-kit na fase Operacional.

### 3. Design tático por BC

Design tático por BC fica **fora do escopo do domain-kit** (próxima etapa técnica). Neste exemplo histórico, havia notas por BC (ordem-de-servico, orcamento, estoque, cadastros, acesso) ligadas a decisões D-n — úteis como referência de negócio, não como entrega deste kit.

### 4. Fluxos entregáveis (7)

Path: `01-product/04-operacional/fluxos/{NN}-{slug}.md`.

Distribuídos por BC, numerados **01–07** para rastreio:

| fluxo | BC principal | Arquivo |
| --- | --- | --- |
| 01 | ordem-de-servico | `01-product/04-operacional/fluxos/01-identificacao-e-abertura-os.md` |
| 02 | orcamento | `01-product/04-operacional/fluxos/02-orcamento-inicial.md` |
| 03 | orcamento | `01-product/04-operacional/fluxos/03-decisao-orcamento.md` |
| 04 | estoque | `01-product/04-operacional/fluxos/04-retirada-e-baixa.md` |
| 05 | ordem-de-servico | `01-product/04-operacional/fluxos/05-aguardando-item.md` |
| 06 | orcamento | `01-product/04-operacional/fluxos/06-orcamento-complementar.md` |
| 07 | ordem-de-servico | `01-product/04-operacional/fluxos/07-finalizar-e-entregar.md` |

IDs estáveis `fluxo-01`…`fluxo-07` facilitam rastreio em etapas posteriores (fora deste kit).

### 5. Orquestração de negócio

Coordenação entre BCs (ex.: “Abrir OS”, “Executar fluxo 02”) fica descrita nos próprios fluxos e em D-n — não em pasta técnica.

### 6. Registry produto

**Arquivo:** `05-decisoes/produto.md`

33 decisões D-01…D-33, cada uma com:
- capability
- status (`aceita`)
- texto da decisão
- **link** para evidência (fluxo, ES, discovery)

Exemplo **D-03** (bloquear OS duplicada para mesmo veículo):
- Evidência: `01-product/04-operacional/fluxos/` / discovery do BC ordem-de-servico
- Impacto: invariante no agregado OrdemDeServico

**Fase Operacional:** passou em 2026-08-23 — fim do pipeline domain-kit neste exemplo.

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
    │                    Estratégico+Descoberta ✓    │
    ├─ model ────────────────────────────────────────┤
    │   requisitos RF/RNF                            │
    │   fluxos 01–07                                 │
    │   registry D-01…33                             │
    │                    Operacional ✓               │
    └────────────────────────────────────────────────┘
```

---

## Lições para replicar

1. **ES em workshops pequenos** — mais fácil de manter que 1 diagrama gigante.
2. **D-n cedo** — toda regra polêmica vira linha no registry com link.
3. **Alinhar integração de negócio antes do detalhe técnico** — D-16 evitou acoplamento Orçamento↔Estoque.
4. **Numerar fluxos 01–NN** — IDs estáveis para rastreio (`fluxo-01`, …).
5. **Requisitos em `04-operacional/requisitos.md`** — domain-kit entrega NFR na fase Operacional.

---

## Se refizesse com domain-kit desde o zero

Ordem sugerida pelo kit (igual ao que aconteceu na prática):

```bash
/domain.install
# install: domain-kit/scripts/install-domain-kit.sh /caminho/do/hub
/domain.init oficina-mecanica --initiative tech-challenge-fase1
/domain.discover oficina-mecanica
/domain.model oficina-mecanica --finalize
# → Operacional PASS — fim do domain-kit
```

Tempo estimado humano+agente: 2–4 sessões de chat para MVP rico como a oficina.
