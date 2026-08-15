# Journal

Day 1 is 2026-08-10, the tag is Day 21 (2026-08-30), so Day N falls on August (9 + N).

## Open stubs

A stub past its due date is no longer a plan, it is clutter. Update this table at the
end of each session; anything still `stub` below its due date is a slip, not a backlog.

| File                     | Due            | Status                               |
| ------------------------ | -------------- | -------------------------------------|
| `models.py`              | Day 2 (Aug 11) | done (Aug 13)                        |
| `stats/intervals.py`     | Days 3-11      | partial (percentile + wilson Aug 15) |
| `tests/test_coverage.py` | Day 10 (Aug 19)| stub                                 |
| `stats/power.py`         | Day 16 (Aug 25)| stub                                 |
| `cli.py` `compare` body  | Day 17 (Aug 26)| stub                                 |
| `fixtures.py`            | Day 18 (Aug 27)| stub                                 |
| `docs/METHODOLOGY.md`    | rolling        | outline                              |
| `stats/gate.py`          | Days 12, 15    | stub                                 |

## 2026-08-10 — Day 1: scaffold

- Changed: full package scaffold — pyproject (ruff line-length 100, mypy strict on
  `src/errorbar`, pytest with a deselected-by-default `slow` marker), Apache-2.0 LICENSE
  (the old one was a saved HTML page), README, `.gitignore`, CI running
  ruff → format → mypy → pytest → pytest -m slow, docstring-only module stubs, and a typer
  CLI with a `compare` stub. Resolved the exit-code collision immediately rather than on
  Day 17: verdicts moved to 0/10/11/12, leaving click's 1 and 2 alone, so a mistyped path
  can never be read as a WARN. Contract updated in `cli.py`, README, and CLAUDE.md.
- Next: Day 2 — models in `models.py`, starting from the `Interval` tests in
  `tests/test_models.py`.
- Unclear: nothing blocking. Watch that the three skipped placeholder tests get replaced
  by real ones rather than accumulating.


## 2026-08-13 — Day 2 (2 days late): models

- Changed: `models.py` implemented by hand — `SampleResult` (task_id, seed, score,
  passed), `RunResult` (run_id, samples, plus `task_ids()`, `scores_for_task()`,
  `mean_by_task()`), and `Interval` (point, low, high, alpha, method) with
  `__post_init__` validation. Design decisions made and defended: `mean_by_task` is a
  method not a cached field (measurement and interpretation stay separate);
  `scores_for_task` raises KeyError on an unknown task rather than returning an empty
  list (silent empties become nan deep in the bootstrap); `task_ids()` returns sorted
  for determinism; alpha bounds are exclusive, point bounds inclusive. No numpy in
  models — `sum(x)/len(x)` keeps it a pure data module.
- Next: Day 3 — percentile bootstrap in `stats/intervals.py`.
- Unclear: nothing blocking. Running one day behind on errorbar; DSA and ML tracks
  are on schedule.

## 2026-08-14 — Day 3: intervals

- Changed: `percentile_bootstrap` in `stats/intervals.py`, hand-written.
  Method string built from `n_resamples` rather than hardcoded, so a 2000-resample call can't claim 10000.
  `ValueError` at n < 2 rather than a zero-width interval. Five tests including
  a coarse-support case documenting why seeds converge at n=5.
- Next: Day 4 — `wilson_interval`, closed form. The k=5, n=5 test is the point of it.
- Unclear: nothing blocking. Nothing yet proves the function reads the `rng`
  it's handed rather than a hardcoded one — Day 5's determinism audit covers it.

## 2026-08-15 — Day 3: intervals

- Changed: `wilson_interval` in `stats/intervals.py`. Closed-form, no rng —
  deterministic by construction. Boundary correction at k=0 and k=n substitutes the exact
  algebraic result for the float-drifted one; verified by watching 
  `test_wilson_point_always_inside` fail without it. Seven tests including the Wald-
  collapse comparison and the symmetry invariant.
- Next: Day 5 determinism audit — every stochastic function takes an explicit rng,
  no module-level state. That plus this clears the Week 1 gate.
- Unclear: whether the domain still interests me. Deciding tomorrow with Week 1 finished, not tonight.
