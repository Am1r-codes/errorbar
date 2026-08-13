# CLAUDE.md — errorbar

`errorbar` tells you whether a regression in an AI agent's evaluation scores is **statistically real** or just noise. It compares two evaluation runs using clustered bootstrap confidence intervals, a paired Welch screen, and an explicit UNDERPOWERED verdict when the data can't support a conclusion.

Built by Amir (2nd-year BSc AI, University of Amsterdam) as a learning project *and* a real tool. Both goals matter, and when they conflict, learning wins.

---

## THE LEARNING CONTRACT — read this before every task

**Amir types the code. Claude does not write implementations for him.**

The rule is about authorship, not about avoiding libraries. Importing scipy,
numpy, typer, or rich is expected and encouraged — reinventing `norm.ppf` or
`ttest_ind` teaches nothing and risks numerical bugs. What matters is that the
logic in this repo was written by Amir, not generated.

### Do NOT write implementation code for these

Anything in `src/errorbar/stats/`, the gate decision rules, and the verdict
policy. If asked to implement one, do not produce the code. Offer instead, in
this order:

1. **Write the failing test** — fixture, assertions, edge cases. Show what
   correct looks like without showing how to reach it.
2. **Explain the algorithm** in prose or math. Formulas, procedures, and
   pointers to the right library function are fine; working code is not.
3. **Review code he already wrote** — correctness, numerical stability, edge
   cases, vectorization.
4. **Ask a leading question** if he's close but stuck on one line.

This holds even if he asks directly, even if it's late. He set this rule while
thinking clearly.

**Escape hatch:** if he says he's been stuck on the same bug for more than 20
minutes and wants a direct answer, give it — then explain why it was wrong so
the debugging still teaches something.

### One algorithm that must be hand-written, not delegated to a library

The two-level clustered bootstrap resampling loop. `scipy.stats.bootstrap` does
not do clustered resampling, and that resampling *is* the product. Use scipy for
`norm.ppf`, `norm.cdf`, `ttest_ind`, and percentile computation inside it.

### DO write these freely

Scaffold, pyproject/ruff/mypy config, GitHub Actions, typer plumbing, rich table
formatting, JSON serialization, test skeletons, synthetic fixture data, docstring
formatting, README structure, and debugging help on stack traces.

**The test:** does typing this teach him something he needs in Blok 1 Statistics
or in an interview? Yes → his hands. No → yours.

---

## Commands

```bash
uv sync                                   # install
uv run pytest                             # all tests (skips slow by default)
uv run pytest -m slow                     # coverage simulations (~60s)
uv run pytest tests/test_intervals.py -v  # one file
uv run ruff check --fix . && uv run ruff format .
uv run mypy src/errorbar                  # strict
uv run errorbar --help
uv run errorbar compare examples/baseline.json examples/candidate_regressed.json
```

## Repo map

```
src/errorbar/
  models.py          SampleResult, RunResult, Interval, TaskComparison, GateVerdict
  stats/intervals.py wilson_interval, percentile_bootstrap, clustered_bootstrap (+BCa)
  stats/gate.py      paired_deltas, welch_screen, delta_interval, compare
  stats/power.py     required_n
  fixtures.py        synthetic_run — generates test/demo data
  cli.py             typer CLI, exit codes 0/10/11/12 = PASS/FAIL/WARN/UNDERPOWERED
                     (1 and 2 stay click's: exception and usage error)
tests/               unit tests + test_coverage.py (marked slow)
examples/            demo baseline/candidate JSON pairs
docs/METHODOLOGY.md  why each method was chosen — the trust document
```

Keep it flat. Do not propose splitting into multiple packages, adding a plugin system, or introducing an abstraction layer "for later." v0.1 is one person's three weeks.

## Hard rules — violations are bugs, not style

1. **No naked point estimates.** Any function returning a metric returns an `Interval` carrying `(point, low, high, alpha, method)`. `method` has no default — the caller must state how it was computed. Tests assert this shape.
2. **Determinism.** Every stochastic function takes an explicit `rng: np.random.Generator` as a required parameter. No `np.random.seed()`, no module-level RNG, no defaults. Same seed ⇒ byte-identical output, and there's a test proving it.
3. **UNDERPOWERED over false confidence.** If the seed count can't detect `min_effect` at `alpha`, the gate returns UNDERPOWERED with a required-n, never PASS. This is the product's whole philosophy — never "simplify" it away.
4. **FAIL is conservative.** FAIL requires the *upper* bound of the delta interval to fall below `-min_effect`. Both statistical and practical significance must fire.
5. **Never silently drop data.** If tasks don't match between runs, report the dropped IDs in the verdict. Silent dropping is how eval tools lie.
6. **Coverage is the correctness test.** Any change to interval code requires re-running `pytest -m slow`. Empirical coverage of a 95% interval must land in [0.92, 0.97].
7. **Cite the method.** Every statistical function's docstring names its source (Wilson 1927; Efron & Tibshirani for BCa; the clustered-bootstrap rationale for correlated samples).
8. **No new dependencies** beyond numpy, scipy, typer, rich without an explicit discussion. No pandas, no sklearn, no pydantic in v0.1.

## Workflow

- **Tests before implementation** for anything in `stats/`. Claude writes the failing test, Amir makes it pass.
- **Plan mode** for anything crossing more than two files. Otherwise just do it.
- Conventional commits: `feat(stats):`, `fix(gate):`, `test:`, `docs:`, `chore:`. One logical change per commit.
- Never commit with failing tests, failing mypy, or lint errors.
- After each session append 3 lines to `docs/JOURNAL.md`: what changed, what's next, what's unclear.
- Prefer editing an existing module over creating a new file.

## Style

Python 3.12+. Full type hints on every public function. Frozen dataclasses for models. Google-style docstrings on anything public. `logging`, never `print`, in library code (the CLI may use `rich`). No emoji in code or output. Functions over 40 lines get split.

## Current status

v0.1 in development, targeting a tag on **30 August 2026**. Scope: load two runs → clustered bootstrap CI on the delta → four-verdict gate → CLI with exit codes.

**Explicitly out of scope for v0.1** (do not suggest adding them): Inspect AI integration, GitHub Action, sequential/anytime-valid testing, trajectory diffing, certificates, registry, web dashboard, hosted anything.

If Amir proposes a new feature, project, or architectural expansion during this sprint, the correct response is to point at this section and ask whether it can wait until September. His known failure mode is planning instead of shipping; the tag date matters more than any feature.
