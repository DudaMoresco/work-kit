# Wrapper: ddd-design-estrategico

**Skill:** [`skills/ddd-design-estrategico/SKILL.md`](../skills/ddd-design-estrategico/SKILL.md) (bundled).

**Invocada por:** `/domain.discover` (etapa estratégico)

**Pré-condições:** `domain.init` feito; enunciado ou scan disponível; `{produto}` confirmado

**Inputs:** narrativa de negócio, enunciado, achados do scan (opcional)

**Outputs no hub:**
- `products/{produto}/01-product/01-vision/01-design-estrategico.md`

**Pós-execução:** marcar `discover.estrategico: ready` em `domain-status.json`; regenerate dashboard

**Handoff:** subdomínios classificados → próximo passo stories ou ES no mesmo discover
