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
    ("arch", "Arch-kit", "/arch.route"),
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
        "handoff": "Handoff → arch-kit",
    },
}

# Legacy alias for render_gate_card
GATE_DISPLAY = PHASE_DISPLAY

DEFAULT_PLANTUML_SERVER = "http://127.0.0.1:8765"
DASHBOARD_VENDOR_REL = "dashboard-assets/vendor"
DASHBOARD_VENDOR_FILES = ("marked.min.js", "mermaid.min.js")


def sync_dashboard_vendor_assets(hub: Path) -> Path:
    """Copy vendor JS to a visible hub folder (Cursor/Simple Browser blocks .domain/)."""
    src_dir = Path(__file__).resolve().parent / "vendor"
    dest_dir = hub / DASHBOARD_VENDOR_REL
    dest_dir.mkdir(parents=True, exist_ok=True)
    for name in DASHBOARD_VENDOR_FILES:
        src = src_dir / name
        if not src.is_file():
            raise FileNotFoundError(f"Vendor asset missing: {src}")
        shutil.copy2(src, dest_dir / name)
    return dest_dir


def dashboard_vendor_script_tags(depth: int = 2) -> str:
    """Script tags relative to dashboard.html (products/{p}/ = depth 2)."""
    prefix = "/".join([".."] * depth)
    base = f"{prefix}/{DASHBOARD_VENDOR_REL}"
    return "\n".join(
        f'<script src="{base}/{name}"></script>' for name in DASHBOARD_VENDOR_FILES
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
    """Legacy alias — maps phases to G0/G1/G2 for backward compatibility."""
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
        "arch/**/*.md",
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

    req_path = "04-platform/01-non-functional/01-requisitos.md"
    fields.append(
        _file_field("requisitos", "Requisitos NFR (produto)", product_dir, model, req_path)
    )

    reg_path = product_dir / "flows-registry.yml"
    op_dir = product_dir / "01-product/03-operacional/fluxos"
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

    reg_md = "03-registry/produto.md"
    fields.append(
        _file_field("registry", "Registry D-n", product_dir, model, reg_md)
    )
    return fields


def render_phase_card(phase_id: str, status: str) -> str:
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
            f'<span class="gate-card-meta-item">Handoff: <strong>{escape(handoff)}</strong></span>'
        )
    return (
        f'<article class="gate-card {cls}">'
        f'<div class="gate-card-head">'
        f'<span class="gate-card-sub">{escape(subtitle)}</span>'
        f'<span class="gate-card-badge">{escape(badge)}</span>'
        f"</div>"
        f'<h4 class="gate-card-title">{escape(title)}</h4>'
        f'<p class="gate-card-desc">{escape(description)}</p>'
        f'<div class="gate-card-meta">'
        f'<span class="gate-card-meta-item">Comando: <code>{escape(command)}</code></span>'
        f"{handoff_html}"
        f"</div>"
        f"</article>"
    )


def render_gate_card(gate_id: str, status: str) -> str:
    """Legacy — redirects to phase cards when possible."""
    legacy_map = {"G0": "evidencias", "G1": "estrategico", "G2": "operacional"}
    pid = legacy_map.get(gate_id, gate_id)
    if pid in PHASE_DISPLAY:
        return render_phase_card(pid, status)
    return render_phase_card(gate_id, status)




def render_product_card_link(product_dir: Path) -> str:
    """Link to product-README.md cartão do produto."""
    card = product_dir / "product-README.md"
    if not card.is_file():
        return ""
    return (
        '<div class="product-card-link">'
        '<a class="btn-product-card" data-doc="product-README.md" href="#">'
        "Cartão do produto"
        "</a>"
        '<span class="product-card-hint">Visão PM · benefícios · índice de artefatos</span>'
        "</div>"
    )


def render_active_change_banner(status: dict) -> str:
    """Banner when an evolutionary session is open (/domain.change)."""
    ac = status.get("activeChange")
    if not ac or not isinstance(ac, dict):
        return ""
    kind = ac.get("kind", "—")
    cid = ac.get("id", "—")
    title = ac.get("title", "")
    cmd = ac.get("suggestedCommand", "")
    phases = ", ".join(ac.get("phasesImpacted", [])) or "—"
    title_bit = f" — {title}" if title else ""
    cmd_bit = (
        f'<p class="active-change-cmd">Próximo: <code>{escape(cmd)}</code></p>'
        if cmd
        else ""
    )
    return (
        f'<div class="active-change-banner" role="status">'
        f'<strong>Sessão ativa</strong> · {escape(kind)} · <code>{escape(cid)}</code>'
        f"{escape(title_bit)}"
        f'<span class="active-change-phases">Fases: {escape(phases)}</span>'
        f"{cmd_bit}"
        f"</div>"
    )


