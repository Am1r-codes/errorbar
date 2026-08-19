# Methodology

Why each interval method in `errorbar` was chosen, and where it stops being trustworthy.
This is the trust document: if you are deciding whether to believe a number this library
produced, this is the page that has to convince you.

Scope: v0.1 ships two estimators. Methods named in the source docstrings but not built —
clustered bootstrap, BCa correction, the Welch screen, the verdict logic — are deferred,
and their rationale is deliberately not written here. See
[JOURNAL.md](JOURNAL.md).

## Percentile bootstrap

**What it does.** `percentile_bootstrap(values, rng, n_resamples=10_000, alpha=0.05)`
resamples `values` with replacement `n_resamples` times, takes the mean of each resample,
and reads the interval off the empirical 2.5th and 97.5th percentiles of those means. It
returns an `Interval` whose `method` string carries the actual resample count
(`percentile_bootstrap_10000`), built from the argument rather than hardcoded, so a
2000-resample call cannot claim to be a 10000-resample one.

**Why this method.** It is the baseline nonparametric estimator and the reference the
other methods get checked against. It assumes nothing about the shape of the score
distribution, which matters because eval scores are frequently bounded, multi-modal, or
spiky in ways that make a normal-theory interval optimistic. It is also the simplest thing
that can be checked for correctness by simulation, which makes it the right first method
to build rather than the best one.

`ValueError` at `n < 2` rather than a zero-width interval: a single observation has no
spread to estimate, and returning `[x, x]` would be a confident-looking lie.

**Limitations.**

- *First-order accurate only.* The percentile bootstrap's coverage error shrinks as
  `O(n^-1/2)`. It applies no bias correction and no acceleration, so on a skewed
  sampling distribution — which is what you get near the pass-rate boundaries — the
  interval is shifted relative to the truth. BCa (Efron & Tibshirani 1993, ch. 14) is the
  second-order fix and is not implemented.
- *It quantises on a coarse value grid.* At small `n` with scores on a coarse grid, the
  set of achievable resample means is finite and small, so the empirical percentiles land
  on the same grid points regardless of seed. For the five values `[0.1, 0.4, 0.6, 0.9,
  0.3]`, resampling 5 of 5 with replacement yields only **36 distinct achievable means**
  spanning 41 grid positions. At `n_resamples = 10_000` the quantiles have converged onto
  that grid, and two different seeds return byte-identical bounds. This is documented in
  `test_determinism` in `tests/test_intervals.py`, and it is a genuine trap: a
  determinism test that passes on such data proves nothing about whether the function
  reads the `rng` it was handed. `tests/test_determinism.py` checks the bit-generator
  state advances for exactly this reason, and `test_different_seed_differs` uses 40
  continuous-valued scores so that seed sensitivity is actually observable.
- *No clustering.* It resamples observations independently. If the values passed in are
  repeated seeds on the same task, they are correlated, independent resampling
  understates the variance, and the interval comes out too narrow. Do not use this
  function on multi-seed-per-task data until the clustered bootstrap exists.

## Wilson score interval

**What it does.** `wilson_interval(successes, trials, alpha=0.05)` returns the Wilson
score interval for a binomial proportion — a pass rate. It is closed-form and takes no
`rng`, so it is deterministic by construction.

Source: Wilson (1927), "Probable Inference, the Law of Succession, and Statistical
Inference", *JASA* 22(158).

**Why this method.** The obvious alternative, the Wald interval, has badly degraded
coverage at small `n` and at proportions near 0 or 1 — which is exactly the regime eval
pass rates live in. Wald builds its standard error from the observed p̂, so at p̂ = 0 or
p̂ = 1 the standard error is zero and the interval collapses to a point: 5 passes out of 5
reports a pass rate of 100% ± 0. Wilson uses the hypothesized proportion instead, so it
never collapses. `test_wilson_survives_where_wald_collapses` pins this directly — Wald
width is exactly 0.0 at 5/5 where Wilson still spans [0.566, 1.000]. That test is the
reason the function exists.

Wald also escapes the unit interval at the boundaries, reporting negative lower bounds for
low pass rates. Wilson cannot: its bounds are algebraically confined to [0, 1].

**Boundary correction.** At `k = 0` and `k = n` the algebra gives exactly 0 and exactly 1,
but floating-point evaluation drifts a hair off — far enough to push a bound past `point`
and trip `Interval.__post_init__`'s own invariant. The implementation substitutes the exact
algebraic result at those two cases. This was verified by removing the correction and
watching `test_wilson_point_always_inside` fail, rather than by assuming it was needed.

**Limitations.**

- *Binomial only.* It needs a count of successes out of trials. It does not apply to
  continuous scores; use the bootstrap for those.
- *Independence assumed.* The interval assumes `trials` independent Bernoulli draws.
  Repeated seeds on the same task are not independent, and the interval will be too narrow
  on such data for the same reason the unclustered bootstrap is.
- *Not exact.* Wilson is an approximation with substantially better small-sample coverage
  than Wald, not a guaranteed-coverage method. Its actual coverage oscillates with `n` and
  `p`, and can dip below nominal. Clopper–Pearson is the conservative exact alternative and
  is not implemented.

## What is not validated

The empirical coverage simulations described in `tests/test_coverage.py` — draw many
synthetic runs with known ground truth, build a nominal 95% interval for each, count how
often the truth falls inside, require the rate to land in [0.92, 0.97] — are **not
written**. That file is a skipped placeholder.

Both estimators above are therefore justified by derivation, by published reference values
(`test_wilson_known_values` checks all six cases at n=5 to 1e-6), and by invariant tests.
Neither has been shown to cover at its nominal rate on this codebase's own data. That is
the single largest gap in this document, and it is the first thing to build if the project
resumes.
