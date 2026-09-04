#!/usr/bin/env bash
# Regenerate domain-kit dashboard for a product (and hub index).
set -euo pipefail

HUB_ROOT="${DOMAIN_HUB_ROOT:-$(pwd)}"
PRODUCT="${1:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEN="${SCRIPT_DIR}/generate_domain_dashboard.py"

if [[ -z "${PRODUCT}" ]]; then
  echo "Usage: regenerate_dashboard.sh products/{produto-slug}" >&2
  echo "  or:  regenerate_dashboard.sh {produto-slug}" >&2
  exit 1
fi

# Accept products/foo or foo
PRODUCT="${PRODUCT#products/}"

python3 "${GEN}" --hub "${HUB_ROOT}" --product "${PRODUCT}"
