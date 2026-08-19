"""Confidence interval estimators.

Implemented:

- ``wilson_interval``: score interval for a binomial proportion. Preferred over
  the Wald interval, which has badly degraded coverage at small ``n`` and at
  proportions near 0 or 1 -- exactly the regime eval pass-rates live in.
  Source: Wilson (1927), "Probable Inference, the Law of Succession, and
  Statistical Inference", JASA 22(158). Unlike the Wald interval, its standard
  error uses the hypothesized proportion rather than ``p̂``, so it never
  collapses at the boundary when the observed rate is 0 or 1. Closed-form, so
  it takes no ``rng``.

- ``percentile_bootstrap``: the plain percentile bootstrap, as the baseline
  resampling estimator and the reference the other methods are checked against.
  Stochastic, so it takes an explicit ``rng``.

Deferred (see ``docs/JOURNAL.md``):

- ``clustered_bootstrap``: resamples whole tasks rather than individual samples.
  Repeated seeds on the same task are correlated, so resampling samples
  independently understates the variance and produces intervals that are too
  narrow. Clustering on task ID is what keeps coverage honest.

- BCa correction: bias-corrected and accelerated percentile bootstrap, for the
  skewed sampling distributions that show up near the pass-rate boundaries.
  Source: Efron & Tibshirani (1993), "An Introduction to the Bootstrap", ch. 14.

Every estimator here returns an ``Interval``. Stochastic estimators take an
explicit ``rng`` and never create one internally; deterministic ones take no
``rng`` at all. ``tests/test_determinism.py`` rejects any function here whose
``rng`` parameter carries a default, and checks that a generator handed to a
stochastic estimator is genuinely consumed.

Empirical coverage has NOT been validated: ``tests/test_coverage.py`` is an
unwritten placeholder. See the "What is not validated" section of
``docs/METHODOLOGY.md``.
"""

from collections.abc import Sequence
from math import sqrt

import numpy as np
from scipy.stats import norm

from errorbar.models import Interval


def percentile_bootstrap(
    values: Sequence[float],
    rng: np.random.Generator,
    n_resamples: int = 10_000,
    alpha: float = 0.05,
) -> Interval:
    """The plain percentile bootstrap.

    This is the baseline resampling estimator and the reference the other methods
    are checked against.
    """
    arr = np.asarray(values, dtype=float)
    n = len(arr)
    if n < 2:
        raise ValueError(f"percentile_bootstrap needs at least 2 values, got {n}")
    vals_mean = float(np.mean(arr))

    boot_means = np.empty(n_resamples)
    for i in range(n_resamples):
        idx = rng.integers(0, n, size=n)
        boot_means[i] = arr[idx].mean()

    low, high = np.percentile(boot_means, [100 * alpha / 2, 100 * (1 - alpha / 2)])

    return Interval(
        point=vals_mean,
        low=float(low),
        high=float(high),
        alpha=alpha,
        method=f"percentile_bootstrap_{n_resamples}",
    )


def wilson_interval(successes: int, trials: int, alpha: float = 0.05) -> Interval:
    """Wilson score interval for a binomial proportion.

    Source: Wilson (1927), "Probable Inference, the Law of Succession, and
    Statistical Inference", JASA 22(158). Unlike the Wald interval, its
    standard error uses the hypothesized proportion rather than ``p̂``, so it
    never collapses at the boundary when the observed rate is 0 or 1.
    """
    if trials <= 0:
        raise ValueError(f"Trials must be at least 1; trials {trials}")
    if successes < 0:
        raise ValueError(f"Successes must be at least 0; successes {successes}")
    if successes > trials:
        raise ValueError(
            f"Successes are more than the given trials: successes {successes} > trials {trials}"
        )

    p_hat = successes / trials
    z = norm.ppf(1 - alpha / 2)
    denom = 1 + z**2 / trials
    center = (p_hat + z**2 / (2 * trials)) / denom
    margin = (z / denom) * sqrt(p_hat * (1 - p_hat) / trials + z**2 / (4 * trials**2))
    low, high = center - margin, center + margin

    # the algebra gives exactly 0 at k=0 and exactly 1 at k=n; floating point drifts a hair off,
    # which can push the bound past `point` and break the interval's own invariant.
    if successes == 0:
        low = 0.0
    if successes == trials:
        high = 1.0

    return Interval(
        point=float(p_hat), low=float(low), high=float(high), alpha=alpha, method="wilson_score"
    )
