#!/usr/bin/env bash
# Serve the architecture hub over HTTP so dashboard.html renders in Cursor/VS Code.
# file:// and webviews often block scripts under hidden folders (.domain/).
#
# Usage: .domain/scripts/start_dashboard_server.sh
# Override: DASHBOARD_PORT=8766 bash start_dashboard_server.sh

set -euo pipefail

HUB_ROOT="${DOMAIN_HUB_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
PORT="${DASHBOARD_PORT:-8766}"

if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:"${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Dashboard server já está rodando na porta ${PORT}."
else
  echo "Subindo servidor HTTP na porta ${PORT} (hub: ${HUB_ROOT})..."
  python3 -m http.server "${PORT}" --directory "${HUB_ROOT}" >/dev/null 2>&1 &
  sleep 0.4
fi

echo ""
echo "Abra no Cursor:"
echo "  Cmd+Shift+P → Simple Browser: Show"
echo "  http://127.0.0.1:${PORT}/dashboard.html"
echo ""
echo "Produto:"
echo "  http://127.0.0.1:${PORT}/products/notificacao-dividas-pendencias/dashboard.html"
echo ""
echo "Para parar: kill \$(lsof -t -iTCP:${PORT} -sTCP:LISTEN)"
