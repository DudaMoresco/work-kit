#!/usr/bin/env python3
"""Generate static HTML dashboard for domain-kit product progress."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

try:
    import markdown  # optional
except ImportError:
    markdown = None


def md_to_html(text: str) -> str:
    if markdown:
        return markdown.markdown(text, extensions=["tables", "fenced_code"])
    return f"<pre>{escape(text)}</pre>"


def parse_flows_registry(path: Path) -> list[dict]:
    if not path.exists():
        return []
    flows: list[dict] = []
    cur: dict = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"\s*-\s*id:", line):
            if cur:
                flows.append(cur)
            cur = {}
        m = re.match(r"\s*id:\s*(fluxo-\d+)", line)
        if m:
            cur["id"] = m.group(1)
        for key in ("title", "bc", "path", "status", "orchestration_ref"):
            km = re.match(rf"\s*{key}:\s*(.+)", line)
            if km:
                cur[key] = km.group(1).strip().strip('"')
        dm = re.match(r"\s*deps:\s*\[(.*)\]", line)
        if dm:
            inner = dm.group(1).strip()
            cur["deps"] = (
                [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
                if inner
                else []
            )
    if cur:
        flows.append(cur)
    return flows


def gate_status(hub: Path, product: str) -> dict[str, str]:
    script = Path(__file__).resolve().parent / "validate_gate.py"
    out: dict[str, str] = {}
    for g in ("G0", "G1", "G2"):
        try:
            r = subprocess.run(
                [sys.executable, str(script), "--hub", str(hub), "--product", product, "--gate", g],
                capture_output=True,
                text=True,
            )
            out[g] = "PASS" if r.returncode == 0 else "FAIL"
        except OSError:
            out[g] = "?"
    return out


def collect_artifacts(product_dir: Path) -> list[tuple[str, Path]]:
    patterns = [
        "01-product/01-vision/*.md",
        "01-product/02-domain/*.md",
        "01-product/04-integration/*.md",
        "02-capabilities/*/design-tatico.md",
        "02-capabilities/*/fluxos/*.md",
        "03-registry/*.md",
        "04-platform/01-non-functional/*.md",
    ]
    found: list[tuple[str, Path]] = []
    for pat in patterns:
        for p in sorted(product_dir.glob(pat)):
            if p.is_file():
                found.append((p.relative_to(product_dir).as_posix(), p))
    return found


def render_page(
    title: str,
    body: str,
    guide_hint: str = "",
) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{escape(title)}</title>
<style>
:root {{ font-family: system-ui, sans-serif; line-height: 1.5; }}
body {{ max-width: 1100px; margin: 0 auto; padding: 1rem 1.5rem; }}
h1,h2 {{ border-bottom: 1px solid #ccc; padding-bottom: .3rem; }}
.pipeline {{ display: flex; gap: .5rem; flex-wrap: wrap; margin: 1rem 0; }}
.chip {{ padding: .25rem .6rem; border-radius: 4px; font-size: .85rem; }}
.pass {{ background: #d4edda; }}
.fail {{ background: #f8d7da; }}
.pending {{ background: #e2e3e5; }}
.flow-grid {{ display: grid; grid-template-columns: repeat(auto-fill,minmax(200px,1fr)); gap: .5rem; }}
.flow-card {{ border: 1px solid #ddd; padding: .5rem; border-radius: 6px; font-size: .9rem; }}
.flow-card.ready {{ border-color: #28a745; }}
.flow-card.draft {{ border-color: #ffc107; }}
.tabs {{ display: flex; gap: .25rem; flex-wrap: wrap; margin: 1rem 0; }}
.tab {{ padding: .3rem .6rem; cursor: pointer; border: 1px solid #ccc; border-radius: 4px 4px 0 0; }}
.doc {{ border: 1px solid #ccc; padding: 1rem; border-radius: 0 6px 6px 6px; max-height: 480px; overflow: auto; }}
.help {{ background: #f0f7ff; padding: .75rem; border-radius: 6px; margin: 1rem 0; font-size: .9rem; }}
</style>
</head>
<body>
{body}
{guide_hint}
<p><small>Gerado {escape(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))} — read-only</small></p>
</body>
</html>"""