def render_discover_home(
    fields: list[dict],
    total_pct: int,
    next_cmd: str,
    phases: dict[str, str],
    phase_index: int,
    operacional_fields: list[dict] | None = None,
    product_card_html: str = "",
    active_change_html: str = "",
) -> str:
    if not fields:
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
    op_cards = ""
    if operacional_fields:
        for f in operacional_fields:
            st = f["state"]
            op_cards += (
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
    op_section = op_cards or '<p class="home-section-hint">Fluxos de negócio, NFRs de produto e registry D-n.</p>'
    fill_cls = "ready" if total_pct >= 100 else "partial" if total_pct > 0 else "pending"
    current_label = (
        PIPELINE_STEPS[phase_index][1]
        if 0 <= phase_index < len(PIPELINE_STEPS)
        else "—"
    )
    phase_cards = "".join(
        render_phase_card(p, phases.get(p, "?")) for p in PHASE_ORDER
    )
    pipeline = render_pipeline_bar(phase_index)
    return (
        f'<div class="discover-home">'
        f'<h2 class="center-title">Domain-kit</h2>'
        f'<p class="center-sub">Modelagem de problema e domínio — legível por produto e engenharia.</p>'
        f"{product_card_html}"
        f"{active_change_html}"
        f'<section class="home-section">'
        f'<h3 class="home-section-title">Pipeline</h3>'
        f"{pipeline}"
        f'<p class="home-section-hint">Etapa atual: <strong>{escape(current_label)}</strong> '
        f"— design tático e integração técnica ficam no arch-kit.</p>"
        f"</section>"
        f'<section class="home-section">'
        f'<h3 class="home-section-title">Fases</h3>'
        f'<p class="home-section-hint"><strong>Pendente</strong> indica artefatos '
        f"ainda incompletos na fase — não é erro de sistema.</p>"
        f'<div class="gate-cards">{phase_cards}</div>'
        f"</section>"
        f'<section class="home-section">'
        f'<h3 class="home-section-title">Artefatos · Estratégico + Descoberta · {total_pct}%</h3>'
        f'<div class="discover-summary">'
        f'<div class="discover-summary-label">Progresso</div>'
        f'<div class="field-bar field-bar-lg"><div class="field-bar-fill {fill_cls}" '
        f'style="width:{total_pct}%"></div></div>'
        f"</div>"
        f'<div class="discover-legend">'
        f'<span class="legend-ready">Pronto</span>'
        f'<span class="legend-draft">Rascunho</span>'
        f'<span class="legend-partial">Parcial</span>'
        f'<span class="legend-pending">Pendente</span>'
        f"</div>"
        f'<div class="discover-fields">{"".join(field_cards)}</div>'
        f"</section>"
        f'<section class="home-section home-section-last">'
        f'<h3 class="home-section-title">Artefatos · Operacional</h3>'
        f'<div class="discover-fields">{op_section}</div>'
        f"</section>"
        f'<div class="next-cmd">Próximo comando sugerido: <code>{escape(next_cmd)}</code></div>'
        f"</div>"
    )


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
.shell { max-width: 1440px; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }
.main-layout {
  display: grid; grid-template-columns: minmax(240px, 280px) 1fr;
  gap: 1.25rem; align-items: start; margin-top: 1.25rem;
}
@media (max-width: 900px) { .main-layout { grid-template-columns: 1fr; } }
.sidebar {
  position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow-y: auto;
  display: flex; flex-direction: column; gap: 0.75rem;
}
.sidebar-section {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.85rem; box-shadow: var(--shadow);
}
.sidebar-section h3 {
  margin: 0 0 0.65rem; font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--muted); font-weight: 600;
}
.sidebar-section-head {
  display: flex; align-items: center; justify-content: space-between; gap: 0.5rem;
  margin-bottom: 0.65rem;
}
.sidebar-section-head h3 { margin: 0; }
.sidebar-toggle {
  border: 1px solid var(--border); background: var(--surface-2); color: var(--muted);
  font-size: 0.68rem; font-weight: 600; padding: 0.2rem 0.5rem; border-radius: 6px;
  cursor: pointer; text-transform: uppercase; letter-spacing: 0.04em;
}
.sidebar-toggle:hover { color: var(--text); border-color: var(--accent); }
#discover-panel.collapsed { display: none; }
#discover-show-btn { width: 100%; }
.sidebar .gates { flex-direction: column; }
.sidebar .gate { min-width: 0; }
.sidebar .pipeline-track { flex-direction: column; align-items: stretch; padding: 0; }
.sidebar .step { min-width: 0; text-align: left; padding: 0.45rem 0 0.45rem 1.25rem; }
.sidebar .step-dot { margin: 0 0 0.35rem 0; }
.sidebar .step:not(:last-child)::after {
  top: 18px; left: 5px; width: 2px; height: calc(100% - 4px);
}
.work-area {
  display: flex; flex-direction: column; min-width: 0; min-height: calc(100vh - 12rem);
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); box-shadow: var(--shadow); overflow: hidden;
}
.center-panel { display: none; flex: 1; min-height: 0; overflow: auto; padding: 1.5rem 1.75rem; }
.center-panel.active { display: block; }
.center-title { margin: 0; font-size: 1.5rem; font-weight: 650; letter-spacing: -0.02em; }
.center-sub { color: var(--muted); font-size: 0.92rem; margin: 0.35rem 0 1.25rem; }
.discover-home { max-width: 100%; }
.home-section {
  margin-bottom: 1.75rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border);
}
.home-section-last { border-bottom: none; margin-bottom: 1rem; padding-bottom: 0; }
.home-section-title { margin: 0 0 0.5rem; font-size: 1rem; font-weight: 650; color: var(--text); }
.home-section-hint { font-size: 0.85rem; color: var(--muted); margin: 0 0 1rem; line-height: 1.5; }
.home-section-hint strong { color: var(--text); font-weight: 600; }
.pipeline-bar {
  display: flex; align-items: center; flex-wrap: wrap; gap: 0; overflow-x: auto;
  margin-bottom: 0.65rem;
}
.pipe-step {
  padding: 0.55rem 0.85rem; border-radius: 8px; border: 1px solid var(--border);
  min-width: 92px; text-align: center; background: transparent;
}
.pipe-step.done { background: var(--surface-2); }
.pipe-step.current { border-color: var(--accent); background: var(--accent-dim); }
.pipe-step-label { font-size: 0.78rem; font-weight: 600; display: block; }
.pipe-step-cmd {
  font-size: 0.66rem; color: var(--muted); font-family: ui-monospace, monospace;
  display: block; margin-top: 0.15rem;
}
.pipe-connector { width: 18px; height: 2px; background: var(--border); flex-shrink: 0; }
.pipe-connector.done { background: var(--pass); }
.gate-cards {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 0.85rem;
}
.gate-card {
  padding: 1rem 1.1rem; border-radius: 10px; border: 1px solid var(--border);
  background: var(--surface-2);
}
.gate-card.pass { border-top: 3px solid var(--pass); }
.gate-card.fail { border-top: 3px solid var(--fail); }
.gate-card.pending { border-top: 3px solid var(--pending); }
.gate-card-head {
  display: flex; justify-content: space-between; align-items: center; gap: 0.5rem;
  margin-bottom: 0.35rem;
}
.gate-card-sub {
  font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.04em;
}
.gate-card-badge {
  font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;
  padding: 0.15rem 0.45rem; border-radius: 6px; flex-shrink: 0;
}
.gate-card.pass .gate-card-badge { background: var(--pass-bg); color: var(--pass); }
.gate-card.fail .gate-card-badge { background: var(--fail-bg); color: var(--fail); }
.gate-card.pending .gate-card-badge { background: var(--pending-bg); color: var(--pending); }
.gate-card-title { margin: 0.25rem 0 0.5rem; font-size: 0.95rem; font-weight: 650; }
.gate-card-desc { font-size: 0.84rem; color: var(--muted); margin: 0 0 0.75rem; line-height: 1.5; }
.gate-card-meta {
  display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; font-size: 0.75rem; color: var(--muted);
}
.gate-card-meta code { color: var(--accent); font-size: 0.72rem; }
.gate-card-meta strong { color: var(--text); font-weight: 600; }
.discover-stats {
  display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 1.25rem;
}
.discover-stat {
  flex: 1; min-width: 88px; padding: 0.75rem 0.85rem; border-radius: 10px;
  border: 1px solid var(--border); background: var(--surface-2); text-align: center;
}
.discover-stat-value { display: block; font-size: 1.25rem; font-weight: 700; }
.discover-stat-label {
  display: block; font-size: 0.68rem; text-transform: uppercase;
  letter-spacing: 0.05em; color: var(--muted); margin-top: 0.2rem;
}
.discover-stat.ready .discover-stat-value { color: var(--pass); }
.discover-stat.partial .discover-stat-value { color: var(--accent); }
.discover-stat.pending .discover-stat-value { color: var(--pending); }
.discover-fields {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 0.75rem; margin: 1rem 0 1.25rem;
}
.discover-field-card {
  padding: 0.85rem 1rem; border-radius: 10px; border: 1px solid var(--border);
  background: var(--surface-2);
}
.discover-field-head {
  display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;
}
.discover-field-dot {
  width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0;
}
.discover-field-dot.ready { background: var(--pass); }
.discover-field-dot.draft { background: var(--draft); }
.discover-field-dot.partial { background: var(--accent); }
.discover-field-dot.pending { background: var(--border); }
.discover-field-label { flex: 1; font-size: 0.84rem; font-weight: 600; min-width: 0; }
.discover-field-hint { font-size: 0.72rem; color: var(--muted); margin-top: 0.35rem; }
.nav-home {
  display: block; width: 100%; text-align: left; padding: 0.75rem 0.85rem;
  border-radius: 10px; border: 1px solid var(--border); background: var(--surface-2);
  color: var(--text); cursor: pointer; transition: border-color 0.12s, background 0.12s;
}
.nav-home:hover { border-color: var(--muted); }
.nav-home.active { border-color: var(--accent); background: var(--accent-dim); }
.nav-home-title { display: block; font-size: 0.88rem; font-weight: 650; }
.nav-home-sub { display: block; font-size: 0.72rem; color: var(--muted); margin-top: 0.15rem; }
.nav-tree { margin-bottom: 0.5rem; }
.nav-tree summary {
  cursor: pointer; font-size: 0.72rem; text-transform: uppercase;
  letter-spacing: 0.06em; color: var(--muted); font-weight: 600;
  list-style: none; display: flex; align-items: center; gap: 0.35rem;
}
.nav-tree summary::-webkit-details-marker { display: none; }
.nav-tree summary::before { content: "▸"; font-size: 0.65rem; }
.nav-tree[open] summary::before { content: "▾"; }
.nav-file-list { list-style: none; margin: 0.45rem 0 0; padding: 0; }
.nav-file-item {
  display: flex; align-items: center; gap: 0.4rem; width: 100%;
  padding: 0.4rem 0.5rem; border-radius: 6px; border: 1px solid transparent;
  cursor: pointer; text-align: left; background: transparent; color: var(--text);
  margin-bottom: 0.15rem;
}
.nav-file-item:hover { background: var(--surface-2); }
.nav-file-item.selected {
  background: var(--accent-dim); border-color: rgba(245, 158, 11, 0.35);
}
.nav-file-item.draft.selected { background: var(--draft-bg); border-color: rgba(96, 165, 250, 0.35); }
.nav-file-path {
  flex: 1; min-width: 0; font-size: 0.72rem; font-family: ui-monospace, monospace;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.nav-file-badge {
  flex-shrink: 0; font-size: 0.6rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.04em; padding: 0.1rem 0.35rem; border-radius: 5px;
  background: var(--draft-bg); color: var(--draft);
}
.nav-file-search {
  width: 100%; padding: 0.4rem 0.55rem; border-radius: 6px; margin-bottom: 0.45rem;
  border: 1px solid var(--border); background: var(--surface); color: var(--text);
  font-size: 0.75rem;
}
.nav-file-search::placeholder { color: var(--muted); }
.nav-file-search:focus { outline: none; border-color: var(--accent); }
.nav-file-empty {
  padding: 0.65rem; font-size: 0.75rem; color: var(--muted); text-align: center;
  border: 1px dashed var(--border); border-radius: 6px;
}
.file-view-bar {
  display: flex; flex-wrap: wrap; align-items: center; gap: 0.65rem;
  padding-bottom: 1rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border);
}
.btn-back {
  padding: 0.4rem 0.75rem; border-radius: 8px; border: 1px solid var(--border);
  background: var(--surface-2); color: var(--text); font-size: 0.8rem; font-weight: 600;
  cursor: pointer;
}
.btn-back:hover { border-color: var(--accent); color: var(--accent); }
.file-breadcrumb { font-size: 0.8rem; color: var(--muted); }
.file-breadcrumb strong { color: var(--text); font-weight: 600; }
.file-breadcrumb code {
  font-family: ui-monospace, monospace; font-size: 0.78rem; color: var(--accent);
}
.view-hint { font-size: 0.78rem; color: var(--muted); }
.center-panel .preview-body { padding: 0; min-height: 360px; }
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
.hero-card-link { margin-top: 0.6rem; }
.btn-product-card {
  display: inline-block; padding: 0.45rem 0.9rem; border-radius: 8px;
  border: 1px solid var(--accent); background: var(--accent-dim);
  color: var(--accent); font-size: 0.85rem; font-weight: 600; text-decoration: none; cursor: pointer;
}
.btn-product-card:hover { filter: brightness(1.08); }
.product-card-link { margin: 0.75rem 0 0.25rem; display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; }
.product-card-hint { font-size: 0.82rem; color: var(--muted); }
.active-change-banner {
  margin: 0.75rem 0 0; padding: 0.75rem 1rem; border-radius: 8px;
  border: 1px solid rgba(59, 130, 246, 0.45); background: rgba(59, 130, 246, 0.08);
  font-size: 0.88rem; line-height: 1.45;
}
.active-change-phases { display: block; margin-top: 0.35rem; font-size: 0.8rem; color: var(--muted); }
.active-change-cmd { margin: 0.4rem 0 0; font-size: 0.85rem; }
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
.count {
  display: inline-block; margin-left: 0.35rem; padding: 0.1rem 0.45rem; border-radius: 999px;
  font-size: 0.72rem; background: var(--draft-bg); color: var(--draft);
}
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
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 0.5rem;
  padding: 0.65rem 0.75rem; border: 1px solid var(--border); border-radius: 8px;
  background: var(--surface-2); margin-bottom: 0.45rem; cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.draft-item:hover, .draft-item.selected { border-color: var(--draft); background: var(--draft-bg); }
