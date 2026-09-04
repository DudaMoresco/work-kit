# Wrapper: fluxos operacionais (domain-kit + arch-kit)

**Invocada por:** `/domain.flow {NN}`

**Pré-condições:** deps de fluxo satisfeitas (`flow_deps.py`); fases Estratégico + Descoberta PASS

## Camada negócio (domain-kit — obrigatória)

- `products/{produto}/01-product/03-operacional/fluxos/{NN}-{slug}.md`
- Template: `templates/fluxo-operacional.md`
- Linguagem ubíqua; referências técnicas só em nota "as-is" opcional

## Camada técnica (arch-kit — opcional)

- `products/{produto}/arch/fluxos/{NN}-{slug}-tecnico.md`
- Sequência de serviços, filas, payloads, idempotência

## Registry

- Atualizar `flows-registry.yml` — `path` aponta para fluxo **operacional** (negócio)
- Status `ready` quando camada negócio promovida e validada

**Pós-execução:** regenerate dashboard; sugerir próximo fluxo desbloqueado
