#!/usr/bin/env bash
# Bootstrap domain-kit test-hub — sandbox local para validar skills/wrappers/templates.
#
# Usage:
#   bash bootstrap-test-hub.sh           # install + demo product
#   bash bootstrap-test-hub.sh --clean   # wipe generated dirs and reinstall
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEST_HUB="${KIT_ROOT}/test-hub"
PRODUCT="demo-produto"
INITIATIVE="demo-iniciativa"

CLEAN=false
for arg in "$@"; do
  case "${arg}" in
    --clean) CLEAN=true ;;
    -h|--help)
      echo "Usage: bootstrap-test-hub.sh [--clean]"
      exit 0
      ;;
  esac
done

if [[ "${CLEAN}" == true ]]; then
  echo "Cleaning ${TEST_HUB} generated content..."
  rm -rf "${TEST_HUB}/.cursor" "${TEST_HUB}/.domain" "${TEST_HUB}/products" "${TEST_HUB}/dashboard.html" "${TEST_HUB}/MANIFEST.md"
fi

mkdir -p "${TEST_HUB}"

echo "==> Installing domain-kit into test-hub"
bash "${SCRIPT_DIR}/install-domain-kit.sh" "${TEST_HUB}"

# skills_pack: test-hub lives inside domain-kit — point to parent package
CONFIG="${TEST_HUB}/.domain/config.yml"
python3 - <<PY
from pathlib import Path

path = Path("${CONFIG}")
text = path.read_text(encoding="utf-8")
text = text.replace("skills_pack: ../work-kit/domain-kit", "skills_pack: ..")
text = text.replace("# Monorepo work-hub: ../work-kit/domain-kit", "# test-hub sandbox: ..")
if "skills_pack: .." not in text:
    raise SystemExit("config.yml patch failed — unexpected format")
path.write_text(text, encoding="utf-8")
print(f"Patched {path}")
PY

# Demo initiative (manual source for domain.scan wizard)
INIT_DIR="${TEST_HUB}/initiatives/${INITIATIVE}"
mkdir -p "${INIT_DIR}"
cat > "${INIT_DIR}/01-enunciado.md" <<'MD'
# Enunciado demo — domain-kit test-hub

Produto fictício **Biblioteca Comunitária** para validar o pipeline domain-kit.

## Escopo MVP

- Cadastro de membros e empréstimo de exemplares
- Reserva de título indisponível
- Multa por atraso na devolução
- Painel do bibliotecário (JWT)

## Fora do MVP

- Integração com ERP municipal
- App mobile nativo

## Bounded contexts sugeridos (rascunho)

1. **Empréstimo** — ciclo reserva → retirada → devolução
2. **Acervo** — exemplares, cópias, disponibilidade
3. **Membro** — cadastro e situação (adimplência)
4. **Acesso** — autenticação bibliotecário

_Use este arquivo como fonte manual na fase 0 de `/domain.init`._
MD

# Demo product — lazy init (indices only)
PRODUCT_DIR="${TEST_HUB}/products/${PRODUCT}"
mkdir -p "${PRODUCT_DIR}/03-registry"

substitute_template() {
  local src="$1"
  local dst="$2"
  python3 - "${src}" "${dst}" "${PRODUCT}" "${INITIATIVE}" <<'PY'
import sys
from pathlib import Path

src, dst, product, initiative = sys.argv[1:5]
text = Path(src).read_text(encoding="utf-8")
text = text.replace("{produto}", product).replace("{iniciativa}", initiative).replace("{status}", "pending")
Path(dst).write_text(text, encoding="utf-8")
PY
}

substitute_template "${KIT_ROOT}/templates/sources.yml" "${PRODUCT_DIR}/sources.yml"
substitute_template "${KIT_ROOT}/templates/flows-registry.yml" "${PRODUCT_DIR}/flows-registry.yml"

# Fonte manual pré-configurada — init testável sem MCP externo (GitHub/GitLab)
python3 - <<PY
from pathlib import Path

path = Path("${PRODUCT_DIR}/sources.yml")
text = path.read_text(encoding="utf-8")
needle = "  manual: []\n  # - path: initiatives/${INITIATIVE}/01-enunciado.md\n  #   purpose: enunciado oficial"
replacement = (
    "  manual:\n"
    "  - path: initiatives/${INITIATIVE}/01-enunciado.md\n"
    "    purpose: enunciado oficial (Biblioteca Comunitária — test-hub demo)"
)
if needle not in text:
    raise SystemExit("sources.yml patch failed — unexpected format")
path.write_text(text.replace(needle, replacement), encoding="utf-8")
print(f"Wired manual source in {path}")
PY
substitute_template "${KIT_ROOT}/templates/domain-status.json" "${PRODUCT_DIR}/domain-status.json"
substitute_template "${KIT_ROOT}/templates/product-README.md" "${PRODUCT_DIR}/product-README.md"

# Registry stub
cat > "${PRODUCT_DIR}/03-registry/produto.md" <<MD
# Registry — ${PRODUCT}

Decisões de produto (D-n). Preencher via \`/domain.decision\` e fluxos.

| ID | Título | Status |
| --- | --- | --- |
| _(vazio)_ | — | — |
MD

echo "==> Regenerating dashboard"
DOMAIN_HUB_ROOT="${TEST_HUB}" bash "${TEST_HUB}/.domain/scripts/regenerate_dashboard.sh" "${PRODUCT}"

# Manifest for diff inspection
MANIFEST="${TEST_HUB}/MANIFEST.md"
{
  echo "# Test-hub manifest"
  echo ""
  echo "Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo ""
  echo "## Skills instaladas"
  echo ""
  find "${TEST_HUB}/.cursor/skills" -name 'SKILL.md' 2>/dev/null | sort | while read -r f; do
    rel="${f#${TEST_HUB}/}"
    echo "- \`${rel}\`"
  done
  echo ""
  echo "## Wrappers + skills bundled"
  echo ""
  if [[ -d "${TEST_HUB}/.domain/skills" ]]; then
    echo "Skills em \`.domain/skills/\`:"
    find "${TEST_HUB}/.domain/skills" -mindepth 1 -maxdepth 1 -type d | sort | while read -r d; do
      echo "- \`$(basename "${d}")\`"
    done
  else
    echo "_(missing .domain/skills)_"
  fi
  echo ""
  if [[ -d "${TEST_HUB}/.domain/wrappers" ]]; then
    find "${TEST_HUB}/.domain/wrappers" -maxdepth 1 -name '*.md' | sort | while read -r f; do
      echo "- \`.domain/wrappers/$(basename "${f}")\`"
    done
  else
    echo "_(missing .domain/wrappers)_"
  fi
  echo ""
  echo "## Produto demo"
  echo ""
  find "${TEST_HUB}/products/${PRODUCT}" -type f 2>/dev/null | sort | while read -r f; do
    rel="${f#${TEST_HUB}/}"
    echo "- \`${rel}\`"
  done
} > "${MANIFEST}"

echo ""
echo "Test-hub ready: ${TEST_HUB}"
echo "  Open folder in Cursor: ${TEST_HUB}"
echo "  Dashboard: products/${PRODUCT}/dashboard.html"
echo "  Manifest: MANIFEST.md"
echo "  First commands: /domain.init demo-produto  (Evidências)  then  /domain.discover"
echo ""
echo "Edit domain-kit templates/wrappers, then re-run:"
echo "  bash domain-kit/scripts/bootstrap-test-hub.sh"
