#!/usr/bin/env python3
"""Validate domain-kit phases for a product in architecture-hub.

Phases: evidencias → estrategico → descoberta → operacional → arch-kit handoff.
Legacy gate aliases: G0=evidencias, G1=estrategico+descoberta, G2=operacional.
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
            "04-platform/01-non-functional/01-requisitos.md",
            "03-registry/produto.md",
        ],
        "fluxos_min": 1,
    },
}

# Legacy gate → phase mapping (G1 requires both estrategico and descoberta)
GATE_ALIASES = {
    "G0": ["evidencias"],
    "G1": ["estrategico", "descoberta"],
    "G2": ["operacional"],
}

PHASE_ORDER = ["evidencias", "estrategico", "descoberta", "operacional"]

OPERACIONAL_FLUXOS_DIR = "01-product/03-operacional/fluxos"
LEGACY_FLUXOS_GLOB = "02-capabilities/**/fluxos/*.md"
ARCH_INTEGRATION_PATH = "arch/01-integration/01-contextos.md"
LEGACY_INTEGRATION_PATH = "01-product/04-integration/01-contextos.md"


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
    legacy_files = list(product_dir.glob(LEGACY_FLUXOS_GLOB))

    if reg.exists():
        text = reg.read_text(encoding="utf-8")
        ready = len(re.findall(r"status:\s*ready", text))
        total = len(re.findall(r"id:\s*fluxo-", text))
        if total > 0:
            return ready, total

    total_files = len(op_files) + len(legacy_files)
    return total_files, total_files


def has_arch_legacy(product_dir: Path, status: dict) -> bool:
    arch = status.get("arch") or {}
    if arch.get("integrationAdopted") or arch.get("capabilitiesAdopted"):
        return True
    if (product_dir / ARCH_INTEGRATION_PATH).is_file():
        return True
    cap_root = product_dir / "02-capabilities"
    if cap_root.is_dir():
        for bc_dir in cap_root.iterdir():
            if bc_dir.is_dir() and (bc_dir / "design-tatico.md").is_file():
                return True
    return False


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


def validate_gate_alias(
    product_dir: Path,
    gate: str,
    status: dict,
    mode: str = "full",
) -> tuple[bool, list[str]]:
    phases = GATE_ALIASES.get(gate, [])
    if not phases:
        return False, [f"unknown gate {gate}"]
    all_issues: list[str] = []
    all_pass = True
    for phase in phases:
        ok, issues = validate_phase(product_dir, phase, status, mode=mode)
        if not ok:
            all_pass = False
            all_issues.extend(issues)
    return all_pass, all_issues


def has_evidence_brief(product_dir: Path) -> bool:
    return (product_dir / "01-product/00-scan/sintese-evidencias.md").is_file()


def suggest_next_command(results: dict[str, dict], product_dir: Path | None = None) -> str:
    def passed(name: str) -> bool:
        return results.get(name, {}).get("pass", False)

    ev = passed("evidencias")
    est = passed("estrategico")
    desc = passed("descoberta")
    op = passed("operacional")
    op_issues = results.get("operacional", {}).get("issues", [])

    if not ev:
        return "/domain.init {produto}  # completar evidências (scan)"
    if product_dir is not None and ev and not has_evidence_brief(product_dir):
        return "/domain.init {produto}  # completar síntese de evidências"
    if not est:
        return "/domain.discover {produto} --stage strategic|contexts  # fase estratégico"
    if not desc:
        return "/domain.discover {produto} --stage stories|event-storming  # fase descoberta"
    if not op:
        if any("requisitos" in i for i in op_issues):
            return "/domain.model {produto} --finalize  # requisitos NFR de produto"
        if any("fluxo" in i.lower() for i in op_issues):
            return "/domain.flow {NN}  # fluxo operacional de negócio"
        return "/domain.model {produto} --finalize  # fechar fase operacional"
    return "/arch.route {produto}  # operacional ok — handoff arch-kit"


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
    """Merge legacy gates/discover/model into phases schema."""
    phases_pass = {p: results[p]["pass"] for p in PHASE_ORDER if p in results}
    status["phases"] = phases_pass
    status["phaseIssues"] = {p: results[p].get("issues", []) for p in PHASE_ORDER if p in results}
    # Legacy aliases for tools not yet updated
    status["gates"] = {
        "G0": phases_pass.get("evidencias", False),
        "G1": phases_pass.get("estrategico", False) and phases_pass.get("descoberta", False),
        "G2": phases_pass.get("operacional", False),
    }
    status["gateIssues"] = {
        "G0": status["phaseIssues"].get("evidencias", []),
        "G1": (
            status["phaseIssues"].get("estrategico", [])
            + status["phaseIssues"].get("descoberta", [])
        ),
        "G2": status["phaseIssues"].get("operacional", []),
    }
    status["phase"] = compute_product_phase(results)
    return status


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate domain-kit phases")
    parser.add_argument("--hub", type=Path, default=Path.cwd(), help="Hub root")
    parser.add_argument("--product", required=True, help="Product slug")
    parser.add_argument(
        "--phase",
        choices=PHASE_ORDER + ["all"],
        default=None,
        help="Phase to validate",
    )
    parser.add_argument(
        "--gate",
        choices=["G0", "G1", "G2", "all"],
        default=None,
        help="Legacy gate alias (deprecated)",
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

    if args.phase:
        phases = PHASE_ORDER if args.phase == "all" else [args.phase]
    elif args.gate:
        if args.gate == "all":
            phases = PHASE_ORDER
        else:
            phases = GATE_ALIASES[args.gate]
    else:
        phases = PHASE_ORDER

    results: dict[str, dict] = {}
    for p in PHASE_ORDER:
        ok, issues = validate_phase(product_dir, p, status, mode=args.mode)
        results[p] = {"pass": ok, "issues": issues}

    # When validating a subset, only expose requested phases in output
    if args.phase and args.phase != "all":
        output_results = {args.phase: results[args.phase]}
    elif args.gate and args.gate != "all":
        gate_ok, gate_issues = validate_gate_alias(product_dir, args.gate, status, mode=args.mode)
        output_results = {
            args.gate: {"pass": gate_ok, "issues": gate_issues},
            "phases": {p: results[p] for p in GATE_ALIASES[args.gate]},
        }
    else:
        output_results = results

    next_cmd = suggest_next_command(results, product_dir).replace("{produto}", args.product)

    if args.json:
        payload: dict = {
            "phases": results,
            "suggestedNextCommand": next_cmd,
            "productPhase": compute_product_phase(results),
        }
        if args.gate and args.gate != "all":
            payload["gates"] = {args.gate: output_results[args.gate]}
        else:
            payload["gates"] = {
                g: validate_gate_alias(product_dir, g, status, mode=args.mode)[0]
                for g in ("G0", "G1", "G2")
            }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        for p in (phases if args.gate is None else PHASE_ORDER):
            if p in results:
                r = results[p]
                mark = "PASS" if r["pass"] else "FAIL"
                print(f"{p} ({PHASES[p]['name']}): {mark}")
                for i in r["issues"]:
                    print(f"  - {i}")
        if args.gate and args.gate != "all":
            gate_ok, gate_issues = validate_gate_alias(product_dir, args.gate, status, mode=args.mode)
            mark = "PASS" if gate_ok else "FAIL"
            print(f"\nLegacy {args.gate}: {mark}")
            for i in gate_issues:
                print(f"  - {i}")
        if args.suggest or (args.phase is None and args.gate is None):
            print(f"Suggested next: {next_cmd}")

    # Exit code: scoped to requested phase/gate; full suite only for all/default
    if args.phase and args.phase != "all":
        return 0 if results[args.phase]["pass"] else 1
    if args.gate and args.gate != "all":
        gate_ok, _ = validate_gate_alias(product_dir, args.gate, status, mode=args.mode)
        return 0 if gate_ok else 1
    all_ok = all(results[p]["pass"] for p in PHASE_ORDER)
    return 0 if all_ok else 1


# Backward-compatible aliases for external imports
validate_gate = validate_phase
GATES = PHASES

if __name__ == "__main__":
    sys.exit(main())
