"""
md_render.py — Shared programmatic Markdown-to-HTML renderer.

Extracted from doc2html-motion/program/stage_04_render.py. Provides pure
parsing and rendering functions that any agent with Markdown input can import
to generate interactive HTML widgets without AI token cost.

Usage in a programmatic stage:
    import sys
    from pathlib import Path
    _SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "html-shell"
    sys.path.insert(0, str(_SKILL_DIR))
    from md_render import (
        parse_rendered_md, render_blocks_html, motion_widget_html, widget_css
    )

    uid_counter = [0]
    title, lang, sections = parse_rendered_md(raw_md)
    for sec in sections:
        body_html = render_blocks_html(sec["blocks"], uid_counter)
        ...
    css = widget_css()

All functions are pure (no file I/O, no global state). The uid_counter list
is a mutable container owned by the caller; pass the same instance across
render_blocks_html calls within a single render to ensure globally-unique IDs.
"""

from __future__ import annotations
import html as _html_lib
import re


# ── Markdown inline utilities ──────────────────────────────────────────────────

def md_inline(text: str) -> str:
    """Convert inline Markdown to HTML (bold, italic, code, links)."""
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__([^_\n]+)__',     r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*\n]+)\*',     r'<em>\1</em>', text)
    text = re.sub(r'_([^_\n]+)_',       r'<em>\1</em>', text)
    text = re.sub(r'`([^`\n]+)`',       r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def _slugify(text: str) -> str:
    """Convert text to a simple kebab-case slug (for section IDs only)."""
    return re.sub(r'[^\w]+', '-', text.lower()).strip('-')


def detect_lang(text: str) -> str:
    """Detect document language from common word frequency. Returns 'pt-BR' or 'en'."""
    pt = len(re.findall(
        r'\b(de|da|do|para|com|uma|um|por|que|não|são|está|como|mais|também)\b',
        text, re.I
    ))
    return "pt-BR" if pt > 5 else "en"


# ── Status badge helpers ───────────────────────────────────────────────────────

_STATUS_VOCAB: dict[str, str] = {
    "ok": "ok", "done": "ok", "completo": "ok", "concluído": "ok", "aprovado": "ok",
    "yes": "ok", "sim": "ok", "✓": "ok", "pass": "ok",
    "warn": "warn", "warning": "warn", "atenção": "warn", "pendente": "warn",
    "pending": "warn", "in progress": "warn", "em andamento": "warn", "partial": "warn",
    "danger": "danger", "erro": "danger", "error": "danger", "risco": "danger",
    "failed": "danger", "falhou": "danger", "no": "danger", "não": "danger", "✗": "danger",
    "info": "info", "informação": "info", "note": "info",
    "n/a": "muted", "—": "muted", "-": "muted", "tbd": "muted",
}


def _status_semantic(text: str) -> str | None:
    return _STATUS_VOCAB.get(text.strip().lower())


def _is_numeric_cell(text: str) -> bool:
    return bool(re.match(r'^[\d\s,.$€R%+\-–]+$', text.strip()))


# ── List item parser ───────────────────────────────────────────────────────────

def _parse_list_items(raw_lines: list[str]) -> list[dict]:
    """Parse raw bullet lines into structured items with depth and checklist state."""
    items = []
    for line in raw_lines:
        stripped = line.lstrip()
        depth = (len(line) - len(stripped)) // 2
        text = re.sub(r'^[-*]\s+', '', stripped).strip()
        checked: bool | None = None
        cm = re.match(r'^\[([ xX])\]\s*(.*)', text)
        if cm:
            checked = cm.group(1).lower() == 'x'
            text = cm.group(2).strip()
        items.append({"text": text, "depth": depth, "checked": checked})
    return items


def _classify_items(items: list[dict]) -> str:
    """Classify a list of parsed items into a widget type string."""
    top = [it for it in items if it["depth"] == 0]
    if not top:
        return "highlight"
    if all(it["checked"] is not None for it in top):
        return "checklist"
    if any(it["depth"] > 0 for it in items):
        return "tree"
    def_count = sum(1 for it in top if re.match(r'\*\*[^*]+\*\*', it["text"]))
    if def_count >= max(2, len(top) * 0.6):
        return "def_list"
    return "card_grid" if len(top) > 8 else "highlight"


# ── Block parser ───────────────────────────────────────────────────────────────

def parse_blocks(lines: list[str]) -> list[dict]:
    """Parse section lines into typed content blocks."""
    blocks: list[dict] = []
    para: list[str] = []

    def _flush_para() -> None:
        joined = " ".join(para).strip()
        para.clear()
        if not joined:
            return
        fig = re.match(r'!\[([^\]]*)\]\(([^)]+)\)\s*$', joined.strip())
        if fig:
            blocks.append({"type": "figure", "alt": fig.group(1), "src": fig.group(2)})
        else:
            blocks.append({"type": "para", "content": joined})

    i = 0
    while i < len(lines):
        line = lines[i]

        if line.strip().startswith("```"):
            _flush_para()
            lang = line.strip()[3:].strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append({"type": "code", "lang": lang, "content": "\n".join(code_lines)})
            i += 1
            continue

        if line.startswith("> ") or line == ">":
            _flush_para()
            bq: list[str] = []
            while i < len(lines) and (lines[i].startswith("> ") or lines[i] == ">"):
                bq.append(lines[i][2:].strip() if lines[i].startswith("> ") else "")
                i += 1
            if bq:
                blocks.append({"type": "blockquote", "lines": bq})
            continue

        if line.startswith("### "):
            _flush_para()
            blocks.append({"type": "h3", "content": line[4:].strip()})

        elif line.startswith("#### "):
            _flush_para()
            blocks.append({"type": "h4", "content": line[5:].strip()})

        elif line.startswith("- ") or line.startswith("* "):
            _flush_para()
            raw: list[str] = []
            while i < len(lines) and (
                lines[i].startswith("- ") or
                lines[i].startswith("* ") or
                re.match(r'^  +[-*] ', lines[i])
            ):
                raw.append(lines[i])
                i += 1
            if raw:
                items = _parse_list_items(raw)
                kind  = _classify_items(items)
                blocks.append({"type": kind, "items": items})
            continue

        elif re.match(r'^\d+\.\s', line):
            _flush_para()
            ol_items: list[dict] = []
            while i < len(lines) and re.match(r'^\d+\.\s', lines[i]):
                ol_items.append({"text": re.sub(r'^\d+\.\s+', '', lines[i]).strip(),
                                  "depth": 0, "checked": None})
                i += 1
            blocks.append({"type": "ol", "items": ol_items})
            continue

        elif "|" in line and i + 1 < len(lines) and re.match(r'^\s*\|[-| :]+\|', lines[i + 1]):
            _flush_para()
            tbl: list[str] = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                tbl.append(lines[i])
                i += 1
            blocks.append({"type": "table", "lines": tbl})
            continue

        elif line.strip() in ("", "---", "***", "- - -"):
            _flush_para()

        else:
            para.append(line.strip())

        i += 1

    _flush_para()
    return [b for b in blocks if (
        b.get("content") or b.get("items") or b.get("lines") or
        b.get("src") or b["type"] == "code"
    )]


def parse_rendered_md(content: str) -> tuple[str, str, list[dict]]:
    """
    Parse rendered.md content into (title, lang, sections).

    Args:
        content: Full text of rendered.md (may include frontmatter separated by ---).

    Returns:
        title:    Document title (from first # heading, or "Document").
        lang:     Detected language ("pt-BR" or "en").
        sections: List of section dicts: {id, heading, blocks: list[dict]}.
    """
    if "\n---\n" in content:
        content = content.split("\n---\n", 1)[1]

    lines = content.splitlines()
    lang  = detect_lang(content)

    title = "Document"
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    sections: list[dict] = []
    current: dict | None  = None
    buf: list[str]        = []

    def _flush_section() -> None:
        if current is not None:
            current["blocks"] = parse_blocks(buf)
            sections.append(current)

    for line in lines:
        if line.startswith("## "):
            _flush_section()
            heading = line[3:].strip()
            current = {"id": _slugify(heading), "heading": heading, "blocks": []}
            buf = []
        elif current is not None:
            buf.append(line)

    _flush_section()
    return title, lang, sections


# ── Widget renderers ───────────────────────────────────────────────────────────

def render_highlight_list(items: list[dict]) -> str:
    """Render a bullet list as an accent-styled highlight list."""
    top = [it for it in items if it["depth"] == 0]
    lis = "\n".join(f'<li>{md_inline(it["text"])}</li>' for it in top)
    return f'<ul class="highlight-list widget">\n{lis}\n</ul>'


def render_card_grid(items: list[dict]) -> str:
    """Render a large bullet list as a card grid (>8 items or explicit card_grid type)."""
    top = [it for it in items if it["depth"] == 0]
    cards = []
    for it in top:
        text = it["text"]
        m = re.match(r'\*\*([^*]+)\*\*\s*(.*)', text, re.DOTALL)
        if m:
            title = md_inline(f"**{m.group(1)}**")
            body  = md_inline(m.group(2).lstrip("—:– ").strip())
        else:
            if ". " in text:
                idx = text.index(". ")
                title = md_inline(text[:idx + 1])
                body  = md_inline(text[idx + 2:].strip())
            else:
                title = md_inline(text)
                body  = ""
        body_html = f'<div class="card-body">{body}</div>' if body else ""
        cards.append(
            f'<div class="card-item">'
            f'<div class="card-title">{title}</div>'
            f'{body_html}'
            f'</div>'
        )
    return f'<div class="card-grid widget">\n{"".join(cards)}\n</div>'


def render_checklist(items: list[dict], uid: str) -> str:
    """Render a checklist with an SVG progress ring and localStorage persistence."""
    top = [it for it in items if it["depth"] == 0]
    total = len(top)
    done  = sum(1 for it in top if it["checked"])
    pct   = int(done / total * 100) if total else 0
    circ  = 150.8
    offset = circ - (circ * pct / 100)
    label_text = "itens concluídos"

    item_rows = []
    for idx, it in enumerate(top):
        iid      = f"{uid}-i{idx}"
        checked  = 'checked' if it["checked"] else ''
        done_cls = ' done' if it["checked"] else ''
        item_rows.append(
            f'<div class="checklist-item{done_cls}" id="{iid}">'
            f'<input type="checkbox" {checked} '
            f'onchange="updateChecklist(\'{uid}\',\'{iid}\',this.checked)">'
            f'<label class="checklist-label" for="{iid}">'
            f'<span class="item-text">{md_inline(it["text"])}</span>'
            f'</label>'
            f'</div>'
        )

    items_html = "\n".join(item_rows)
    return f'''<div class="checklist-widget widget" id="{uid}" data-checklist=\'{{"uid":"{uid}","total":{total},"done":{done}}}\'>
  <div class="checklist-ring-wrap">
    <svg class="progress-ring" viewBox="0 0 60 60" aria-hidden="true">
      <circle class="ring-track" cx="30" cy="30" r="24"/>
      <circle class="ring-fill" id="{uid}-ring" cx="30" cy="30" r="24"
              style="stroke-dashoffset:{offset:.1f}"/>
    </svg>
    <div class="ring-label">
      <span class="ring-pct" id="{uid}-pct">{pct}%</span>
      {label_text}
    </div>
  </div>
  <div class="checklist-group">
    <div class="checklist-items">
{items_html}
    </div>
  </div>
</div>'''


def render_sortable_table(table_lines: list[str], uid: str) -> str:
    """Render a Markdown table as a sortable data table with status badges."""
    if len(table_lines) < 2:
        return ""

    headers = [c.strip() for c in table_lines[0].strip().strip("|").split("|")]
    is_status_col  = [False] * len(headers)
    is_numeric_col = [False] * len(headers)

    data_rows = [r for r in table_lines[2:] if "|" in r]
    if data_rows:
        for col_idx in range(len(headers)):
            cells = []
            for row in data_rows:
                parts = [c.strip() for c in row.strip().strip("|").split("|")]
                if col_idx < len(parts):
                    cells.append(parts[col_idx])
            if cells:
                status_hits  = sum(1 for c in cells if _status_semantic(c))
                numeric_hits = sum(1 for c in cells if _is_numeric_cell(c) and c.strip())
                is_status_col[col_idx]  = status_hits >= len(cells) * 0.5
                is_numeric_col[col_idx] = (not is_status_col[col_idx]) and numeric_hits >= len(cells) * 0.5

    th_cells = []
    for ci, h in enumerate(headers):
        th_cells.append(
            f'<th onclick="sortTable(\'{uid}\',{ci})">'
            f'{md_inline(h)}<span class="sort-icon"></span></th>'
        )
    thead = f'<thead><tr>{"".join(th_cells)}</tr></thead>'

    tbody_rows = []
    for row_line in data_rows:
        cells = [c.strip() for c in row_line.strip().strip("|").split("|")]
        td_cells = []
        for ci in range(len(headers)):
            val = cells[ci] if ci < len(cells) else ""
            sem = _status_semantic(val) if is_status_col[ci] else None
            if sem:
                cell_html = f'<span class="status-badge status-{sem}">{md_inline(val)}</span>'
                td_cells.append(f'<td>{cell_html}</td>')
            elif is_numeric_col[ci]:
                td_cells.append(f'<td class="mono-cell">{md_inline(val)}</td>')
            else:
                td_cells.append(f'<td>{md_inline(val)}</td>')
        tbody_rows.append(f'<tr>{"".join(td_cells)}</tr>')

    tbody = f'<tbody>{"".join(tbody_rows)}</tbody>'
    return (
        f'<div class="table-wrap widget">'
        f'<table class="data-table" id="{uid}">'
        f'{thead}{tbody}'
        f'</table></div>'
    )


def render_pull_quote(lines: list[str]) -> str:
    """Render a blockquote as a styled pull quote."""
    text = " ".join(line for line in lines if line)
    return f'<blockquote class="pull-quote widget">{md_inline(text)}</blockquote>'


def render_code_block(content: str, lang: str) -> str:
    """Render a fenced code block with optional language label."""
    escaped = _html_lib.escape(content)
    label   = f'<div class="code-lang-label">{lang}</div>' if lang else ""
    return (
        f'<div class="code-block-wrap widget">'
        f'{label}'
        f'<pre><code>{escaped}</code></pre>'
        f'</div>'
    )


def render_figure(src: str, alt: str) -> str:
    """Render an image as a centered figure with caption."""
    safe_src = _html_lib.escape(src)
    safe_alt = _html_lib.escape(alt)
    return (
        f'<div class="figure-wrap widget">'
        f'<img src="{safe_src}" alt="{safe_alt}" loading="lazy">'
        f'<div class="figure-caption">{safe_alt}</div>'
        f'</div>'
    )


def render_def_list(items: list[dict]) -> str:
    """Render a definition list where items use **term** — definition format."""
    top = [it for it in items if it["depth"] == 0]
    entries = []
    for it in top:
        text = it["text"]
        m = re.match(r'\*\*([^*]+)\*\*\s*([—:–,]?\s*)(.*)', text, re.DOTALL)
        if m:
            term = m.group(1).strip()
            defn = m.group(3).strip()
        else:
            term = text
            defn = ""
        defn_html = f'<div class="def-definition">{md_inline(defn)}</div>' if defn else ""
        entries.append(
            f'<div class="def-entry">'
            f'<div class="def-term">{md_inline(term)}</div>'
            f'{defn_html}'
            f'</div>'
        )
    return f'<div class="def-list widget">{"".join(entries)}</div>'


def render_tree(items: list[dict], uid: str) -> str:
    """Render a nested bullet list as an expandable tree with collapse controls."""
    top = [it for it in items if it["depth"] == 0]

    def _children_of(parent_idx: int) -> list[dict]:
        result = []
        j = parent_idx + 1
        while j < len(items) and items[j]["depth"] > 0:
            result.append(items[j])
            j += 1
        return result

    def _render_node(item: dict, top_idx: int) -> str:
        children = _children_of(
            next(k for k, it in enumerate(items) if it is item)
        )
        if children:
            leaves = "".join(
                f'<div class="tree-leaf">{md_inline(c["text"])}</div>'
                for c in children if c["depth"] == 1
            )
            return (
                f'<div class="tree-node">'
                f'<details open><summary>{md_inline(item["text"])}</summary>'
                f'{leaves}'
                f'</details></div>'
            )
        return f'<div class="tree-leaf" style="padding-left:.75rem">{md_inline(item["text"])}</div>'

    nodes_html = "".join(_render_node(it, i) for i, it in enumerate(top))
    return (
        f'<div class="tree-controls">'
        f'<button class="tree-ctrl-btn" onclick="expandAllTree(\'{uid}\')">Expand All</button>'
        f'<button class="tree-ctrl-btn" onclick="collapseAllTree(\'{uid}\')">Collapse</button>'
        f'</div>'
        f'<div class="tree widget" id="{uid}">{nodes_html}</div>'
    )


def motion_widget_html(uid: str, concept_summary: str = "") -> str:
    """
    Generate a motion-canvas placeholder widget.

    Stage 05 (embed-motion) replaces the /* ANIMATION_CODE_PLACEHOLDER_[uid] */
    comment with actual Canvas 2D animation code from Stage 03.
    """
    aria = (concept_summary[:60] if concept_summary else uid).replace('"', "'")
    return (
        f'<div class="motion-canvas-widget widget" id="mc-{uid}">\n'
        f'  <canvas id="canvas-{uid}" class="motion-canvas-el"\n'
        f'          width="800" height="450"\n'
        f'          aria-label="{aria}"></canvas>\n'
        f'  <script>\n'
        f'  (function() {{\n'
        f"    'use strict';\n"
        f"    var _canvas = document.getElementById('canvas-{uid}');\n"
        f'    if (!_canvas || !_canvas.getContext) return;\n'
        f"    var _ctx = _canvas.getContext('2d');\n"
        f'    function _resize() {{\n'
        f'      var dpr = window.devicePixelRatio || 1;\n'
        f'      var rect = _canvas.getBoundingClientRect();\n'
        f'      if (rect.width === 0) return;\n'
        f'      _canvas.width  = rect.width  * dpr;\n'
        f'      _canvas.height = rect.height * dpr;\n'
        f'      _ctx.setTransform(dpr, 0, 0, dpr, 0, 0);\n'
        f'    }}\n'
        f'    _resize();\n'
        f"    window.addEventListener('resize', _resize);\n"
        f'    /* ANIMATION_CODE_PLACEHOLDER_{uid} */\n'
        f'  }})();\n'
        f'  </script>\n'
        f'</div>'
    )


# ── Block renderer dispatcher ──────────────────────────────────────────────────

def render_widget_block(block: dict, uid: str) -> str:
    """Dispatch a typed content block to the appropriate widget renderer."""
    t = block["type"]
    if t == "highlight":
        return render_highlight_list(block["items"])
    if t == "card_grid":
        return render_card_grid(block["items"])
    if t == "checklist":
        return render_checklist(block["items"], uid)
    if t == "def_list":
        return render_def_list(block["items"])
    if t == "tree":
        return render_tree(block["items"], uid)
    if t == "table":
        return render_sortable_table(block["lines"], uid)
    if t == "blockquote":
        return render_pull_quote(block["lines"])
    if t == "code":
        return render_code_block(block["content"], block.get("lang", ""))
    if t == "figure":
        return render_figure(block["src"], block["alt"])
    return f'<div class="prose-card widget"><p>{md_inline(str(block.get("content", "")))}</p></div>'


def render_blocks_html(blocks: list[dict], uid_counter: list[int]) -> str:
    """
    Render a list of content blocks to HTML.

    Consecutive prose blocks (para/h3/h4/ol) are grouped into a single
    prose-card widget. Non-prose widget blocks stand alone. A lone h3/h4
    immediately preceding a widget renders as a plain subheading.

    Args:
        blocks:      List of typed block dicts from parse_blocks().
        uid_counter: Single-element mutable list [int] used to generate
                     unique widget IDs. Pass the same instance across multiple
                     render_blocks_html calls in one render pass.

    Returns:
        HTML string of rendered blocks.
    """
    def _next_uid() -> str:
        uid_counter[0] += 1
        return f"w{uid_counter[0]}"

    parts: list[str] = []
    prose_buf: list[dict] = []
    PROSE_TYPES = {"para", "h3", "h4", "ol"}

    def _flush_prose() -> None:
        if not prose_buf:
            return
        if len(prose_buf) == 1 and prose_buf[0]["type"] in ("h3", "h4"):
            tag = prose_buf[0]["type"]
            parts.append(
                f'<{tag} class="section-subheading">'
                f'{md_inline(prose_buf[0]["content"])}'
                f'</{tag}>'
            )
            prose_buf.clear()
            return
        inner: list[str] = []
        for b in prose_buf:
            t = b["type"]
            if t == "para":
                inner.append(f'<p>{md_inline(b["content"])}</p>')
            elif t == "h3":
                inner.append(f'<h3>{md_inline(b["content"])}</h3>')
            elif t == "h4":
                inner.append(f'<h4>{md_inline(b["content"])}</h4>')
            elif t == "ol":
                lis = "".join(f'<li>{md_inline(it["text"])}</li>' for it in b["items"])
                inner.append(f'<ol>{lis}</ol>')
        parts.append(f'<div class="prose-card widget">\n{"".join(inner)}\n</div>')
        prose_buf.clear()

    for block in blocks:
        if block["type"] in PROSE_TYPES:
            prose_buf.append(block)
        else:
            _flush_prose()
            uid = _next_uid()
            parts.append(render_widget_block(block, uid))

    _flush_prose()
    return "\n\n".join(p for p in parts if p.strip())


# ── Widget CSS ─────────────────────────────────────────────────────────────────

def widget_css() -> str:
    """Return the complete widget CSS for all programmatic renderer widgets."""
    return """\
/* ── Programmatic render — widget CSS ── */

/* KPI */
.kpi-summary-text { color: var(--ink-55); margin-bottom: 1rem; font-size: .95rem; }
.kpi-row { display: flex; flex-wrap: wrap; gap: 1rem; margin-bottom: .5rem; }
.kpi-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 1.125rem 1.25rem;
  min-width: 130px; flex: 1;
  transition: transform .18s ease, box-shadow .18s ease; cursor: default;
}
.kpi-card:hover { transform: scale(1.03); box-shadow: 0 0 0 1px var(--accent), 0 6px 20px rgba(0,0,0,.09); }
.kpi-card .kpi-label {
  font-size: .72rem; font-weight: 600; color: var(--ink-55);
  text-transform: uppercase; letter-spacing: .08em; margin-bottom: .3rem;
}
.kpi-card .kpi-value { font-family: var(--font-mono, monospace); font-size: clamp(1.2rem, 3.5vw, 1.8rem); font-weight: 700; color: var(--accent); }
.kpi-card.kpi-ok    { background: color-mix(in srgb, var(--ok)     12%, transparent); }
.kpi-card.kpi-warn  { background: color-mix(in srgb, var(--warn)   12%, transparent); }
.kpi-card.kpi-danger{ background: color-mix(in srgb, var(--danger) 12%, transparent); }
.kpi-card.kpi-info  { background: color-mix(in srgb, var(--info)   12%, transparent); }
.kpi-card.kpi-ok     .kpi-value { color: var(--ok); }
.kpi-card.kpi-warn   .kpi-value { color: var(--warn); }
.kpi-card.kpi-danger .kpi-value { color: var(--danger); }
.kpi-card.kpi-info   .kpi-value { color: var(--info); }

/* Highlight list */
.highlight-list { list-style: none; display: flex; flex-direction: column; gap: .35rem; }
.highlight-list li {
  display: flex; align-items: flex-start; gap: .55rem;
  padding: .5rem .75rem; background: var(--surface);
  border-radius: 4px; border: 1px solid var(--border);
  font-size: .9rem; line-height: 1.55;
}
.highlight-list li::before { content: "\\203A"; color: var(--accent); font-weight: 700; flex-shrink: 0; font-size: 1.1em; }
.hl-badge {
  margin-left: auto; font-size: .7rem; padding: .1rem .45rem;
  border-radius: 99px; background: var(--surface-2); color: var(--ink-55); white-space: nowrap;
}

/* Card grid */
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(220px, 100%), 1fr)); gap: .9rem; }
.card-item {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 1.25rem;
  transition: transform .18s ease, box-shadow .18s ease;
}
.card-item:hover { transform: translateY(-2px); box-shadow: 0 6px 22px rgba(0,0,0,.07); }
.card-item .card-title { font-weight: 600; margin-bottom: .35rem; font-size: .9rem; }
.card-item .card-body  { font-size: .83rem; color: var(--ink-55); line-height: 1.55; }

/* Data table */
.table-wrap { overflow-x: auto; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; margin-bottom: .5rem; }
.data-table { width: 100%; border-collapse: collapse; font-size: .81rem; }
.data-table th, .data-table td { padding: .55rem .8rem; text-align: left; border-bottom: 1px solid var(--border); }
.data-table th {
  background: var(--surface-2); font-size: .71rem; font-weight: 600;
  color: var(--ink-55); text-transform: uppercase; letter-spacing: .05em;
  cursor: pointer; user-select: none; white-space: nowrap;
}
.data-table th:hover { color: var(--accent); }
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: var(--surface-2); }
.sort-icon::after { content: " \\2195"; opacity: .35; font-size: .8em; }
.data-table th.asc  .sort-icon::after { content: " \\25B2"; opacity: 1; }
.data-table th.desc .sort-icon::after { content: " \\25BC"; opacity: 1; }
.mono-cell { font-family: var(--font-mono, monospace); font-size: .8rem; }
.status-badge {
  display: inline-block; font-size: .69rem; font-weight: 600;
  padding: .15rem .5rem; border-radius: 99px; white-space: nowrap;
}
.status-ok     { background: color-mix(in srgb, var(--ok)     15%, transparent); color: var(--ok); }
.status-warn   { background: color-mix(in srgb, var(--warn)   15%, transparent); color: var(--warn); }
.status-danger { background: color-mix(in srgb, var(--danger) 15%, transparent); color: var(--danger); }
.status-info   { background: color-mix(in srgb, var(--info)   15%, transparent); color: var(--info); }
.status-muted  { background: var(--surface-2); color: var(--ink-55); }
.raci-cell { text-align: center; font-weight: 700; font-size: .8rem; }
.raci-R { color: var(--accent); } .raci-A { color: var(--danger); }
.raci-C { color: var(--info); }   .raci-I { color: var(--ink-55); }

/* Pull quote */
.pull-quote {
  background: color-mix(in srgb, var(--accent) 7%, transparent);
  border-left: 4px solid var(--accent); border-radius: 0 6px 6px 0;
  padding: .9rem 1.375rem; font-style: italic;
  font-size: 1.025rem; color: var(--ink); line-height: 1.65; margin: .25rem 0;
}
.pull-quote .attribution {
  display: block; margin-top: .45rem; font-style: normal;
  font-size: .78rem; color: var(--ink-55);
}

/* Code block */
.code-block-wrap { background: #1a1e26; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
.code-lang-label {
  font-size: .69rem; padding: .32rem .75rem;
  background: rgba(255,255,255,.06); color: rgba(255,255,255,.48);
  font-family: var(--font-mono, monospace); letter-spacing: .05em; text-transform: uppercase;
}
.code-block-wrap pre {
  padding: .875rem 1.125rem; overflow-x: auto; margin: 0;
  font-family: var(--font-mono, monospace); font-size: .81rem; line-height: 1.65; color: #e2e6ee;
}

/* Figure */
.figure-wrap { text-align: center; padding: .75rem 0; }
.figure-wrap img { max-width: 100%; max-height: 300px; object-fit: contain; border-radius: 6px; }
.figure-caption { font-size: .78rem; color: var(--ink-55); margin-top: .4rem; }

/* Definition list */
.def-list { display: flex; flex-direction: column; gap: .45rem; }
.def-entry {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 7px; padding: .8rem 1.1rem;
  transition: transform .18s ease, box-shadow .18s ease;
}
.def-entry:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,.06); }
.def-term       { font-weight: 600; margin-bottom: .18rem; color: var(--ink); font-size: .9rem; }
.def-definition { font-size: .85rem; color: var(--ink-55); line-height: 1.55; }

/* Tree */
.tree-controls { display: flex; gap: .45rem; margin-bottom: .5rem; }
.tree-ctrl-btn {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 4px; color: var(--ink-55); cursor: pointer;
  font-size: .71rem; font-weight: 600; padding: .18rem .55rem; transition: all .18s;
}
.tree-ctrl-btn:hover { color: var(--accent); border-color: var(--accent); }
.tree { user-select: none; }
.tree-node { margin-left: clamp(.3rem, 2vw, 1rem); }
.tree-node > details > summary {
  cursor: pointer; padding: .22rem .4rem; border-radius: 4px;
  list-style: none; display: flex; align-items: center; gap: .45rem;
  color: var(--ink); font-size: .87rem;
}
.tree-node > details > summary::-webkit-details-marker { display: none; }
.tree-node > details > summary:hover { background: var(--surface); color: var(--accent); }
.tree-node > details > summary::before { content: "\\25B6"; font-size: .6rem; color: var(--ink-55); }
.tree-node > details[open] > summary::before { content: "\\25BC"; }
.tree-leaf { padding: .22rem .4rem .22rem 1.5rem; font-size: .85rem; color: var(--ink-55); }

/* Checklist */
.checklist-widget { padding: .25rem 0; }
.checklist-ring-wrap { display: flex; align-items: center; gap: .7rem; margin-bottom: .875rem; }
.progress-ring { width: 54px; height: 54px; transform: rotate(-90deg); flex-shrink: 0; }
.ring-track { fill: none; stroke: var(--surface-2, #e0e0e0); stroke-width: 5; }
.ring-fill  {
  fill: none; stroke: var(--accent); stroke-width: 5; stroke-linecap: round;
  stroke-dasharray: 150.8; stroke-dashoffset: 150.8;
  transition: stroke-dashoffset 500ms ease;
}
.ring-label { font-size: .85rem; color: var(--ink-55); line-height: 1.4; }
.ring-label .ring-pct { font-family: var(--font-mono, monospace); font-size: 1.15rem; color: var(--accent); display: block; font-weight: 700; }
.checklist-group-label {
  font-weight: 600; font-size: .875rem; color: var(--ink-55);
  margin-bottom: .35rem; cursor: pointer; display: flex; align-items: center; gap: .35rem;
}
.checklist-group-label::before { content: "\\25BE"; color: var(--accent); }
.checklist-group.collapsed .checklist-group-label::before { content: "\\25B8"; }
.checklist-group.collapsed .checklist-items { display: none; }
.checklist-item {
  display: flex; align-items: flex-start; gap: .55rem;
  padding: .4rem .45rem; border-radius: 4px; border-left: 3px solid transparent;
  cursor: pointer;
}
.checklist-item:hover { background: var(--surface); }
.checklist-item input[type=checkbox] { margin-top: .25rem; accent-color: var(--accent); flex-shrink: 0; }
.checklist-label { flex: 1; min-width: 0; font-size: .875rem; line-height: 1.5; cursor: pointer; }
.checklist-item.done .checklist-label { text-decoration: line-through; color: var(--ink-55); }

/* Section subheading (h3/h4 before a widget, not in prose-card) */
.section-subheading {
  font-size: .8rem; font-weight: 700; color: var(--ink-55);
  text-transform: uppercase; letter-spacing: .06em;
  margin: 1rem 0 .4rem; padding-bottom: .25rem;
  border-bottom: 1px solid var(--border);
}

/* Prose card */
.prose-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 1.25rem 1.5rem;
}
.prose-card:hover { box-shadow: 0 3px 14px rgba(0,0,0,.05); }
.prose-card p  { margin-bottom: .75rem; line-height: 1.7; font-size: .91rem; }
.prose-card p:last-child { margin-bottom: 0; }
.prose-card ul, .prose-card ol { padding-left: 1.5rem; margin-bottom: .7rem; }
.prose-card li { margin-bottom: .28rem; font-size: .89rem; line-height: 1.55; }
.prose-card h3 { font-size: .95rem; font-weight: 600; margin: .9rem 0 .45rem; color: var(--ink); }
.prose-card h4 { font-size: .85rem; font-weight: 600; margin: .7rem 0 .35rem; color: var(--ink-55); }
.prose-card code {
  font-family: var(--font-mono, monospace);
  background: var(--surface-2); border-radius: 3px;
  padding: .1em .35em; font-size: .875em;
}

/* Motion canvas */
.motion-canvas-widget {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; overflow: hidden; margin: 1rem 0;
}
.motion-canvas-el { width: 100%; height: auto; display: block; aspect-ratio: 16 / 9; }

/* Responsive */
@media (max-width: 768px) {
  .kpi-row  { gap: .5rem; }
  .kpi-card { min-width: 100px; }
  .card-grid { grid-template-columns: 1fr; }
  .highlight-list li { font-size: .85rem; }
  .pull-quote { font-size: .95rem; }
}
@media print {
  .motion-canvas-widget { display: none !important; }
  .checklist-item input { display: none; }
}
"""
