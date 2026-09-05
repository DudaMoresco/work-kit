#!/usr/bin/env python3
"""Ensure draft workspace, update manifest, regenerate dashboard — visibility during init/scan."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def substitute(text: str, product: str) -> str:
    return text.replace("{produto}", product)


def ensure_draft_workspace(product_dir: Path, kit_root: Path, product: str) -> list[str]:
    created: list[str] = []
    draft_dir = product_dir / ".draft"
    draft_dir.mkdir(parents=True, exist_ok=True)
    templates = kit_root / "templates"

    for name, template_name in (
        ("README.md", "draft-README.md"),
        ("manifest.json", "draft-manifest.json"),
    ):
        dst = draft_dir / name
        if dst.exists():
            continue
        src = templates / template_name
        if not src.exists():
            continue
        text = substitute(src.read_text(encoding="utf-8"), product)
        dst.write_text(text, encoding="utf-8")
        created.append(f".draft/{name}")

    return created


def register_pending(
    product_dir: Path,
    product: str,
    draft_path: str,
    target_path: str,
    command: str,
) -> None:
    manifest_path = product_dir / ".draft" / "manifest.json"
    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    else:
        data = {"product": product, "updatedAt": None, "pending": []}

    data["product"] = product
    draft_norm = draft_path if draft_path.startswith(".draft/") else f".draft/{draft_path.lstrip('/')}"
    pending = data.get("pending", [])
    pending = [e for e in pending if e.get("targetPath") != target_path]
    pending.append(
        {
            "draftPath": draft_norm,
            "targetPath": target_path,
            "command": command,
            "status": "awaiting_approval",
        }
    )
    data["pending"] = pending
    data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def list_draft_files(product_dir: Path) -> list[str]:
    draft_root = product_dir / ".draft"
    if not draft_root.is_dir():
        return []
    out: list[str] = []
    for p in sorted(draft_root.rglob("*")):
        if p.is_file() and p.name not in ("manifest.json", "README.md"):
            out.append(p.relative_to(product_dir).as_posix())
    return out


def regenerate_dashboard(hub: Path, product: str) -> bool:
    script = Path(__file__).resolve().parent / "generate_domain_dashboard.py"
    r = subprocess.run(
        [sys.executable, str(script), "--hub", str(hub), "--product", product],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0 and r.stderr:
        print(r.stderr, file=sys.stderr)
    return r.returncode == 0


def visibility_summary(hub: Path, product: str, product_dir: Path) -> dict:
    dashboard = product_dir / "dashboard.html"
    hub_dashboard = hub / "dashboard.html"
    changelog = product_dir / "CHANGELOG.md"
    manifest = product_dir / ".draft" / "manifest.json"
    pending = 0
    if manifest.exists():
        try:
            pending = len(json.loads(manifest.read_text(encoding="utf-8")).get("pending", []))
        except json.JSONDecodeError:
            pending = 0
    drafts = list_draft_files(product_dir)
    return {
        "product": product,
        "dashboard": str(dashboard.relative_to(hub)) if dashboard.exists() else None,
        "hubDashboard": str(hub_dashboard.relative_to(hub)) if hub_dashboard.exists() else None,
        "changelog": str(changelog.relative_to(hub)) if changelog.exists() else None,
        "draftDir": f"products/{product}/.draft/",
        "draftFiles": drafts,
        "pendingPromotes": pending,
    }


def print_visibility_markdown(summary: dict) -> None:
    print("\n## Visibilidade do workspace\n")
    if summary.get("dashboard"):
        print(f"- **Dashboard:** `{summary['dashboard']}` (aba **Rascunhos**)")
    if summary.get("hubDashboard"):
        print(f"- **Índice hub:** `{summary['hubDashboard']}`")
    if summary.get("changelog"):
        print(f"- **Changelog:** `{summary['changelog']}`")
    print(f"- **Pasta rascunhos:** `{summary['draftDir']}`")
    if summary.get("draftFiles"):
        print("- **Arquivos em .draft/:**")
        for f in summary["draftFiles"]:
            print(f"  - `{f}`")
    else:
        print("- **Arquivos em .draft/:** _(nenhum ainda)_")
    n = summary.get("pendingPromotes", 0)
    if n:
        print(f"- **Promotes pendentes (manifest):** {n}")


def resolve_kit_root(hub: Path) -> Path:
    env = os.environ.get("DOMAIN_KIT_ROOT")
    if env:
        candidate = Path(env).expanduser().resolve()
        if candidate.is_dir():
            return candidate
    cfg = hub / ".domain" / "config.yml"
    if cfg.exists():
        for line in cfg.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("skills_pack:"):
                rel = line.split(":", 1)[1].strip()
                candidate = (hub / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
                if candidate.is_dir():
                    return candidate
    return Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync draft workspace + dashboard visibility")
    parser.add_argument("--hub", type=Path, default=Path.cwd())
    parser.add_argument("--product", required=True)
    parser.add_argument("--register", action="append", default=[], metavar="DRAFT:TARGET:CMD")
    parser.add_argument("--no-dashboard", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    hub = args.hub.resolve()
    product = args.product
    product_dir = hub / "products" / product
    if not product_dir.is_dir():
        print(f"Product not found: {product_dir}", file=sys.stderr)
        return 2

    kit_root = resolve_kit_root(hub)
    created = ensure_draft_workspace(product_dir, kit_root, product)

    for spec in args.register:
        parts = spec.split(":", 2)
        if len(parts) != 3:
            print(f"Invalid --register (use draft:target:command): {spec}", file=sys.stderr)
            return 2
        register_pending(product_dir, product, parts[0], parts[1], parts[2])

    dashboard_ok = True
    if not args.no_dashboard:
        dashboard_ok = regenerate_dashboard(hub, product)

    summary = visibility_summary(hub, product, product_dir)
    summary["scaffoldCreated"] = created
    summary["dashboardRegenerated"] = dashboard_ok and not args.no_dashboard

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        if created:
            print("Scaffold criado:", ", ".join(created))
        print_visibility_markdown(summary)

    return 0 if dashboard_ok else 1


if __name__ == "__main__":
    sys.exit(main())