def build_product_dashboard(hub: Path, product: str) -> str:
    product_dir = hub / "products" / product
    status: dict = {}
    sp = product_dir / "domain-status.json"
    if sp.exists():
        status = json.loads(sp.read_text(encoding="utf-8"))

    gates = gate_status(hub, product)
    flows = parse_flows_registry(product_dir / "flows-registry.yml")
    artifacts = collect_artifacts(product_dir)

    chips = "".join(
        f'<span class="chip {"pass" if v == "PASS" else "fail" if v == "FAIL" else "pending"}">{g}: {v}</span>'
        for g, v in gates.items()
    )

    flow_cards = []
    for f in flows:
        st = f.get("status", "draft")
        deps = ", ".join(f.get("deps", [])) or "—"
        flow_cards.append(
            f'<div class="flow-card {escape(st)}">'
            f'<strong>{escape(f.get("id", "?"))}</strong><br/>'
            f'{escape(f.get("title", ""))}<br/>'
            f'<small>bc: {escape(f.get("bc", ""))} · deps: {escape(deps)} · {escape(st)}</small>'
            f"</div>"
        )
    flow_html = "".join(flow_cards) or "<p>Nenhum fluxo no registry.</p>"

    scan = status.get("scan", "pending")
    phase = status.get("phase", "?")
    next_cmd = status.get("nextSuggested", "/domain.status")

    art_links = "".join(
        f'<li><a href="#" data-doc="{escape(rel)}">{escape(rel)}</a></li>'
        for rel, _ in artifacts[:40]
    )

    first_doc = ""
    if artifacts:
        first_doc = md_to_html(artifacts[0][1].read_text(encoding="utf-8"))

    help_box = """
<div class="help">
<b>Domain-kit</b> — mapeamento de negócio antes da arquitetura.
Consulte GUIDE.md e ONBOARDING.md no pacote domain-kit.
Regra: conversar antes de gravar; scan cita fontes externas.
</div>
"""

    body = f"""
<h1>Domain-Kit — {escape(product)}</h1>
<p>Fase: <b>{escape(str(phase))}</b> · Scan: <b>{escape(str(scan))}</b> · Próximo: <code>{escape(next_cmd)}</code></p>
<h2>Pipeline / Gates</h2>
<div class="pipeline">{chips}</div>
<h2>Fluxos</h2>
<div class="flow-grid">{flow_html}</div>
<h2>Artefatos ({len(artifacts)})</h2>
<ul>{art_links}</ul>
<h2>Preview</h2>
<div class="doc" id="doc-preview">{first_doc}</div>
"""
    return render_page(f"Domain-Kit — {product}", body, help_box)


def build_hub_index(hub: Path) -> str:
    products_dir = hub / "products"
    links = []
    if products_dir.is_dir():
        for p in sorted(products_dir.iterdir()):
            if p.is_dir() and (p / "domain-status.json").exists():
                links.append(
                    f'<li><a href="products/{escape(p.name)}/dashboard.html">{escape(p.name)}</a></li>'
                )
    body = f"<h1>Architecture Hub — Domain-Kit</h1><ul>{''.join(links) or '<li>Nenhum produto com domain-status</li>'}</ul>"
    return render_page("Domain-Kit Index", body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub", type=Path, default=Path.cwd())
    parser.add_argument("--product", help="Product slug (omit for hub index only)")
    args = parser.parse_args()

    hub = args.hub.resolve()
    if args.product:
        html = build_product_dashboard(hub, args.product)
        out = hub / "products" / args.product / "dashboard.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
        print(f"Wrote {out}")

    idx = build_hub_index(hub)
    idx_path = hub / "dashboard.html"
    idx_path.write_text(idx, encoding="utf-8")
    print(f"Wrote {idx_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
