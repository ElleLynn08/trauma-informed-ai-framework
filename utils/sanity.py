# utils/sanity.py
# =============================================================================
# Sanity Utilities for Data Projects
# =============================================================================
# This module provides helper functions for:
#   • Environment checks (versions, package presence)
#   • Path setup and required file assertions
#   • Data sanity routines (overviews, label balance, integrity checks)
#   • Reproducibility utilities (random seeds, saving checkpoints)
#   • 🕷️ Elle's Spider Check (peace-of-mind data peek)
#
# Design goals:
#   - Lightweight, notebook-friendly, explicit.
#   - Comments first: future-you (and reviewers) should learn by reading it.
# =============================================================================

from __future__ import annotations

from pathlib import Path
import importlib.util
import platform
import random
import subprocess
import sys
import os
from typing import Iterable, Optional, Tuple, Dict, Any

import numpy as np
import pandas as pd

# --- make display() available both in notebooks and scripts -------------------
try:
    from IPython.display import display  # type: ignore
except Exception:  # fallback when IPython isn't present
    def display(obj):  # type: ignore
        print(obj)


# -----------------------------------------------------------------------------
# -------- Environment ---------------------------------------------------------
# -----------------------------------------------------------------------------
def sanity_env(pkgs: Iterable[str] = ("pandas", "numpy", "matplotlib", "seaborn", "sklearn")) -> None:
    """
    Print Python + system info and confirm key packages are importable.
    Handy for bug reports and cross-machine reproducibility.
    """
    print(f"Python : {sys.version.split()[0]} | {platform.platform()}")
    print(f"Exe    : {sys.executable}")
    print(f"CWD    : {os.getcwd()}")
    for p in pkgs:
        print(f"{p:10s}: {'FOUND' if importlib.util.find_spec(p) else 'MISSING'}")


def freeze_top(top: Iterable[str] = ("pandas", "numpy", "scikit-learn", "matplotlib", "seaborn")) -> None:
    """
    Show versions of a chosen set of dependencies (mini 'pip freeze').
    """
    res = subprocess.run(
        [sys.executable, "-m", "pip", "freeze", "--disable-pip-version-check"],
        text=True,
        capture_output=True,
        check=False,
    )
    have = {ln.split("==")[0]: ln for ln in res.stdout.splitlines() if "==" in ln}
    print("Top deps:")
    for name in top:
        print(" ", have.get(name, f"{name}==?"))


# -----------------------------------------------------------------------------
# -------- Paths ---------------------------------------------------------------
# -----------------------------------------------------------------------------
def setup_paths(start: Path | None = None) -> Tuple[Path, Path, Path, Path, Path]:
    """
    Return (root_dir, data_dir, raw_dir, clean_dir, out_dir) and ensure they exist.

    root_dir  = repo root (auto-detected if a "data" folder exists)
    data_dir  = project-level data folder
    raw_dir   = location for raw DAIC-WOZ data
    clean_dir = pre-cleaned intermediates
    out_dir   = outputs (checkpoints, models, figures)
    """
    start = Path(start or Path.cwd())
    root_dir = start if (start / "data").exists() else start.parent
    data_dir = root_dir / "data"
    raw_dir = data_dir / "raw" / "daic_woz"
    clean_dir = data_dir / "cleaned"
    out_dir = root_dir / "outputs"
    for d in (data_dir, raw_dir, clean_dir, out_dir):
        d.mkdir(parents=True, exist_ok=True)
    return root_dir, data_dir, raw_dir, clean_dir, out_dir


def require_files(paths: Iterable[Path]) -> None:
    """
    Assert that required files exist; raise AssertionError if any are missing.
    """
    missing = [p for p in paths if not Path(p).exists()]
    assert not missing, f"Missing required files:\n{missing}"
    print("Files OK ✅")


