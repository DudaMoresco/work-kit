# Wrapper: ddd-design-tatico

**Skill:** [`skills/ddd-design-tatico/SKILL.md`](../skills/ddd-design-tatico/SKILL.md) (bundled para referência / handoff arch-kit).

**Invocada por:** `/arch.capability {bc}` (quando arch-kit instalado). **`/domain.capability` está deprecated.**

**Outputs no hub (arch-kit):**
- `products/{produto}/arch/{bc}/design-tatico.md`
- `products/{produto}/arch/{bc}/README.md`

**Legado:** `02-capabilities/{bc}/design-tatico.md` — marcado em `domain-status.json` → `arch.capabilitiesAdopted`; não bloqueia fase Operacional.

**Domain-kit:** agregados podem aparecer apenas como resultado visual de **event storming** (post-it), sem camadas nem código.
