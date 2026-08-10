# errorbar

Statistically rigorous regression testing for AI agents.

`errorbar` tells you whether a regression in an AI agent's evaluation scores is
**statistically real** or just noise. It compares two evaluation runs using clustered
bootstrap confidence intervals, a paired Welch screen, and an explicit `UNDERPOWERED`
verdict for when the data cannot support a conclusion.

> **Status:** v0.1 in development. The scaffold is in place; the statistics are not
> implemented yet.

## Why

Agent evals are noisy. A 3-point drop on 40 tasks might be a real regression, or it
might be the same model on a different Tuesday. Most eval tooling reports a naked point
estimate and lets you draw the conclusion yourself, which is how eval tools lie.

`errorbar` refuses to. Every metric it returns carries an interval, the method that
produced it, and an alpha. When your seed count is too small to detect the effect you
care about, it says `UNDERPOWERED` and tells you how many seeds you would need.

## Install

```bash
uv sync
```

## Usage

```bash
uv run errorbar --help
uv run errorbar compare examples/baseline.json examples/candidate_regressed.json
```

### Exit codes

| Code | Verdict        | Meaning                                                        |
| ---- | -------------- | -------------------------------------------------------------- |
| 0    | `PASS`         | No regression detected, and the run had the power to find one.  |
| 10   | `FAIL`         | Regression is both statistically and practically significant.   |
| 11   | `WARN`         | Signal present, but the interval straddles the threshold.       |
| 12   | `UNDERPOWERED` | Not enough data to conclude anything. Add seeds.                |

Verdicts start at 10 on purpose. Codes 1 and 2 belong to click — uncaught exception and
usage error respectively — so a mistyped path exits 2 and can never be misread as a
borderline WARN. "The tool broke" and "the tool has an opinion" stay in disjoint ranges.

## Development

```bash
uv sync                                   # install
uv run pytest                             # all tests (skips slow by default)
uv run pytest -m slow                     # coverage simulations
uv run ruff check --fix . && uv run ruff format .
uv run mypy src/errorbar                  # strict
```

## Design rules

- **No naked point estimates.** Every metric is an `Interval` carrying
  `(point, low, high, alpha, method)`, and `method` has no default.
- **Determinism.** Every stochastic function takes an explicit
  `rng: numpy.random.Generator`. Same seed, byte-identical output.
- **`UNDERPOWERED` over false confidence.** An underpowered comparison never returns
  `PASS`.
- **`FAIL` is conservative.** It requires the *upper* bound of the delta interval to
  fall below `-min_effect`.
- **Never silently drop data.** Tasks that fail to match between runs are reported by
  ID in the verdict.

See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) for why each method was chosen.

## License

Apache-2.0. See [`LICENSE`](LICENSE).
