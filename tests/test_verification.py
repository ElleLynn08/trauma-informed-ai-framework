import sys, pathlib
# Ensure src/ is on the path for CI/local runs
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / 'src'))

import numpy as np
import pandas as pd
import pytest
from verification import (
    check_event_triplet, check_window_bounds, check_sampling_consistency,
    assert_disjoint_splits, min_class_presence, assert_label_domain
)

def test_check_event_triplet_ok():
    ok, msg = check_event_triplet(0, 5, 10, 100)
    assert ok

def test_check_event_triplet_violation():
    ok, msg = check_event_triplet(5, 3, 8, 100)  # onset >= apex
    assert not ok
    assert "Violation" in msg or "Constraint violation" in msg

def test_check_window_bounds_ok():
    ok, msg = check_window_bounds(10, 20, 100)
    assert ok

def test_check_window_bounds_violation():
    ok, msg = check_window_bounds(90, 20, 100)
    assert not ok

def test_check_sampling_consistency_ok():
    ok, msg = check_sampling_consistency(frames=300, fps=30.0, duration_sec=10.0, tolerance=0.01)
    assert ok

def test_check_sampling_consistency_bad_fps():
    ok, msg = check_sampling_consistency(frames=300, fps=0.0, duration_sec=10.0)
    assert not ok
    assert "fps must be positive" in msg

def test_assert_disjoint_splits_ok():
    assert_disjoint_splits([1,2,3], [4,5], [6,7])

def test_assert_disjoint_splits_overlap():
    with pytest.raises(AssertionError):
        assert_disjoint_splits([1,2,3], [3,4], [5])

def test_min_class_presence_ok():
    labels_by_split = {'train':[0,0,1,1,1], 'val':[0,1,1,1,0], 'test':[0,1,0,1,1]}
    min_class_presence(labels_by_split, min_count=2)

def test_min_class_presence_fail():
    with pytest.raises(AssertionError):
        min_class_presence({'train':[0,0,0], 'val':[1,1,1], 'test':[0]}, min_count=2)

def test_assert_label_domain_ok():
    assert_label_domain([0, 1, 0, 1], allowed=(0,1))

def test_assert_label_domain_bad():
    with pytest.raises(AssertionError):
        assert_label_domain([0, 1, 2], allowed=(0,1))
