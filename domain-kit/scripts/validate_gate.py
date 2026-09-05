#!/usr/bin/env python3
"""Validate domain-kit phases for a product in the hub.

Phases: evidencias → estrategico → descoberta → operacional.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PHASES = {
    "evidencias": {
        "name": "Evidências",
        "question": "O que sabemos, com fonte?",
        "paths": [],
    },
    "estrategico": {
        "name": "Estratégico",
        "question": "Por quê existe? Onde estão as fronteiras? Como falamos?",
        "paths": [
            "01-product/01-vision/01-design-estrategico.md",
            "01-product/02-domain/desafio-negocio.md",
            "01-product/02-domain/bounded-contexts.md",
            "01-product/02-domain/linguagem-ubiqua.md",
        ],
    },
    "descoberta": {
        "name": "Descoberta",
        "question": "Como o domínio se comporta no tempo e no dia a dia?",
        "paths": [],
        "one_of_dirs": [
            "01-product/03-discovery/01-event-storming",
            "01-product/03-discovery/02-domain-storytelling",
        ],
    },
    "operacional": {
        "name": "Operacional",
        "question": "Quais cenários ponta a ponta queremos garantir?",
        "paths": [
            "01-product/04-operacional/requisitos.md",
            "05-decisoes/produto.md",
        ],
        "fluxos_min": 1,
    },
}

PHASE_ORDER = ["evidencias", "estrategico", "descoberta", "operacional"]

OPERACIONAL_FLUXOS_DIR = "01-product/04-operacional/fluxos"


def check_evidencias(product_dir: Path, status: dict) -> tuple[bool, list[str]]:
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
        "scan not run — run /domain.init or /domain.scan or set scan: skipped in domain-status.json"
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


def count_operacional_flows(product_dir: Path) -> tuple[int, int]:
    """Return (ready_count, total_count) for business operational flows."""
    reg = product_dir / "flows-registry.yml"
    op_dir = product_dir / OPERACIONAL_FLUXOS_DIR
    op_files = list(op_dir.glob("*.md")) if op_dir.is_dir() else []

    if reg.exists():
        body = reg.read_text(encoding="utf-8")
        ready = len(re.findall(r"status:\s*ready", body))
        total = len(re.findall(r"id:\s*fluxo-", body))
        if total > 0:
            return ready, total

    return len(op_files), len(op_files)


def validate_phase(
    product_dir: Path,
    phase: str,
    status: dict,
    mode: str = "full",
) -> tuple[bool, list[str]]:
    spec = PHASES[phase]
    issues: list[str] = []

    if phase == "evidencias":
        return check_evidencias(product_dir, status)

    if phase == "estrategico":
        issues.extend(check_paths(product_dir, spec.get("paths", [])))
        return len(issues) == 0, issues

    if phase == "descoberta":
        if mode == "minimal":
            # Discovery optional in minimal — PASS without issues; warn on stderr only
            if not check_one_of_dirs(product_dir, spec.get("one_of_dirs", [])):
                print(
                    "WARN: minimal mode — descoberta vazia (event-storming/stories opcional)",
                    file=sys.stderr,
                )
            return True, []
        if not check_one_of_dirs(product_dir, spec.get("one_of_dirs", [])):
            issues.append("need event-storming OR domain-storytelling discovery")
        return len(issues) == 0, issues

    if phase == "operacional":
        issues.extend(check_paths(product_dir, spec.get("paths", [])))
        ready, total = count_operacional_flows(product_dir)
        fluxos_min = spec.get("fluxos_min", 1)
        if total < fluxos_min:
            issues.append(
                f"need at least {fluxos_min} fluxo operacional "
                f"in {OPERACIONAL_FLUXOS_DIR}/ or flows-registry.yml (ready)"
            )
        elif ready < fluxos_min and reg_has_flows(product_dir):
            issues.append(f"flows-registry: need at least {fluxos_min} fluxo(s) with status ready")
        return len(issues) == 0, issues

    issues.extend(check_paths(product_dir, spec.get("paths", [])))
    return len(issues) == 0, issues


def reg_has_flows(product_dir: Path) -> bool:
    reg = product_dir / "flows-registry.yml"
    if not reg.exists():
        return False
    return bool(re.search(r"id:\s*fluxo-", reg.read_text(encoding="utf-8")))


def has_evidence_brief(product_dir: Path) -> bool:
    return (product_dir / "01-product/00-scan/sintese-evidencias.md").is_file()


def suggest_next_command(results: dict[str, dict], product_dir: Path | None = None) -> str:
    if not results.get("evidencias", {}).get("pass"):
        return "/domain.init {produto}  # completar evidências (scan)"
    if product_dir and not has_evidence_brief(product_dir):
        return "/domain.init {produto}  # síntese de evidências"
    if not results.get("estrategico", {}).get("pass"):
        return "/domain.discover {produto} --stage strategic|contexts"
    if not results.get("descoberta", {}).get("pass"):
        return "/domain.discover {produto} --stage stories|event-storming"
    if not results.get("operacional", {}).get("pass"):
        op_issues = results.get("operacional", {}).get("issues", [])
        if any("fluxo" in i for i in op_issues):
            return "/domain.flow 01  # ou próximo NN em flows-registry"
        if any("requisitos" in i for i in op_issues):
            return "/domain.model {produto} --finalize  # requisitos NFR de produto"
        if any("05-decisoes" in i or "registry" in i for i in op_issues):
            return "/domain.decision  # registry D-n"
        return "/domain.model {produto} --finalize"
    return "Fases do domain-kit concluídas"


def compute_product_phase(results: dict[str, dict]) -> str:
    if not results.get("evidencias", {}).get("pass"):
        return "evidencias"
    if not results.get("estrategico", {}).get("pass"):
        return "estrategico-in-progress"
    if not results.get("descoberta", {}).get("pass"):
        return "descoberta-in-progress"
    if not results.get("operacional", {}).get("pass"):
        return "operacional-in-progress"
    return "domain-complete"


def migrate_status_schema(status: dict, results: dict[str, dict]) -> dict:
    """Write phases schema into domain-status.json fields."""
    status["phases"] = {p: results[p]["pass"] for p in PHASE_ORDER if p in results}
    status["phaseIssues"] = {
        p: results[p].get("issues", []) for p in PHASE_ORDER if p in results
    }
    status.pop("gates", None)
    status.pop("gateIssues", None)
    status["phase"] = compute_product_phase(results)
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate domain-kit phases")
    parser.add_argument("--hub", type=Path, default=Path.cwd(), help="Hub root")
    parser.add_argument("--product", required=True, help="Product slug")
    parser.add_argument(
        "--phase",
        choices=PHASE_ORDER + ["all"],
        default="all",
        help="Phase to validate (default: all)",
    )
    parser.add_argument("--mode", choices=["full", "minimal", "incremental"], default="full")
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

    phases = PHASE_ORDER if args.phase == "all" else [args.phase]

    results: dict[str, dict] = {}
    for p in PHASE_ORDER:
        ok, issues = validate_phase(product_dir, p, status, mode=args.mode)
        results[p] = {"pass": ok, "issues": issues}

    next_cmd = suggest_next_command(results, product_dir).replace("{produto}", args.product)

    if args.json:
        payload = {
            "phases": results,
            "suggestedNextCommand": next_cmd,
            "productPhase": compute_product_phase(results),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for p in phases:
            r = results[p]
            mark = "PASS" if r["pass"] else "FAIL"
            print(f"{p} ({PHASES[p]['name']}): {mark}")
            for i in r["issues"]:
                print(f"  - {i}")
        if args.suggest or args.phase == "all":
            print(f"Suggested next: {next_cmd}")

    if args.phase != "all":
        return 0 if results[args.phase]["pass"] else 1
    return 0 if all(results[p]["pass"] for p in PHASE_ORDER) else 1


validate_gate = validate_phase
GATES = PHASES

if __name__ == "__main__":
    sys.exit(main())
