#!/usr/bin/env python3
"""Validate domain-kit gates G0, G1, G2 for a product in architecture-hub."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

GATES = {
    "G0": {
        "name": "Scan",
        "optional": True,
        "paths": [],
    },
    "G1": {
        "name": "Discover complete",
        "paths": [
            "01-product/01-vision/01-design-estrategico.md",
            "01-product/02-domain/bounded-contexts.md",
            "01-product/02-domain/desafio-negocio.md",
            "01-product/02-domain/linguagem-ubiqua.md",
        ],
        "one_of_dirs": [
            "01-product/03-discovery/01-event-storming",
            "01-product/03-discovery/02-domain-storytelling",
        ],
    },
    "G2": {
        "name": "Model complete",
        "paths": [
            "01-product/04-integration/01-contextos.md",
            "04-platform/01-non-functional/01-requisitos.md",
            "03-registry/produto.md",
        ],
        "capabilities": True,
        "fluxos_min": 1,
    },
}


def check_g0(product_dir: Path, status: dict) -> tuple[bool, list[str]]:
    issues: list[str] = []
    scan_dir = product_dir / "01-product/00-scan"
    scan_status = status.get("scan", "pending")
    sources = product_dir / "sources.yml"
    if not sources.exists():
        issues.append("sources.yml missing (optional)")
        return True, issues
    if scan_status in ("complete", "partial", "skipped"):
        return True, issues
    if scan_dir.exists() and (scan_dir / "scan-manifest.json").exists():
        return True, issues
    issues.append("scan not run — run /domain.scan or set scan: skipped in domain-status.json")
    return False, issues


def check_paths(product_dir: Path, rel_paths: list[str]) -> list[str]:
    missing = []
    for rel in rel_paths:
        if not (product_dir / rel).exists():
            missing.append(rel)
    return missing


def check_one_of_dirs(product_dir: Path, dirs: list[str]) -> bool:
    for d in dirs:
        p = product_dir / d
        if p.is_dir() and any(p.iterdir()):
            return True
    return False


def check_capabilities(product_dir: Path) -> list[str]:
    issues: list[str] = []
    cap_root = product_dir / "02-capabilities"
    if not cap_root.is_dir():
        return ["02-capabilities/ missing"]
    bcs = [d for d in cap_root.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not bcs:
        issues.append("no capabilities under 02-capabilities/")
        return issues
    for bc in bcs:
        if not (bc / "design-tatico.md").exists():
            issues.append(f"missing design-tatico.md for {bc.name}")
    return issues


def count_ready_flows(product_dir: Path) -> tuple[int, int]:
    reg = product_dir / "flows-registry.yml"
    if not reg.exists():
        flux_dirs = list((product_dir / "02-capabilities").rglob("fluxos/*.md"))
        return len(flux_dirs), len(flux_dirs)
    text = reg.read_text(encoding="utf-8")
    ready = len(re.findall(r"status:\s*ready", text))
    total = len(re.findall(r"id:\s*fluxo-", text))
    return ready, total


def validate_gate(product_dir: Path, gate: str, status: dict) -> tuple[bool, list[str]]:
    spec = GATES[gate]
    issues: list[str] = []

    if gate == "G0":
        return check_g0(product_dir, status)

    issues.extend(check_paths(product_dir, spec.get("paths", [])))

    if gate == "G1":
        if not check_one_of_dirs(product_dir, spec.get("one_of_dirs", [])):
            issues.append("need event-storming OR domain-storytelling discovery")

    if gate == "G2" and spec.get("capabilities"):
        issues.extend(check_capabilities(product_dir))
        ready, total = count_ready_flows(product_dir)
        if total < spec.get("fluxos_min", 1):
            issues.append(f"flows-registry: need at least {spec['fluxos_min']} fluxo(s)")

    return len(issues) == 0, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate domain-kit gates")
    parser.add_argument("--hub", type=Path, default=Path.cwd(), help="Hub root")
    parser.add_argument("--product", required=True, help="Product slug")
    parser.add_argument("--gate", choices=["G0", "G1", "G2", "all"], default="all")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    product_dir = args.hub / "products" / args.product
    if not product_dir.is_dir():
        print(f"Product not found: {product_dir}", file=sys.stderr)
        return 2

    status_path = product_dir / "domain-status.json"
    status: dict = {}
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))

    gates = ["G0", "G1", "G2"] if args.gate == "all" else [args.gate]
    results = {}
    for g in gates:
        ok, issues = validate_gate(product_dir, g, status)
        results[g] = {"pass": ok, "issues": issues}

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for g, r in results.items():
            mark = "PASS" if r["pass"] else "FAIL"
            print(f"{g} ({GATES[g]['name']}): {mark}")
            for i in r["issues"]:
                print(f"  - {i}")

    all_ok = all(r["pass"] for r in results.values())
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
