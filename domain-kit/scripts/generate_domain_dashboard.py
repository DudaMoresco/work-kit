#!/usr/bin/env python3
"""Generate static HTML dashboard for domain-kit product progress."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape, unescape
from pathlib import Path

try:
    import markdown  # optional
except ImportError:
    markdown = None

PIPELINE_STEPS = [
    ("init", "Init", "/domain.init"),
    ("discover", "Discover", "/domain.discover"),
    ("model", "Model", "/domain.model"),
    ("flow", "Fluxos", "/domain.flow"),
    ("arch", "Arch-kit", "/arch.route"),
]

DEFAULT_PLANTUML_SERVER = "http://127.0.0.1:8765"
PLANTUML_CODE_BLOCK_RE = re.compile(
    r'<pre><code class="language-(?:plantuml|uml|puml)">(.*?)</code></pre>',
    re.DOTALL | re.IGNORECASE,
)


def load_plantuml_server(hub: Path) -> str:
    if env := os.environ.get("PLANTUML_SERVER"):
        return env.rstrip("/")
    cfg_path = hub / ".domain" / "config.yml"
    if cfg_path.is_file():
        in_plantuml = False
        for line in cfg_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped == "plantuml:":
                in_plantuml = True
                continue
            if in_plantuml:
                if stripped and not line.startswith(" "):
                    break
                match = re.match(r"\s+server:\s*(.+)", line)
                if match:
                    return match.group(1).strip().strip('"').strip("'").rstrip("/")
    return DEFAULT_PLANTUML_SERVER


def fetch_plantuml_svg(source: str, server: str) -> str | None:
    url = f"{server.rstrip('/')}/svg"
    try:
        req = urllib.request.Request(
            url,
            data=source.encode("utf-8"),
            headers={"Content-Type": "text/plain"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
    except (urllib.error.URLError, OSError, TimeoutError):
        return None
    if body.lstrip().startswith("<"):
        return body
    return None


def embed_plantuml_svgs(html: str, server: str) -> str:
    def replace_block(match: re.Match[str]) -> str:
        source = unescape(match.group(1))
        svg = fetch_plantuml_svg(source, server)
        if svg:
            return f'<div class="plantuml-diagram">{svg}</div>'
        return match.group(0)

    return PLANTUML_CODE_BLOCK_RE.sub(replace_block, html)


def md_to_html(text: str) -> str:
    if markdown:
        return markdown.markdown(text, extensions=["tables", "fenced_code"])
    print(
        "WARNING: pacote 'markdown' ausente — preview em texto bruto. "
        "Instale: python3 -m pip install -r scripts/requirements.txt",
        file=sys.stderr,
    )
    return f"<pre class='md-fallback'>{escape(text)}</pre>"


def file_to_preview_html(path: Path, plantuml_server: str) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return "<p><em>Erro ao ler arquivo.</em></p>"
    suffix = path.suffix.lower()
    if suffix in (".json", ".yml", ".yaml"):
        return f"<pre class='md-fallback'><code>{escape(text)}</code></pre>"
    return embed_plantuml_svgs(md_to_html(text), plantuml_server)


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
    root_files = ["CHANGELOG.md", "README.md", "product-README.md"]
    found: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for name in root_files:
        p = product_dir / name
        if p.is_file() and name not in seen:
            seen.add(name)
            found.append((name, p))
    patterns = [
        "01-product/**/*.md",
        "02-capabilities/**/*.md",
        "03-registry/*.md",
        "04-platform/**/*.md",
    ]
    found: list[tuple[str, Path]] = []
    seen: set[str] = set()
    for pat in patterns:
        for p in sorted(product_dir.glob(pat)):
            if not p.is_file():
                continue
            rel = p.relative_to(product_dir).as_posix()
            if rel.startswith(".draft/"):
                continue
            if rel not in seen:
                seen.add(rel)
                found.append((rel, p))
    return found


def load_draft_manifest(product_dir: Path) -> dict:
    path = product_dir / ".draft" / "manifest.json"
    if not path.exists():
        return {"pending": [], "updatedAt": None}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("pending", [])
        return data
    except json.JSONDecodeError:
        return {"pending": [], "updatedAt": None, "error": "manifest inválido"}


def collect_draft_files(product_dir: Path) -> list[tuple[str, Path]]:
    draft_root = product_dir / ".draft"
    if not draft_root.is_dir():
        return []
    found: list[tuple[str, Path]] = []
    for p in sorted(draft_root.rglob("*")):
        if p.is_file() and p.name not in ("manifest.json", "README.md"):
            rel = p.relative_to(product_dir).as_posix()
            found.append((rel, p))
    return found


def phase_index(phase: str) -> int:
    mapping = {"init": 0, "scan": 0, "discover": 1, "model": 2, "flow": 3, "done": 4}
    return mapping.get(str(phase).lower(), 0)


def _draft_has(product_dir: Path, canonical_rel: str) -> bool:
    draft = product_dir / ".draft" / canonical_rel
    return draft.is_file()


def _count_md_in_dir(path: Path) -> int:
    if not path.is_dir():
        return 0
    return sum(1 for p in path.iterdir() if p.is_file() and p.suffix.lower() == ".md")


def compute_discover_fields(product_dir: Path, status: dict) -> list[dict]:
    """Progress per discover field — canonical paths + .draft hints + domain-status.json."""
    discover = status.get("discover") or {}
    scan_st = str(status.get("scan", "pending"))

    fields: list[dict] = []

    # Scan / fontes (fase 0)
    scan_pct = 0
    scan_state = "pending"
    scan_hint = ""
    if scan_st in ("complete", "skipped"):
        scan_pct, scan_state = 100, "ready"
        scan_hint = scan_st
    elif scan_st == "partial":
        scan_pct, scan_state = 60, "partial"
        scan_hint = "parcial"
    elif (product_dir / "01-product/00-scan/scan-manifest.json").is_file():
        scan_pct, scan_state = 100, "ready"
        scan_hint = "manifest promovido"
    elif _draft_has(product_dir, "01-product/00-scan/scan-manifest.json") or _draft_has(
        product_dir, "sources.yml"
    ):
        scan_pct, scan_state = 45, "draft"
        scan_hint = "rascunho aguardando OK"
    fields.append(
        {
            "key": "scan",
            "label": "Scan / fontes",
            "pct": scan_pct,
            "state": scan_state,
            "hint": scan_hint or scan_st,
        }
    )

    # Síntese de evidências (init fase 0c)
    brief_path = "01-product/00-scan/sintese-evidencias.md"
    fields.append(
        _file_field("evidenceBrief", "Síntese evidências", product_dir, discover, brief_path)
    )

    # Design estratégico
    estr_path = "01-product/01-vision/01-design-estrategico.md"
    fields.append(_file_field("estrategico", "Design estratégico", product_dir, discover, estr_path))

    # Domain stories (≥2 MD para G1)
    stories_dir = product_dir / "01-product/03-discovery/02-domain-storytelling"
    draft_stories = _count_md_in_dir(product_dir / ".draft/01-product/03-discovery/02-domain-storytelling")
    n_stories = _count_md_in_dir(stories_dir)
    st_json = str(discover.get("stories", "pending"))
    if n_stories >= 2 or st_json in ("ready", "complete"):
        s_state, s_pct, s_hint = "ready", 100, f"{n_stories} história(s)"
    elif n_stories == 1:
        s_state, s_pct, s_hint = "partial", 50, "1/2+ histórias"
    elif draft_stories >= 1:
        s_state, s_pct, s_hint = "draft", 40, f"rascunho ({draft_stories} MD)"
    else:
        s_state, s_pct, s_hint = "pending", 0, st_json
    fields.append(
        {"key": "stories", "label": "Domain stories", "pct": s_pct, "state": s_state, "hint": s_hint}
    )

    # Event storming (pasta não vazia)
    es_dir = product_dir / "01-product/03-discovery/01-event-storming"
    draft_es = product_dir / ".draft/01-product/03-discovery/01-event-storming"
    if es_dir.is_dir() and any(es_dir.iterdir()):
        es_state, es_pct, es_hint = "ready", 100, "workshop registrado"
    elif draft_es.is_dir() and any(draft_es.iterdir()):
        es_state, es_pct, es_hint = "draft", 45, "rascunho ES"
    else:
        es_json = str(discover.get("eventStorming", "pending"))
        es_state, es_pct = "pending", 0
        es_hint = es_json
    fields.append(
        {
            "key": "eventStorming",
            "label": "Event storming",
            "pct": es_pct,
            "state": es_state,
            "hint": es_hint,
        }
    )

    # UL + BCs (3 arquivos)
    bc_files = [
        "01-product/02-domain/desafio-negocio.md",
        "01-product/02-domain/linguagem-ubiqua.md",
        "01-product/02-domain/bounded-contexts.md",
    ]
    have = sum(1 for rel in bc_files if (product_dir / rel).is_file())
    draft_have = sum(1 for rel in bc_files if _draft_has(product_dir, rel))
    bc_json = str(discover.get("boundedContexts", "pending"))
    if have == 3 or bc_json in ("ready", "complete"):
        bc_state, bc_pct, bc_hint = "ready", 100, "desafio + UL + BCs"
    elif have > 0:
        bc_state, bc_pct, bc_hint = "partial", int(have / 3 * 100), f"{have}/3 arquivos"
    elif draft_have > 0:
        bc_state, bc_pct, bc_hint = "draft", int(draft_have / 3 * 100), f"rascunho {draft_have}/3"
    else:
        bc_state, bc_pct, bc_hint = "pending", 0, bc_json
    fields.append(
        {
            "key": "boundedContexts",
            "label": "Linguagem + BCs",
            "pct": bc_pct,
            "state": bc_state,
            "hint": bc_hint,
        }
    )

    return fields


def _file_field(key: str, label: str, product_dir: Path, discover: dict, rel: str) -> dict:
    canonical = (product_dir / rel).is_file()
    draft = _draft_has(product_dir, rel)
    json_st = str(discover.get(key, "pending"))
    if canonical or json_st in ("ready", "complete"):
        return {"key": key, "label": label, "pct": 100, "state": "ready", "hint": "promovido"}
    if draft:
        return {"key": key, "label": label, "pct": 50, "state": "draft", "hint": "rascunho em .draft/"}
    return {"key": key, "label": label, "pct": 0, "state": "pending", "hint": json_st}


def render_discover_progress(fields: list[dict]) -> tuple[str, int]:
    if not fields:
        return "", 0
    total_pct = sum(f["pct"] for f in fields) // len(fields)
    rows = []
    state_label = {
        "ready": "Pronto",
        "draft": "Rascunho",
        "partial": "Parcial",
        "pending": "Pendente",
    }
    for f in fields:
        st = f["state"]
        rows.append(
            f'<div class="field-row">'
            f'<div class="field-label">{escape(f["label"])}</div>'
            f'<div class="field-bar"><div class="field-bar-fill {escape(st)}" style="width:{f["pct"]}%"></div></div>'
            f'<div class="field-status status-{escape(st)}">{escape(state_label.get(st, st))}</div>'
            f'<div class="field-hint">{escape(f.get("hint", ""))}</div>'
            f"</div>"
        )
    summary = (
        f'<div class="discover-summary">'
        f'<div class="discover-summary-label">Discover · {total_pct}%</div>'
        f'<div class="field-bar field-bar-lg"><div class="field-bar-fill {"ready" if total_pct >= 100 else "partial" if total_pct > 0 else "pending"}" '
        f'style="width:{total_pct}%"></div></div>'
        f"</div>"
    )
    return summary + "".join(rows), total_pct


def shared_styles() -> str:
    return """