.draft-target { font-family: ui-monospace, monospace; font-size: 0.75rem; word-break: break-all; }
.draft-cmd { font-size: 0.68rem; color: var(--muted); }
.badge-await { font-size: 0.65rem; padding: 0.15rem 0.4rem; border-radius: 6px; background: var(--draft-bg); color: var(--draft); font-weight: 600; }
.art-list { list-style: none; padding: 0; margin: 0; max-height: 280px; overflow-y: auto; }
.art-list li {
  padding: 0.45rem 0.55rem; border-radius: 8px; cursor: pointer; font-size: 0.75rem;
  font-family: ui-monospace, monospace; border: 1px solid transparent;
}
.art-list li:hover { background: var(--surface-2); }
.art-list li.selected { background: var(--accent-dim); border-color: rgba(245, 158, 11, 0.4); color: var(--accent); }
.preview-wrap {
  border: 1px solid var(--border); border-radius: var(--radius);
  background: var(--surface); overflow: hidden; min-height: 420px; flex: 1;
  display: flex; flex-direction: column;
}
.preview-header {
  padding: 0.65rem 1rem; background: var(--surface-2); border-bottom: 1px solid var(--border);
  font-family: ui-monospace, monospace; font-size: 0.8rem; color: var(--muted);
}
.preview-body {
  padding: 1.25rem; flex: 1; min-height: 360px;
  overflow: auto; font-size: 0.92rem;
}
.preview-body > :first-child { margin-top: 0; }
.preview-body pre, .preview-body .md-fallback {
  white-space: pre-wrap; word-break: break-word; margin: 0.75rem 0;
  font-family: ui-monospace, monospace; font-size: 0.82rem;
}
.preview-body h1 { font-size: 1.5rem; margin: 0 0 0.75rem; color: var(--text); }
.preview-body h2 {
  font-size: 1.2rem; margin: 1.25rem 0 0.5rem; color: var(--text);
  border-bottom: 1px solid var(--border); padding-bottom: 0.25rem;
}
.preview-body h3, .preview-body h4 { margin: 1rem 0 0.4rem; color: var(--text); }
.preview-body p { margin: 0.5rem 0; }
.preview-body ul, .preview-body ol { margin: 0.5rem 0; padding-left: 1.5rem; }
.preview-body li { margin: 0.25rem 0; }
.preview-body li > p { margin: 0.25rem 0; }
.preview-body blockquote {
  margin: 0.75rem 0; padding: 0.5rem 1rem; border-left: 3px solid var(--accent);
  background: var(--surface-2); color: var(--muted);
}
.preview-body code {
  font-family: ui-monospace, monospace; font-size: 0.86em;
  background: var(--surface-2); padding: 0.15rem 0.35rem; border-radius: 4px;
}
.preview-body pre {
  background: var(--surface-2); border: 1px solid var(--border);
  border-radius: 8px; padding: 0.85rem 1rem; overflow-x: auto;
}
.preview-body pre code { background: none; padding: 0; font-size: 0.82rem; }
.preview-body table { border-collapse: collapse; width: 100%; margin: 0.75rem 0; font-size: 0.88rem; }
.preview-body th, .preview-body td { border: 1px solid var(--border); padding: 0.45rem 0.65rem; text-align: left; }
.preview-body th { background: var(--surface-2); font-weight: 600; }
.preview-body tr:nth-child(even) td { background: rgba(36, 48, 68, 0.35); }
.preview-body a { color: var(--accent); }
.preview-body hr { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }
.preview-body strong { color: var(--text); font-weight: 650; }
.flow-list-compact { display: flex; flex-direction: column; gap: 0.4rem; max-height: 180px; overflow-y: auto; }
.flow-chip {
  padding: 0.45rem 0.55rem; border-radius: 8px; border: 1px solid var(--border);
  background: var(--surface-2); font-size: 0.72rem;
}
.flow-chip.ready { border-left: 3px solid var(--pass); }
.flow-chip.draft, .flow-chip.clarifying { border-left: 3px solid var(--accent); }
.flow-chip-id { font-weight: 700; }
.flow-chip-title { color: var(--muted); margin-top: 0.15rem; }
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
.discover-legend { display: flex; flex-wrap: wrap; gap: 0.5rem; font-size: 0.68rem; color: var(--muted); margin-bottom: 0.75rem; }
.sidebar .field-row {
  grid-template-columns: 1fr; gap: 0.25rem; margin-bottom: 0.65rem;
}
.sidebar .field-status { text-align: left; }
.sidebar .field-hint { margin-top: 0; }
.sidebar .discover-summary { margin-bottom: 0.85rem; }
.discover-legend span::before { content: ""; display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 0.35rem; vertical-align: middle; }
.legend-ready::before { background: var(--pass); }
.legend-draft::before { background: var(--draft); }
.legend-partial::before { background: var(--accent); }
.legend-pending::before { background: var(--border); }
.plantuml-diagram { margin: 1rem 0; overflow-x: auto; text-align: center; }
.plantuml-diagram svg, .plantuml-diagram img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
.plantuml-loading { color: var(--muted); font-size: 0.85rem; font-style: italic; padding: 0.5rem 0; }
.plantuml-hint {
  margin: 0.5rem 0 1rem; padding: 0.75rem 1rem; border-radius: 8px;
  border: 1px dashed var(--border); background: var(--surface-2);
  color: var(--muted); font-size: 0.85rem;
}
.plantuml-hint code { color: var(--accent); font-size: 0.82rem; }
.mermaid-diagram { margin: 1rem 0; overflow-x: auto; text-align: center; }
.mermaid-diagram svg { max-width: 100%; height: auto; display: block; margin: 0 auto; }
.mermaid-hint {
  margin: 0.5rem 0 1rem; padding: 0.75rem 1rem; border-radius: 8px;
  border: 1px dashed var(--border); background: var(--surface-2);
  color: var(--muted); font-size: 0.85rem;
}
"""


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


def render_shell(title: str, body: str, extra_script: str = "", extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{escape(title)}</title>
<style>{shared_styles()}</style>
{extra_head}
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
    product_card_html = render_product_card_link(product_dir)
    active_change_html = render_active_change_banner(status)
    discover_home_html = render_discover_home(
        discover_fields,
        discover_total,
        str(next_cmd),
        phases,
        p_idx,
        operacional_fields,
        product_card_html,
        active_change_html,
    )

    flow_chips = []
    for f in flows:
        st = f.get("status", "draft")
        flow_chips.append(
            f'<div class="flow-chip {escape(st)}">'
            f'<div class="flow-chip-id">{escape(f.get("id", "?"))}</div>'
            f'<div class="flow-chip-title">{escape(f.get("title", "Sem título"))}</div>'
            f"</div>"
        )
    flow_sidebar_html = "".join(flow_chips) or '<div class="empty" style="padding:1rem;font-size:0.8rem">Nenhum fluxo.</div>'

    draft_count = len(pending) or len(draft_files)

    draft_items = []
    if pending:
        for entry in pending:
            target = entry.get("targetPath", "?")
            draft_items.append(_render_nav_draft_item(target, "aguardando OK"))
    elif draft_files:
        for rel, _ in draft_files:
            draft_items.append(_render_nav_draft_item(rel, "rascunho"))
    draft_list_html = "".join(draft_items)
    if not draft_list_html:
        draft_list_html = '<li class="nav-file-empty">Nenhum rascunho pendente.</li>'

    art_count = len(artifacts)
    art_items = "".join(_render_nav_artifact_item(rel) for rel, _ in artifacts) or (
        '<li class="nav-file-empty">Nenhum artefato promovido ainda.</li>'
    )

    docs_payload: dict[str, str] = {}
    for rel, path in artifacts:
        docs_payload[rel] = file_to_preview_text(path)

    drafts_payload: dict[str, str] = {}
    for rel, path in draft_files:
        drafts_payload[rel] = file_to_preview_text(path)

    # map targetPath -> draftPath content for pending entries
    for entry in pending:
        target = entry.get("targetPath", "")
        draft_path = entry.get("draftPath", "").lstrip("./")
        full = product_dir / draft_path if draft_path else None
        if target and full and full.is_file():
            drafts_payload[target] = file_to_preview_text(full)

    script = f"""
