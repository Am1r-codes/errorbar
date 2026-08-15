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

from math import sqrt

import numpy as np
import pytest
from scipy.stats import norm

from errorbar.stats.intervals import percentile_bootstrap, wilson_interval

WILSON_N5 = [
    (0, 0.000000, 0.434482),
    (1, 0.036224, 0.624465),
    (2, 0.117621, 0.769276),
    (3, 0.230724, 0.882379),
    (4, 0.375535, 0.963776),
    (5, 0.565518, 1.000000),
]


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


def test_wilson_known_values():
    for k, exp_low, exp_high in WILSON_N5:
        result = wilson_interval(successes=k, trials=5)
        assert result.low == pytest.approx(exp_low, abs=1e-6)
        assert result.high == pytest.approx(exp_high, abs=1e-6)
        assert result.method == "wilson_score"


def test_wilson_survives_where_wald_collapses():
    """This is why the function exists."""
    n = 5
    p_hat = 1.0
    z = norm.ppf(0.975)
    wald_se = sqrt(p_hat * (1 - p_hat) / n)
    wald_width = 2 * z * wald_se
    wilson = wilson_interval(successes=5, trials=n)
    wilson_width = wilson.high - wilson.low
    assert wald_width == 0.0
    assert wilson_width > 0.0


def test_wilson_zero_successes():
    result = wilson_interval(successes=0, trials=5)
    assert result.low == 0.0
    assert result.high == pytest.approx(0.434482, abs=1e-6)


def test_wilson_symmetry():
    lower = wilson_interval(1, 5)
    upper = wilson_interval(4, 5)
    assert lower.low + upper.high == pytest.approx(1.0, abs=1e-9)
    assert lower.high + upper.low == pytest.approx(1.0, abs=1e-9)


def test_wilson_point_always_inside():
    for trials in (5, 20, 100):
        for successes in range(trials + 1):
            result = wilson_interval(successes, trials)
            assert result.low <= result.point <= result.high


def test_wilson_smaller_alpha_widens_interval():
    loose = wilson_interval(3, 5, 0.20)
    strict = wilson_interval(3, 5, 0.05)
    loose_width = loose.high - loose.low
    strict_width = strict.high - strict.low
    assert loose_width < strict_width


def test_wilson_rejects_invalid_input():
    with pytest.raises(ValueError, match="at least 1"):
        wilson_interval(successes=0, trials=0)

    with pytest.raises(ValueError, match="at least 0"):
        wilson_interval(successes=-1, trials=5)

    with pytest.raises(ValueError, match="more than the given trials"):
        wilson_interval(successes=6, trials=5)
