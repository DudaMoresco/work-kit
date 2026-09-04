#!/usr/bin/env python3
"""Check flow dependencies before /domain.flow NN."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_flows_registry(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    flows: dict[str, dict] = {}
    current_id: str | None = None
    for line in text.splitlines():
        m = re.match(r"\s*-\s*id:\s*(fluxo-\d+)", line)
        if m:
            current_id = m.group(1)
            flows[current_id] = {"deps": [], "status": "draft"}
            continue
        if current_id is None:
            continue
        dm = re.match(r"\s*deps:\s*\[(.*)\]", line)
        if dm:
            inner = dm.group(1).strip()
            if inner:
                flows[current_id]["deps"] = [
                    x.strip().strip('"').strip("'") for x in inner.split(",")
                ]
        sm = re.match(r"\s*status:\s*(\w+)", line)
        if sm:
            flows[current_id]["status"] = sm.group(1)
    return flows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("product_dir", type=Path, help="products/{produto}")
    parser.add_argument("flow_num", type=str, help="01 or fluxo-01")
    args = parser.parse_args()

    fid = args.flow_num if args.flow_num.startswith("fluxo-") else f"fluxo-{int(args.flow_num):02d}"
    reg_path = args.product_dir / "flows-registry.yml"
    flows = parse_flows_registry(reg_path)

    if fid not in flows:
        print(f"WARN: {fid} not in flows-registry.yml — deps check skipped")
        return 0

    deps = flows[fid]["deps"]
    missing: list[str] = []
    not_ready: list[str] = []
    for dep in deps:
        if dep not in flows:
            missing.append(dep)
            continue
        if flows[dep].get("status") != "ready":
            not_ready.append(dep)

    if missing or not_ready:
        parts: list[str] = []
        if missing:
            parts.append(f"deps missing from registry: {', '.join(missing)}")
        if not_ready:
            parts.append(f"deps not ready: {', '.join(not_ready)}")
        print(f"FAIL: {fid} blocked — {'; '.join(parts)}")
        return 1

    print(f"PASS: {fid} deps satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
