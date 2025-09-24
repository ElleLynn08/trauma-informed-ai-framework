"""Lightweight verification utilities (SMT guardrails + split checks).

This module adds 'fail-fast' safety to data pipeline and demonstrates
practical formal-methods concepts from Automated Verification.
It uses Z3 when available and falls back to pure-Python checks otherwise.

Functions:
    check_event_triplet(onset, apex, offset, n_frames) -> (ok, msg)
    check_window_bounds(start, length, n_frames) -> (ok, msg)
    check_sampling_consistency(frames, fps, duration_sec, tolerance=0.02) -> (ok, msg)
    assert_disjoint_splits(train_ids, val_ids, test_ids) -> None
    min_class_presence(labels_by_split, min_count=5) -> None
    assert_label_domain(y, allowed=(0,1)) -> None
"""

from typing import Tuple, Dict, Iterable
import pandas as pd

try:
    from z3 import Int, Solver, And, sat
    Z3_AVAILABLE = True
except Exception:
    Z3_AVAILABLE = False


def check_event_triplet(onset: int, apex: int, offset: int, n_frames: int) -> Tuple[bool, str]:
    """Ensure 0 <= onset < apex < offset <= n_frames-1."""
    if not Z3_AVAILABLE:
        ok = (0 <= onset < apex < offset <= (n_frames - 1))
        return ok, "OK" if ok else f"Violation: (onset={onset}, apex={apex}, offset={offset}, n={n_frames})"
    o, a, f, N = Int("o"), Int("a"), Int("f"), Int("N")
    s = Solver()
    s.add(o == onset, a == apex, f == offset, N == n_frames)
    s.add(And(0 <= o, o < a, a < f, f <= N - 1))
    if s.check() == sat:
        return True, "OK"
    return False, f"Constraint violation for (onset={onset}, apex={apex}, offset={offset}, n={n_frames})"


def check_window_bounds(start: int, length: int, n_frames: int) -> Tuple[bool, str]:
    """Ensure a feature window [start, start+length) stays within [0, n_frames)."""
    if not Z3_AVAILABLE:
        ok = (0 <= start) and (length >= 0) and (start + length <= n_frames)
        return ok, "OK" if ok else f"Window out of bounds: start={start}, length={length}, n={n_frames}"
    s, L, N = Int("s"), Int("L"), Int("N")
    solver = Solver()
    solver.add(s == start, L == length, N == n_frames)
    solver.add(And(0 <= s, 0 <= L, s + L <= N))
    if solver.check() == sat:
        return True, "OK"
    return False, f"Window out of bounds: start={start}, length={length}, n={n_frames}"


def check_sampling_consistency(frames: int, fps: float, duration_sec: float, tolerance: float = 0.02) -> Tuple[bool, str]:
    """Check duration ≈ frames / fps within tolerance and fps > 0."""
    if fps <= 0:
        return False, "fps must be positive"
    expected = frames / fps
    ok = abs(expected - duration_sec) <= (tolerance * max(1.0, duration_sec))
    return ok, "OK" if ok else f"Inconsistent timing: frames={frames}, fps={fps}, duration={duration_sec:.3f}s"


def assert_disjoint_splits(train_ids: Iterable, val_ids: Iterable, test_ids: Iterable) -> None:
    t, v, u = set(train_ids), set(val_ids), set(test_ids)
    overlap = (t & v) | (t & u) | (v & u)
    assert len(overlap) == 0, f"Subject overlap across splits: {overlap}"


def min_class_presence(labels_by_split: Dict[str, Iterable], min_count: int = 5) -> None:
    """Raise AssertionError if any class falls below min_count in any split."""
    from collections import Counter
    for split, labels in labels_by_split.items():
        counts = Counter(labels)
        too_small = {c: n for c, n in counts.items() if n < min_count}
        assert not too_small, f"{split} has underrepresented classes: {too_small}"


def assert_label_domain(y: Iterable, allowed=tuple([0, 1])) -> None:
    bad = set(pd.Series(list(y)).unique()) - set(allowed)
    assert not bad, f"Unexpected labels detected: {bad}"
