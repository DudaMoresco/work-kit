# Wrapper: ddd-linguagem-e-contextos

**Skill:** [`skills/ddd-linguagem-e-contextos/SKILL.md`](../skills/ddd-linguagem-e-contextos/SKILL.md) (bundled).

**Invocada por:** `/domain.discover` (fechamento discover)

**Pré-condições:** discovery parcial ou completo

**Outputs no hub:**
- `products/{produto}/01-product/02-domain/desafio-negocio.md`
- `products/{produto}/01-product/02-domain/linguagem-ubiqua.md`
- `products/{produto}/01-product/02-domain/bounded-contexts.md`

**Pós-execução:** validar fases **Estratégico** e **Descoberta** (`validate_gate.py --phase estrategico|descoberta`)
