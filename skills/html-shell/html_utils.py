"""
html_utils.py — Shared utilities for HTML-generating agents.

Functions:
  slugify(text)                        — text → kebab-case slug (accent-safe)
  fmt_currency(value, currency)        — float → "BRL 1,234"
  validate_schema(data, schema_path)   — JSON Schema validation (raises ValueError)
  validate_ci_input(data, schema_path) — CI→PI boundary validation with context
  parse_design_style(slug, styles_dir) — parse design-style-[slug].md into token dict
  build_css_tokens(style)              — build :root {...} CSS block from token dict

Usage:
    import sys
    from pathlib import Path
    _SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "html-shell"
    sys.path.insert(0, str(_SKILL_DIR))
    from html_utils import slugify, fmt_currency, validate_schema, validate_ci_input
    from html_utils import parse_design_style, build_css_tokens
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any


def slugify(text: str) -> str:
    """
    Convert text to a URL-safe kebab-case slug.

    Normalizes accented characters (Portuguese, Spanish, French, German)
    to their ASCII base, then replaces non-alphanumeric runs with hyphens.

    Examples:
        slugify("Cronograma do Projeto")  → "cronograma-do-projeto"
        slugify("Análise de Riscos")      → "analise-de-riscos"
        slugify("Étapes & Délais")        → "etapes-delais"
    """
    text = text.lower().strip()
    text = re.sub(r"[àáâãäå]", "a", text)
    text = re.sub(r"[èéêë]", "e", text)
    text = re.sub(r"[ìíîï]", "i", text)
    text = re.sub(r"[òóôõö]", "o", text)
    text = re.sub(r"[ùúûü]", "u", text)
    text = re.sub(r"[ç]", "c", text)
    text = re.sub(r"[ñ]", "n", text)
    text = re.sub(r"[ý]", "y", text)
    text = re.sub(r"[ß]", "ss", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def fmt_currency(value: float, currency: str = "BRL") -> str:
    """
    Format a float as a human-readable currency string.

    Uses thousands separators and no decimal places (suitable for budget display).

    Examples:
        fmt_currency(150000)         → "BRL 150,000"
        fmt_currency(1234567, "USD") → "USD 1,234,567"
    """
    return f"{currency} {value:,.0f}"


def validate_schema(data: dict[str, Any], schema_path: Path) -> None:
    """
    Validate *data* against a JSON Schema file.

    Raises:
        RuntimeError: If jsonschema is not installed.
        ValueError:   If the data fails schema validation (with field + message context).
    """
    try:
        import jsonschema
    except ImportError:
        raise RuntimeError(
            "jsonschema is required. Install with: pip install jsonschema"
        )
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise ValueError(
            f"Schema validation failed for {schema_path.name}:\n{e.message}"
        ) from e


def validate_ci_input(data: dict[str, Any], schema_path: Path) -> None:
    """
    Validate input arriving from an upstream cognitive stage (CI→PI boundary).

    Wraps validate_schema with additional context explaining that the failure
    originated in the upstream cognitive stage, not in the current programmatic stage.

    Raises:
        RuntimeError: If jsonschema is not installed.
        ValueError:   If the CI output fails schema validation.
    """
    try:
        validate_schema(data, schema_path)
    except ValueError as e:
        raise ValueError(
            f"CI→PI boundary validation failed.\n"
            f"The upstream cognitive stage did not produce valid structured output.\n"
            f"Schema: {schema_path.name}\n"
            f"Detail: {e}"
        ) from e


# ── Design style parsing ───────────────────────────────────────────────────────

# Hardcoded fallbacks for all 5 bundled design styles.
# Used when the styles_dir doesn't contain the requested slug.
DESIGN_STYLE_FALLBACKS: dict[str, dict] = {
    "dark-terminal": {
        "default_theme": "dark",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Mono:wght@400;500&display=swap",
        "css_root": (
            "  --bg:#0d1117;--surface:#161b22;--surface-2:#1c2128;\n"
            "  --border:#21262d;--ink:#e6edf3;--ink-55:#8b949e;--ink-20:#30363d;\n"
            "  --accent:#f0a500;--ok:#3fb950;--warn:#d29922;--danger:#f85149;--info:#388bfd;\n"
            "  --font-body:'Space Grotesk',sans-serif;\n"
            "  --font-display:'Space Grotesk',sans-serif;\n"
            "  --font-mono:'DM Mono',monospace;"
        ),
        "css_dark": "",
        "css_light": (
            "  --bg:#f6f8fa;--surface:#fff;--surface-2:#f6f8fa;\n"
            "  --border:#d0d7de;--ink:#1f2328;--ink-55:#636c76;--ink-20:#d0d7de;"
        ),
    },
    "clinical-blue": {
        "default_theme": "light",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap",
        "css_root": (
            "  --bg:#f8fafc;--surface:#fff;--surface-2:#f1f5f9;\n"
            "  --border:#e2e8f0;--ink:#0f172a;--ink-55:#64748b;--ink-20:#cbd5e1;\n"
            "  --accent:#2563eb;--ok:#16a34a;--warn:#d97706;--danger:#dc2626;--info:#0ea5e9;\n"
            "  --font-body:'Inter',sans-serif;\n"
            "  --font-display:'Inter',sans-serif;\n"
            "  --font-mono:'JetBrains Mono',monospace;"
        ),
        "css_dark": (
            "  --bg:#0f1e35;--surface:#172a47;--surface-2:#1f3556;\n"
            "  --border:#2c456a;--ink:#eaf1fb;--ink-55:#9bb0cc;--ink-20:#3a527a;"
        ),
        "css_light": "",
    },
    "editorial-warm": {
        "default_theme": "light",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Source+Sans+3:wght@400;600&display=swap",
        "css_root": (
            "  --bg:#fdf8f3;--surface:#fff;--surface-2:#fef3e2;\n"
            "  --border:#e8d9c4;--ink:#2c1a0e;--ink-55:#8a7060;--ink-20:#d4c4b0;\n"
            "  --accent:#c0722a;--ok:#5a8a3c;--warn:#c08030;--danger:#c03030;--info:#3060c0;\n"
            "  --font-body:'Source Sans 3',sans-serif;\n"
            "  --font-display:'Lora',serif;\n"
            "  --font-mono:monospace;"
        ),
        "css_dark": (
            "  --bg:#1e1a14;--surface:#2a2520;--surface-2:#332e28;\n"
            "  --border:rgba(244,240,232,.14);--ink:#f4f0e8;\n"
            "  --ink-55:rgba(244,240,232,.55);--ink-20:rgba(244,240,232,.14);"
        ),
        "css_light": "",
    },
    "pastel-soft": {
        "default_theme": "light",
        "fonts_url": "https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap",
        "css_root": (
            "  --bg:#fafafa;--surface:#fff;--surface-2:#f0f4ff;\n"
            "  --border:#e4e8f0;--ink:#2d3748;--ink-55:#718096;--ink-20:#e2e8f0;\n"
            "  --accent:#7c6af0;--ok:#48bb78;--warn:#f6ad55;--danger:#fc8181;--info:#63b3ed;\n"
            "  --font-body:'Nunito',sans-serif;\n"
            "  --font-display:'Nunito',sans-serif;\n"
            "  --font-mono:monospace;"
        ),
        "css_dark": (
            "  --bg:#1a1726;--surface:#262238;--surface-2:#312c46;\n"
            "  --border:#3a3450;--ink:#f0ecfb;--ink-55:#a097b8;--ink-20:#4d4566;"
        ),
        "css_light": "",
    },
    "brutalist-mono": {
        "default_theme": "light",
        "fonts_url": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap",
        "css_root": (
            "  --bg:#fff;--surface:#f5f5f5;--surface-2:#ebebeb;\n"
            "  --border:#000;--ink:#000;--ink-55:#555;--ink-20:#ccc;\n"
            "  --accent:#000;--ok:#006600;--warn:#885500;--danger:#cc0000;--info:#0000cc;\n"
            "  --font-body:'IBM Plex Mono',monospace;\n"
            "  --font-display:'IBM Plex Mono',monospace;\n"
            "  --font-mono:'IBM Plex Mono',monospace;"
        ),
        "css_dark": (
            "  --bg:#0a0a0a;--surface:#1a1a1a;--surface-2:#262626;\n"
            "  --border:#f2f0eb;--ink:#f2f0eb;--ink-55:#a0a0a0;--ink-20:#404040;"
        ),
        "css_light": "",
    },
}


def _parse_token_table(section_text: str) -> dict[str, str]:
    """Extract CSS custom property tokens from a Markdown token table."""
    tokens: dict[str, str] = {}
    for m in re.finditer(r'\|\s*`(--[\w-]+)`\s*\|\s*`([^`]+)`', section_text):
        tokens[m.group(1)] = m.group(2)
    return tokens


def _tokens_to_css(tokens: dict[str, str]) -> str:
    return "\n".join(f"  {k}: {v};" for k, v in tokens.items())


def _infer_font_vars(text: str, css_root: str) -> str:
    """Infer --font-body/display/mono vars from display+body and mono rows if absent."""
    if "--font-body" in css_root:
        return css_root
    extra = []
    m = re.search(r'Display \+ body\s*\|\s*([^|]+)\|', text)
    if m:
        fam = m.group(1).strip()
        extra.append(f"  --font-body: '{fam}', sans-serif;")
        extra.append(f"  --font-display: '{fam}', sans-serif;")
    m = re.search(r'(?i)mono[^|]*\|\s*([^|]+)\|', text)
    if m:
        fam = m.group(1).strip()
        extra.append(f"  --font-mono: '{fam}', monospace;")
    return (css_root + "\n" + "\n".join(extra)).strip()


def parse_design_style(slug: str, styles_dir: Path) -> dict:
    """
    Parse a design-style-[slug].md file into a style token dict.

    Args:
        slug:       Design style slug (e.g. "clinical-blue", "dark-terminal").
        styles_dir: Path to the directory containing design-style-*.md files
                    (typically skills/md2html-cognitive/design-styles/).

    Returns:
        Dict with keys: default_theme, fonts_url, css_root, css_light.
        Falls back to DESIGN_STYLE_FALLBACKS["clinical-blue"] if the file is
        not found and the slug has no hardcoded entry.

    Example:
        style = parse_design_style("dark-terminal", _STYLES_DIR)
        css   = build_css_tokens(style)
    """
    path = styles_dir / f"design-style-{slug}.md"
    if not path.exists():
        return DESIGN_STYLE_FALLBACKS.get(slug, DESIGN_STYLE_FALLBACKS["clinical-blue"])

    text = path.read_text(encoding="utf-8")

    m = re.search(r'Default theme:\s*\*\*(\w+)\*\*', text)
    default_theme = m.group(1) if m else "light"

    m = re.search(r'Google Fonts URL\s*\n+```\s*\n(https://[^\n]+)', text)
    fonts_url = m.group(1).strip() if m else ""

    m = re.search(r'###\s*`:root`[^\n]*\n(.*?)(?=\n###|\Z)', text, re.DOTALL)
    root_tokens = _parse_token_table(m.group(1)) if m else {}

    m = re.search(r'###\s*`\[data-theme="light"\]`[^\n]*\n(.*?)(?=\n###|\Z)', text, re.DOTALL)
    light_tokens = _parse_token_table(m.group(1)) if m else {}

    m = re.search(r'###\s*`\[data-theme="dark"\]`[^\n]*\n(.*?)(?=\n###|\Z)', text, re.DOTALL)
    dark_tokens = _parse_token_table(m.group(1)) if m else {}

    css_root  = _infer_font_vars(text, _tokens_to_css(root_tokens))
    css_light = _tokens_to_css(light_tokens)
    css_dark  = _tokens_to_css(dark_tokens)

    return {
        "default_theme": default_theme,
        "fonts_url": fonts_url,
        "css_root": css_root,
        "css_light": css_light,
        "css_dark": css_dark,
    }


def build_css_tokens(style: dict) -> str:
    """
    Build a complete CSS :root {...} + theme override blocks
    from a parsed style dict (as returned by parse_design_style).

    Returns:
        CSS string ready to substitute into the {{CSS_TOKENS}} placeholder
        in html_foundation.html.

    Example:
        style = parse_design_style("clinical-blue", styles_dir)
        html  = template.replace("{{CSS_TOKENS}}", build_css_tokens(style))
    """
    css = f":root {{\n{style['css_root']}\n}}"
    if style.get("css_dark"):
        css += f'\n[data-theme="dark"] {{\n{style["css_dark"]}\n}}'
    if style.get("css_light"):
        css += f'\n[data-theme="light"] {{\n{style["css_light"]}\n}}'
    return css


def build_css_tokens_scoped(style: dict, slug: str) -> str:
    """
    Build scoped CSS token blocks for the runtime style switcher.

    Scopes tokens to html[data-style="slug"] so that multiple styles can
    coexist in the same HTML file. Activating a style is a single
    setAttribute('data-style', slug) on <html>, with no page reload.

    Returns:
        CSS string ready to embed directly in a <style> block.

    Example:
        style = parse_design_style("dark-terminal", styles_dir)
        css   = build_css_tokens_scoped(style, "dark-terminal")
    """
    css = f'html[data-style="{slug}"] {{\n{style["css_root"]}\n}}'
    if style.get("css_dark"):
        css += f'\nhtml[data-style="{slug}"][data-theme="dark"] {{\n{style["css_dark"]}\n}}'
    if style.get("css_light"):
        css += f'\nhtml[data-style="{slug}"][data-theme="light"] {{\n{style["css_light"]}\n}}'
    return css
