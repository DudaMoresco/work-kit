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

PHASE_ORDER = ["evidencias", "estrategico", "descoberta", "operacional"]


def substitute(text: str, product: str, initiative: str = "") -> str:
    return (
        text.replace("{produto}", product)
        .replace("{iniciativa}", initiative or "—")
        .replace("{status}", "pending")
    )


def ensure_indices(product_dir: Path, kit_root: Path, product: str, initiative: str) -> list[str]:
    created: list[str] = []
    templates_dir = kit_root / "templates"
    if not templates_dir.is_dir():
        templates_dir = Path(__file__).resolve().parent.parent / "templates"

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

    op_fluxos = product_dir / "01-product/03-operacional/fluxos"
    if not op_fluxos.is_dir():
        op_fluxos.mkdir(parents=True, exist_ok=True)
        created.append(str(op_fluxos.relative_to(product_dir)))

    evolucoes = product_dir / "01-product/02-domain/evolucoes.md"
    if not evolucoes.exists():
        evolucoes.parent.mkdir(parents=True, exist_ok=True)
        tpl_evo = templates_dir / "evolucoes.md"
        if tpl_evo.exists():
            text_evo = substitute(tpl_evo.read_text(encoding="utf-8"), product, initiative)
        else:
            text_evo = (
                f"# Evoluções de produto — {product}\n\n"
                "Mudanças intencionais (E-n). Abrir via `/domain.change --kind evolution`.\n"
            )
        evolucoes.write_text(text_evo, encoding="utf-8")
        created.append(str(evolucoes.relative_to(product_dir)))

    return created


def infer_initiative(hub: Path, product_dir: Path) -> str:
    for name in ("product-README.md", "README.md"):
        readme = product_dir / name
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


def detect_arch_legacy(product_dir: Path) -> dict:
    """Mark design-tatico and integration docs adopted by arch-kit without blocking domain phases."""
    arch: dict = {"capabilitiesAdopted": [], "integrationAdopted": False}
    cap_root = product_dir / "02-capabilities"
    if cap_root.is_dir():
        for bc_dir in sorted(cap_root.iterdir()):
            if bc_dir.is_dir() and (bc_dir / "design-tatico.md").is_file():
                arch["capabilitiesAdopted"].append(bc_dir.name)
    arch_path = product_dir / "arch/01-integration/01-contextos.md"
    legacy_path = product_dir / "01-product/04-integration/01-contextos.md"
    if arch_path.is_file():
        arch["integrationAdopted"] = True
    elif legacy_path.is_file() and "arch-kit" not in legacy_path.read_text(encoding="utf-8")[:200]:
        # Legacy full integration doc still at old path — migrate hint only
        arch["integrationLegacyPath"] = str(legacy_path.relative_to(product_dir))
    return arch


def update_status_from_phases(product_dir: Path, hub: Path, product: str) -> dict:
    script = hub / ".domain" / "scripts" / "validate_gate.py"
    status_path = product_dir / "domain-status.json"
    status: dict = {}
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))

    results: dict[str, dict] = {}
    if script.exists():
        proc = subprocess.run(
            [
                sys.executable,
                str(script),
                "--hub",
                str(hub),
                "--product",
                product,
                "--json",
            ],
            capture_output=True,
            text=True,
        )
        if proc.stdout.strip():
            data = json.loads(proc.stdout)
            results = data.get("phases", {})

    phases_pass = {p: results.get(p, {}).get("pass", False) for p in PHASE_ORDER}
    phase_issues = {p: results.get(p, {}).get("issues", []) for p in PHASE_ORDER}

    status.setdefault("product", product)
    status["adoptedAt"] = datetime.now(timezone.utc).isoformat()
    status["phases"] = phases_pass
    status["phaseIssues"] = phase_issues
    status["gates"] = {
        "G0": phases_pass.get("evidencias", False),
        "G1": phases_pass.get("estrategico", False) and phases_pass.get("descoberta", False),
        "G2": phases_pass.get("operacional", False),
    }
    status["gateIssues"] = {
        "G0": phase_issues.get("evidencias", []),
        "G1": phase_issues.get("estrategico", []) + phase_issues.get("descoberta", []),
        "G2": phase_issues.get("operacional", []),
    }

    arch = detect_arch_legacy(product_dir)
    status.setdefault("arch", {}).update(arch)

    if phases_pass.get("operacional"):
        status["phase"] = "domain-complete"
    elif phases_pass.get("descoberta") and phases_pass.get("estrategico"):
        status["phase"] = "operacional-in-progress"
    elif phases_pass.get("estrategico"):
        status["phase"] = "descoberta-in-progress"
    elif phases_pass.get("evidencias"):
        status["phase"] = "estrategico-in-progress"
    else:
        status["phase"] = "evidencias"

    if phases_pass.get("evidencias"):
        status["scan"] = status.get("scan") or "complete"

    if script.exists() and proc.stdout.strip():
        status["nextSuggested"] = json.loads(proc.stdout).get("suggestedNextCommand", status.get("nextSuggested"))

    status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return status


def suggest_next_command(status: dict) -> str:
    return status.get("nextSuggested", "/domain.status")


def inventory_existing(product_dir: Path) -> dict:
    inv: dict = {"paths": [], "capabilities": [], "fluxos": 0, "arch": []}
    for p in sorted(product_dir.rglob("*")):
        if p.is_file() and ".draft" not in p.parts:
            rel = str(p.relative_to(product_dir))
            inv["paths"].append(rel)
    cap_root = product_dir / "02-capabilities"
    if cap_root.is_dir():
        inv["capabilities"] = [
            d.name for d in cap_root.iterdir() if d.is_dir() and not d.name.startswith(".")
        ]
    op_dir = product_dir / "01-product/03-operacional/fluxos"
    inv["fluxos"] = len(list(op_dir.glob("*.md"))) if op_dir.is_dir() else 0
    inv["fluxos"] += len(list(cap_root.rglob("fluxos/*.md"))) if cap_root.is_dir() else 0
    arch_root = product_dir / "arch"
    if arch_root.is_dir():
        inv["arch"] = [str(p.relative_to(product_dir)) for p in arch_root.rglob("*.md")]
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
    status = update_status_from_phases(product_dir, hub, args.product)
    next_cmd = suggest_next_command(status)

    report = {
        "product": args.product,
        "initiative": initiative,
        "indicesCreated": created,
        "inventory": inventory,
        "phases": status.get("phases"),
        "phaseIssues": status.get("phaseIssues"),
        "gates": status.get("gates"),
        "gateIssues": status.get("gateIssues"),
        "arch": status.get("arch"),
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
        print(f"Capabilities (arch legacy): {', '.join(inventory['capabilities']) or '(none)'}")
        print(f"Fluxos found: {inventory['fluxos']}")
        if inventory.get("arch"):
            print(f"Arch artifacts: {len(inventory['arch'])}")
        for p in PHASE_ORDER:
            ok = status.get("phases", {}).get(p, False)
            print(f"{p}: {'PASS' if ok else 'FAIL'}")
            for issue in status.get("phaseIssues", {}).get(p, []):
                print(f"  - {issue}")
        print(f"Suggested next: {report['suggestedNextCommand']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
