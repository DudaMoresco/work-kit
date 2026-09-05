/* domain-kit dashboard client — layout ciclo completo */
const DOCS = window.__DK_DOCS__ || {};
const DRAFTS = window.__DK_DRAFTS__ || {};
const PLANTUML_SERVER = window.__DK_PLANTUML_SERVER__ || "http://127.0.0.1:8765";
const VENDOR_CDN = {
  marked: "https://cdn.jsdelivr.net/npm/marked@11.1.1/marked.min.js",
  mermaid: "https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js",
};

function escapeHtml(text) {
  const el = document.createElement('div');
  el.textContent = text;
  return el.innerHTML;
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const existing = document.querySelector(`script[src="${src}"]`);
    if (existing) {
      existing.addEventListener('load', () => resolve());
      existing.addEventListener('error', () => reject(new Error(src)));
      // already loaded
      if (existing.dataset.loaded === '1') resolve();
      return;
    }
    const s = document.createElement('script');
    s.src = src;
    s.async = true;
    s.onload = () => { s.dataset.loaded = '1'; resolve(); };
    s.onerror = () => reject(new Error('Failed to load ' + src));
    document.head.appendChild(s);
  });
}

async function ensurePreviewLibs() {
  const markedOk = () => !!(window.marked && (window.marked.parse || typeof window.marked === 'function'));
  if (!markedOk()) {
    try { await loadScript(VENDOR_CDN.marked); } catch (_) {}
  }
  if (!window.mermaid) {
    try { await loadScript(VENDOR_CDN.mermaid); } catch (_) {}
  }
}

function parseMarkdown(text) {
  const m = window.marked;
  if (!m) return null;
  try {
    if (typeof m.parse === 'function') return m.parse(text, { gfm: true, breaks: false });
    if (typeof m.marked === 'function') return m.marked(text, { gfm: true, breaks: false });
    if (typeof m === 'function') return m(text, { gfm: true, breaks: false });
  } catch (_) {}
  return null;
}

