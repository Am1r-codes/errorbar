"""Tests for the frozen data models.

To come alongside Day 2:

- ``Interval`` rejects construction without an explicit ``method``.
- ``Interval`` rejects ``low > point`` and ``point > high``.
- All models are genuinely frozen: attribute assignment raises.
- ``RunResult`` round-trips through JSON without losing task IDs.
"""

import errorbar


def test_package_exposes_version():
    assert errorbar.__version__ == "0.1.0"
