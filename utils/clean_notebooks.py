#!/usr/bin/env python3
"""
Clean Jupyter notebooks by:
- normalizing smart punctuation to ASCII
- removing non-ASCII chars except selected emoji ranges
- preserving whitespace, newlines, ZWJ and variation selectors used by emoji

Usage:
  python utils/clean_notebooks.py --check notebooks/
  python utils/clean_notebooks.py --write notebooks/
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, Tuple

# ASCII replacements for common smart characters (shown as Unicode escapes)
#   \u2018 \u2019  -> apostrophe '
#   \u201C \u201D  -> double quote "
#   \u2013 \u2014  -> hyphen -
#   \u2026        -> ellipsis "..."
ASCII_MAP = {
    "\u2018": "'", "\u2019": "'",  # left/right single quotation mark
    "\u201C": '"', "\u201D": '"',  # left/right double quotation mark
    "\u2013": "-", "\u2014": "-",  # en dash, em dash
    "\u2026": "...",               # ellipsis
}

# Allowed emoji-related codepoints to keep when stripping:
# - Zero-width joiner (\u200D) and variation selector-16 (\uFE0F) are kept,
#   because many emoji sequences rely on them.
# - Emoji ranges are applied via regex below (U+2600..U+27BF etc.).
ZWJ = "\u200D"
VS16 = "\uFE0F"

# Regex for characters we consider "emoji-ish" and should keep.
# Ranges shown as Unicode escapes to keep this file ASCII-only.
EMOJI_KEEP_RE = re.compile(
    "["                       # start class
    "\u2600-\u27BF"           # misc symbols, dingbats (e.g., U+2600..U+27BF)
    "\U0001F300-\U0001F5FF"   # symbols & pictographs
    "\U0001F600-\U0001F64F"   # emoticons
    "\U0001F680-\U0001F6FF"   # transport & map
    "\U0001F700-\U0001F77F"   # alchemical symbols
    "\U0001F900-\U0001F9FF"   # supplemental symbols & pictographs
    "\U0001FA70-\U0001FAFF"   # symbols & pictographs extended-A
    "]"
)

def normalize_text(s: str) -> str:
    """Normalize a notebook text blob to ASCII with limited emoji allowed."""
    if not s:
        return s
    # Replace known smart punctuation with ASCII equivalents
    for k, v in ASCII_MAP.items():
        s = s.replace(k, v)

    # Build cleaned string by iterating codepoints
    out_chars = []
    for ch in s:
        code = ord(ch)
        if ch in (ZWJ, VS16):
            out_chars.append(ch)
            continue
        if EMOJI_KEEP_RE.match(ch):
            out_chars.append(ch)
            continue
        # Keep ASCII
        if code < 128:
            out_chars.append(ch)
            continue
        # Otherwise drop the non-ASCII char
        # (you could also map or log here if desired)
    return "".join(out_chars)

def clean_notebook(nb_json: dict) -> Tuple[dict, int]:
    """Return cleaned notebook JSON and number of edits."""
    edits = 0
    def _maybe_norm(x: str) -> str:
        nonlocal edits
        y = normalize_text(x)
        if y != x:
            edits += 1
        return y

    for cell in nb_json.get("cells", []):
        if "source" in cell and isinstance(cell["source"], list):
            cell["source"] = [_maybe_norm(line) for line in cell["source"]]
        elif "source" in cell and isinstance(cell["source"], str):
            cell["source"] = _maybe_norm(cell["source"])

        # Also normalize outputs' text/plain, text/html, etc.
        for out in cell.get("outputs", []) or []:
            if "text" in out and isinstance(out["text"], list):
                out["text"] = [_maybe_norm(line) for line in out["text"]]
            elif "text" in out and isinstance(out["text"], str):
                out["text"] = _maybe_norm(out["text"])
            for key in ("text/plain", "text/html"):
                data = out.get("data", {})
                if key in data and isinstance(data[key], list):
                    data[key] = [_maybe_norm(line) for line in data[key]]
                elif key in data and isinstance(data[key], str):
                    data[key] = _maybe_norm(data[key])

    return nb_json, edits

def iter_notebooks(root: Path) -> Iterable[Path]:
    """Yield .ipynb files under root (recursively), skipping hidden dirs."""
    for p in root.rglob("*.ipynb"):
        parts = set(p.parts)
        if any(x.startswith(".") for x in parts):
            continue
        yield p

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Normalize notebooks to ASCII (keep limited emoji)."
    )
    ap.add_argument("--check", action="store_true", help="Report files needing changes.")
    ap.add_argument("--write", action="store_true", help="Rewrite files in-place.")
    ap.add_argument("paths", nargs="+", help="Notebook files or folders to process.")
    args = ap.parse_args()

    if not (args.check or args.write):
        ap.error("choose one of --check or --write")

    changed = []
    for raw in args.paths:
        path = Path(raw)
        targets = [path] if path.is_file() else list(iter_notebooks(path))
        for nb_path in targets:
            try:
                nb = json.loads(nb_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"skip unreadable: {nb_path} ({e})")
                continue

            cleaned, edits = clean_notebook(nb)
            if edits > 0:
                if args.write:
                    nb_path.write_text(json.dumps(cleaned, ensure_ascii=False, indent=1), encoding="utf-8")
                    print(f"wrote: {nb_path} (edits={edits})")
                else:
                    changed.append(nb_path)

    if args.check:
        if changed:
            print("\nNOTEBBOOKS NEED NORMALIZATION:")
            for p in changed:
                print(" -", p)
            raise SystemExit(1)
        else:
            print("all notebooks clean.")

if __name__ == "__main__":
    main()

