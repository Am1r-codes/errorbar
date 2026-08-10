"""Tests for the regression gate.

To come alongside Days 12, 15:

- A large, obvious regression on plenty of seeds returns FAIL.
- The same regression on too few seeds returns UNDERPOWERED, never PASS.
- FAIL requires the interval's *upper* bound below ``-min_effect``: a delta that
  is statistically significant but smaller than ``min_effect`` returns WARN.
- Tasks present in only one run are reported by ID in the verdict, never
  silently dropped.
- Determinism: the same seed produces the same verdict.
"""

import pytest


@pytest.mark.skip(reason="gate.py not implemented yet")
def test_placeholder():
    raise AssertionError
