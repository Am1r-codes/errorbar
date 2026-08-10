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

import pytest


@pytest.mark.skip(reason="intervals.py not implemented yet")
def test_placeholder():
    raise AssertionError