# -----------------------------------------------------------------------------
# -------- Data sanity ---------------------------------------------------------
# -----------------------------------------------------------------------------
def data_overview(df: pd.DataFrame, show_nulls: int = 10) -> None:
    """
    Quick overview:
      • Shape (#rows, #cols)
      • First 3 rows
      • Dtypes
      • Top N null counts
    """
    print("Shape:", df.shape)
    display(df.head(3))
    display(df.dtypes)
    nulls = df.isna().sum().sort_values(ascending=False)
    print("Nulls (top):")
    display(nulls[nulls > 0].head(show_nulls))


def label_balance(df: pd.DataFrame, label_col: str, binary_col: Optional[str] = None) -> None:
    """
    Show label distributions.
    - For numeric labels: histogram over integer bins.
    - For binary/nominal: counts per class (if binary_col provided).
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # seaborn.set() is older; set_theme() is the modern entry point
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots()
    lo, hi = int(df[label_col].min()), int(df[label_col].max())
    rng = range(lo, hi + 1)
    sns.histplot(df[label_col], bins=rng, ax=ax)
    ax.set_title(f"{label_col} distribution")
    plt.show()

    if binary_col and binary_col in df.columns:
        display(df[binary_col].value_counts(dropna=False).rename("count").to_frame())
        sns.countplot(x=df[binary_col])
        plt.title(f"{binary_col} balance")
        plt.show()


def check_integrity(
    df: pd.DataFrame,
    id_col: Optional[str] = None,
    label_col: Optional[str] = None,
    label_range: Optional[Tuple[int, int]] = None,
) -> None:
    """
    Integrity checks:
      • Duplicate IDs (if id_col provided)
      • Label values within [lo, hi] (if label_col + label_range provided)
    """
    if id_col and id_col in df.columns:
        dup = df.duplicated(subset=[id_col]).sum()
        print(f"Duplicate {id_col}: {dup}")
        assert dup == 0, f"Found {dup} duplicate {id_col}"

    if label_col and label_col in df.columns and label_range:
        lo, hi = label_range
        assert df[label_col].between(lo, hi).all(), f"{label_col} outside [{lo},{hi}]"


# -----------------------------------------------------------------------------
# -------- Repro & checkpoints -------------------------------------------------
# -----------------------------------------------------------------------------
def set_seeds(seed: int = 42) -> int:
    """
    Set seeds for Python's random and NumPy RNGs.
    """
    random.seed(seed)
    np.random.seed(seed)
    print("Seed set:", seed)
    return seed


def save_checkpoint(df: pd.DataFrame, out_path: Path, n: int = 100) -> Path:
    """
    Save a small checkpoint (top N rows) of a DataFrame as Parquet.
    Great for debugging or sharing a lightweight sample.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.head(n).to_parquet(out_path, index=False)
    print("Checkpoint saved:", out_path)
    return out_path


# -----------------------------------------------------------------------------
# -------- Elle's Spider Check -------------------------------------------------
# -----------------------------------------------------------------------------
def spider_check(df: pd.DataFrame, name: str = "DataFrame", peek: int = 2) -> Dict[str, Any]:
    """
    🕷️ Elle's Spider Check — a peace-of-mind data peek.

    Origin:
        Like pulling back the covers in a cabin to make sure no critters are
        hiding before you rest. A tiny ritual for peace of mind.

    In practice:
        • Show the first few rows (head)
        • Confirm shape matches expectations
        • Surface null counts (top few) to catch obvious issues early
    """
    result: Dict[str, Any] = {
        "name": name,
        "shape": df.shape,
        "null_counts": df.isna().sum().to_dict(),
        "peek": df.head(peek).to_dict(orient="records"),
    }

    # Log a compact, helpful summary (works in notebooks and scripts)
    print(f"\n🕷️ Spider Check [{name}] — shape={df.shape}")
    # show only a few null counts to keep logs readable
    top5_nulls = dict(list(result["null_counts"].items())[:5])
    print("Null counts (top 5):", top5_nulls)
    display(df.head(peek))

    return result

