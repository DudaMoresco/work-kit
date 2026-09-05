# Wrapper: fluxos operacionais

**Skills:**
- [`skills/fluxos-entregaveis/SKILL.md`](../skills/fluxos-entregaveis/SKILL.md) — know-how de fluxos to-be
- [`skills/fluxogramas-decisao/SKILL.md`](../skills/fluxogramas-decisao/SKILL.md) — as-is (`discover --mode as-is-first` → `03-discovery/00-as-is/`)

**Invocada por:** `/domain.flow {NN}`

**Pré-condições:** deps de fluxo satisfeitas (`flow_deps.py`); fases Estratégico + Descoberta PASS

## Camada negócio (domain-kit — obrigatória)

- `products/{produto}/01-product/04-operacional/fluxos/{NN}-{slug}.md`
- Template: `templates/fluxo-operacional.md`
- Linguagem ubíqua; referências técnicas só em nota "as-is" opcional

## Camada técnica (fora do escopo do domain-kit — opcional)

- `products/{produto}/arch/fluxos/{NN}-{slug}-tecnico.md`
- Sequência de serviços, filas, payloads, idempotência

## Registry

- Atualizar `flows-registry.yml` — `path` aponta para fluxo **operacional** (negócio) sob `04-operacional/fluxos/`
- Status `ready` quando camada negócio promovida e validada

**Pós-execução:** regenerate dashboard; sugerir próximo fluxo desbloqueado
