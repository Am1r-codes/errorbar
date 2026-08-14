"""Confidence interval estimators.

Planned contents (Days 3, 4, 8, 9, 11):

- ``wilson_interval``: score interval for a binomial proportion. Preferred over
  the Wald interval, which has badly degraded coverage at small ``n`` and at
  proportions near 0 or 1 -- exactly the regime eval pass-rates live in.
  Source: Wilson (1927), "Probable Inference, the Law of Succession, and
  Statistical Inference", JASA 22(158).

- ``percentile_bootstrap``: the plain percentile bootstrap, as the baseline
  resampling estimator and the reference the other methods are checked against.

- ``clustered_bootstrap``: resamples whole tasks rather than individual samples.
  Repeated seeds on the same task are correlated, so resampling samples
  independently understates the variance and produces intervals that are too
  narrow. Clustering on task ID is what keeps coverage honest.

- BCa correction: bias-corrected and accelerated percentile bootstrap, for the
  skewed sampling distributions that show up near the pass-rate boundaries.
  Source: Efron & Tibshirani (1993), "An Introduction to the Bootstrap", ch. 14.

Every estimator here returns an ``Interval`` and takes an explicit ``rng``.
Empirical coverage of a nominal 95% interval must land in [0.92, 0.97]; see
``tests/test_coverage.py``.
"""

from collections.abc import Sequence

import numpy as np

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
        raise ValueError(f"there must be more than 2 values in n: there is {n} right now.")
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
