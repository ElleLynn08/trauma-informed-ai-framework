#!/usr/bin/env python3
"""
SAFE VERSION — Only remove cells marked with '# stripme'
Usage:
  python scripts/strip_bad_cells.py notebooks/your_notebook.ipynb
"""

import sys
from pathlib import Path
import nbformat as nbf

if len(sys.argv) != 2:
    print("Usage: python strip_bad_cells.py <notebook.ipynb>")
    sys.exit(2)

nb_path = Path(sys.argv[1])
backup = nb_path.with_suffix(".ipynb.bak")
print("Reading:", nb_path)
nb = nbf.read(nb_path, as_version=4)
backup.write_bytes(nb_path.read_bytes())
print("✅ Backup written to:", backup)

def is_strippable(cell):
    return cell.cell_type == "code" and "# stripme" in cell.source

kept = []
removed = 0
for c in nb.cells:
    if is_strippable(c):
        removed += 1
        continue
    kept.append(c)

nb.cells = kept
nbf.write(nb, nb_path)
print(f"✅ Removed {removed} cell(s). Saved updated file: {nb_path}")

