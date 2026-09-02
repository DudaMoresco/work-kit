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
        "name": "Scan complete",
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
        issues.append("sources.yml missing — run /domain.init")
        return False, issues
    if scan_status in ("complete", "partial", "skipped"):
        return True, issues
    if scan_dir.exists() and (scan_dir / "scan-manifest.json").exists():
        return True, issues
    issues.append(
        "scan not run — run /domain.init (primeiro scan, G0) or /domain.scan or set scan: skipped in domain-status.json"
    )
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


def check_capabilities(product_dir: Path, bc: str | None = None) -> list[str]:
    issues: list[str] = []
    cap_root = product_dir / "02-capabilities"
    if not cap_root.is_dir():
        return ["02-capabilities/ missing"]
    if bc:
        bc_dir = cap_root / bc
        if not bc_dir.is_dir():
            return [f"capability {bc}/ missing"]
        if not (bc_dir / "design-tatico.md").exists():
            issues.append(f"missing design-tatico.md for {bc}")
        if not (bc_dir / "README.md").exists():
            issues.append(f"missing README.md for {bc}")
        return issues
    bcs = [d for d in cap_root.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not bcs:
        issues.append("no capabilities under 02-capabilities/")
        return issues
    for bc_dir in bcs:
        if not (bc_dir / "design-tatico.md").exists():
            issues.append(f"missing design-tatico.md for {bc_dir.name}")
    return issues


def count_ready_flows(product_dir: Path, bc: str | None = None) -> tuple[int, int]:
    reg = product_dir / "flows-registry.yml"
    if bc:
        flux_dir = product_dir / "02-capabilities" / bc / "fluxos"
        flux_files = list(flux_dir.glob("*.md")) if flux_dir.is_dir() else []
        return len(flux_files), len(flux_files)
    if not reg.exists():
        flux_dirs = list((product_dir / "02-capabilities").rglob("fluxos/*.md"))
        return len(flux_dirs), len(flux_dirs)
    text = reg.read_text(encoding="utf-8")
    ready = len(re.findall(r"status:\s*ready", text))
    total = len(re.findall(r"id:\s*fluxo-", text))
    return ready, total


def validate_gate(
    product_dir: Path,
    gate: str,
    status: dict,
    mode: str = "full",
    bc: str | None = None,
) -> tuple[bool, list[str]]:
    spec = GATES[gate]
    issues: list[str] = []

    if gate == "G0":
        return check_g0(product_dir, status)

    if gate == "G1":
        issues.extend(check_paths(product_dir, spec.get("paths", [])))
        if mode == "minimal":
            # minimal relaxes discovery artifacts — still need BCs + strategic
            if not check_one_of_dirs(product_dir, spec.get("one_of_dirs", [])):
                issues.append("minimal mode: discovery optional but recommended")
        elif not check_one_of_dirs(product_dir, spec.get("one_of_dirs", [])):
            issues.append("need event-storming OR domain-storytelling discovery")
        return len(issues) == 0, issues

    if gate == "G2":
        if mode == "incremental":
            if not bc:
                return False, ["--bc required for incremental G2 validation"]
            issues.extend(check_capabilities(product_dir, bc))
            ready, total = count_ready_flows(product_dir, bc)
            if total < 1:
                issues.append(f"need at least 1 fluxo for capability {bc}")
            reg = product_dir / "03-registry/produto.md"
            if not reg.exists():
                issues.append("03-registry/produto.md missing")
            return len(issues) == 0, issues

        issues.extend(check_paths(product_dir, spec.get("paths", [])))
        if spec.get("capabilities"):
            issues.extend(check_capabilities(product_dir))
            ready, total = count_ready_flows(product_dir)
            if total < spec.get("fluxos_min", 1):
                issues.append(f"flows-registry: need at least {spec['fluxos_min']} fluxo(s)")
        return len(issues) == 0, issues

    issues.extend(check_paths(product_dir, spec.get("paths", [])))
    return len(issues) == 0, issues


def has_evidence_brief(product_dir: Path) -> bool:
    return (product_dir / "01-product/00-scan/sintese-evidencias.md").is_file()


def suggest_next_command(results: dict[str, dict], product_dir: Path | None = None) -> str:
    g0 = results.get("G0", {}).get("pass", False)
    g1 = results.get("G1", {}).get("pass", False)
    g2 = results.get("G2", {}).get("pass", False)
    g2_issues = results.get("G2", {}).get("issues", [])

    if not g0:
        return "/domain.init {produto}  # completar primeiro scan (G0)"
    if product_dir is not None and g0 and not has_evidence_brief(product_dir):
        return "/domain.init {produto}  # completar síntese (Fase 0c)"
    if not g1:
        return "/domain.discover {produto}  # lacunas + descoberta DDD (G1)"
    if not g2:
        if any("design-tatico" in i for i in g2_issues):
            return "/domain.capability {bc}  # tático pendente"
        if any("fluxo" in i.lower() or "flows" in i.lower() for i in g2_issues):
            return "/domain.flow {NN}  # fluxo pendente"
        if any("integracao" in i or "contextos" in i for i in g2_issues):
            return "/domain.model {produto}  # integração pendente"
        return "/domain.model {produto} --finalize  # fechar G2"
    return "/arch.route {produto}  # G2 ok — handoff arch-kit"


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate domain-kit gates")
    parser.add_argument("--hub", type=Path, default=Path.cwd(), help="Hub root")
    parser.add_argument("--product", required=True, help="Product slug")
    parser.add_argument("--gate", choices=["G0", "G1", "G2", "all"], default="all")
    parser.add_argument("--mode", choices=["full", "minimal", "incremental"], default="full")
    parser.add_argument("--bc", default=None, help="Bounded context slug (incremental G2)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--suggest", action="store_true", help="Print suggested next command")
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
        ok, issues = validate_gate(product_dir, g, status, mode=args.mode, bc=args.bc)
        results[g] = {"pass": ok, "issues": issues}

    next_cmd = suggest_next_command(results, product_dir).replace("{produto}", args.product)

    if args.json:
        payload = {"gates": results, "suggestedNextCommand": next_cmd}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for g, r in results.items():
            mark = "PASS" if r["pass"] else "FAIL"
            print(f"{g} ({GATES[g]['name']}): {mark}")
            for i in r["issues"]:
                print(f"  - {i}")
        if args.suggest or args.gate == "all":
            print(f"Suggested next: {next_cmd}")

    all_ok = all(r["pass"] for r in results.values())
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