:root {
  --bg: #0f1419;
  --surface: #1a2332;
  --surface-2: #243044;
  --border: #2d3a4f;
  --text: #e8edf4;
  --muted: #8b9cb3;
  --accent: #f59e0b;
  --accent-dim: rgba(245, 158, 11, 0.15);
  --pass: #34d399;
  --pass-bg: rgba(52, 211, 153, 0.12);
  --fail: #f87171;
  --fail-bg: rgba(248, 113, 113, 0.12);
  --pending: #94a3b8;
  --pending-bg: rgba(148, 163, 184, 0.12);
  --draft: #60a5fa;
  --draft-bg: rgba(96, 165, 250, 0.12);
  --radius: 12px;
  --shadow: 0 4px 24px rgba(0, 0, 0, 0.35);
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  line-height: 1.55;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(245, 158, 11, 0.08), transparent),
    linear-gradient(180deg, var(--bg) 0%, #0a0e14 100%);
  color: var(--text);
}
.shell { max-width: 1200px; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }
.hero {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem 1.75rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.25rem;
}
.hero-top { display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.hero h1 { margin: 0; font-size: 1.75rem; font-weight: 650; letter-spacing: -0.02em; }
.hero-sub { color: var(--muted); font-size: 0.95rem; margin: 0.35rem 0 0; }
.pills { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
.pill {
  font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em;
  padding: 0.28rem 0.65rem; border-radius: 999px; border: 1px solid var(--border);
  background: var(--surface-2);
}
.pill-accent { border-color: var(--accent); color: var(--accent); background: var(--accent-dim); }
.next-cmd {
  margin-top: 1rem; padding: 0.75rem 1rem; border-radius: 8px;
  background: var(--accent-dim); border: 1px solid rgba(245, 158, 11, 0.35);
  font-size: 0.92rem;
}
.next-cmd code { color: var(--accent); font-weight: 600; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
@media (max-width: 768px) { .grid-2 { grid-template-columns: 1fr; } }
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
}
.card h2 { margin: 0 0 1rem; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); font-weight: 600; }
.gates { display: flex; gap: 0.6rem; flex-wrap: wrap; }
.gate {
  flex: 1; min-width: 100px; text-align: center; padding: 0.85rem 0.5rem;
  border-radius: 10px; border: 1px solid var(--border); background: var(--surface-2);
}
.gate-label { font-size: 0.72rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
.gate-value { font-size: 1.1rem; font-weight: 700; margin-top: 0.25rem; }
.gate.pass { border-color: var(--pass); background: var(--pass-bg); }
.gate.pass .gate-value { color: var(--pass); }
.gate.fail { border-color: var(--fail); background: var(--fail-bg); }
.gate.fail .gate-value { color: var(--fail); }
.gate.pending { border-color: var(--pending); background: var(--pending-bg); }
.gate.pending .gate-value { color: var(--pending); }
.pipeline-track {
  display: flex; align-items: center; gap: 0; overflow-x: auto; padding: 0.25rem 0;
}
.step {
  flex: 1; min-width: 90px; text-align: center; position: relative; padding: 0.5rem 0.25rem;
}
.step-dot {
  width: 12px; height: 12px; border-radius: 50%; margin: 0 auto 0.4rem;
  background: var(--border); border: 2px solid var(--surface-2);
}
.step.done .step-dot { background: var(--pass); border-color: var(--pass); box-shadow: 0 0 0 3px var(--pass-bg); }
.step.current .step-dot { background: var(--accent); border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-dim); }
.step-label { font-size: 0.72rem; color: var(--muted); font-weight: 600; }
.step.current .step-label { color: var(--accent); }
.step:not(:last-child)::after {
  content: ""; position: absolute; top: 11px; left: calc(50% + 8px); width: calc(100% - 16px);
  height: 2px; background: var(--border); z-index: 0;
}
.step.done:not(:last-child)::after { background: var(--pass); }
.tabs {
  display: flex; gap: 0.35rem; flex-wrap: wrap; margin: 1.25rem 0 0;
  border-bottom: 1px solid var(--border); padding-bottom: 0;
}
.tab {
  padding: 0.55rem 1rem; cursor: pointer; border: none; background: transparent;
  color: var(--muted); font-size: 0.88rem; font-weight: 600; border-radius: 8px 8px 0 0;
  border-bottom: 2px solid transparent; margin-bottom: -1px;
}
.tab:hover { color: var(--text); background: var(--surface-2); }
.tab.active { color: var(--accent); border-bottom-color: var(--accent); background: var(--surface); }
.tab .count {
  display: inline-block; margin-left: 0.35rem; padding: 0.1rem 0.45rem; border-radius: 999px;
  font-size: 0.72rem; background: var(--draft-bg); color: var(--draft);
}
.panel { display: none; animation: fade 0.2s ease; }
.panel.active { display: block; }
@keyframes fade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
.flow-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.75rem; }
.flow-card {
  padding: 1rem; border-radius: 10px; border: 1px solid var(--border);
  background: var(--surface-2); transition: border-color 0.15s;
}
.flow-card:hover { border-color: var(--muted); }
.flow-card.ready { border-left: 3px solid var(--pass); }
.flow-card.draft, .flow-card.clarifying { border-left: 3px solid var(--accent); }
.flow-id { font-weight: 700; font-size: 0.95rem; }
.flow-title { color: var(--muted); font-size: 0.85rem; margin: 0.35rem 0; }
.flow-meta { font-size: 0.75rem; color: var(--muted); }
.empty {
  text-align: center; padding: 2.5rem 1rem; color: var(--muted);
  border: 1px dashed var(--border); border-radius: var(--radius);
}
.draft-list { list-style: none; padding: 0; margin: 0; }
.draft-item {
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.75rem;
  padding: 1rem; border: 1px solid var(--border); border-radius: 10px;
  background: var(--surface-2); margin-bottom: 0.6rem; cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.draft-item:hover, .draft-item.selected { border-color: var(--draft); background: var(--draft-bg); }
.draft-target { font-family: ui-monospace, monospace; font-size: 0.82rem; word-break: break-all; }
.draft-cmd { font-size: 0.75rem; color: var(--muted); }
.badge-await { font-size: 0.72rem; padding: 0.2rem 0.5rem; border-radius: 6px; background: var(--draft-bg); color: var(--draft); font-weight: 600; }
.art-list { list-style: none; padding: 0; margin: 0; max-height: 420px; overflow-y: auto; }
.art-list li {
  padding: 0.55rem 0.75rem; border-radius: 8px; cursor: pointer; font-size: 0.85rem;
  font-family: ui-monospace, monospace; border: 1px solid transparent;
}
.art-list li:hover { background: var(--surface-2); }
.art-list li.selected { background: var(--accent-dim); border-color: rgba(245, 158, 11, 0.4); color: var(--accent); }
.preview-wrap {
  border: 1px solid var(--border); border-radius: var(--radius);
  background: var(--surface); overflow: hidden; min-height: 320px;
}
.preview-header {
  padding: 0.65rem 1rem; background: var(--surface-2); border-bottom: 1px solid var(--border);
  font-family: ui-monospace, monospace; font-size: 0.8rem; color: var(--muted);
}
.preview-body {
  padding: 1.25rem; max-height: 520px; overflow: auto; font-size: 0.92rem;
}
.preview-body pre, .preview-body .md-fallback {
  white-space: pre-wrap; word-break: break-word; margin: 0;
  font-family: ui-monospace, monospace; font-size: 0.82rem;
}
.preview-body h1, .preview-body h2, .preview-body h3 { margin-top: 1rem; color: var(--text); }
.preview-body table { border-collapse: collapse; width: 100%; margin: 0.5rem 0; }
.preview-body th, .preview-body td { border: 1px solid var(--border); padding: 0.4rem 0.6rem; text-align: left; }
.preview-body a { color: var(--accent); }
.split { display: grid; grid-template-columns: 280px 1fr; gap: 1rem; }
@media (max-width: 900px) { .split { grid-template-columns: 1fr; } }
.help {
  margin-top: 1.5rem; padding: 1rem 1.25rem; border-radius: var(--radius);
  background: var(--surface-2); border: 1px solid var(--border); font-size: 0.88rem; color: var(--muted);
}
.help strong { color: var(--text); }
.footer { margin-top: 2rem; text-align: center; font-size: 0.78rem; color: var(--muted); }
.discover-summary { margin-bottom: 1.25rem; }
.discover-summary-label { font-size: 0.82rem; font-weight: 600; color: var(--muted); margin-bottom: 0.4rem; }
.field-bar-lg { height: 10px; margin-top: 0.25rem; }
.field-row {
  display: grid; grid-template-columns: minmax(120px, 150px) 1fr minmax(72px, 88px);
  gap: 0.5rem 0.75rem; align-items: center; margin-bottom: 0.85rem;
}
.field-label { font-size: 0.84rem; font-weight: 600; }
.field-bar { height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; }
.field-bar-fill { height: 100%; border-radius: 4px; min-width: 2px; }
.field-bar-fill.ready { background: var(--pass); }
.field-bar-fill.draft { background: var(--draft); }
.field-bar-fill.partial { background: var(--accent); }
.field-bar-fill.pending { background: var(--border); }
.field-status { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; text-align: right; }
.status-ready { color: var(--pass); }
.status-draft { color: var(--draft); }
.status-partial { color: var(--accent); }
.status-pending { color: var(--pending); }
.field-hint { grid-column: 1 / -1; font-size: 0.72rem; color: var(--muted); margin: -0.35rem 0 0; padding-left: 0.15rem; }
.discover-legend { display: flex; flex-wrap: wrap; gap: 0.75rem; font-size: 0.72rem; color: var(--muted); margin-bottom: 1rem; }
.discover-legend span::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 0.35rem; vertical-align: middle; }
.legend-ready::before { background: var(--pass); }
.legend-draft::before { background: var(--draft); }
.legend-partial::before { background: var(--accent); }
.legend-pending::before { background: var(--border); }
.plantuml-diagram { margin: 1rem 0; overflow-x: auto; }
.plantuml-diagram svg { max-width: 100%; height: auto; display: block; }
.plantuml-hint {
  margin: 0.5rem 0 1rem; padding: 0.75rem 1rem; border-radius: 8px;
  border: 1px dashed var(--border); background: var(--surface-2);
  color: var(--muted); font-size: 0.85rem;
}
.plantuml-hint code { color: var(--accent); font-size: 0.82rem; }
"""


def render_shell(title: str, body: str, extra_script: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{escape(title)}</title>
<style>{shared_styles()}</style>
</head>
<body>
<div class="shell">
{body}
<p class="footer">Gerado {escape(datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC"))} · read-only · domain-kit</p>
</div>
<script>{extra_script}</script>
</body>
</html>"""


