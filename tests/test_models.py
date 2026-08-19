"""Tests for the frozen data models.

Covers the design decisions defended when ``models.py`` was written:

- ``Interval`` requires an explicit ``method``; there is no default, so a
  result can never travel without stating how it was produced.
- ``Interval`` validates its own bounds. Point bounds are inclusive, alpha
  bounds are exclusive.
- All models are genuinely frozen: attribute assignment raises.
- ``task_ids()`` returns sorted unique IDs, for determinism.
- ``scores_for_task`` raises ``KeyError`` on an unknown task rather than
  returning an empty list, because silent empties become nan deep in the
  bootstrap.

No JSON round-trip test: ``models.py`` has no serialization. When run loading
lands, that test lands with it.
"""

import dataclasses
import importlib.metadata

import pytest

import errorbar
from errorbar.models import Interval, RunResult, SampleResult


def _run() -> RunResult:
    return RunResult(
        run_id="r1",
        samples=[
            SampleResult(task_id="beta", seed=1, score=0.4, passed=False),
            SampleResult(task_id="alpha", seed=1, score=0.8, passed=True),
            SampleResult(task_id="beta", seed=2, score=0.6, passed=True),
            SampleResult(task_id="alpha", seed=2, score=0.6, passed=True),
        ],
    )


def test_version_matches_distribution_metadata():
    """`__version__` and the packaged version must not drift apart."""
    assert errorbar.__version__ == importlib.metadata.version("errorbar")


def test_interval_requires_explicit_method():
    """``method`` has no default: omitting it is a construction error."""
    with pytest.raises(TypeError):
        Interval(point=0.5, low=0.4, high=0.6, alpha=0.05)  # type: ignore[call-arg]


def test_interval_rejects_low_above_high():
    with pytest.raises(ValueError, match="exceeds high"):
        Interval(point=0.5, low=0.9, high=0.1, alpha=0.05, method="m")


@pytest.mark.parametrize("point", [0.05, 0.95])
def test_interval_rejects_point_outside_bounds(point: float):
    with pytest.raises(ValueError, match="outside"):
        Interval(point=point, low=0.1, high=0.9, alpha=0.05, method="m")


@pytest.mark.parametrize("point", [0.1, 0.9])
def test_interval_point_bounds_are_inclusive(point: float):
    """A point sitting exactly on a bound is valid: k=0 and k=n produce these."""
    assert Interval(point=point, low=0.1, high=0.9, alpha=0.05, method="m").point == point


@pytest.mark.parametrize("alpha", [0.0, 1.0, -0.1, 1.5])
def test_interval_rejects_alpha_outside_open_unit_interval(alpha: float):
    """Alpha bounds are exclusive: alpha of exactly 0 or 1 is meaningless."""
    with pytest.raises(ValueError, match="alpha"):
        Interval(point=0.5, low=0.1, high=0.9, alpha=alpha, method="m")


@pytest.mark.parametrize(
    "model",
    [
        SampleResult(task_id="t", seed=0, score=0.5, passed=True),
        RunResult(run_id="r", samples=[]),
        Interval(point=0.5, low=0.4, high=0.6, alpha=0.05, method="m"),
    ],
)
def test_models_are_frozen(model: SampleResult | RunResult | Interval):
    field = next(iter(dataclasses.fields(model))).name
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(model, field, "mutated")


def test_task_ids_are_sorted_and_unique():
    """Sorted for determinism: iteration order must not depend on input order."""
    assert _run().task_ids() == ["alpha", "beta"]


def test_scores_for_task_raises_on_unknown_task():
    """KeyError, not an empty list: silent empties become nan in the bootstrap."""
    with pytest.raises(KeyError, match="nope"):
        _run().scores_for_task("nope")


def test_scores_for_task_returns_sorted_scores():
    assert _run().scores_for_task("beta") == [0.4, 0.6]


def test_mean_by_task():
    assert _run().mean_by_task() == {"alpha": pytest.approx(0.7), "beta": pytest.approx(0.5)}
