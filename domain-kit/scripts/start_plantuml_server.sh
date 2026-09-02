#!/usr/bin/env bash
# Start a local PlantUML server for domain-kit dashboard preview.
#
# Default port 8765 (avoids collision with Spring Boot 8080, Vite 5173, etc.).
# Override: PLANTUML_PORT=9000 bash start_plantuml_server.sh
#
set -euo pipefail

PORT="${PLANTUML_PORT:-8765}"
CONTAINER_NAME="${PLANTUML_CONTAINER:-domain-kit-plantuml}"
IMAGE="${PLANTUML_IMAGE:-plantuml/plantuml-server:jetty}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker não encontrado. Instale Docker Desktop ou use PlantUML localmente." >&2
  echo "Docs: domain-kit/references/plantuml-dashboard.md" >&2
  exit 1
fi

if docker ps --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "PlantUML server já está rodando (container ${CONTAINER_NAME})."
  docker ps --filter "name=^${CONTAINER_NAME}$" --format '  {{.Ports}}'
  echo "URL: http://127.0.0.1:${PORT}"
  exit 0
fi

if docker ps -a --format '{{.Names}}' | grep -qx "${CONTAINER_NAME}"; then
  echo "Reiniciando container ${CONTAINER_NAME}..."
  docker start "${CONTAINER_NAME}" >/dev/null
else
  echo "Subindo PlantUML server (porta host ${PORT} → container 8080)..."
  docker run -d --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p "127.0.0.1:${PORT}:8080" \
    "${IMAGE}" >/dev/null
fi

echo "PlantUML server: http://127.0.0.1:${PORT}"
echo "Dashboard: regenere com regenerate_dashboard.sh e abra a aba Preview."
echo "Parar: docker stop ${CONTAINER_NAME}"
