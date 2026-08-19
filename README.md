# errorbar

Confidence interval methods for stochastic evaluation data.

## Why

Agents are stochastic: the same suite run twice gives different scores. A single run
reports one number with no indication of how far that number moves when nothing about the
system has changed. Comparing two single runs therefore tells you nothing — you cannot
tell a regression from the spread until you measure the spread.

## Status

### Implemented

- `percentile_bootstrap` — nonparametric CI for the mean of a set of scores.
- `wilson_interval` — score interval for a binomial proportion (pass rates).
- Determinism contract — every stochastic function takes an explicit
  `numpy.random.Generator`, enforced by tests.

### Not implemented

- Clustered bootstrap (resampling whole tasks, for correlated seeds).
- Gate logic (PASS / FAIL / WARN / UNDERPOWERED verdicts).
- CLI — `errorbar compare` exits 20 with "not implemented in v0.1".
- Power analysis (required-n for a given effect size).

Paused during university term. See [docs/JOURNAL.md](docs/JOURNAL.md) for what was built,
what was deferred, and why.

## Quickstart

```python
import numpy as np

from errorbar.stats.intervals import percentile_bootstrap, wilson_interval

# Ten runs of the same suite, same agent. The spread is the whole point.
scores = [0.82, 0.91, 0.78, 0.88, 0.85, 0.79, 0.93, 0.81, 0.87, 0.84]

mean = percentile_bootstrap(scores, rng=np.random.default_rng(0))
print(f"mean score  {mean.point:.3f}  95% CI [{mean.low:.3f}, {mean.high:.3f}]  {mean.method}")

# Pass rate as a proportion: 9 of those 10 runs cleared the bar.
rate = wilson_interval(successes=9, trials=10)
print(f"pass rate   {rate.point:.3f}  95% CI [{rate.low:.3f}, {rate.high:.3f}]  {rate.method}")
```

```text
mean score  0.848  95% CI [0.819, 0.878]  percentile_bootstrap_10000
pass rate   0.900  95% CI [0.596, 0.982]  wilson_score
```

That pass rate is the argument for the library in one line: 9 out of 10 is consistent with
a true rate anywhere from 0.60 to 0.98. Both functions return an `Interval` carrying
`(point, low, high, alpha, method)` — `method` has no default, so a result always states
how it was produced.

See [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for why each method was chosen and where it
breaks down.

## Install

Requires Python 3.12+.

```bash
git clone https://github.com/Am1r-codes/errorbar
cd errorbar
uv sync
uv run pytest
```

## License

Apache-2.0. See [LICENSE](LICENSE).