def build_product_dashboard(hub: Path, product: str) -> str:
    product_dir = hub / "products" / product
    plantuml_server = load_plantuml_server(hub)
    status: dict = {}
    sp = product_dir / "domain-status.json"
    if sp.exists():
        status = json.loads(sp.read_text(encoding="utf-8"))

    gates = gate_status(hub, product)
    flows = parse_flows_registry(product_dir / "flows-registry.yml")
    artifacts = collect_artifacts(product_dir)
    draft_manifest = load_draft_manifest(product_dir)
    pending = draft_manifest.get("pending", [])
    draft_files = collect_draft_files(product_dir)

    phase = str(status.get("phase", "init"))
    scan = str(status.get("scan", "pending"))
    next_cmd = status.get("nextSuggested", "/domain.discover")
    p_idx = phase_index(phase)

    discover_fields = compute_discover_fields(product_dir, status)
    discover_html, discover_total = render_discover_progress(discover_fields)

    gate_html = []
    for g, v in gates.items():
        cls = "pass" if v == "PASS" else "fail" if v == "FAIL" else "pending"
        gate_html.append(
            f'<div class="gate {cls}"><div class="gate-label">{g}</div>'
            f'<div class="gate-value">{escape(v)}</div></div>'
        )

    steps_html = []
    for i, (key, label, _cmd) in enumerate(PIPELINE_STEPS):
        cls = "done" if i < p_idx else "current" if i == p_idx else ""
        steps_html.append(
            f'<div class="step {cls}"><div class="step-dot"></div><div class="step-label">{escape(label)}</div></div>'
        )

    flow_cards = []
    for f in flows:
        st = f.get("status", "draft")
        deps = ", ".join(f.get("deps", [])) or "—"
        flow_cards.append(
            f'<div class="flow-card {escape(st)}">'
            f'<div class="flow-id">{escape(f.get("id", "?"))}</div>'
            f'<div class="flow-title">{escape(f.get("title", "Sem título"))}</div>'
            f'<div class="flow-meta">bc: {escape(f.get("bc", "—"))} · deps: {escape(deps)} · {escape(st)}</div>'
            f"</div>"
        )
    flow_html = "".join(flow_cards) or '<div class="empty">Nenhum fluxo registrado.<br/><small>Use <code>/domain.flow</code> após discover.</small></div>'

    draft_count = len(pending) or len(draft_files)
    draft_badge = f'<span class="count">{draft_count}</span>' if draft_count else ""

    draft_items = []
    if pending:
        for entry in pending:
            target = entry.get("targetPath", "?")
            cmd = entry.get("command", "—")
            draft_items.append(
                f'<li class="draft-item" data-draft-key="{escape(target)}" role="button" tabindex="0">'
                f'<div><div class="draft-target">{escape(target)}</div>'
                f'<div class="draft-cmd">{escape(cmd)}</div></div>'
                f'<span class="badge-await">aguardando OK</span></li>'
            )
    elif draft_files:
        for rel, _ in draft_files:
            draft_items.append(
                f'<li class="draft-item" data-draft-key="{escape(rel)}" role="button" tabindex="0">'
                f'<div><div class="draft-target">{escape(rel)}</div>'
                f'<div class="draft-cmd">arquivo em .draft/</div></div>'
                f'<span class="badge-await">rascunho</span></li>'
            )
    draft_list_html = "".join(draft_items) or (
        '<div class="empty">Nenhum rascunho pendente.<br/><small>Plan mode: artefatos aparecem aqui antes do promote.</small></div>'
    )

    art_count = len(artifacts)
    art_items = "".join(
        f'<li data-doc="{escape(rel)}" role="button" tabindex="0">{escape(rel)}</li>'
        for rel, _ in artifacts
    ) or '<li class="empty" style="list-style:none">Nenhum artefato promovido ainda.</li>'

    docs_payload: dict[str, str] = {}
    for rel, path in artifacts:
        try:
            docs_payload[rel] = file_to_preview_html(path, plantuml_server)
        except OSError:
            docs_payload[rel] = "<p><em>Erro ao ler arquivo.</em></p>"

    drafts_payload: dict[str, str] = {}
    for rel, path in draft_files:
        try:
            drafts_payload[rel] = file_to_preview_html(path, plantuml_server)
        except OSError:
            drafts_payload[rel] = "<p><em>Erro ao ler rascunho.</em></p>"

    # map targetPath -> draftPath content for pending entries
    for entry in pending:
        target = entry.get("targetPath", "")
        draft_path = entry.get("draftPath", "").lstrip("./")
        full = product_dir / draft_path if draft_path else None
        if target and full and full.is_file():
            drafts_payload[target] = file_to_preview_html(full, plantuml_server)

    first_preview = ""
    first_key = ""
    if drafts_payload:
        first_key = next(iter(drafts_payload))
        first_preview = drafts_payload[first_key]
    elif docs_payload:
        first_key = next(iter(docs_payload))
        first_preview = docs_payload[first_key]
    else:
        first_preview = '<p class="empty" style="border:none">Selecione um artefato ou rascunho na lista.</p>'

    script = f"""
const DOCS = {json.dumps(docs_payload)};
const DRAFTS = {json.dumps(drafts_payload)};
const PLANTUML_SERVER = {json.dumps(plantuml_server)};

function showTab(name) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.tab === name));
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('active', p.dataset.panel === name));
}}

async function renderPlantUmlIn(container) {{
  const blocks = container.querySelectorAll(
    'pre code.language-plantuml, pre code.language-uml, pre code.language-puml'
  );
  if (!blocks.length) return;
  let showedHint = false;
  for (const block of blocks) {{
    const pre = block.closest('pre');
    if (!pre || pre.dataset.plantumlDone) continue;
    const source = block.textContent;
    try {{
      const resp = await fetch(PLANTUML_SERVER + '/svg', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'text/plain' }},
        body: source,
      }});
      if (!resp.ok) throw new Error(resp.statusText);
      const svg = await resp.text();
      const wrap = document.createElement('div');
      wrap.className = 'plantuml-diagram';
      wrap.innerHTML = svg;
      pre.replaceWith(wrap);
    }} catch (err) {{
      if (!showedHint) {{
        const hint = document.createElement('div');
        hint.className = 'plantuml-hint';
        hint.innerHTML = '<p><em>Diagrama PlantUML não renderizado.</em> Suba o servidor local: '
          + '<code>.domain/scripts/start_plantuml_server.sh</code> '
          + '(porta 8765). Ver <code>domain-kit/references/plantuml-dashboard.md</code>.</p>';
        pre.insertAdjacentElement('afterend', hint);
        showedHint = true;
      }}
      pre.dataset.plantumlDone = 'failed';
    }}
  }}
}}

async function setPreview(key, html, label) {{
  document.getElementById('preview-path').textContent = label || key || '—';
  const el = document.getElementById('doc-preview');
  el.innerHTML = html || '<p class="empty">Sem conteúdo.</p>';
  await renderPlantUmlIn(el);
}}

document.querySelectorAll('.tab').forEach(tab => {{
  tab.addEventListener('click', () => showTab(tab.dataset.tab));
}});

document.querySelectorAll('.art-list li[data-doc]').forEach(li => {{
  li.addEventListener('click', () => {{
    document.querySelectorAll('.art-list li').forEach(x => x.classList.remove('selected'));
    li.classList.add('selected');
    const k = li.dataset.doc;
    setPreview(k, DOCS[k], k);
    showTab('preview');
  }});
}});

document.querySelectorAll('.draft-item').forEach(li => {{
  li.addEventListener('click', () => {{
    document.querySelectorAll('.draft-item').forEach(x => x.classList.remove('selected'));
    li.classList.add('selected');
    const k = li.dataset.draftKey;
    const html = DRAFTS[k] || DRAFTS['.draft/' + k] || Object.entries(DRAFTS).find(([p]) => p.endsWith(k))?.[1];
    setPreview(k, html, 'draft → ' + k);
    showTab('preview');
  }});
}});

showTab('overview');
setPreview({json.dumps(first_key)}, {json.dumps(first_preview)}, {json.dumps(first_key)});
"""

    body = f"""
<header class="hero">
  <div class="hero-top">
    <div>
      <h1>{escape(product)}</h1>
      <p class="hero-sub">Domain-kit · mapeamento negócio → domínio</p>
    </div>
    <div class="pills">
      <span class="pill pill-accent">fase: {escape(phase)}</span>
      <span class="pill">scan: {escape(scan)}</span>
      <span class="pill">discover: {discover_total}%</span>
      <span class="pill">{art_count} artefatos</span>
    </div>
  </div>
  <div class="next-cmd">Próximo comando sugerido: <code>{escape(next_cmd)}</code></div>
</header>

<div class="grid-2">
  <div class="card">
    <h2>Gates</h2>
    <div class="gates">{''.join(gate_html)}</div>
  </div>
  <div class="card">
    <h2>Pipeline</h2>
    <div class="pipeline-track">{''.join(steps_html)}</div>
  </div>
</div>

<nav class="tabs">
  <button type="button" class="tab active" data-tab="overview">Visão geral</button>
  <button type="button" class="tab" data-tab="drafts">Rascunhos{draft_badge}</button>
  <button type="button" class="tab" data-tab="artifacts">Artefatos ({art_count})</button>
  <button type="button" class="tab" data-tab="preview">Preview</button>
</nav>

<section class="panel active" data-panel="overview">
  <div class="card" style="margin-top:1rem;margin-bottom:0.75rem">
    <h2>Onde acompanhar</h2>
    <ul class="art-list" style="margin:0">
      <li><code>products/{escape(product)}/dashboard.html</code> — este painel (aba Rascunhos)</li>
      <li><code>products/{escape(product)}/.draft/</code> — arquivos aguardando OK</li>
      <li><code>products/{escape(product)}/CHANGELOG.md</code> — log após promotes</li>
    </ul>
  </div>
  <div class="card" style="margin-top:1rem">
    <h2>Progresso discover</h2>
    <div class="discover-legend">
      <span class="legend-ready">Pronto (promovido)</span>
      <span class="legend-draft">Rascunho (.draft/)</span>
      <span class="legend-partial">Parcial</span>
      <span class="legend-pending">Pendente</span>
    </div>
    {discover_html}
  </div>
  <div class="card" style="margin-top:1rem">
    <h2>Fluxos entregáveis</h2>
    <div class="flow-grid">{flow_html}</div>
  </div>
</section>

<section class="panel" data-panel="drafts">
  <div class="card" style="margin-top:1rem">
    <h2>Rascunhos pendentes (plan mode)</h2>
    <p style="color:var(--muted);font-size:0.88rem;margin:0 0 1rem">
      Conteúdo em <code>.draft/</code> aguardando <code>ok</code> / <code>pode gravar</code> no chat.
      {f' Atualizado: {escape(str(draft_manifest.get("updatedAt") or "—"))}.' if draft_manifest.get("updatedAt") else ""}
    </p>
    <ul class="draft-list">{draft_list_html}</ul>
  </div>
</section>

<section class="panel" data-panel="artifacts">
  <div class="card" style="margin-top:1rem">
    <h2>Artefatos promovidos</h2>
    <div class="split">
      <ul class="art-list">{art_items}</ul>
      <p style="color:var(--muted);font-size:0.85rem;margin:0">Clique para preview →</p>
    </div>
  </div>
</section>

<section class="panel" data-panel="preview">
  <div class="preview-wrap" style="margin-top:1rem">
    <div class="preview-header" id="preview-path">{escape(first_key or "—")}</div>
    <div class="preview-body" id="doc-preview">{first_preview}</div>
  </div>
</section>

<div class="help">
  <strong>Plan mode</strong> — rascunhos não contam em gates até promote.
  Discover unificado (fontes + DDD). Docs: <code>domain-kit/GUIDE.md</code>
</div>
"""

    return render_shell(f"Domain-Kit — {product}", body, script)


