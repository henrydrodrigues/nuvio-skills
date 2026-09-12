"""
embed_motion.py — Shared CLI for motion-canvas injection and HTML finalization.

Shared across all agents that generate HTML with motion animations.
Any agent can call this script directly via its html-shell skill junction:
    python skills/html-shell/embed_motion.py --html ... --animation ...

Operations (in order):
  1. Inject animation JS code from Stage 03 into motion-canvas widget placeholder(s).
  2. Inline Chart.js CDN <script> tag with the local vendor bundle.
  3. Strip Google Fonts <link> tags (CSS var() fallbacks ensure readability).

Reads:  [html]                    — Stage 04 HTML output (overwritten in-place)
        [animation/animations]    — Stage 03 animation JS files
        vendor/chart.umd.min.js   — sibling vendor directory (auto-resolved)

Delegates to html_embed utilities:
  hoist_block_functions()     — fix block-scoped function decls in strict-mode IIFE
  inject_animation_code()     — replace /* ANIMATION_CODE_PLACEHOLDER_[uid] */
  finalize()                  — inline Chart.js, strip Google Fonts

CLI usage:
  Single motion (N=1, backward-compatible):
    python embed_motion.py --html out.html --animation animation-code.js

  Multi-motion (N>1):
    python embed_motion.py --html out.html \\
      --animations motion-1:animation-code-1.js,motion-2:animation-code-2.js
"""

from __future__ import annotations
import sys
from pathlib import Path

# ── Load html_embed from the same directory (no sys.path manipulation needed) ─
_SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SKILL_DIR))
from html_embed import finalize, inject_animation_code, hoist_block_functions  # noqa: E402


def run(html_path: Path, animations: list[tuple[str, Path]]) -> None:
    """
    Inject animation code for each (uid, path) pair, inline CDN scripts,
    and strip external font links. Overwrites the HTML file in-place.
    Raises ValueError on any validation failure.

    Args:
        html_path:  Path to the HTML file to process in-place.
        animations: List of (uid, animation_path) pairs, e.g.:
            [("motion-main", Path("animation-code.js"))]            # N=1
            [("motion-1", Path("animation-code-1.js")),             # N>1
             ("motion-2", Path("animation-code-2.js"))]
    """
    html = html_path.read_text(encoding="utf-8")

    for uid, animation_path in animations:
        animation_js = animation_path.read_text(encoding="utf-8")
        animation_js = hoist_block_functions(animation_js)
        html = inject_animation_code(html, uid, animation_js)

    html = finalize(html, vendor_dir=_SKILL_DIR / "vendor")
    html_path.write_text(html, encoding="utf-8")


# ── CLI entrypoint ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Inject animation code, inline CDN scripts, strip external fonts."
    )
    parser.add_argument(
        "--html", metavar="FILE", required=True,
        help="Path to Stage 04 HTML output (will be overwritten in-place)."
    )
    parser.add_argument(
        "--animation", metavar="FILE", required=False,
        help=(
            "Path to animation-code.js from Stage 03 (single-motion, backward-compatible). "
            "Implies uid=motion-main. Use --animations for multi-motion."
        )
    )
    parser.add_argument(
        "--animations", metavar="UID:FILE,...", required=False,
        help=(
            "Comma-separated uid:path pairs for multi-motion injection. "
            "Example: motion-1:path/animation-code-1.js,motion-2:path/animation-code-2.js"
        )
    )
    args = parser.parse_args()

    if args.animation and args.animations:
        print("ERROR: Use --animation OR --animations, not both.", file=sys.stderr)
        sys.exit(1)
    if not args.animation and not args.animations:
        print("ERROR: Provide --animation (single-motion) or --animations (multi-motion).",
              file=sys.stderr)
        sys.exit(1)

    html_path = Path(args.html)
    if not html_path.exists():
        print(f"ERROR: HTML file not found: {html_path}", file=sys.stderr)
        sys.exit(1)

    if args.animation:
        animation_path = Path(args.animation)
        if not animation_path.exists():
            print(f"ERROR: Animation code file not found: {animation_path}", file=sys.stderr)
            sys.exit(1)
        animations = [("motion-main", animation_path)]

    else:
        animations = []
        for pair in args.animations.split(","):
            pair = pair.strip()
            if ":" not in pair:
                print(
                    f"ERROR: Invalid --animations entry (expected uid:path): {pair!r}",
                    file=sys.stderr,
                )
                sys.exit(1)
            uid, path_str = pair.split(":", 1)
            anim_path = Path(path_str.strip())
            if not anim_path.exists():
                print(f"ERROR: Animation code file not found: {anim_path}", file=sys.stderr)
                sys.exit(1)
            animations.append((uid.strip(), anim_path))

    try:
        run(html_path, animations)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    uids = ", ".join(uid for uid, _ in animations)
    print(
        f"OK: Injected {len(animations)} animation(s) [{uids}], "
        f"inlined CDN scripts, stripped fonts -> {html_path.name}"
    )
