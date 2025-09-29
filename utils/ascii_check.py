# =============================================================================
# ASCII Spider Check 🕷️
# =============================================================================
# Utility to crawl files/folders and report non-ASCII characters.
# Complements clean_notebooks.py (which focuses only on Jupyter notebooks).
# This one is broader: works for .py, .md, .txt, .csv, and .ipynb (metadata).
#
# Why:
#   Hidden non-ASCII characters can sneak into code and docs (smart quotes,
#   thin spaces, odd dashes). They often break linters, CI, or parsers.
#   This script surfaces exactly where they are so you can fix them fast.
#
# Usage examples:
#   python utils/ascii_check.py utils/sanity.py
#   python utils/ascii_check.py notebooks/
#   python utils/ascii_check.py utils/ notebooks/ README.md
#
# Flags:
#   --no-ignore-emojis     Do not whitelist the default emojis/symbols.
#   --whitelist-add "@$%"  Add extra characters to the whitelist.
#   --ext ".py,.md"        Limit to specific extensions (comma-separated).
#   --summary              Print only a final summary line (quiet mode).
#
# Exit code:
#   0  -> no issues found
#   1  -> one or more files contain non-ASCII characters (outside whitelist)
# =============================================================================

from __future__ import annotations

from pathlib import Path
from typing import Iterable, List, Tuple, Set
import argparse
import sys

# -----------------------------------------------------------------------------
# Whitelists and defaults
# -----------------------------------------------------------------------------

# Default whitelist: allowed non-ASCII characters that will NOT be flagged.
# These are "friendly critters" intentionally used in comments/logs/README.
DEFAULT_WHITELIST: Set[str] = {
    # Emojis (existing + section headers + variation selector)
    "🕷", "🕷️", "✅", "⚠", "⚠️", "❓", "❌", "️",
    "📌", "🧠", "📚", "⚡", "🛠", "🛠️", "🧪", "📦", "🌱",
    "👉", "🔭", "🧾", "✨",

    # Punctuation
    "•", "–", "—", "…", "→",

    # Symbols from examples
    "☀", "✈", "✔"
}


# Default text-like extensions to check when crawling folders.
DEFAULT_EXTS: Set[str] = {".py", ".md", ".txt", ".csv", ".ipynb"}

# -----------------------------------------------------------------------------
# Core scanning logic
# -----------------------------------------------------------------------------
def ascii_issues_in_file(
    path: Path,
    ignore_emojis: bool = True,
    whitelist: Iterable[str] = (),
) -> List[Tuple[int, int, str, str]]:
    """
    Scan a single file for non-ASCII characters.

    Returns a list of issues:
        [(line_number, column_number, offending_char, stripped_line_text), ...]

    Notes:
        - File is opened as UTF-8. Binary/unreadable encodings will raise.
        - If ignore_emojis is True, any character in 'whitelist' is skipped.
    """
    issues: List[Tuple[int, int, str, str]] = []
    allowed = set(whitelist) if ignore_emojis else set()

    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            for colno, ch in enumerate(line, start=1):
                if ord(ch) > 127 and ch not in allowed:
                    # Record: line, column, repr(char), and the stripped line
                    issues.append((lineno, colno, repr(ch), line.rstrip("\n")))

    return issues


def is_text_candidate(file: Path, allowed_exts: Set[str]) -> bool:
    """Return True if the file should be scanned based on its extension."""
    return file.is_file() and file.suffix.lower() in allowed_exts


def crawl_paths(
    targets: Iterable[Path],
    allowed_exts: Set[str],
    ignore_emojis: bool,
    whitelist: Iterable[str],
    summary_only: bool,
) -> int:
    """
    Crawl files and folders. Print findings.
    Return the total number of files with issues.
    """
    files_with_issues = 0

    def scan_file(p: Path) -> None:
        nonlocal files_with_issues
        try:
            issues = ascii_issues_in_file(p, ignore_emojis=ignore_emojis, whitelist=whitelist)
        except Exception as e:
            if not summary_only:
                print(f"❓ Skipped (unreadable as UTF-8): {p} ({e})")
            return

        if issues:
            files_with_issues += 1
            if not summary_only:
                print(f"\n⚠️ Non-ASCII characters found in {p}:")
                for lineno, colno, ch_repr, snippet in issues:
                    print(f"  line {lineno:>5}, col {colno:>3}: {ch_repr} in -> {snippet}")
        else:
            if not summary_only:
                print(f"✅ {p} is clean ASCII (aside from allowed symbols).")

    for target in targets:
        if target.is_file():
            scan_file(target)
        elif target.is_dir():
            for file in target.rglob("*"):
                if is_text_candidate(file, allowed_exts):
                    scan_file(file)
        else:
            if not summary_only:
                print(f"❌ Path does not exist or is not a file/folder: {target}")

    if summary_only:
        if files_with_issues:
            print(f"⚠️ Non-ASCII found in {files_with_issues} file(s).")
        else:
            print("✅ No non-ASCII issues detected (aside from allowed symbols).")

    return files_with_issues


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ascii_check.py",
        description="ASCII Spider Check 🕷️ — report non-ASCII characters in files/folders.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more files/folders to scan.",
    )
    parser.add_argument(
        "--no-ignore-emojis",
        action="store_true",
        help="Do not whitelist the default emojis/symbols (🕷️ ✅ • – — … → ❓ ⚠️ ❌).",
    )
    parser.add_argument(
        "--whitelist-add",
        default="",
        help="Additional characters to whitelist, e.g. '@$%'.",
    )
    parser.add_argument(
        "--ext",
        default=",".join(sorted(DEFAULT_EXTS)),
        help="Comma-separated list of file extensions to scan (default: .py,.md,.txt,.csv,.ipynb).",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Summary-only (quiet) output.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    targets = [Path(p) for p in args.paths]
    allowed_exts = {e.strip().lower() for e in args.ext.split(",") if e.strip()}

    # Build whitelist
    whitelist: Set[str] = set()
    if not args.no_ignore_emojis:
        whitelist |= DEFAULT_WHITELIST
    if args.whitelist_add:
        for ch in args.whitelist_add:
            whitelist.add(ch)

    # Run crawl
    files_with_issues = crawl_paths(
        targets=targets,
        allowed_exts=allowed_exts,
        ignore_emojis=not args.no_ignore_emojis,
        whitelist=whitelist,
        summary_only=args.summary,
    )

    return 1 if files_with_issues else 0


if __name__ == "__main__":
    sys.exit(main())



