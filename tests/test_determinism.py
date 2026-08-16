"""Determinism contract tests for stochastic and deterministic functions."""

import inspect
from copy import deepcopy

import numpy as np

import errorbar.stats.intervals as intervals
from errorbar.stats.intervals import percentile_bootstrap, wilson_interval


def test_all_public_functions_require_explicit_rng_when_named_rng():
    """Any future stochastic API must accept RNG explicitly, never with a default."""
    public_members = []
    for name, value in vars(intervals).items():
        if name.startswith("_"):
            continue
        if callable(value) and getattr(value, "__module__", None) == intervals.__name__:
            public_members.append(value)

    assert public_members, "no public functions were inspected; the contract test is vacuous"

    for fn in public_members:
        signature = inspect.signature(fn)
        if "rng" in signature.parameters:
            assert signature.parameters["rng"].default is inspect.Parameter.empty


def test_stochastic_functions_reproduce_with_same_seed():
    """A fresh generator with the same seed reproduces exactly the same output."""
    values = [0.1, 0.4, 0.6, 0.9, 0.3]

    a = percentile_bootstrap(values, np.random.default_rng(42))
    b = percentile_bootstrap(values, np.random.default_rng(42))

    assert a == b


def test_deterministic_functions_need_no_seed_at_all():
    """Deterministic functions are stable across repeated calls with identical inputs."""
    a = wilson_interval(successes=3, trials=5, alpha=0.05)
    b = wilson_interval(successes=3, trials=5, alpha=0.05)

    assert a == b


def test_rng_is_genuinely_consumed():
    """The supplied generator advances when the stochastic routine uses it."""
    values = [0.2, 0.5, 0.7, 0.9, 0.4, 0.6]
    rng = np.random.default_rng(123)
    before = deepcopy(rng.bit_generator.state)

    percentile_bootstrap(values, rng, n_resamples=250, alpha=0.05)

    after = rng.bit_generator.state
    assert after != before