/** Offline-ish fallback: keep fenced code blocks so PlantUML/Mermaid can still run. */
function renderMarkdownFallback(text) {
  const parts = [];
  const fence = /```([^\n`]*)\n([\s\S]*?)```/g;
  let last = 0;
  let match;
  while ((match = fence.exec(text)) !== null) {
    const before = text.slice(last, match.index);
    if (before.trim()) {
      parts.push(`<pre class="md-fallback">${escapeHtml(before)}</pre>`);
    }
    const lang = (match[1] || '').trim().split(/\s+/)[0].toLowerCase();
    const body = match[2] || '';
    const cls = lang ? ` class="language-${escapeHtml(lang)}"` : '';
    parts.push(`<pre><code${cls}>${escapeHtml(body)}</code></pre>`);
    last = match.index + match[0].length;
  }
  const rest = text.slice(last);
  if (rest.trim()) {
    parts.push(`<pre class="md-fallback">${escapeHtml(rest)}</pre>`);
  }
  return parts.join('\n') || `<pre class="md-fallback">${escapeHtml(text)}</pre>`;
}

function renderMarkdown(text, path) {
  if (!text) return '<p class="empty">Sem conteúdo.</p>';
  const ext = (path || '').split('.').pop().toLowerCase();
  if (ext === 'md') {
    return parseMarkdown(text) || renderMarkdownFallback(text);
  }
  return `<pre class="md-fallback"><code>${escapeHtml(text)}</code></pre>`;
}

function normalizePlantUmlSource(source) {
  const trimmed = (source || '').trim();
  if (!trimmed) return '';
  if (/@startuml/i.test(trimmed)) return trimmed;
  return '@startuml\n' + trimmed + '\n@enduml';
}

function encode6bit(b) {
  if (b < 10) return String.fromCharCode(48 + b);
  b -= 10;
  if (b < 26) return String.fromCharCode(65 + b);
  b -= 26;
  if (b < 26) return String.fromCharCode(97 + b);
  b -= 26;
  if (b === 0) return '-';
  if (b === 1) return '_';
  return '?';
}

function append3bytes(b1, b2, b3) {
  const c1 = b1 >> 2;
  const c2 = ((b1 & 0x3) << 4) | (b2 >> 4);
  const c3 = ((b2 & 0xF) << 2) | (b3 >> 6);
  const c4 = b3 & 0x3F;
  return (
    encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) +
    encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)
  );
}

function encodePlantUml64(data) {
  let r = '';
  for (let i = 0; i < data.length; i += 3) {
    if (i + 2 === data.length) {
      r += append3bytes(data.charCodeAt(i), data.charCodeAt(i + 1), 0);
    } else if (i + 1 === data.length) {
      r += append3bytes(data.charCodeAt(i), 0, 0);
    } else {
      r += append3bytes(data.charCodeAt(i), data.charCodeAt(i + 1), data.charCodeAt(i + 2));
    }
  }
  return r;
}

async function deflateRaw(text) {
  const data = new TextEncoder().encode(text);
  if (typeof CompressionStream !== 'undefined') {
    const stream = new Blob([data]).stream().pipeThrough(new CompressionStream('deflate-raw'));
    const buf = await new Response(stream).arrayBuffer();
    return String.fromCharCode(...new Uint8Array(buf));
  }
  return null;
}

async function plantumlSvgUrl(source) {
  const normalized = normalizePlantUmlSource(source);
  const deflated = await deflateRaw(normalized);
  if (!deflated) return null;
  return PLANTUML_SERVER + '/svg/' + encodePlantUml64(deflated);
}

function isPlantUmlBlock(codeEl) {
  const cls = (codeEl.className || '').toLowerCase();
  if (/language-(plantuml|uml|puml)\b/.test(cls)) return true;
  return /@startuml/i.test(codeEl.textContent || '');
}

function findPlantUmlBlocks(container) {
  const blocks = [];
  container.querySelectorAll('pre code').forEach(code => {
    if (isPlantUmlBlock(code)) {
      const pre = code.closest('pre');
      if (pre && !pre.dataset.plantumlDone) blocks.push(code);
    }
  });
  return blocks;
}

function showPlantUmlHint(pre) {
  if (pre.dataset.plantumlHint) return;
  pre.dataset.plantumlHint = '1';
  const hint = document.createElement('div');
  hint.className = 'plantuml-hint';
  hint.innerHTML = '<p><em>Diagrama PlantUML não renderizado.</em> Suba o servidor local: '
    + '<code>.domain/scripts/start_plantuml_server.sh</code> '
    + '(porta 8765).</p>';
  pre.insertAdjacentElement('afterend', hint);
}

async function renderPlantUmlBlock(codeEl) {
  const pre = codeEl.closest('pre');
  if (!pre || pre.dataset.plantumlDone) return;
  const source = normalizePlantUmlSource(codeEl.textContent);

  async function renderViaImg() {
    const url = await plantumlSvgUrl(source);
    if (!url) return null;
    return new Promise(resolve => {
      const img = document.createElement('img');
      img.alt = 'Diagrama PlantUML';
      img.onload = () => resolve(img);
      img.onerror = () => resolve(null);
      img.src = url;
    });
  }

  async function renderViaPost() {
    try {
      const resp = await fetch(PLANTUML_SERVER + '/svg', {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain' },
        body: source,
      });
      if (!resp.ok) return null;
      const svg = await resp.text();
      if (!svg.includes('<svg')) return null;
      const wrap = document.createElement('div');
      wrap.innerHTML = svg;
      return wrap.firstElementChild || wrap;
    } catch (_) {
      return null;
    }
  }

  const rendered = await renderViaImg() || await renderViaPost();
  if (rendered) {
    const wrap = document.createElement('div');
    wrap.className = 'plantuml-diagram';
    wrap.appendChild(rendered);
    pre.replaceWith(wrap);
    return;
  }

  pre.dataset.plantumlDone = 'failed';
  showPlantUmlHint(pre);
}

async function renderPlantUmlIn(container) {
  const blocks = findPlantUmlBlocks(container);
  for (const block of blocks) {
    await renderPlantUmlBlock(block);
  }
}

let mermaidReady = false;
function ensureMermaid() {
  if (mermaidReady || !window.mermaid) return false;
  mermaid.initialize({
    startOnLoad: false,
    theme: 'dark',
    securityLevel: 'loose',
    flowchart: { useMaxWidth: true, htmlLabels: true },
  });
  mermaidReady = true;
  return true;
}

function findMermaidBlocks(container) {
  const blocks = [];
  container.querySelectorAll('pre code').forEach(code => {
    const cls = (code.className || '').toLowerCase();
    if (!/language-mermaid\b/.test(cls)) return;
    const pre = code.closest('pre');
    if (pre && !pre.dataset.mermaidDone) blocks.push(code);
  });
  return blocks;
}

async function renderMermaidBlock(codeEl) {
  const pre = codeEl.closest('pre');
  if (!pre || pre.dataset.mermaidDone) return;
  if (!ensureMermaid()) {
    pre.dataset.mermaidDone = 'failed';
    return;
  }
  const source = (codeEl.textContent || '').trim();
  const id = 'mermaid-' + Math.random().toString(36).slice(2, 10);
  try {
    const result = await mermaid.render(id, source);
    const wrap = document.createElement('div');
    wrap.className = 'mermaid-diagram';
    wrap.innerHTML = result.svg;
    pre.replaceWith(wrap);
  } catch (err) {
    pre.dataset.mermaidDone = 'failed';
    const hint = document.createElement('div');
    hint.className = 'mermaid-hint';
    hint.innerHTML = '<p><em>Diagrama Mermaid não renderizado.</em> '
      + escapeHtml(String(err.message || err)) + '</p>';
    pre.insertAdjacentElement('afterend', hint);
  }
}

async function renderMermaidIn(container) {
  const blocks = findMermaidBlocks(container);
  for (const block of blocks) {
    await renderMermaidBlock(block);
  }
}

async function setPreview(key, text) {
  const el = document.getElementById('doc-preview');
  if (!el) return;
  await ensurePreviewLibs();
  el.innerHTML = renderMarkdown(text, key);
  await renderMermaidIn(el);
  await renderPlantUmlIn(el);
}

const app = document.querySelector('.app, .shell');
const MODE_KEY = 'dk-dashboard-mode';

function setMode(mode) {
  if (!app) return;
  const next = mode === 'artefatos' ? 'artefatos' : 'ciclo';
  app.dataset.mode = next;
  document.querySelectorAll('.mode-btn').forEach(btn => {
    const on = btn.dataset.mode === next;
    btn.classList.toggle('active', on);
    btn.setAttribute('aria-selected', on ? 'true' : 'false');
  });
  try { localStorage.setItem(MODE_KEY, next); } catch (_) {}
}

async function showFile(key, text, isDraft) {
  setMode('artefatos');
  const wrap = document.getElementById('file-preview-wrap');
  const empty = document.getElementById('preview-empty');
  if (wrap) wrap.hidden = false;
  if (empty) empty.hidden = true;
  document.querySelectorAll('.file-item').forEach(x => {
    const itemKey = x.dataset.doc || x.dataset.draftKey;
    x.classList.toggle('selected', itemKey === key);
  });
  const kind = document.getElementById('file-kind');
  const pathEl = document.getElementById('file-path');
  if (kind) kind.textContent = isDraft ? 'Rascunho' : 'Artefato';
  if (pathEl) pathEl.textContent = key || '—';
  await setPreview(key, text);
  wrap?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  try { localStorage.setItem('dk-center-view', 'file:' + key); } catch (_) {}
}

function hidePreview() {
  const wrap = document.getElementById('file-preview-wrap');
  const empty = document.getElementById('preview-empty');
  if (wrap) wrap.hidden = true;
  if (empty) empty.hidden = false;
  document.querySelectorAll('.file-item').forEach(x => x.classList.remove('selected'));
  try { localStorage.setItem('dk-center-view', 'overview'); } catch (_) {}
}

function draftTextFor(key) {
  return DRAFTS[key] || DRAFTS['.draft/' + key]
    || Object.entries(DRAFTS).find(([p]) => p.endsWith(key))?.[1] || '';
}

document.querySelectorAll('.mode-btn').forEach(btn => {
  btn.addEventListener('click', () => setMode(btn.dataset.mode));
});

document.getElementById('btn-goto-artefatos')?.addEventListener('click', () => {
  setMode('artefatos');
});

document.querySelectorAll('.phase').forEach(btn => {
  btn.addEventListener('click', () => {
    setMode('artefatos');
    const phase = btn.dataset.phase;
    const filter = document.getElementById('file-filter');
    if (filter) {
      filter.value = phase || '';
      filter.dispatchEvent(new Event('input'));
    }
    document.querySelectorAll('.browse-nav .file-item').forEach(item => {
      if (item.dataset.phase === phase) {
        item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    });
  });
});

document.getElementById('back-overview')?.addEventListener('click', () => hidePreview());

document.querySelectorAll('.file-item[data-doc]').forEach(li => {
  const open = () => {
    const k = li.dataset.doc;
    showFile(k, DOCS[k] || '', false);
  };
  li.addEventListener('click', (e) => {
    e.preventDefault();
    open();
  });
  li.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
  });
});

document.querySelectorAll('.file-item[data-draft-key]').forEach(li => {
  const open = () => {
    const k = li.dataset.draftKey;
    showFile(k, draftTextFor(k), true);
  };
  li.addEventListener('click', open);
  li.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
  });
});

document.querySelectorAll('a[data-doc]').forEach(a => {
  a.addEventListener('click', (e) => {
    e.preventDefault();
    const k = a.dataset.doc;
    showFile(k, DOCS[k] || '', false);
  });
});

document.getElementById('file-filter')?.addEventListener('input', (e) => {
  const q = (e.target.value || '').trim().toLowerCase();
  document.querySelectorAll('.browse-nav .file-item').forEach(item => {
    const name = (item.querySelector('.file-name')?.textContent || '').toLowerCase();
    const tag = (item.querySelector('.file-tag')?.textContent || '').toLowerCase();
    const phase = (item.dataset.phase || '').toLowerCase();
    const path = (item.dataset.doc || item.dataset.draftKey || '').toLowerCase();
    const hay = `${name} ${tag} ${phase} ${path}`;
    item.hidden = Boolean(q) && !hay.includes(q);
  });
});

document.getElementById('btn-copy-cmd')?.addEventListener('click', async () => {
  const cmd = document.getElementById('btn-copy-cmd')?.dataset.cmd || '';
  if (!cmd) return;
  try {
    await navigator.clipboard.writeText(cmd);
    const btn = document.getElementById('btn-copy-cmd');
    const old = btn.textContent;
    btn.textContent = 'Copiado';
    setTimeout(() => { btn.textContent = old; }, 1200);
  } catch (_) {}
});

try {
  setMode(localStorage.getItem(MODE_KEY) || 'ciclo');
} catch (_) {
  setMode('ciclo');
}

try {
  const saved = localStorage.getItem('dk-center-view');
  if (saved && saved.startsWith('file:')) {
    const key = saved.slice(5);
    const draft = draftTextFor(key);
    if (DOCS[key]) showFile(key, DOCS[key], false);
    else if (draft) showFile(key, draft, true);
  }
} catch (_) {}
