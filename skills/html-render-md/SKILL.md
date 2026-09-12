---
name: html-render-md
description: >
  Pure Python functions for parsing Markdown into typed blocks and rendering
  interactive HTML widgets. Use when an agent has a programmatic HTML export
  path (html_export_mode: programmatic) and its input is a Markdown file.
---

# html-render-md — Shared Programmatic Markdown-to-HTML Renderer

Provides pure Python functions for parsing Markdown content into typed blocks
and rendering them as interactive HTML widgets. Any agent that takes Markdown
as input and needs a programmatic HTML path (zero token cost) imports from
this skill.

## When to Use

- Your agent has a programmatic HTML export path (e.g., `html_export_mode: programmatic`)
- Your agent's input is a rendered Markdown file (e.g., `rendered.md`)
- You want to avoid duplicating the widget renderer code across agents

## When NOT to Use

- Your agent's data source is structured JSON (not Markdown) → write agent-specific renderer
- You only need the cognitive HTML path → use `md2html-cognitive` instead

## Import Pattern

```python
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "html-render-md"
sys.path.insert(0, str(_SKILL_DIR))
from md_render import (
    parse_rendered_md,
    render_blocks_html,
    motion_widget_html,
    widget_css,
    md_inline,
    detect_lang,
)
```

## Core Workflow

```python
uid_counter = [0]                                    # shared mutable counter for widget IDs
title, lang, sections = parse_rendered_md(raw_md)    # parse frontmatter + sections

for sec in sections:
    body_html = render_blocks_html(sec["blocks"], uid_counter)
    # sec["id"]      → section slug (for sidebar nav)
    # sec["heading"] → section heading text
    # body_html      → rendered HTML string

css = widget_css()   # complete widget CSS for <style> block
```

## Public API

### Parsing

| Function | Signature | Returns |
|----------|-----------|---------|
| `parse_rendered_md` | `(content: str)` | `(title, lang, sections)` — sections have `{id, heading, blocks}` |
| `parse_blocks` | `(lines: list[str])` | `list[dict]` — typed block dicts |
| `detect_lang` | `(text: str)` | `"pt-BR"` or `"en"` |

### Rendering

| Function | Signature | Returns |
|----------|-----------|---------|
| `render_blocks_html` | `(blocks, uid_counter: list[int])` | HTML string — pass same `uid_counter` across calls |
| `render_widget_block` | `(block: dict, uid: str)` | HTML string for one block |
| `motion_widget_html` | `(uid: str, concept_summary: str = "")` | Canvas placeholder widget HTML |
| `widget_css` | `()` | Complete CSS string for all widgets |
| `md_inline` | `(text: str)` | HTML string with bold/italic/code/links |

### Individual Widget Renderers

All accept typed data and return HTML strings:

- `render_highlight_list(items)` — accent bullet list
- `render_card_grid(items)` — responsive card grid (>8 items)
- `render_checklist(items, uid)` — SVG progress ring + localStorage
- `render_sortable_table(table_lines, uid)` — sortable table with status badges
- `render_pull_quote(lines)` — accent-border blockquote
- `render_code_block(content, lang)` — dark code block with language label
- `render_figure(src, alt)` — centered image with caption
- `render_def_list(items)` — **term** — definition entries
- `render_tree(items, uid)` — expandable `<details>` tree with controls

## Block Types

`parse_blocks()` produces blocks with these `type` values:

| type | Widget renderer | Trigger in Markdown |
|------|----------------|---------------------|
| `highlight` | `render_highlight_list` | ≤8 simple bullet items |
| `card_grid` | `render_card_grid` | >8 bullet items |
| `checklist` | `render_checklist` | `- [x]` / `- [ ]` items |
| `def_list` | `render_def_list` | bullets where ≥60% start with `**bold**` |
| `tree` | `render_tree` | nested bullets (depth > 0) |
| `table` | `render_sortable_table` | Markdown table (pipe syntax) |
| `blockquote` | `render_pull_quote` | `> ` prefix lines |
| `code` | `render_code_block` | fenced code ` ``` ` |
| `figure` | `render_figure` | inline `![alt](src)` |
| `para` | grouped into `prose-card` | plain paragraphs |
| `h3` / `h4` | subheading or prose-card | `### ` / `#### ` |
| `ol` | ordered list in `prose-card` | `1. ` prefix lines |

## Motion Canvas

`motion_widget_html(uid, concept_summary)` generates a canvas placeholder that
`html-shell/embed_motion.py` will fill with animation code from Stage 03.

The placeholder comment `/* ANIMATION_CODE_PLACEHOLDER_{uid} */` must survive
Stage 04 output untouched for Stage 05 to inject the animation.

## uid_counter

Pass a single-element list `[0]` as `uid_counter` to `render_blocks_html`.
The function mutates it to generate sequential widget IDs (`w1`, `w2`, ...).
Share the same instance across multiple `render_blocks_html` calls in one
render pass to guarantee globally-unique IDs within the HTML document.

## Agent Junction Setup

```bash
# Windows (run in agent root)
powershell -Command "New-Item -ItemType Junction -Path skills/html-render-md -Target (Resolve-Path ../../../skills/html-render-md)"

# Linux/Mac
ln -s ../../../skills/html-render-md skills/html-render-md
```
