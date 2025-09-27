#!/usr/bin/env python3
"""
Clean Jupyter notebooks by:
- normalizing curly quotes/dashes/ellipsis to ASCII
- stripping non-ASCII characters EXCEPT emojis (common ranges)
- preserving whitespace, newlines, ZWJ + variation selectors used by emoji

Usage:
  python utils/clean_notebooks.py --check notebooks/
  python utils/clean_notebooks.py --write notebooks/
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Iterable

# ascii replacements for common “smart” characters
ASCII_MAP = {
    "\u2018": "'", "\u2019": "'",  # ‘ ’
    "\u201C": '"', "\u201D": '"',  # “ ”
    "\u2013": "-", "\u2014": "-",  # – —
    "\u2026": "...",               # …
    "\u00A0": " ",                 # non-breaking space
}

# emoji & symbols ranges to KEEP (rough but practical)
#   Misc Symbols + Dingbats + Emoji + supplemental + flags + transport etc.
EMOJI_KEEP = re.compile(
    "["                       # begin class
    "\U0001F300-\U0001FAFF"   # main emoji blocks
    "\U0001F900-\U0001F9FF"   # Supplemental Symbols and Pictographs
    "\U00002600-\U000027BF"   # Misc symbols, dingbats (☀️✈️✔️…)
    "\U0001F1E6-\U0001F1FF"   # regional indicator (flags)
    "]"
)

# special codepoints used inside emoji sequences we should keep
SPECIAL_OK = {0x200D, 0xFE0F}  # ZWJ & variation selector-16

def normalize_text(s: str) -> tuple[str, bool]:
    """Return (cleaned_text, changed?). Safer version that preserves leading indentation."""
    lines = s.splitlines()
    cleaned = []
    changed = False

    for line in lines:
        leading = len(line) - len(line.lstrip(" \t"))
        prefix = line[:leading]
        body = line[leading:]

        # map smart quotes/dashes only inside the body
        for k, v in ASCII_MAP.items():
            if k in body:
                body = body.replace(k, v)
                changed = True

        out_chars = []
        for ch in body:
            cp = ord(ch)
            if ch == "\n" or ch == "\t":
                out_chars.append(ch); continue
            if cp < 128:
                out_chars.append(ch); continue
            if cp in SPECIAL_OK:
                out_chars.append(ch); continue
            if EMOJI_KEEP.match(ch):
                out_chars.append(ch); continue
            out_chars.append(" "); changed = True

        cleaned_line = prefix + "".join(out_chars)
        cleaned.append(cleaned_line)

    final = "\n".join(cleaned)
    if "  " in final:
        final = re.sub(r"[ ]{2,}", " ", final); changed = True

    return final, changed


def iter_notebook_cells(nb: dict) -> Iterable[tuple[list, int]]:
    """Yield (cell_source_list, cell_index) for code/markdown cells."""
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") in {"code", "markdown"}:
            src = cell.get("source")
            # source may be string or list of lines
            if isinstance(src, list):
                yield src, i
            elif isinstance(src, str):
                lines = src.splitlines(keepends=True)
                cell["source"] = lines
                yield lines, i

def clean_notebook(path: Path, write: bool) -> bool:
    nb = json.loads(path.read_text(encoding="utf-8"))
    touched = False
    for src, _ in iter_notebook_cells(nb):
        for j, line in enumerate(src):
            cleaned, changed = normalize_text(line)
            if changed:
                src[j] = cleaned
                touched = True
    if touched and write:
        path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    return touched

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="Notebook files or directories")
    ap.add_argument("--check", action="store_true", help="Only report problems")
    ap.add_argument("--write", action="store_true", help="Rewrite notebooks in place")
    args = ap.parse_args()
    if not (args.check ^ args.write):
        ap.error("Choose exactly one of --check or --write")

    any_touched = False
    for p in args.paths:
        pth = Path(p)
        items = [pth] if pth.suffix == ".ipynb" else list(pth.rglob("*.ipynb"))
        for nb in items:
            touched = clean_notebook(nb, write=args.write)
            if touched:
                any_touched = True
                action = "would change" if args.check else "cleaned"
                print(f"{action}: {nb}")

    if args.check and any_touched:
        raise SystemExit(1)  # signal CI/pre-commit that cleaning is needed

if __name__ == "__main__":
    main()
