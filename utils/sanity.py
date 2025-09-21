# utils/sanity.py
from __future__ import annotations
from pathlib import Path
import sys, os, platform, importlib.util, subprocess, random
import numpy as np
import pandas as pd
from typing import Iterable, Optional

# -------- Environment --------
def sanity_env(pkgs: Iterable[str] = ("pandas","numpy","matplotlib","seaborn","sklearn")) -> None:
    """Print kernel/python info and confirm key packages are importable."""
    print(f"Python: {sys.version.split()[0]} | {platform.platform()}")
    print(f"Exe   : {sys.executable}")
    print(f"CWD   : {os.getcwd()}")
    for p in pkgs:
        print(f"{p:10s}:", "FOUND" if importlib.util.find_spec(p) else "MISSING")

def freeze_top(top=("pandas","numpy","scikit-learn","matplotlib","seaborn")) -> None:
    """Print versions of a few key deps."""
    res = subprocess.run([sys.executable,"-m","pip","freeze","--disable-pip-version-check"],
                         text=True, capture_output=True)
    have = {ln.split("==")[0]: ln for ln in res.stdout.splitlines() if "==" in ln}
    print("Top deps:")
    for name in top:
        print(" ", have.get(name, f"{name}==?"))

# -------- Paths --------
def setup_paths(start: Path | None = None):
    """Return ROOT/DATA/RAW/CLEAN/OUT Path objects (and ensure they exist)."""
    start = Path(start or Path.cwd())
    ROOT  = start if (start/"data").exists() else start.parent
    DATA  = ROOT/"data"
    RAW   = DATA/"raw"/"daic_woz"
    CLEAN = DATA/"cleaned"
    OUT   = ROOT/"outputs"
    for d in (DATA, RAW, CLEAN, OUT):
        d.mkdir(parents=True, exist_ok=True)
    return ROOT, DATA, RAW, CLEAN, OUT

def require_files(paths: Iterable[Path]) -> None:
    missing = [p for p in paths if not Path(p).exists()]
    assert not missing, f"Missing required files:\n{missing}"
    print("Files OK ✅")

# -------- Data sanity --------
def data_overview(df: pd.DataFrame, show_nulls: int = 10) -> None:
    print("Shape:", df.shape)
    display(df.head(3))
    display(df.dtypes)
    nulls = df.isna().sum().sort_values(ascending=False)
    print("Nulls (top):"); display(nulls[nulls>0].head(show_nulls))

def label_balance(df: pd.DataFrame, label_col: str, binary_col: Optional[str] = None) -> None:
    import matplotlib.pyplot as plt, seaborn as sns
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    rng = range(int(df[label_col].min()), int(df[label_col].max())+1)
    sns.histplot(df[label_col], bins=rng, ax=ax)
    ax.set_title(f"{label_col} distribution"); plt.show()
    if binary_col and binary_col in df.columns:
        display(df[binary_col].value_counts(dropna=False).rename("count").to_frame())
        sns.countplot(x=df[binary_col]); plt.title(f"{binary_col} balance"); plt.show()

def check_integrity(df: pd.DataFrame, id_col: Optional[str] = None,
                    label_col: Optional[str] = None,
                    label_range: Optional[tuple[int,int]] = None) -> None:
    if id_col and id_col in df.columns:
        dup = df.duplicated(subset=[id_col]).sum()
        print(f"Duplicate {id_col}: {dup}")
        assert dup == 0, f"Found {dup} duplicate {id_col}"
    if label_col and label_col in df.columns and label_range:
        lo, hi = label_range
        assert df[label_col].between(lo, hi).all(), f"{label_col} outside [{lo},{hi}]"

# -------- Repro & checkpoints --------
def set_seeds(seed: int = 42) -> int:
    random.seed(seed); np.random.seed(seed)
    print("Seed set:", seed); return seed

def save_checkpoint(df: pd.DataFrame, out_path: Path, n: int = 100) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.head(n).to_parquet(out_path, index=False)
    print("Checkpoint saved:", out_path)
    return out_path
