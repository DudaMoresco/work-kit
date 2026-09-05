#!/usr/bin/env bash
# Install domain-kit into architecture-hub (domain.install).
#
# Usage:
#   bash install-domain-kit.sh /path/to/architecture-hub
#
set -euo pipefail

HUB_ROOT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KIT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
COMMANDS_DIR="${KIT_ROOT}/templates/commands"
CURSOR_SKILLS="${HUB_ROOT}/.cursor/skills"
DOMAIN_DIR="${HUB_ROOT}/.domain"

if [[ ! -d "${COMMANDS_DIR}" ]]; then
  echo "domain-kit templates not found: ${COMMANDS_DIR}" >&2
  exit 1
fi

mkdir -p "${CURSOR_SKILLS}" "${DOMAIN_DIR}/scripts" "${DOMAIN_DIR}/clarify"

install_command_skill() {
  local template_name="$1"
  local skill_name="$2"
  local template_file="${COMMANDS_DIR}/${template_name}.md"
  local target_dir="${CURSOR_SKILLS}/${skill_name}"
  local target_file="${target_dir}/SKILL.md"

  [[ -f "${template_file}" ]] || return 0

  mkdir -p "${target_dir}"
  python3 - "${template_file}" "${target_file}" "${skill_name}" <<'PY'
import sys
from pathlib import Path

template_path, target_path, skill_name = sys.argv[1:4]
content = Path(template_path).read_text(encoding="utf-8")

if content.startswith("---"):
    end = content.find("\n---", 3)
    if end == -1:
        body = content
        frontmatter = f"name: {skill_name}\ndescription: Domain-kit {skill_name}\n"
    else:
        frontmatter = content[3:end].strip()
        body = content[end + 4 :].lstrip("\n")
        if "name:" not in frontmatter:
            frontmatter = f"name: {skill_name}\n{frontmatter}"
    output = f"---\n{frontmatter}\n---\n\n{body}"
else:
    output = f"---\nname: {skill_name}\ndescription: Domain-kit\n---\n\n{content}"

Path(target_path).write_text(output, encoding="utf-8")
PY
  echo "Installed ${target_file}"
}

# Meta + macro + micro commands
install_command_skill "domain-install" "domain-install"
for cmd in init scan clarify status discover model flow capability decision change; do
  install_command_skill "${cmd}" "domain-${cmd}"
done

# Pack skill (orchestrator)
mkdir -p "${CURSOR_SKILLS}/domain-kit"
cp "${KIT_ROOT}/SKILL.md" "${CURSOR_SKILLS}/domain-kit/SKILL.md"

# .domain scripts and config
cp "${KIT_ROOT}/scripts/"*.py "${DOMAIN_DIR}/scripts/"
cp "${KIT_ROOT}/scripts/regenerate_dashboard.sh" "${DOMAIN_DIR}/scripts/"
cp "${KIT_ROOT}/scripts/start_plantuml_server.sh" "${DOMAIN_DIR}/scripts/"
cp "${KIT_ROOT}/scripts/start_dashboard_server.sh" "${DOMAIN_DIR}/scripts/" 2>/dev/null || true
cp "${KIT_ROOT}/scripts/requirements.txt" "${DOMAIN_DIR}/scripts/" 2>/dev/null || true
# Dashboard HTML/CSS/JS templates (editáveis; sync → dashboard-assets/ na regeneração)
rm -rf "${DOMAIN_DIR}/scripts/dashboard" "${DOMAIN_DIR}/scripts/vendor"
cp -R "${KIT_ROOT}/scripts/dashboard" "${DOMAIN_DIR}/scripts/dashboard"
if [[ -d "${KIT_ROOT}/scripts/vendor" ]]; then
  cp -R "${KIT_ROOT}/scripts/vendor" "${DOMAIN_DIR}/scripts/vendor"
fi
chmod +x "${DOMAIN_DIR}/scripts/"*.py "${DOMAIN_DIR}/scripts/"*.sh 2>/dev/null || true

cp "${KIT_ROOT}/templates/config.yml" "${DOMAIN_DIR}/config.yml"
cp "${KIT_ROOT}/templates/clarify/"*.md "${DOMAIN_DIR}/clarify/"
# includes scan-discover.md (scan wizard Plan phase)

# Bundled know-how skills + wrappers (kit is self-contained; no ~/.cursor/skills dependency)
if [[ ! -d "${KIT_ROOT}/skills" ]]; then
  echo "domain-kit skills/ missing — clone completo do repo necessário" >&2
  exit 1
fi
rm -rf "${DOMAIN_DIR}/skills" "${DOMAIN_DIR}/wrappers"
cp -R "${KIT_ROOT}/skills" "${DOMAIN_DIR}/skills"
cp -R "${KIT_ROOT}/wrappers" "${DOMAIN_DIR}/wrappers"
echo "Installed .domain/skills/ and .domain/wrappers/"

# MCP status snapshot (best-effort)
MCP_STATUS="${DOMAIN_DIR}/mcp-status.json"
python3 - <<PY
import json
from datetime import datetime, timezone
from pathlib import Path

status = {
    "checkedAt": datetime.now(timezone.utc).isoformat(),
    "note": "Configure MCPs in Cursor Settings. GitHub used by domain.init and domain.scan.",
    "recommended": ["user-github", "user-plantuml"],
    "optional": ["user-Notion"],
    "manualFallback": ["gitlab via glab/imports", "confluence via exports"],
}
Path("${MCP_STATUS}").write_text(json.dumps(status, indent=2), encoding="utf-8")
print(f"Wrote ${MCP_STATUS}")
PY

echo ""
echo "Domain-kit installed in ${HUB_ROOT}"
echo "  .domain/skills/     # know-how DDD bundled"
echo "  .domain/wrappers/   # contratos de path/fase"
echo "  .domain/scripts/regenerate_dashboard.sh products/{produto}"
echo "  .domain/scripts/start_plantuml_server.sh  # PlantUML preview (porta 8765)"
echo "  Commands: /domain.install (done), /domain.init, /domain.scan, /domain.change, ..."
echo "  Docs: ${KIT_ROOT}/GUIDE.md"
echo ""
echo "Kit autossuficiente: skills DDD estão em .domain/skills/ (não usa ~/.cursor/skills)."
