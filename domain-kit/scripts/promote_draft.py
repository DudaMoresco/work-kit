#!/usr/bin/env python3
"""Promote domain-kit draft files to canonical hub paths."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {"product": "", "updatedAt": None, "pending": []}
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def save_manifest(manifest_path: Path, data: dict) -> None:
    data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def promote_one(product_dir: Path, entry: dict, dry_run: bool) -> None:
    draft_rel = entry.get("draftPath", "").strip()
    if draft_rel.startswith("./"):
        draft_rel = draft_rel[2:]
    target_rel = entry.get("targetPath", "")
    if not draft_rel or not target_rel:
        raise ValueError(f"invalid manifest entry: {entry}")

    draft_path = product_dir / draft_rel
    target_path = product_dir / target_rel

    if not draft_path.exists():
        raise FileNotFoundError(f"draft missing: {draft_path}")

    if dry_run:
        print(f"would promote {draft_path} -> {target_path}")
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(draft_path, target_path)
    draft_path.unlink()
    # prune empty draft dirs
    parent = draft_path.parent
    draft_root = product_dir / ".draft"
    while parent != draft_root and parent.exists() and not any(parent.iterdir()):
        parent.rmdir()
        parent = parent.parent
    print(f"promoted {target_rel}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote .draft/ files to canonical paths")
    parser.add_argument("--hub", default=".", help="Hub root")
    parser.add_argument("--product", required=True, help="Product slug")
    parser.add_argument("--target", help="Promote single targetPath from manifest")
    parser.add_argument("--all", action="store_true", help="Promote all pending")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    hub = Path(args.hub).resolve()
    product_dir = hub / "products" / args.product
    manifest_path = product_dir / ".draft" / "manifest.json"

    if not product_dir.is_dir():
        print(f"product not found: {product_dir}", file=sys.stderr)
        return 1

    data = load_manifest(manifest_path)
    pending = data.get("pending", [])

    if args.all:
        targets = pending
    elif args.target:
        targets = [e for e in pending if e.get("targetPath") == args.target]
        if not targets:
            print(f"no pending entry for target: {args.target}", file=sys.stderr)
            return 1
    else:
        parser.error("specify --target PATH or --all")

    for entry in list(targets):
        promote_one(product_dir, entry, args.dry_run)
        if not args.dry_run:
            pending.remove(entry)

    if not args.dry_run:
        data["pending"] = pending
        save_manifest(manifest_path, data)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
