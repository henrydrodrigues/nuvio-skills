---
name: html-shell
description: >
  Shared HTML output infrastructure: pre-compiled base template, finalization
  utilities, Chart.js vendor bundle, and post-processing helpers for all agents
  that generate interactive HTML output.
---

# html-shell — Shared HTML Output Skill

Shared infrastructure for all agents that generate interactive HTML output.
Provides the pre-compiled base template, finalization utilities, and common
helpers used by `doc2html-motion`, `project-planner`, and any future
HTML-generating agent.

No code duplication — agents consume this skill via a junction:
`agent/skills/html-shell/` → `src/skills/html-shell/`

---

## Contents

| File | Purpose |
|------|---------|
| `html_foundation.html` | Pre-compiled HTML template (page shell, CSS foundation, JS utilities) |
| `html_conventions_widgets.md` | Slim extract: Section 2 (Design Style Integration) + Section 4 (Widget Patterns) |
| `html_embed.py` | Post-processing: inject animation code, inline Chart.js, strip Google Fonts |
| `html_utils.py` | Shared utilities: `slugify`, `fmt_currency`, `validate_schema`, `validate_ci_input` |
| `vendor/chart.umd.min.js` | Chart.js 4.x UMD bundle for offline-capable inlining |

---

## Usage

### 1. HTML template (cognitive stage)

Read `skills/html-shell/html_foundation.html` and inject content into `{{...}}` placeholders.
Read `skills/html-shell/html_conventions_widgets.md` for widget HTML/CSS patterns and design
style integration instructions.

Full placeholder reference and widget vocabulary are in the parent skill:
`skills/md2html-cognitive/html-conventions.md`.

### 2. Motion-canvas widget (cognitive stage)

Any agent can include one or more animated canvas sections by using the `motion-canvas`
widget (Section 4.23 in `html_conventions_widgets.md`). Multiple instances per page are
supported via distinct `uid` values.

For agents without a separate animation-synthesis stage (e.g. `project-planner`), write
the complete animation code directly into the widget's `<script>` block.

For `doc2html-motion`, Stage 04 inserts a placeholder comment and Stage 05 injects the code:
```
/* ANIMATION_CODE_PLACEHOLDER_[uid] */
```

### 3. Post-processing (programmatic stage)

```python
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "html-shell"
sys.path.insert(0, str(_SKILL_DIR))

from html_embed import finalize, inject_animation_code
from html_utils import slugify, fmt_currency, validate_schema, validate_ci_input

# Inject animation code (doc2html-motion only — other agents write code directly)
html = inject_animation_code(html, uid="motion-main", animation_js=code_str)

# Make HTML self-contained for offline use (all agents)
html = finalize(html, vendor_dir=_SKILL_DIR / "vendor")

# Common utilities
slug = slugify("Análise de Riscos")      # → "analise-de-riscos"
fmt_currency(150_000, "BRL")            # → "BRL 150,000"
validate_schema(data, schema_path)      # raises ValueError on failure
validate_ci_input(data, schema_path)    # same, with CI→PI boundary context
```

---

## Regenerating html_foundation.html and html_conventions_widgets.md

Run after every edit to `html-conventions.md`:

```bash
cd src/agents/hybrid/doc2html-motion
python program/build_foundation.py \
  --conventions skills/md2html-cognitive/html-conventions.md \
  --output-dir skills/html-shell \
  --verify
```

Both output files are committed to version control.
`html_foundation.html` is the authoritative pre-compiled template for all agents.

---

## Agents using this skill

| Agent | Junction path | Usage |
|-------|---------------|-------|
| `doc2html-motion` | `skills/html-shell/` → `src/skills/html-shell/` | Template (Stage 04), embed (Stage 05) |
| `project-planner` | `skills/html-shell/` → `src/skills/html-shell/` | Template + utilities (Stage 07) |