const DOCS = {json.dumps(docs_payload)};
const DRAFTS = {json.dumps(drafts_payload)};
const PLANTUML_SERVER = {json.dumps(plantuml_server)};

function escapeHtml(text) {{
  const el = document.createElement('div');
  el.textContent = text;
  return el.innerHTML;
}}

function renderMarkdown(text, path) {{
  if (!text) return '<p class="empty">Sem conteúdo.</p>';
  const ext = (path || '').split('.').pop().toLowerCase();
  if (ext === 'md' && window.marked) {{
    return marked.parse(text, {{ gfm: true, breaks: false }});
  }}
  if (ext === 'md') {{
    return `<pre class="md-fallback">${{escapeHtml(text)}}</pre>`;
  }}
  return `<pre class="md-fallback"><code>${{escapeHtml(text)}}</code></pre>`;
}}

function normalizePlantUmlSource(source) {{
  const trimmed = (source || '').trim();
  if (!trimmed) return '';
  if (/@startuml/i.test(trimmed)) return trimmed;
  return '@startuml\\n' + trimmed + '\\n@enduml';
}}

function encode6bit(b) {{
  if (b < 10) return String.fromCharCode(48 + b);
  b -= 10;
  if (b < 26) return String.fromCharCode(65 + b);
  b -= 26;
  if (b < 26) return String.fromCharCode(97 + b);
  b -= 26;
  if (b === 0) return '-';
  if (b === 1) return '_';
  return '?';
}}

