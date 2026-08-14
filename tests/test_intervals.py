"""Tests for the interval estimators.

To come alongside Days 3, 4, 8, 9, 11:

- ``wilson_interval`` matches published values at the textbook cases, and stays
  inside [0, 1] at p = 0 and p = 1 where Wald escapes the unit interval.
- Every estimator returns an ``Interval`` whose ``method`` is set.
- Determinism: the same ``rng`` seed produces byte-identical output.
- ``clustered_bootstrap`` yields wider intervals than ``percentile_bootstrap``
  on the same correlated data -- if it does not, the clustering is not working.
- Degenerate inputs: a single task, a single seed, zero variance.
"""

import numpy as np
import pytest

from errorbar.stats.intervals import percentile_bootstrap


def test_point_inside_interval():
    values = [1.0, 0.3, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9, 0.4, 0.2]
    rng = np.random.default_rng(0)
    result = percentile_bootstrap(values, rng)
    assert result.low <= result.point <= result.high
    assert result.method == "percentile_bootstrap_10000"


def test_determinism():
    values = [0.1, 0.4, 0.6, 0.9, 0.3]
    a = percentile_bootstrap(values, np.random.default_rng(42))
    b = percentile_bootstrap(values, np.random.default_rng(42))
    assert a.low == b.low
    assert a.high == b.high
    # n=5 on a 0.1 grid yields only 36 achievable means,
    # so at B=10,000 the quantiles converge and different seeds agree.


def test_wider_data_wider_interval():
    tight = [0.50, 0.51, 0.49, 0.50, 0.52, 0.48, 0.51, 0.49]
    wide = [0.05, 0.95, 0.20, 0.80, 0.10, 0.90, 0.30, 0.70]
    t = percentile_bootstrap(tight, np.random.default_rng(1))
    w = percentile_bootstrap(wide, np.random.default_rng(1))
    assert (t.high - t.low) < (w.high - w.low)


def test_different_seed_differs():
    values = [
        0.625095,
        0.897214,
        0.775686,
        0.225207,
        0.300166,
        0.873553,
        0.005265,
        0.821228,
        0.797069,
        0.467935,
        0.303032,
        0.278426,
        0.25487,
        0.445076,
        0.504548,
        0.553497,
        0.9955,
        0.792662,
        0.622179,
        0.98896,
        0.215309,
        0.160212,
        0.61254,
        0.043942,
        0.03568,
        0.514889,
        0.466206,
        0.917168,
        0.629226,
        0.514118,
        0.496873,
        0.247515,
        0.011794,
        0.192402,
        0.692032,
        0.200607,
        0.369536,
        0.003734,
        0.830048,
        0.154461,
    ]
    a = percentile_bootstrap(values, np.random.default_rng(42))
    b = percentile_bootstrap(values, np.random.default_rng(43))
    assert a.low != b.low
    assert a.high != b.high


def test_single_value_raises():
    with pytest.raises(ValueError):
        percentile_bootstrap([0.5], np.random.default_rng(0))
