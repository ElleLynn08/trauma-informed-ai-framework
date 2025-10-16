
#!/usr/bin/env python3
"""
check_notebook_outputs.py — confirm that Jupyter notebooks contain executed outputs.

Usage:
  python check_notebook_outputs.py notebooks/
"""

import sys
from pathlib import Path
import nbformat

if len(sys.argv) != 2:
    print("Usage: python check_notebook_outputs.py <notebooks_dir>")
    sys.exit(2)

nb_dir = Path(sys.argv[1])
if not nb_dir.is_dir():
    print("❌ Provided path is not a directory:", nb_dir)
    sys.exit(1)

notebooks = list(nb_dir.glob("*.ipynb"))
if not notebooks:
    print("⚠️ No notebooks found in:", nb_dir)
    sys.exit(0)

print(f"🔍 Checking {len(notebooks)} notebooks in: {nb_dir}")
missing_output = False

for nb_path in notebooks:
    nb = nbformat.read(nb_path, as_version=4)
    has_output = any(
        cell.get("outputs") for cell in nb.cells if cell.cell_type == "code"
    )
    if has_output:
        print(f"✅ {nb_path.name} contains output cells.")
    else:
        print(f"❌ {nb_path.name} has NO visible outputs.")
        missing_output = True

if missing_output:
    print("\n🚨 Some notebooks are missing outputs! Double-check before pushing.")
    sys.exit(1)

print("\n✅ All notebooks appear to contain executed outputs.")