function append3bytes(b1, b2, b3) {{
  const c1 = b1 >> 2;
  const c2 = ((b1 & 0x3) << 4) | (b2 >> 4);
  const c3 = ((b2 & 0xF) << 2) | (b3 >> 6);
  const c4 = b3 & 0x3F;
  return (
    encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) +
    encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)
  );
}}

function encodePlantUml64(data) {{
  let r = '';
  for (let i = 0; i < data.length; i += 3) {{
    if (i + 2 === data.length) {{
      r += append3bytes(data.charCodeAt(i), data.charCodeAt(i + 1), 0);
    }} else if (i + 1 === data.length) {{
      r += append3bytes(data.charCodeAt(i), 0, 0);
    }} else {{
      r += append3bytes(data.charCodeAt(i), data.charCodeAt(i + 1), data.charCodeAt(i + 2));
    }}
  }}
  return r;
}}

async function deflateRaw(text) {{
  const data = new TextEncoder().encode(text);
  if (typeof CompressionStream !== 'undefined') {{
    const stream = new Blob([data]).stream().pipeThrough(new CompressionStream('deflate-raw'));
    const buf = await new Response(stream).arrayBuffer();
    return String.fromCharCode(...new Uint8Array(buf));
  }}
  return null;
}}

async function plantumlSvgUrl(source) {{
  const normalized = normalizePlantUmlSource(source);
  const deflated = await deflateRaw(normalized);
  if (!deflated) return null;
  return PLANTUML_SERVER + '/svg/' + encodePlantUml64(deflated);
}}