def build_hub_index(hub: Path) -> str:
    products_dir = hub / "products"
    cards = []
    if products_dir.is_dir():
        for p in sorted(products_dir.iterdir()):
            if not p.is_dir():
                continue
            status_path = p / "domain-status.json"
            if not status_path.exists():
                continue
            try:
                st = json.loads(status_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                st = {}
            phase = st.get("phase", "?")
            next_cmd = st.get("nextSuggested", "—")
            draft_n = 0
            dm = p / ".draft" / "manifest.json"
            if dm.exists():
                try:
                    draft_n = len(json.loads(dm.read_text(encoding="utf-8")).get("pending", []))
                except json.JSONDecodeError:
                    pass
            draft_hint = f' · <span style="color:var(--draft)">{draft_n} rascunho(s)</span>' if draft_n else ""
            cards.append(
                f'<a class="product-card" href="products/{escape(p.name)}/dashboard.html">'
                f'<div class="product-name">{escape(p.name)}</div>'
                f'<div class="product-meta">fase: {escape(str(phase))} · próximo: <code>{escape(str(next_cmd))}</code>{draft_hint}</div>'
                f"</a>"
            )

    extra_css = """
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin-top: 1.5rem; }
.product-card {
  display: block; text-decoration: none; color: inherit; padding: 1.25rem;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
  transition: border-color 0.15s, transform 0.15s;
}
.product-card:hover { border-color: var(--accent); transform: translateY(-2px); }
.product-name { font-size: 1.15rem; font-weight: 650; margin-bottom: 0.5rem; }
.product-meta { font-size: 0.82rem; color: var(--muted); }
.product-meta code { color: var(--accent); font-size: 0.78rem; }
"""
    body = f"""
<style>{extra_css}</style>
<header class="hero">
  <h1>Architecture Hub</h1>
  <p class="hero-sub">Domain-kit — produtos em mapeamento de domínio</p>
</header>
<div class="product-grid">{''.join(cards) or '<div class="empty">Nenhum produto com domain-status.json</div>'}</div>
"""
    return render_shell("Domain-Kit Index", body)


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
