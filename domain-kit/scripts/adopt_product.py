#!/usr/bin/env python3
"""Adopt an existing product in architecture-hub — generate missing indices and gap report."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TEMPLATES = [
    "sources.yml",
    "flows-registry.yml",
    "domain-status.json",
    "product-README.md",
    "CHANGELOG.md",
]


def substitute(text: str, product: str, initiative: str = "") -> str:
    return (
        text.replace("{produto}", product)
        .replace("{iniciativa}", initiative or "—")
        .replace("{status}", "pending")
    )


def ensure_indices(product_dir: Path, kit_root: Path, product: str, initiative: str) -> list[str]:
    created: list[str] = []
    templates_dir = kit_root / "templates"

    for name in TEMPLATES:
        dst = product_dir / name
        if dst.exists():
            continue
        src = templates_dir / name
        if not src.exists():
            continue
        text = substitute(src.read_text(encoding="utf-8"), product, initiative)
        dst.write_text(text, encoding="utf-8")
        created.append(str(dst.relative_to(product_dir)))

    registry = product_dir / "03-registry" / "produto.md"
    if not registry.exists():
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text(
            f"# Registry — {product}\n\n"
            "Decisões de produto (D-n). Preencher via `/domain.decision` e fluxos.\n\n"
            "| ID | Título | Status |\n| --- | --- | --- |\n| _(vazio)_ | — | — |\n",
            encoding="utf-8",
        )
        created.append(str(registry.relative_to(product_dir)))

    return created


def infer_initiative(hub: Path, product_dir: Path) -> str:
    readme = product_dir / "README.md"
    if readme.exists():
        m = re.search(r"iniciativa:\s*(\S+)", readme.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    initiatives = hub / "initiatives"
    if initiatives.is_dir():
        for d in sorted(initiatives.iterdir()):
            if d.is_dir():
                return d.name
    return ""


def update_status_from_gates(product_dir: Path, hub: Path, product: str) -> dict:
    script = hub / ".domain" / "scripts" / "validate_gate.py"
    status_path = product_dir / "domain-status.json"
    status: dict = {}
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))

    gates = {"G0": False, "G1": False, "G2": False}
    gate_issues: dict[str, list[str]] = {}

    if script.exists():
        for gate in ("G0", "G1", "G2"):
            proc = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--hub",
                    str(hub),
                    "--product",
                    product,
                    "--gate",
                    gate,
                    "--json",
                ],
                capture_output=True,
                text=True,
            )
            if proc.stdout.strip():
                data = json.loads(proc.stdout)
                gate_data = data.get("gates", data)
                gates[gate] = gate_data[gate]["pass"]
                gate_issues[gate] = gate_data[gate]["issues"]
    else:
        gate_issues = {"G0": ["validate_gate.py not installed — run /domain.install"]}

    status.setdefault("product", product)
    status["adoptedAt"] = datetime.now(timezone.utc).isoformat()
    status["gates"] = gates
    status["gateIssues"] = gate_issues

    if gates["G0"]:
        status["scan"] = status.get("scan") or "complete"
    if gates["G2"]:
        status["phase"] = "model_complete"
    elif gates["G1"]:
        status["phase"] = "discover_complete"
    elif gates["G0"]:
        status["phase"] = "init_complete"
    else:
        status["phase"] = "adopted"

    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return status


def suggest_next_command(
    gates: dict[str, bool], gate_issues: dict[str, list[str]], product_dir: Path | None = None
) -> str:
    if not gates.get("G0"):
        if any("scan not run" in i for i in gate_issues.get("G0", [])):
            return "/domain.init {produto}  # completar primeiro scan (G0)"
        return "/domain.init {produto}  # completar G0"
    if product_dir is not None:
        brief = product_dir / "01-product/00-scan/sintese-evidencias.md"
        if gates.get("G0") and not brief.is_file():
            return "/domain.init {produto}  # completar síntese (Fase 0c)"
    if not gates.get("G1"):
        return "/domain.discover {produto}  # lacunas (0b) + DDD — ou --mode minimal / as-is-first"
    if not gates.get("G2"):
        issues = gate_issues.get("G2", [])
        if any("design-tatico" in i for i in issues):
            return "/domain.capability {bc}  # tático pendente"
        if any("fluxo" in i.lower() or "flows" in i.lower() for i in issues):
            return "/domain.flow {NN}  # fluxo pendente"
        return "/domain.model --finalize  # fechar G2"
    return "/arch.route  # G2 ok — handoff arch-kit"


def inventory_existing(product_dir: Path) -> dict:
    inv: dict = {"paths": [], "capabilities": [], "fluxos": 0}
    for p in sorted(product_dir.rglob("*")):
        if p.is_file() and ".draft" not in p.parts:
            rel = str(p.relative_to(product_dir))
            inv["paths"].append(rel)
    cap_root = product_dir / "02-capabilities"
    if cap_root.is_dir():
        inv["capabilities"] = [
            d.name for d in cap_root.iterdir() if d.is_dir() and not d.name.startswith(".")
        ]
        inv["fluxos"] = len(list(cap_root.rglob("fluxos/*.md")))
    return inv


def main() -> int:
    parser = argparse.ArgumentParser(description="Adopt existing product — indices + gap report")
    parser.add_argument("--hub", type=Path, default=Path.cwd(), help="Hub root")
    parser.add_argument("--product", required=True, help="Product slug")
    parser.add_argument("--initiative", default="", help="Initiative slug (optional)")
    parser.add_argument("--kit-root", type=Path, default=None, help="domain-kit root for templates")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    hub = args.hub.resolve()
    product_dir = hub / "products" / args.product
    if not product_dir.is_dir():
        print(f"Product not found: {product_dir}", file=sys.stderr)
        return 2

    kit_root = args.kit_root
    if kit_root is None:
        cfg = hub / ".domain" / "config.yml"
        if cfg.exists() and "skills_pack:" in cfg.read_text(encoding="utf-8"):
            for line in cfg.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("skills_pack:"):
                    rel = line.split(":", 1)[1].strip()
                    kit_root = (hub / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
                    break
        if kit_root is None or not kit_root.is_dir():
            kit_root = hub.parent / "work-kit" / "domain-kit"
        if not kit_root.is_dir():
            kit_root = Path(__file__).resolve().parent.parent

    initiative = args.initiative or infer_initiative(hub, product_dir)
    created = ensure_indices(product_dir, kit_root, args.product, initiative)
    inventory = inventory_existing(product_dir)
    status = update_status_from_gates(product_dir, hub, args.product)
    next_cmd = suggest_next_command(
        status.get("gates", {}), status.get("gateIssues", {}), product_dir
    )

    report = {
        "product": args.product,
        "initiative": initiative,
        "indicesCreated": created,
        "inventory": inventory,
        "gates": status.get("gates"),
        "gateIssues": status.get("gateIssues"),
        "suggestedNextCommand": next_cmd.replace("{produto}", args.product),
        "phase": status.get("phase"),
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Adopted: {args.product}")
        if created:
            print("Indices created:")
            for c in created:
                print(f"  + {c}")
        else:
            print("Indices: all present")
        print(f"Capabilities found: {', '.join(inventory['capabilities']) or '(none)'}")
        print(f"Fluxos found: {inventory['fluxos']}")
        for g in ("G0", "G1", "G2"):
            ok = status.get("gates", {}).get(g, False)
            print(f"{g}: {'PASS' if ok else 'FAIL'}")
            for issue in status.get("gateIssues", {}).get(g, []):
                print(f"  - {issue}")
        print(f"Suggested next: {report['suggestedNextCommand']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