function isPlantUmlBlock(codeEl) {{
  const cls = (codeEl.className || '').toLowerCase();
  if (/language-(plantuml|uml|puml)\\b/.test(cls)) return true;
  return /@startuml/i.test(codeEl.textContent || '');
}}

function findPlantUmlBlocks(container) {{
  const blocks = [];
  container.querySelectorAll('pre code').forEach(code => {{
    if (isPlantUmlBlock(code)) {{
      const pre = code.closest('pre');
      if (pre && !pre.dataset.plantumlDone) blocks.push(code);
    }}
  }});
  return blocks;
}}

function showPlantUmlHint(pre) {{
  if (pre.dataset.plantumlHint) return;
  pre.dataset.plantumlHint = '1';
  const hint = document.createElement('div');
  hint.className = 'plantuml-hint';
  hint.innerHTML = '<p><em>Diagrama PlantUML não renderizado.</em> Suba o servidor local: '
    + '<code>.domain/scripts/start_plantuml_server.sh</code> '
    + '(porta 8765). Ver <code>domain-kit/references/plantuml-dashboard.md</code>.</p>';
  pre.insertAdjacentElement('afterend', hint);
}}

async function renderPlantUmlBlock(codeEl) {{
  const pre = codeEl.closest('pre');
  if (!pre || pre.dataset.plantumlDone) return;
  const source = normalizePlantUmlSource(codeEl.textContent);

  async function renderViaImg() {{
    const url = await plantumlSvgUrl(source);
    if (!url) return null;
    return new Promise(resolve => {{
      const img = document.createElement('img');
      img.alt = 'Diagrama PlantUML';
      img.onload = () => resolve(img);
      img.onerror = () => resolve(null);
      img.src = url;
    }});
  }}

  async function renderViaPost() {{
    try {{
      const resp = await fetch(PLANTUML_SERVER + '/svg', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'text/plain' }},
        body: source,
      }});
      if (!resp.ok) return null;
      const svg = await resp.text();
      if (!svg.includes('<svg')) return null;
      const wrap = document.createElement('div');
      wrap.innerHTML = svg;
      return wrap.firstElementChild || wrap;
    }} catch (_) {{
      return null;
    }}
  }}

  const rendered = await renderViaImg() || await renderViaPost();
  if (rendered) {{
    const wrap = document.createElement('div');
    wrap.className = 'plantuml-diagram';
    wrap.appendChild(rendered);
    pre.replaceWith(wrap);
    return;
  }}

  pre.dataset.plantumlDone = 'failed';
  showPlantUmlHint(pre);
}}

