"""Empirical coverage simulations -- the correctness test for the intervals.

Marked ``slow`` and deselected by default. Run with ``pytest -m slow``.

To come alongside Day 10: draw many synthetic runs with a known ground truth,
build a nominal 95% interval for each, and count how often the truth falls
inside. Coverage must land in [0.92, 0.97]. An interval that does not cover at
its nominal rate is wrong, however elegant its derivation.

Any change to ``stats/intervals.py`` requires re-running this file.
"""

import pytest


@pytest.mark.slow
@pytest.mark.skip(reason="intervals.py not implemented yet")
def test_placeholder():
    raise AssertionError
