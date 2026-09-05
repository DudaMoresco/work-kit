#!/usr/bin/env python3
"""Generate static HTML dashboard for domain-kit product progress."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from html import escape
from pathlib import Path

PIPELINE_STEPS = [
    ("evidencias", "Evidências", "/domain.init"),
    ("estrategico", "Estratégico", "/domain.discover"),
    ("descoberta", "Descoberta", "/domain.discover"),
    ("operacional", "Operacional", "/domain.flow"),
]

PHASE_ORDER = ["evidencias", "estrategico", "descoberta", "operacional"]

PHASE_DISPLAY: dict[str, dict[str, str | None]] = {
    "evidencias": {
        "title": "Evidências indexadas",
        "subtitle": "Pré-requisito",
        "description": (
            "Repositórios e documentos externos mapeados. "
            "O hub sabe de onde tirar evidências sobre o produto."
        ),
        "command": "/domain.scan",
        "handoff": None,
    },
    "estrategico": {
        "title": "Modelagem estratégica",
        "subtitle": "Fase Estratégico",
        "description": (
            "Problema de negócio, visão, subdomínios, bounded contexts "
            "e linguagem ubíqua — legível por produto e engenharia."
        ),
        "command": "/domain.discover --stage strategic|contexts",
        "handoff": None,
    },
    "descoberta": {
        "title": "Descoberta do domínio",
        "subtitle": "Fase Descoberta",
        "description": (
            "Domain stories e/ou event storming — como o domínio "
            "se comporta no tempo e no dia a dia."
        ),
        "command": "/domain.discover --stage stories|event-storming",
        "handoff": None,
    },
    "operacional": {
        "title": "Cenários operacionais",
        "subtitle": "Fase Operacional",
        "description": (
            "Fluxos de negócio ponta a ponta, requisitos de produto (NFRs) "
            "e decisões D-n — sem design tático nem integração técnica."
        ),
        "command": "/domain.flow",
        "handoff": "Fim do domain-kit",
    },
}

# compat alias for render_gate_card
GATE_DISPLAY = PHASE_DISPLAY

DEFAULT_PLANTUML_SERVER = "http://127.0.0.1:8765"
DASHBOARD_ASSETS_REL = "dashboard-assets"
DASHBOARD_VENDOR_REL = f"{DASHBOARD_ASSETS_REL}/vendor"
DASHBOARD_VENDOR_FILES = ("marked.min.js", "mermaid.min.js")
DASHBOARD_UI_FILES = ("dashboard.css", "dashboard.js", "hub-index.css")
DASHBOARD_TEMPLATE_DIR = Path(__file__).resolve().parent / "dashboard"


def _dashboard_templates_dir() -> Path:
    return DASHBOARD_TEMPLATE_DIR


def load_dashboard_template(name: str) -> str:
    path = _dashboard_templates_dir() / name
    if not path.is_file():
        raise FileNotFoundError(f"Dashboard template missing: {path}")
    return path.read_text(encoding="utf-8")


def fill_template(template: str, mapping: dict[str, str]) -> str:
    """Replace {{KEY}} placeholders. Values must already be escaped when needed."""
    out = template
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    leftover = re.findall(r"\{\{([A-Z0-9_]+)\}\}", out)
    if leftover:
        raise ValueError(f"Unfilled dashboard placeholders: {sorted(set(leftover))}")
    return out


def sync_dashboard_vendor_assets(hub: Path) -> Path:
    """Copy vendor + UI assets to hub (Cursor/Simple Browser blocks .domain/)."""
    scripts_dir = Path(__file__).resolve().parent
    vendor_src = scripts_dir / "vendor"
    vendor_dest = hub / DASHBOARD_VENDOR_REL
    vendor_dest.mkdir(parents=True, exist_ok=True)
    for name in DASHBOARD_VENDOR_FILES:
        src = vendor_src / name
        if not src.is_file():
            print(
                f"Warning: vendor asset missing ({src}); "
                "markdown/mermaid preview may be limited.",
                file=sys.stderr,
            )
            continue
        shutil.copy2(src, vendor_dest / name)

    ui_src = scripts_dir / "dashboard"
    ui_dest = hub / DASHBOARD_ASSETS_REL
    ui_dest.mkdir(parents=True, exist_ok=True)
    for name in DASHBOARD_UI_FILES:
        src = ui_src / name
        if not src.is_file():
            print(f"Warning: dashboard UI asset missing ({src})", file=sys.stderr)
            continue
        shutil.copy2(src, ui_dest / name)
    return ui_dest


def dashboard_asset_prefix(depth: int = 2) -> str:
    """Relative path from dashboard.html to dashboard-assets/."""
    prefix = "/".join([".."] * depth) if depth else "."
    return f"{prefix}/{DASHBOARD_ASSETS_REL}" if depth else f"./{DASHBOARD_ASSETS_REL}"


def dashboard_vendor_script_tags(depth: int = 2) -> str:
    """Script tags relative to dashboard.html (products/{p}/ = depth 2)."""
    base = f"{dashboard_asset_prefix(depth)}/vendor"
    cdn = {
        "marked.min.js": "https://cdn.jsdelivr.net/npm/marked@11.1.1/marked.min.js",
        "mermaid.min.js": "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js",
    }
    tags = []
    for name in DASHBOARD_VENDOR_FILES:
        local = f"{base}/{name}"
        fallback = cdn.get(name, "")
        if fallback:
            tags.append(
                f'<script src="{local}" '
                f"onerror=\"this.onerror=null;this.src='{fallback}'\"></script>"
            )
        else:
            tags.append(f'<script src="{local}"></script>')
    return "\n".join(tags)


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


def file_to_preview_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


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


def phase_status(hub: Path, product: str) -> dict[str, str]:
    script = Path(__file__).resolve().parent / "validate_gate.py"
    out: dict[str, str] = {}
    try:
        r = subprocess.run(
            [sys.executable, str(script), "--hub", str(hub), "--product", product, "--json"],
            capture_output=True,
            text=True,
        )
        if r.stdout.strip():
            data = json.loads(r.stdout)
            for p in PHASE_ORDER:
                phase_data = data.get("phases", {}).get(p, {})
                out[p] = "PASS" if phase_data.get("pass") else "FAIL"
    except (OSError, json.JSONDecodeError):
        for p in PHASE_ORDER:
            out[p] = "?"
    return out


def gate_status(hub: Path, product: str) -> dict[str, str]:
    """compat — maps phases to G0/G1/G2."""
    phases = phase_status(hub, product)
    g0 = phases.get("evidencias") == "PASS"
    g1 = phases.get("estrategico") == "PASS" and phases.get("descoberta") == "PASS"
    g2 = phases.get("operacional") == "PASS"
    return {
        "G0": "PASS" if g0 else "FAIL",
        "G1": "PASS" if g1 else "FAIL",
        "G2": "PASS" if g2 else "FAIL",
    }


def collect_artifacts(product_dir: Path) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    seen: set[str] = set()

    def add(rel: str, p: Path) -> None:
        if rel in seen or not p.is_file():
            return
        seen.add(rel)
        found.append((rel, p))

    for name in ("CHANGELOG.md", "README.md", "product-README.md", "sources.yml", "flows-registry.yml"):
        add(name, product_dir / name)

    patterns = [
        "01-product/**/*.md",
        "05-decisoes/*.md",
        "arch/**/*.md",
    ]
    for pat in patterns:
        for p in sorted(product_dir.glob(pat)):
            rel = p.relative_to(product_dir).as_posix()
            if rel.startswith(".draft/"):
                continue
            add(rel, p)
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
    mapping = {
        "evidencias": 0,
        "init": 0,
        "scan": 0,
        "init_complete": 0,
        "estrategico": 1,
        "estrategico-in-progress": 1,
        "discover": 1,
        "discover_complete": 2,
        "descoberta": 2,
        "descoberta-in-progress": 2,
        "operacional": 3,
        "operacional-in-progress": 3,
        "model": 3,
        "model-in-progress": 3,
        "model_complete": 4,
        "domain-complete": 4,
        "done": 4,
        "flow": 3,
    }
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

    # Domain stories (≥2 MD recomendado)
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


def _file_field(
    key: str,
    label: str,
    product_dir: Path,
    discover: dict,
    rel: str,
    alt_rels: list[str] | None = None,
) -> dict:
    alt_rels = alt_rels or []
    canonical = (product_dir / rel).is_file() or any(
        (product_dir / a).is_file() for a in alt_rels
    )
    draft = _draft_has(product_dir, rel) or any(
        _draft_has(product_dir, a) for a in alt_rels
    )
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


def render_pipeline_bar(phase_index: int) -> str:
    parts: list[str] = []
    for i, (_key, label, cmd) in enumerate(PIPELINE_STEPS):
        cls = "done" if i < phase_index else "current" if i == phase_index else "upcoming"
        parts.append(
            f'<div class="pipe-step {cls}">'
            f'<span class="pipe-step-label">{escape(label)}</span>'
            f'<span class="pipe-step-cmd">{escape(cmd)}</span>'
            f"</div>"
        )
        if i < len(PIPELINE_STEPS) - 1:
            conn_cls = "done" if i < phase_index else ""
            parts.append(f'<div class="pipe-connector {conn_cls}"></div>')
    return f'<div class="pipeline-bar">{"".join(parts)}</div>'


def compute_operacional_fields(product_dir: Path, status: dict) -> list[dict]:
    """Progress for operacional phase artifacts."""
    model = status.get("operacional") or status.get("model") or {}
    fields: list[dict] = []

    req_path = "01-product/04-operacional/requisitos.md"
    fields.append(
        _file_field(
            "requisitos",
            "Requisitos NFR (produto)",
            product_dir,
            model,
            req_path,
        )
    )

    reg_path = product_dir / "flows-registry.yml"
    op_dir = product_dir / "01-product/04-operacional/fluxos"
    n_op = _count_md_in_dir(op_dir)
    if reg_path.is_file():
        text = reg_path.read_text(encoding="utf-8")
        ready = len(re.findall(r"status:\s*ready", text))
        total = len(re.findall(r"id:\s*fluxo-", text))
        if ready >= 1:
            f_state, f_pct, f_hint = "ready", 100, f"{ready} fluxo(s) ready"
        elif total >= 1:
            f_state, f_pct, f_hint = "partial", 50, f"{total} fluxo(s) em draft"
        elif n_op >= 1:
            f_state, f_pct, f_hint = "partial", 60, f"{n_op} MD em operacional/"
        else:
            f_state, f_pct, f_hint = "pending", 0, "nenhum fluxo"
    elif n_op >= 1:
        f_state, f_pct, f_hint = "ready", 100, f"{n_op} fluxo(s) em operacional/"
    else:
        f_state, f_pct, f_hint = "pending", 0, "pendente"
    fields.append(
        {"key": "fluxos", "label": "Fluxos operacionais", "pct": f_pct, "state": f_state, "hint": f_hint}
    )

    reg_md = "05-decisoes/produto.md"
    fields.append(
        _file_field(
            "registry",
            "Registry D-n",
            product_dir,
            model,
            reg_md,
        )
    )
    return fields


def render_phase_card(phase_id: str, status: str, *, compact: bool = False) -> str:
    meta = PHASE_DISPLAY.get(phase_id, {})
    title = str(meta.get("title", phase_id))
    subtitle = str(meta.get("subtitle", phase_id))
    description = str(meta.get("description", ""))
    command = str(meta.get("command", "—"))
    handoff = meta.get("handoff")
    cls = "pass" if status == "PASS" else "fail" if status == "FAIL" else "pending"
    badge = "Completo" if status == "PASS" else "Pendente" if status == "FAIL" else status
    handoff_html = ""
    if handoff:
        handoff_html = (
            f'<span class="phase-card-meta-item">Handoff: <strong>{escape(handoff)}</strong></span>'
        )
    desc_html = "" if compact else f'<p class="phase-card-desc">{escape(description)}</p>'
    return (
        f'<article class="phase-card {cls}">'
        f'<div class="phase-card-head">'
        f'<span class="phase-card-sub">{escape(subtitle)}</span>'
        f'<span class="phase-card-badge">{escape(badge)}</span>'
        f"</div>"
        f'<h4 class="phase-card-title">{escape(title)}</h4>'
        f"{desc_html}"
        f'<div class="phase-card-meta">'
        f'<span class="phase-card-meta-item">Comando: <code>{escape(command)}</code></span>'
        f"{handoff_html}"
        f"</div>"
        f"</article>"
    )


def render_gate_card(gate_id: str, status: str) -> str:
    """compat — thin redirect to phase cards."""
    gate_map = {"G0": "evidencias", "G1": "estrategico", "G2": "operacional"}
    pid = gate_map.get(gate_id, gate_id)
    if pid in PHASE_DISPLAY:
        return render_phase_card(pid, status)
    return render_phase_card(gate_id, status)


def _extract_product_readme_fields(text: str) -> dict[str, str]:
    """Pull short PM lines from product-README.md."""
    out: dict[str, str] = {}
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    if title_m:
        out["title"] = title_m.group(1).strip()
    for key, label in (
        ("o_que_e", r"O que é"),
        ("problema", r"Problema que resolve"),
        ("onde", r"Onde está disponível"),
    ):
        m = re.search(rf"\*\*{label}:\*\*\s*(.+)$", text, re.M)
        if m:
            out[key] = m.group(1).strip()
    return out


def render_product_hero(product_dir: Path, phases: dict[str, str]) -> str:
    """Hero cartão PM from product-README.md (Onda 1 layout)."""
    card = product_dir / "product-README.md"
    if not card.is_file():
        return (
            '<div class="product-hero product-hero-empty">'
            "<p>Sem <code>product-README.md</code> — rode <code>/domain.init</code>.</p>"
            "</div>"
        )
    fields = _extract_product_readme_fields(card.read_text(encoding="utf-8"))
    title = fields.get("title") or product_dir.name
    o_que = fields.get("o_que_e", "")
    problema = fields.get("problema", "")
    pills = "".join(
        f'<span class="phase-pill {escape(phases.get(p, "?").lower())}">'
        f"{escape(str(PHASE_DISPLAY.get(p, {}).get('subtitle', p)))} · "
        f"{escape(phases.get(p, '?'))}</span>"
        for p in PHASE_ORDER
    )
    body_bits = []
    if o_que:
        body_bits.append(f"<p><strong>O que é:</strong> {escape(o_que)}</p>")
    if problema:
        body_bits.append(f"<p><strong>Problema:</strong> {escape(problema)}</p>")
    if not body_bits:
        body_bits.append(
            '<p class="muted">Preencha a visão geral no cartão após contexts.</p>'
        )
    return (
        f'<section class="product-hero" aria-label="Cartão do produto">'
        f'<div class="product-hero-top">'
        f'<div class="product-hero-copy">'
        f'<p class="product-hero-kicker">Cartão do produto</p>'
        f"<h2>{escape(title)}</h2>"
        f"{''.join(body_bits)}"
        f"</div>"
        f'<a class="btn-product-card" data-doc="product-README.md" href="#">'
        f"Abrir product-README.md</a>"
        f"</div>"
        f'<div class="product-hero-pills">{pills}</div>'
        f"</section>"
    )


def render_product_card_link(product_dir: Path) -> str:
    """Backward-compatible alias — prefer render_product_hero."""
    return render_product_hero(product_dir, {p: "?" for p in PHASE_ORDER})


def render_active_change_banner(status: dict) -> str:
    """Banner when an evolutionary session is open (/domain.change)."""
    ac = status.get("activeChange")
    if not ac or not isinstance(ac, dict):
        return (
            '<div class="active-change-empty" role="status">'
            "<strong>Nenhuma sessão evolutiva</strong> — use "
            "<code>/domain.change</code> para problema (P-n) ou evolução (E-n)."
            "</div>"
        )
    kind = ac.get("kind", "—")
    cid = ac.get("id", "—")
    title = ac.get("title", "")
    cmd = ac.get("suggestedCommand", "")
    phases = ", ".join(ac.get("phasesImpacted", [])) or "—"
    title_bit = f" — {escape(str(title))}" if title else ""
    cmd_bit = (
        f'<p class="active-change-cmd">Próximo: <code>{escape(cmd)}</code></p>'
        if cmd
        else ""
    )
    doc_link = (
        "01-product/02-domain/evolucoes.md"
        if str(kind).startswith("evolution") or str(cid).upper().startswith("E")
        else "01-product/02-domain/abertos.md"
    )
    link_label = "evolucoes.md" if "evolucoes" in doc_link else "abertos.md"
    return (
        f'<div class="active-change-banner" role="status">'
        f'<div class="active-change-main">'
        f"<strong>Sessão ativa</strong> · {escape(str(kind))} · "
        f"<code>{escape(str(cid))}</code>{title_bit}"
        f'<span class="active-change-phases">Fases: {escape(phases)}</span>'
        f"{cmd_bit}"
        f"</div>"
        f'<div class="active-change-actions">'
        f'<a class="btn-inline" data-doc="{escape(doc_link)}" href="#">{escape(link_label)}</a>'
        f'<span class="active-change-hint">Encerrar: <code>/domain.change --close</code></span>'
        f"</div>"
        f"</div>"
    )


def render_next_cta(next_cmd: str, reason: str) -> str:
    return (
        f'<section class="next-cta" aria-label="Próximo comando">'
        f'<p class="next-cta-kicker">Próximo comando</p>'
        f'<code class="next-cta-cmd">{escape(next_cmd)}</code>'
        f'<p class="next-cta-reason">{escape(reason)}</p>'
        f"</section>"
    )


def _cta_reason(phases: dict[str, str], operacional_fields: list[dict] | None) -> str:
    for p in PHASE_ORDER:
        if phases.get(p) != "PASS":
            if p == "operacional" and operacional_fields:
                for f in operacional_fields:
                    if f.get("state") in ("pending", "partial", "draft"):
                        return f"{f['label']}: {f.get('hint', 'pendente')}"
            label = PHASE_DISPLAY.get(p, {}).get("subtitle", p)
            return f"Fase {label} incompleta"
    return "Operacional ok — modelagem do domain-kit concluída"


def render_flows_grade(flows: list[dict]) -> str:
    if not flows:
        return (
            '<p class="home-section-hint">Nenhum fluxo no registry — '
            "<code>/domain.flow 01</code>.</p>"
        )
    by_id = {f.get("id"): f for f in flows if f.get("id")}
    rows = []
    for f in flows:
        fid = f.get("id", "?")
        st = f.get("status", "draft")
        deps = f.get("deps") or []
        dep_notes: list[str] = []
        blocked = False
        for d in deps:
            if d not in by_id:
                dep_notes.append(f"missing {d}")
                blocked = True
            elif by_id[d].get("status") != "ready":
                dep_notes.append(f"{d} not ready")
                blocked = True
        st_label = "blocked" if blocked and st != "ready" else st
        dep_txt = ", ".join(dep_notes) if dep_notes else ("—" if not deps else ", ".join(deps))
        path = str(f.get("path", "—"))
        path_display = path
        old_path = ""
        rows.append(
            f'<tr class="flow-row {escape(st_label)} {old_path}">'
            f"<td><code>{escape(fid)}</code></td>"
            f'<td><span class="flow-status {escape(st_label)}">{escape(st_label)}</span></td>'
            f"<td>{escape(dep_txt)}</td>"
            f'<td class="flow-path">{escape(path_display)}</td>'
            f"</tr>"
        )
    return (
        '<table class="flows-grade">'
        "<thead><tr><th>ID</th><th>Status</th><th>Deps</th><th>Path</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>"
    )


def render_operacional_checklist(operacional_fields: list[dict]) -> str:
    if not operacional_fields:
        return ""
    items = []
    for f in operacional_fields:
        st = f.get("state", "pending")
        mark = "✓" if st == "ready" else "·"
        items.append(
            f'<li class="op-check {escape(st)}">'
            f'<span class="op-check-mark">{mark}</span> '
            f'{escape(f["label"])} '
            f'<span class="op-check-hint">{escape(f.get("hint", ""))}</span>'
            f"</li>"
        )
    return f'<ul class="op-checklist">{"".join(items)}</ul>'


def render_discover_home(
    fields: list[dict],
    total_pct: int,
    next_cmd: str,
    phases: dict[str, str],
    phase_index: int,
    operacional_fields: list[dict] | None = None,
    product_card_html: str = "",
    active_change_html: str = "",
    flows: list[dict] | None = None,
) -> str:
    if not fields and not product_card_html:
        return '<div class="empty">Nenhum artefato configurado.</div>'
    state_label = {
        "ready": "Pronto",
        "draft": "Rascunho",
        "partial": "Parcial",
        "pending": "Pendente",
    }
    field_cards = []
    for f in fields:
        st = f["state"]
        field_cards.append(
            f'<div class="discover-field-card">'
            f'<div class="discover-field-head">'
            f'<span class="discover-field-dot {escape(st)}"></span>'
            f'<span class="discover-field-label">{escape(f["label"])}</span>'
            f'<span class="field-status status-{escape(st)}">{escape(state_label.get(st, st))}</span>'
            f"</div>"
            f'<div class="field-bar"><div class="field-bar-fill {escape(st)}" style="width:{f["pct"]}%"></div></div>'
            f'<div class="discover-field-hint">{escape(f.get("hint", ""))}</div>'
            f"</div>"
        )
    fill_cls = "ready" if total_pct >= 100 else "partial" if total_pct > 0 else "pending"
    current_label = (
        PIPELINE_STEPS[phase_index][1]
        if 0 <= phase_index < len(PIPELINE_STEPS)
        else "Concluído"
    )
    current_key = (
        PIPELINE_STEPS[phase_index][0]
        if 0 <= phase_index < len(PIPELINE_STEPS)
        else ""
    )
    current_phase_html = ""
    if current_key in PHASE_ORDER:
        op_extra = ""
        if current_key == "operacional":
            op_extra = (
                render_operacional_checklist(operacional_fields or [])
                + render_flows_grade(flows or [])
            )
        current_phase_html = (
            f'<div class="current-phase-panel">'
            f"{render_phase_card(current_key, phases.get(current_key, '?'))}"
            f"{op_extra}"
            f"</div>"
        )
    other_cards = "".join(
        render_phase_card(p, phases.get(p, "?"), compact=True)
        for p in PHASE_ORDER
        if p != current_key
    )
    reason = _cta_reason(phases, operacional_fields)
    cta = render_next_cta(next_cmd, reason)
    pipeline = render_pipeline_bar(phase_index)
    current_body = current_phase_html or (
        '<p class="home-section-hint">Concluído / fora do escopo do domain-kit.</p>'
    )
    return (
        f'<div class="discover-home">'
        f"{active_change_html}"
        f"{product_card_html}"
        f'<section class="home-section">'
        f'<h3 class="home-section-title">Pipeline</h3>'
        f"{pipeline}"
        f'<p class="home-section-hint">Etapa atual: <strong>{escape(current_label)}</strong> '
        f"— design tático e integração técnica ficam fora do escopo do domain-kit.</p>"
        f"</section>"
        f"{cta}"
        f'<section class="home-section">'
        f'<h3 class="home-section-title">Fase atual · {escape(current_label)}</h3>'
        f"{current_body}"
        f"</section>"
        f'<section class="home-section">'
        f'<h3 class="home-section-title">Demais fases</h3>'
        f'<div class="phase-cards phase-cards-compact">{other_cards}</div>'
        f"</section>"
        f'<details class="home-section home-details">'
        f'<summary class="home-section-title">Artefatos · Estratégico + Descoberta · {total_pct}%</summary>'
        f'<div class="discover-summary">'
        f'<div class="discover-summary-label">Progresso</div>'
        f'<div class="field-bar field-bar-lg"><div class="field-bar-fill {fill_cls}" '
        f'style="width:{total_pct}%"></div></div>'
        f"</div>"
        f'<div class="discover-fields">{"".join(field_cards)}</div>'
        f"</details>"
        f"</div>"
    )





def _file_menu_parts(rel: str) -> tuple[str, str]:
    parts = rel.replace("\\", "/").split("/")
    name = parts[-1] if parts else rel
    parent = "/".join(parts[:-1])
    return name, parent


def _render_nav_artifact_item(rel: str) -> str:
    return (
        f'<li class="nav-file-item" data-doc="{escape(rel)}" role="button" tabindex="0">'
        f'<span class="nav-file-path">{escape(rel)}</span></li>'
    )


def _render_nav_draft_item(target: str, badge: str) -> str:
    return (
        f'<li class="nav-file-item draft" data-draft-key="{escape(target)}" role="button" tabindex="0">'
        f'<span class="nav-file-path">{escape(target)}</span>'
        f'<span class="nav-file-badge">{escape(badge)}</span></li>'
    )


def _render_artifact_item(rel: str) -> str:
    name, parent = _file_menu_parts(rel)
    return (
        f'<li class="file-item" data-doc="{escape(rel)}" role="button" tabindex="0">'
        f'<span class="file-icon" aria-hidden="true">MD</span>'
        f'<span class="file-meta">'
        f'<span class="file-name">{escape(name)}</span>'
        f'<span class="file-dir">{escape(parent) if parent else "raiz do produto"}</span>'
        f"</span></li>"
    )


def _render_draft_item(target: str, hint: str, badge: str) -> str:
    name, parent = _file_menu_parts(target)
    return (
        f'<li class="file-item draft-item" data-draft-key="{escape(target)}" role="button" tabindex="0">'
        f'<span class="file-icon draft" aria-hidden="true">DR</span>'
        f'<span class="file-meta">'
        f'<span class="file-name">{escape(name)}</span>'
        f'<span class="file-dir">{escape(parent) if parent else escape(hint)}</span>'
        f"</span>"
        f'<span class="file-badge">{escape(badge)}</span>'
        f"</li>"
    )



def _artifact_phase(rel: str) -> str:
    r = rel.replace("\\", "/")
    if (
        r.startswith("01-product/00-scan/")
        or r in ("sources.yml", "product-README.md", "CHANGELOG.md", "README.md")
    ):
        return "evidencias"
    if "01-vision/" in r or r.startswith("01-product/02-domain/"):
        return "estrategico"
    if "03-discovery/" in r:
        return "descoberta"
    if (
        "04-operacional/" in r
        or r.startswith("05-decisoes/")
        or r == "flows-registry.yml"
    ):
        return "operacional"
    if r.startswith("arch/"):
        return "fora"
    return "outros"


def render_journey_track(phases: dict[str, str], phase_idx: int) -> str:
    cards: list[str] = []
    for i, (pid, label, _cmd) in enumerate(PIPELINE_STEPS):
        st = phases.get(pid, "?")
        if st == "PASS":
            cls, badge = "done", "pass"
        elif i == phase_idx:
            cls, badge = "current", "agora"
        else:
            cls, badge = "pending", "pendente"
        meta = PHASE_DISPLAY.get(pid, {})
        cmd = str(meta.get("command", "—"))
        cards.append(
            f'<button type="button" class="phase {cls}" data-phase="{escape(pid)}">'
            f'<span class="phase-status">{escape(badge)}</span>'
            f'<span class="phase-num">{i + 1}</span>'
            f'<span class="phase-title">{escape(label)}</span>'
            f'<span class="phase-cmd">{escape(cmd)}</span>'
            f"</button>"
        )
    return "".join(cards)


def _now_title_and_copy(
    next_cmd: str,
    phases: dict[str, str],
    operacional_fields: list[dict],
) -> tuple[str, str]:
    reason = _cta_reason(phases, operacional_fields)
    cmd = next_cmd.strip()
    if "flow" in cmd:
        return "Fechar o próximo fluxo operacional", (
            f"{escape(reason)}. Documente o fluxo e atualize o "
            "<code>flows-registry.yml</code>."
        )
    if "model" in cmd and "finalize" in cmd:
        return "Fechar a fase Operacional", (
            "NFRs e fluxos precisam fechar o ciclo do domain-kit. "
            "Depois disso, design tático fica fora do escopo."
        )
    if "model" in cmd:
        return "Modelar requisitos de produto", escape(reason)
    if "decision" in cmd:
        return "Registrar decisão de produto", (
            f"{escape(reason)}. Use <code>/domain.decision</code> para D-n."
        )
    if "discover" in cmd:
        return "Avançar a descoberta de domínio", escape(reason)
    if "scan" in cmd:
        return "Atualizar evidências", (
            "Fonte ou enunciado mudou — rode o scan sem reabrir lacunas de negócio."
        )
    if "init" in cmd:
        return "Inicializar o produto", (
            "Bootstrap + primeiro scan para indexar evidências."
        )
    if "change" in cmd:
        return "Sessão evolutiva", escape(reason)
    if phases.get("operacional") == "PASS":
        return "Ciclo domain-kit concluído", (
            "Todas as fases passaram. Próximos passos técnicos ficam fora do escopo."
        )
    return "Próximo passo do ciclo", escape(reason)


def render_now_panel(
    next_cmd: str,
    phases: dict[str, str],
    discover_fields: list[dict],
    operacional_fields: list[dict],
    phase_idx: int,
) -> str:
    title, copy = _now_title_and_copy(next_cmd, phases, operacional_fields)
    reason = _cta_reason(phases, operacional_fields)
    current_label = (
        PIPELINE_STEPS[phase_idx][1]
        if 0 <= phase_idx < len(PIPELINE_STEPS)
        else "Concluído"
    )
    checks: list[str] = []
    for f in discover_fields:
        st = f.get("state", "pending")
        done = st == "ready"
        mark = "✓" if done else "○"
        cls = "done" if done else ""
        tag = "ok" if done else ("rascunho" if st == "draft" else "todo")
        checks.append(
            f'<li class="check {cls}">'
            f'<span class="mark">{mark}</span>'
            f'<span>{escape(f["label"])} '
            f'<span class="hint">— {escape(f.get("hint", ""))}</span></span>'
            f'<span class="tag">{escape(tag)}</span>'
            f"</li>"
        )
    for f in operacional_fields:
        st = f.get("state", "pending")
        done = st == "ready"
        mark = "✓" if done else "○"
        cls = "done" if done else ""
        tag = "ok" if done else ("parcial" if st == "partial" else "todo")
        checks.append(
            f'<li class="check {cls}">'
            f'<span class="mark">{mark}</span>'
            f'<span>{escape(f["label"])} '
            f'<span class="hint">— {escape(f.get("hint", ""))}</span></span>'
            f'<span class="tag">{escape(tag)}</span>'
            f"</li>"
        )
    checklist = (
        f'<ul class="checklist">{"".join(checks)}</ul>'
        if checks
        else '<p class="empty">Sem checklist de progresso.</p>'
    )
    return (
        f'<p class="panel-label">Agora · {escape(current_label)}</p>'
        f'<h2 class="now-title">{escape(title)}</h2>'
        f'<p class="now-copy">{copy}</p>'
        f'<div class="cta">'
        f"<div>"
        f'<div class="cta-cmd">{escape(next_cmd)}</div>'
        f'<div class="cta-why">{escape(reason)}</div>'
        f"</div>"
        f'<div class="cta-actions">'
        f'<button type="button" class="btn primary" id="btn-copy-cmd" '
        f'data-cmd="{escape(next_cmd)}">Copiar comando</button>'
        f'<button type="button" class="btn ghost" data-tab="fluxos">Ver fluxos</button>'
        f"</div>"
        f"</div>"
        f"{checklist}"
    )


def render_loops_panel(status: dict, product: str) -> str:
    ac = status.get("activeChange")
    loops = [
        (
            "Fonte mudou",
            "Enunciado / repo atualizado — não reabre lacunas de negócio.",
            f"/domain.scan {product}",
            False,
        ),
        (
            "Evolução (E-n)",
            "Abre sessão, trabalha fases impactadas e fecha com --close.",
            "/domain.change --kind evolution …",
            False,
        ),
        (
            "Problema (P-n)",
            "Registra problema aberto e conduz ajuste de UL/BC/fluxo.",
            "/domain.change --kind problem-new …",
            False,
        ),
    ]
    parts: list[str] = []
    for title, copy, cmd, active in loops:
        cls = "active" if active else "idle"
        parts.append(
            f'<div class="loop {cls}">'
            f'<h3 class="loop-title">{escape(title)}</h3>'
            f'<p class="loop-copy">{escape(copy)}</p>'
            f"<code>{escape(cmd)}</code>"
            f"</div>"
        )
    if ac and isinstance(ac, dict):
        kind = ac.get("kind", "—")
        cid = ac.get("id", "—")
        title = ac.get("title", "")
        cmd = ac.get("suggestedCommand", "/domain.change --close")
        title_bit = f" — {escape(str(title))}" if title else ""
        parts.append(
            f'<div class="loop active active-session">'
            f'<h3 class="loop-title">Sessão ativa</h3>'
            f'<p class="loop-copy">{escape(str(kind))} · '
            f"<code>{escape(str(cid))}</code>{title_bit}</p>"
            f"<code>{escape(str(cmd))}</code>"
            f'<p class="loop-copy" style="margin-top:0.45rem">Encerrar: '
            f"<code>/domain.change --close</code></p>"
            f"</div>"
        )
    else:
        parts.append(
            '<div class="loop active-session">'
            '<h3 class="loop-title">Sessão ativa</h3>'
            '<p class="loop-copy">Nenhuma. Use <code>/domain.change</code> '
            "para registrar E-n ou P-n.</p>"
            "</div>"
        )
    return "".join(parts)


def _render_file_button(rel: str, *, draft: bool = False, badge: str = "ok") -> str:
    badge_cls = "draft" if draft or badge in ("aguardando OK", "rascunho") else (
        "miss" if badge in ("pendente", "missing") else ""
    )
    data = f'data-draft-key="{escape(rel)}"' if draft else f'data-doc="{escape(rel)}"'
    return (
        f'<li><button type="button" class="file-item" {data} '
        f'role="button" tabindex="0">'
        f'<span class="file-name">{escape(rel)}</span>'
        f'<span class="file-badge {badge_cls}">{escape(badge)}</span>'
        f"</button></li>"
    )


def render_artifacts_by_phase(
    artifacts: list[tuple[str, Path]],
    phases: dict[str, str],
) -> str:
    buckets: dict[str, list[str]] = {p: [] for p in PHASE_ORDER}
    buckets["fora"] = []
    buckets["outros"] = []
    for rel, _ in artifacts:
        buckets.setdefault(_artifact_phase(rel), []).append(rel)

    blocks: list[str] = []
    labels = {
        "evidencias": "Evidências",
        "estrategico": "Estratégico",
        "descoberta": "Descoberta",
        "operacional": "Operacional",
        "fora": "Fora do escopo",
        "outros": "Outros",
    }
    for key in [*PHASE_ORDER, "fora", "outros"]:
        items = buckets.get(key) or []
        if not items and key in ("fora", "outros"):
            continue
        st = phases.get(key, "")
        if key in PHASE_ORDER:
            if st == "PASS":
                status_html = '<span class="status ok">pass</span>'
            elif st == "FAIL":
                status_html = '<span class="status current">agora</span>'
            else:
                status_html = '<span class="status pending">pendente</span>'
        else:
            status_html = '<span class="status pending">ref</span>'
        if items:
            lis = "".join(_render_file_button(rel) for rel in items)
        else:
            lis = '<li class="nav-file-empty">Nenhum artefato nesta fase.</li>'
        blocks.append(
            f'<div class="phase-block" data-phase-block="{escape(key)}">'
            f'<div class="phase-block-head">'
            f"<h3>{escape(labels.get(key, key))}</h3>"
            f"{status_html}"
            f"</div>"
            f'<ul class="file-list">{lis}</ul>'
            f"</div>"
        )
    return "".join(blocks) or '<div class="empty">Nenhum artefato promovido.</div>'


def render_flows_tab(flows: list[dict]) -> str:
    if not flows:
        return (
            '<div class="empty">Nenhum fluxo no registry — '
            "<code>/domain.flow 01</code>.</div>"
        )
    cards: list[str] = []
    for f in flows:
        st = f.get("status", "draft")
        st_cls = "ready" if st == "ready" else "draft" if st in ("draft", "clarifying") else "todo"
        cards.append(
            f'<div class="flow">'
            f'<div class="flow-id">{escape(f.get("id", "?"))}</div>'
            f"<div>"
            f'<div class="flow-title">{escape(f.get("title", "Sem título"))}</div>'
            f'<div class="flow-meta">{escape(f.get("path", "—"))}</div>'
            f"</div>"
            f'<span class="flow-st {st_cls}">{escape(st)}</span>'
            f"</div>"
        )
    return f'<div class="flows">{"".join(cards)}</div>'


def render_drafts_tab(
    pending: list[dict],
    draft_files: list[tuple[str, Path]],
) -> str:
    items: list[str] = []
    if pending:
        for entry in pending:
            target = entry.get("targetPath", "?")
            items.append(_render_file_button(target, draft=True, badge="aguardando OK"))
    elif draft_files:
        for rel, _ in draft_files:
            items.append(_render_file_button(rel, draft=True, badge="rascunho"))
    if not items:
        return (
            '<div class="empty">Nenhum rascunho pendente.</div>'
            '<p style="margin:0.85rem 0 0;font-size:0.82rem;color:var(--muted)">'
            "Plan mode: rascunhos não contam nas fases até promote.</p>"
        )
    return (
        f'<ul class="file-list">{"".join(items)}</ul>'
        '<p style="margin:0.85rem 0 0;font-size:0.82rem;color:var(--muted)">'
        "Plan mode: rascunhos não contam nas fases até promote.</p>"
    )


def render_command_map(phases: dict[str, str], next_cmd: str) -> str:
    steps = [
        ("/domain.install", "Hub zerado", "install"),
        ("/domain.init", "Bootstrap + 1º scan", "evidencias"),
        ("/domain.discover", "Estratégico + Descoberta", "descoberta"),
        ("/domain.flow", "Fluxos operacionais", "operacional"),
        ("/domain.decision", "Decisões D-n", "operacional"),
        ("/domain.model --finalize", "Fechar Operacional", "operacional"),
        ("/domain.scan", "Fonte externa mudou", "loop"),
        ("/domain.change", "E-n / P-n", "loop"),
    ]
    rows: list[str] = []
    for cmd, label, kind in steps:
        if kind == "install":
            done = True
            tag = "hub"
            mark = "✓"
        elif kind == "loop":
            done = False
            tag = "loop"
            mark = "○"
        else:
            # mark done if prior phases passed enough
            if kind == "evidencias":
                done = phases.get("evidencias") == "PASS"
            elif kind == "descoberta":
                done = (
                    phases.get("estrategico") == "PASS"
                    and phases.get("descoberta") == "PASS"
                )
            else:
                done = phases.get("operacional") == "PASS"
            tag = "feito" if done else ("agora" if cmd.split()[0] in next_cmd else "depois")
            mark = "✓" if done else ("→" if tag == "agora" else "○")
        cls = "done" if done else ""
        rows.append(
            f'<li class="check {cls}">'
            f'<span class="mark">{mark}</span>'
            f"<span><code>{escape(cmd)}</code> · {escape(label)}</span>"
            f'<span class="tag">{escape(tag)}</span>'
            f"</li>"
        )
    return f'<ul class="checklist">{"".join(rows)}</ul>'



def render_shell(
    title: str,
    body: str,
    *,
    depth: int = 0,
    extra_head: str = "",
    bootstrap: str = "",
) -> str:
    """Assemble HTML from scripts/dashboard/shell.html + linked CSS/JS."""
    return fill_template(
        load_dashboard_template("shell.html"),
        {
            "TITLE": escape(title),
            "ASSET_PREFIX": dashboard_asset_prefix(depth),
            "EXTRA_HEAD": extra_head,
            "BODY": body,
            "GENERATED_AT": escape(
                datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M UTC")
            ),
            "BOOTSTRAP": bootstrap,
        },
    )


def build_product_dashboard(hub: Path, product: str) -> str:
    product_dir = hub / "products" / product
    plantuml_server = load_plantuml_server(hub)
    status: dict = {}
    sp = product_dir / "domain-status.json"
    if sp.exists():
        status = json.loads(sp.read_text(encoding="utf-8"))

    phases = phase_status(hub, product)
    next_cmd = status.get("nextSuggested", "/domain.discover")
    try:
        script = Path(__file__).resolve().parent / "validate_gate.py"
        r = subprocess.run(
            [sys.executable, str(script), "--hub", str(hub), "--product", product, "--json"],
            capture_output=True,
            text=True,
        )
        if r.stdout.strip():
            vdata = json.loads(r.stdout)
            next_cmd = vdata.get("suggestedNextCommand", next_cmd)
    except (OSError, json.JSONDecodeError):
        pass

    flows = parse_flows_registry(product_dir / "flows-registry.yml")
    artifacts = collect_artifacts(product_dir)
    draft_manifest = load_draft_manifest(product_dir)
    pending = draft_manifest.get("pending", [])
    draft_files = collect_draft_files(product_dir)

    phase = str(status.get("phase", "evidencias"))
    scan = str(status.get("scan", "pending"))
    p_idx = phase_index(phase)

    discover_fields = compute_discover_fields(product_dir, status)
    operacional_fields = compute_operacional_fields(product_dir, status)
    _, discover_total = render_discover_progress(discover_fields)

    draft_count = len(pending) or len(draft_files)
    art_count = len(artifacts)

    readme = product_dir / "product-README.md"
    product_title = product
    product_sub = "Jornada negócio → domínio. Pipeline termina em Operacional."
    if readme.is_file():
        fields = _extract_product_readme_fields(readme.read_text(encoding="utf-8"))
        product_title = fields.get("title") or product
        if fields.get("o_que_e"):
            product_sub = fields["o_que_e"]

    scan_chip = "ok" if scan in ("done", "ready", "complete", "PASS") else ""

    docs_payload: dict[str, str] = {}
    for rel, path in artifacts:
        docs_payload[rel] = file_to_preview_text(path)

    drafts_payload: dict[str, str] = {}
    for rel, path in draft_files:
        drafts_payload[rel] = file_to_preview_text(path)

    for entry in pending:
        target = entry.get("targetPath", "")
        draft_path = entry.get("draftPath", "").lstrip("./")
        full = product_dir / draft_path if draft_path else None
        if target and full and full.is_file():
            drafts_payload[target] = file_to_preview_text(full)

    bootstrap = (
        "<script>\n"
        f"window.__DK_DOCS__ = {json.dumps(docs_payload)};\n"
        f"window.__DK_DRAFTS__ = {json.dumps(drafts_payload)};\n"
        f"window.__DK_PLANTUML_SERVER__ = {json.dumps(plantuml_server)};\n"
        "</script>"
    )

    body = fill_template(
        load_dashboard_template("product-body.html"),
        {
            "PRODUCT_TITLE": escape(product_title),
            "PRODUCT_SUB": escape(product_sub),
            "PHASE": escape(phase),
            "SCAN": escape(scan),
            "SCAN_CHIP_CLASS": scan_chip,
            "DISCOVER_TOTAL": str(discover_total),
            "ART_COUNT": str(art_count),
            "FLOW_COUNT": str(len(flows)),
            "DRAFT_COUNT": str(draft_count),
            "JOURNEY_TRACK": render_journey_track(phases, p_idx),
            "NOW_PANEL": render_now_panel(
                str(next_cmd), phases, discover_fields, operacional_fields, p_idx
            ),
            "LOOPS_PANEL": render_loops_panel(status, product),
            "ARTIFACTS_BY_PHASE": render_artifacts_by_phase(artifacts, phases),
            "FLOWS_TAB": render_flows_tab(flows),
            "DRAFTS_TAB": render_drafts_tab(pending, draft_files),
            "COMMAND_MAP": render_command_map(phases, str(next_cmd)),
        },
    )

    return render_shell(
        f"Domain-Kit — {product}",
        body,
        depth=2,
        extra_head=dashboard_vendor_script_tags(depth=2),
        bootstrap=bootstrap,
    )



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

    cards_html = "".join(cards) or (
        '<div class="empty">Nenhum produto com domain-status.json</div>'
    )
    asset_prefix = dashboard_asset_prefix(0)
    body = fill_template(
        load_dashboard_template("hub-index-body.html"),
        {"PRODUCT_CARDS": cards_html},
    )
    return render_shell(
        "Domain-Kit Index",
        body,
        depth=0,
        extra_head=f'<link rel="stylesheet" href="{asset_prefix}/hub-index.css"/>',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub", type=Path, default=Path.cwd())
    parser.add_argument("--product", help="Product slug (omit for hub index only)")
    args = parser.parse_args()

    hub = args.hub.resolve()
    sync_dashboard_vendor_assets(hub)
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