async function renderPlantUmlIn(container) {{
  const blocks = findPlantUmlBlocks(container);
  for (const block of blocks) {{
    await renderPlantUmlBlock(block);
  }}
}}

let mermaidReady = false;
function ensureMermaid() {{
  if (mermaidReady || !window.mermaid) return false;
  mermaid.initialize({{
    startOnLoad: false,
    theme: 'dark',
    securityLevel: 'loose',
    flowchart: {{ useMaxWidth: true, htmlLabels: true }},
  }});
  mermaidReady = true;
  return true;
}}

function findMermaidBlocks(container) {{
  const blocks = [];
  container.querySelectorAll('pre code').forEach(code => {{
    const cls = (code.className || '').toLowerCase();
    if (!/language-mermaid\\b/.test(cls)) return;
    const pre = code.closest('pre');
    if (pre && !pre.dataset.mermaidDone) blocks.push(code);
  }});
  return blocks;
}}

async function renderMermaidBlock(codeEl) {{
  const pre = codeEl.closest('pre');
  if (!pre || pre.dataset.mermaidDone) return;
  if (!ensureMermaid()) {{
    pre.dataset.mermaidDone = 'failed';
    return;
  }}
  const source = (codeEl.textContent || '').trim();
  const id = 'mermaid-' + Math.random().toString(36).slice(2, 10);
  try {{
    const result = await mermaid.render(id, source);
    const wrap = document.createElement('div');
    wrap.className = 'mermaid-diagram';
    wrap.innerHTML = result.svg;
    pre.replaceWith(wrap);
  }} catch (err) {{
    pre.dataset.mermaidDone = 'failed';
    const hint = document.createElement('div');
    hint.className = 'mermaid-hint';
    hint.innerHTML = '<p><em>Diagrama Mermaid não renderizado.</em> '
      + escapeHtml(String(err.message || err)) + '</p>';
    pre.insertAdjacentElement('afterend', hint);
  }}
}}

async function renderMermaidIn(container) {{
  const blocks = findMermaidBlocks(container);
  for (const block of blocks) {{
    await renderMermaidBlock(block);
  }}
}}

async function setPreview(key, text) {{
  const el = document.getElementById('doc-preview');
  el.innerHTML = renderMarkdown(text, key);
  await renderMermaidIn(el);
  await renderPlantUmlIn(el);
}}

function setViewHint(text) {{
  const hint = document.getElementById('view-hint');
  if (hint) hint.textContent = text;
}}

function showDiscover() {{
  document.getElementById('center-discover')?.classList.add('active');
  document.getElementById('center-file')?.classList.remove('active');
  document.getElementById('nav-discover')?.classList.add('active');
  document.querySelectorAll('.nav-file-item').forEach(x => x.classList.remove('selected'));
  setViewHint('visão: menu Discover');
  try {{ localStorage.setItem('dk-center-view', 'discover'); }} catch (_) {{}}
}}

