#!/usr/bin/env python3
"""
strip_bad_cells.py — remove old inline cells that cause nbconvert errors.
Usage:
  python scripts/strip_bad_cells.py notebooks/01_import_clean_eda.ipynb
"""
import sys
from pathlib import Path
import nbformat as nbf

if len(sys.argv) != 2:
    print("Usage: python scripts/strip_bad_cells.py <notebook.ipynb>")
    sys.exit(2)

nb_path = Path(sys.argv[1])
backup = nb_path.with_suffix(".ipynb.bak")
print("Reading:", nb_path)
nb = nbf.read(nb_path, as_version=4)
backup.write_bytes(nb_path.read_bytes())
print("Backup written to:", backup)

PATTERNS = [
    "auto-find a likely labels file under RAW",
    "Auto-find a likely labels file under RAW",
    "def score_name",
    "def list_files(base: Path",
    "def find_project_root(",
]

def is_bad(src: str) -> bool:
    return any(pat in src for pat in PATTERNS)

kept = []
removed = 0
for c in nb.cells:
    if c.cell_type == "code" and is_bad(c.source):
        removed += 1
        continue
    kept.append(c)

nb.cells = kept
nbf.write(nb, nb_path)
print(f"Removed {removed} cell(s). Saved:", nb_path)
