"""
config_paths.py
Central place to resolve project paths and list data files.
Keeps notebook cells tiny and avoids indentation issues inside .ipynb JSON.
"""

from pathlib import Path
from typing import Iterable, List, Tuple

# Markers we consider signs of the repo root
MARKERS = ("requirements.txt", ".git", "README.md")

def find_project_root(markers: Iterable[str] = MARKERS) -> Path:
    """
    Walk upward from the current working directory until we find a directory
    that contains any of the marker files (e.g., requirements.txt, .git).
    This makes path handling robust whether you launch from PyCharm, JupyterLab,
    or CLI. If nothing is found, we return the current directory as a fallback.
    """
    here = Path.cwd().resolve()
    for cand in [here, *here.parents]:
        if any((cand / m).exists() for m in markers):
            return cand
    return here

# Resolve canonical paths once, import everywhere else
ROOT = find_project_root()
DATA = ROOT / "data"
RAW = DATA / "raw" / "daic_woz"        # <-- adjust if your raw subfolder differs
CLEAN = DATA / "cleaned"
PROCESSED = DATA / "processed"

def list_files(base: Path, patterns=(".csv", ".tsv", ".xlsx", ".json", ".parquet", ".txt")) -> List[Tuple[Path, float]]:
    """
    Return (relative_path, sizeMB) for readable data files under 'base',
    sorted by size desc then path. Includes common text/binary formats.
    """
    rows: List[Tuple[Path, float]] = []
    if not base.exists():
        return rows
    for p in base.rglob("*"):
        if p.is_file() and p.suffix.lower() in patterns:
            try:
                size_mb = round(p.stat().st_size / 1_000_000, 2)
            except OSError:
                size_mb = float("nan")  # file disappeared between list and stat
            rows.append((p.relative_to(base), size_mb))
    rows.sort(key=lambda x: ((-x[1]) if x[1] == x[1] else float("-inf"), str(x[0])))
    return rows