async function showFile(key, text, isDraft) {{
  document.getElementById('center-discover')?.classList.remove('active');
  document.getElementById('center-file')?.classList.add('active');
  document.getElementById('nav-discover')?.classList.remove('active');
  document.querySelectorAll('.nav-file-item').forEach(x => {{
    const itemKey = x.dataset.doc || x.dataset.draftKey;
    x.classList.toggle('selected', itemKey === key);
  }});
  const kind = document.getElementById('file-kind');
  const pathEl = document.getElementById('file-path');
  if (kind) kind.textContent = isDraft ? 'Rascunho' : 'Artefato';
  if (pathEl) pathEl.textContent = key || '—';
  setViewHint('visão: ' + (key || 'arquivo'));
  await setPreview(key, text);
  try {{ localStorage.setItem('dk-center-view', 'file:' + key); }} catch (_) {{}}
}}

function filterNavFiles(query) {{
  const q = (query || '').trim().toLowerCase();
  document.querySelectorAll('.nav-file-item').forEach(item => {{
    const hay = (item.dataset.doc || item.dataset.draftKey || item.textContent || '').toLowerCase();
    item.hidden = Boolean(q) && !hay.includes(q);
  }});
}}

document.getElementById('nav-discover')?.addEventListener('click', () => showDiscover());
document.getElementById('back-discover')?.addEventListener('click', () => showDiscover());

document.getElementById('nav-file-filter')?.addEventListener('input', (e) => {{
  filterNavFiles(e.target.value);
}});

document.querySelectorAll('.nav-file-item[data-doc]').forEach(li => {{
  const open = () => {{
    const k = li.dataset.doc;
    showFile(k, DOCS[k] || '', false);
  }};
  li.addEventListener('click', open);
  li.addEventListener('keydown', (e) => {{
    if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); open(); }}
  }});
}});

document.querySelectorAll('.nav-file-item[data-draft-key]').forEach(li => {{
  const open = () => {{
    const k = li.dataset.draftKey;
    const text = DRAFTS[k] || DRAFTS['.draft/' + k]
      || Object.entries(DRAFTS).find(([p]) => p.endsWith(k))?.[1] || '';
    showFile(k, text, true);
  }};
  li.addEventListener('click', open);
  li.addEventListener('keydown', (e) => {{
    if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); open(); }}
  }});
}});

showDiscover();
try {{
  const saved = localStorage.getItem('dk-center-view');
  if (saved && saved.startsWith('file:')) {{
    const key = saved.slice(5);
    const draftText = DRAFTS[key] || DRAFTS['.draft/' + key]
      || Object.entries(DRAFTS).find(([p]) => p.endsWith(key))?.[1];
    if (DOCS[key]) showFile(key, DOCS[key], false);
    else if (draftText) showFile(key, draftText, true);
  }}
}} catch (_) {{}}
"""

    product_card_hero = ""
    if (product_dir / "product-README.md").is_file():
        product_card_hero = (
            '<p class="hero-card-link">'
            '<a class="btn-product-card hero" data-doc="product-README.md" href="#">'
            "Cartão do produto</a></p>"
        )

    body = f"""
<header class="hero">
  <div class="hero-top">
    <div>
      <h1>{escape(product)}</h1>
      <p class="hero-sub">Domain-kit · mapeamento negócio → domínio</p>
      {product_card_hero}
    </div>
    <div class="pills">
      <span class="pill pill-accent">fase: {escape(phase)}</span>
      <span class="pill">scan: {escape(scan)}</span>
      <span class="pill">discover: {discover_total}%</span>
      <span class="pill">{art_count} artefatos</span>
      <span class="pill view-hint" id="view-hint">visão: menu Visão geral</span>
    </div>
  </div>
</header>

<div class="main-layout">
  <aside class="sidebar">
    <div class="sidebar-section">
      <h3>Arquivos</h3>
      <button type="button" class="nav-home active" id="nav-discover">
        <span class="nav-home-title">Visão geral</span>
        <span class="nav-home-sub">{discover_total}% · fases</span>
      </button>
      <input type="search" class="nav-file-search" id="nav-file-filter" placeholder="Filtrar arquivos…" autocomplete="off" />
      <details class="nav-tree" open>
        <summary>Artefatos ({art_count})</summary>
        <ul class="nav-file-list">{art_items}</ul>
      </details>
      <details class="nav-tree" open>
        <summary>Rascunhos ({draft_count})</summary>
        <ul class="nav-file-list">{draft_list_html}</ul>
      </details>
    </div>
    <div class="sidebar-section">
      <h3>Fluxos</h3>
      <div class="flow-list-compact">{flow_sidebar_html}</div>
    </div>
  </aside>

  <div class="work-area">
    <div id="center-discover" class="center-panel active">
      {discover_home_html}
    </div>
    <div id="center-file" class="center-panel">
      <div class="file-view-bar">
        <button type="button" class="btn-back" id="back-discover">Voltar ao Discover</button>
        <span class="file-breadcrumb">
          <strong id="file-kind">Artefato</strong> / <code id="file-path">—</code>
        </span>
      </div>
      <div class="preview-body" id="doc-preview"></div>
    </div>
  </div>
</div>

<div class="help">
  <strong>Plan mode</strong> — rascunhos não contam nas fases até promote.
  Discover unificado (fontes + DDD). Docs: <code>domain-kit/GUIDE.md</code>
</div>
"""

    return render_shell(
        f"Domain-Kit — {product}",
        body,
        script,
        extra_head=dashboard_vendor_script_tags(depth=2),
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
