"""
html_embed.py — HTML post-processing utilities shared across all HTML-generating agents.

Functions:
  finalize(html, vendor_dir)                    — inline Chart.js + strip Google Fonts
  inject_animation_code(html, uid, animation_js) — inject animation code into motion-canvas widget
  hoist_block_functions(js)                     — fix block-scoped function decls in strict IIFE
  _brace_depth_map(js)                          — internal: brace depth map for JS string
  _inline_chartjs(html, vendor_dir)             — internal: replace CDN tag with inline bundle
  _strip_google_fonts(html)                     — internal: remove Google Fonts link tags

Usage (in a programmatic stage):
    import sys
    from pathlib import Path
    _SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "html-shell"
    sys.path.insert(0, str(_SKILL_DIR))
    from html_embed import finalize, inject_animation_code, hoist_block_functions

    html = finalize(html, vendor_dir=_SKILL_DIR / "vendor")
    html = inject_animation_code(html, uid="motion-main", animation_js=code)
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

# Default vendor directory (sibling to this script)
DEFAULT_VENDOR_DIR = Path(__file__).resolve().parent / "vendor"

# Regex: <script ... src="...chart.js..." ...></script>  (with or without defer/async)
_RE_CHARTJS_CDN = re.compile(
    r'<script[^>]+src="[^"]*chart[^"]*\.js[^"]*"[^>]*>\s*</script>',
    re.IGNORECASE,
)

# Regex: Google Fonts preconnect + stylesheet links
_RE_GOOGLE_FONTS = re.compile(
    r'<link[^>]+href="https?://fonts\.(googleapis|gstatic)\.com[^"]*"[^>]*>\s*',
    re.IGNORECASE,
)


def finalize(html: str, vendor_dir: Path | None = None) -> str:
    """
    Make an HTML string fully self-contained for offline use:
    1. Replace Chart.js CDN <script> tag with the inlined vendor bundle.
    2. Strip Google Fonts <link> tags (CSS var() fallbacks ensure readability).

    Args:
        html:       HTML content string to process.
        vendor_dir: Directory containing chart.umd.min.js.
                    Defaults to the vendor/ subfolder next to this script.

    Returns:
        Processed HTML string.
    """
    if vendor_dir is None:
        vendor_dir = DEFAULT_VENDOR_DIR
    html = _inline_chartjs(html, vendor_dir)
    html = _strip_google_fonts(html)
    return html


def inject_animation_code(html: str, uid: str, animation_js: str) -> str:
    """
    Inject animation JavaScript into a motion-canvas widget placeholder.

    Stage 04 (render) leaves a placeholder comment inside the motion-canvas
    widget's inline <script> block:
        /* ANIMATION_CODE_PLACEHOLDER_[uid] */

    This function replaces that comment with the actual animation code
    produced by Stage 03 (animation-synthesis).

    Args:
        html:         HTML content string containing the placeholder.
        uid:          Canvas widget UID (e.g. "motion-main"). Must match
                      the uid used in Stage 04's generated widget.
        animation_js: JavaScript code string to inject (IIFE body content —
                      the code that runs inside the (function() { ... })() wrapper).

    Raises:
        ValueError: If the placeholder is missing or appears more than once.

    Returns:
        HTML string with animation code injected.
    """
    placeholder = f"/* ANIMATION_CODE_PLACEHOLDER_{uid} */"
    count = html.count(placeholder)
    if count == 0:
        raise ValueError(
            f"Animation placeholder '{placeholder}' not found in HTML. "
            f"Stage 04 may not have inserted the motion-canvas widget with uid='{uid}'."
        )
    if count > 1:
        raise ValueError(
            f"Animation placeholder '{placeholder}' found {count} times (expected exactly 1). "
            f"Ensure each motion-canvas widget uses a unique uid."
        )
    return html.replace(placeholder, animation_js.strip(), 1)


# ── Animation code utilities ──────────────────────────────────────────────────

def _brace_depth_map(js: str) -> list[int]:
    """
    Return a list of integers, one per character in `js`, recording the brace
    depth at that position. String literals, template literals, and comments
    are skipped so their braces are not counted.

    depth 0  = outer scope of the animation IIFE body (top-level declarations)
    depth 1+ = inside a block (if/else/for/while/function body)
    """
    depths: list[int] = []
    depth = 0
    i = 0
    n = len(js)

    while i < n:
        c = js[i]

        if c == '/' and i + 1 < n and js[i + 1] == '/':
            while i < n and js[i] != '\n':
                depths.append(depth)
                i += 1
            continue

        if c == '/' and i + 1 < n and js[i + 1] == '*':
            depths.append(depth)
            depths.append(depth)
            i += 2
            while i < n:
                if js[i] == '*' and i + 1 < n and js[i + 1] == '/':
                    depths.append(depth)
                    depths.append(depth)
                    i += 2
                    break
                depths.append(depth)
                i += 1
            continue

        if c in ('"', "'", '`'):
            quote = c
            depths.append(depth)
            i += 1
            while i < n:
                ch = js[i]
                if ch == '\\' and i + 1 < n:
                    depths.append(depth)
                    depths.append(depth)
                    i += 2
                    continue
                depths.append(depth)
                if ch == quote:
                    i += 1
                    break
                i += 1
            continue

        if c == '{':
            depths.append(depth)
            depth += 1
        elif c == '}':
            depth = max(0, depth - 1)
            depths.append(depth)
        else:
            depths.append(depth)

        i += 1

    return depths


def hoist_block_functions(js: str) -> str:
    """
    In a strict-mode IIFE body, ``function NAME()`` declarations inside
    ``if``/``else``/loop blocks are block-scoped and invisible to outer-scope
    callers, causing a silent TypeError that kills the RAF loop on the first tick.

    This transform detects every such declaration (brace depth >= 1) and rewrites it:
    1. A ``var NAME = function() {};`` stub is inserted at depth-0 scope,
       immediately before the outer statement that encloses the declaration.
    2. The declaration ``function NAME(`` is rewritten to ``NAME = function(``.
    3. The matching closing ``}`` of that function body is rewritten to ``};``.

    The transform is a no-op when no block-scoped function declarations are found,
    and is idempotent (running it twice produces the same output).
    """
    depths = _brace_depth_map(js)
    func_re = re.compile(r'\bfunction\s+(\w+)\s*\(')

    candidates: list[tuple[int, int, str]] = []
    for m in func_re.finditer(js):
        if depths[m.start()] >= 1:
            candidates.append((m.start(), m.end(), m.group(1)))

    if not candidates:
        return js

    patches: list[tuple[int, int, str]] = []
    stubs_inserted: set[str] = set()

    for decl_start, decl_end, name in reversed(candidates):
        body_open = js.find('{', decl_end)
        if body_open == -1:
            continue
        target_depth = depths[body_open]
        body_close = -1
        for k in range(body_open + 1, len(js)):
            if js[k] == '}' and depths[k] == target_depth:
                body_close = k
                break
        if body_close == -1:
            continue

        patches.append((decl_start, decl_end, f'{name} = function('))
        patches.append((body_close, body_close + 1, '};'))

        if name not in stubs_inserted:
            stubs_inserted.add(name)
            stub_pos = decl_start
            for k in range(decl_start - 1, -1, -1):
                if depths[k] == 0:
                    line_start = js.rfind('\n', 0, k)
                    stub_pos = line_start + 1 if line_start != -1 else 0
                    break
            stub = f'var {name} = function() {{}}; // hoisted — strict-mode block-scope guard\n'
            patches.append((stub_pos, stub_pos, stub))

    patches.sort(key=lambda p: p[0], reverse=True)
    result = list(js)
    for start, end, replacement in patches:
        result[start:end] = list(replacement)
    return ''.join(result)


# ── internal helpers ──────────────────────────────────────────────────────────

def _inline_chartjs(html: str, vendor_dir: Path) -> str:
    """Replace Chart.js CDN <script> tag with inline bundle from vendor/."""
    match = _RE_CHARTJS_CDN.search(html)
    if not match:
        return html  # No Chart.js CDN tag — HTML has no charts or already inlined

    bundle_path = vendor_dir / "chart.umd.min.js"
    if not bundle_path.exists():
        print(
            f"WARNING: Chart.js vendor bundle not found at {bundle_path}. "
            "CDN tag left as-is.",
            file=sys.stderr,
        )
        return html

    bundle_js = bundle_path.read_text(encoding="utf-8")
    inline_tag = f"<script>/* Chart.js (inlined for offline) */\n{bundle_js}\n</script>"
    return html[: match.start()] + inline_tag + html[match.end() :]


def _strip_google_fonts(html: str) -> str:
    """Remove Google Fonts <link> tags — system font stacks serve as fallback."""
    return _RE_GOOGLE_FONTS.sub("", html)
