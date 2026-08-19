# Journal

Day 1 is 2026-08-10, the tag is Day 21 (2026-08-30), so Day N falls on August (9 + N).

## Open stubs

A stub past its due date is no longer a plan, it is clutter. Update this table at the
end of each session; anything still `stub` below its due date is a slip, not a backlog.

Closed out at v0.1.0 (Aug 19). Nothing is `stub` any more: it either shipped or it is
`deferred`, which means it is out of scope for this version and has no due date until
the project is picked back up.

| File                        | Due             | Status                               |
| --------------------------- | --------------- | ------------------------------------ |
| `models.py`                 | Day 2 (Aug 11)  | done (Aug 13)                        |
| `stats/intervals.py`        | Days 3-11       | partial (percentile + wilson Aug 15) |
| `tests/test_determinism.py` | Day 5 (Aug 14)  | done (Aug 16)                        |
| `docs/METHODOLOGY.md`       | rolling         | done (Aug 19, two methods shipped)   |
| `tests/test_models.py`      | Day 2 (Aug 11)  | done (Aug 19, v0.1.1)                |
| `tests/test_coverage.py`    | Day 10 (Aug 19) | deferred                             |
| `stats/gate.py`             | Days 12, 15     | deferred                             |
| `stats/power.py`            | Day 16 (Aug 25) | deferred                             |
| `cli.py` `compare` body     | Day 17 (Aug 26) | deferred (exits 20, not implemented) |
| `fixtures.py`               | Day 18 (Aug 27) | deferred                             |

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

## 2026-08-15 — Day 4: intervals

- Changed: `wilson_interval` in `stats/intervals.py`. Closed-form, no rng —
  deterministic by construction. Boundary correction at k=0 and k=n substitutes the exact
  algebraic result for the float-drifted one; verified by watching
  `test_wilson_point_always_inside` fail without it. Seven tests including the Wald-
  collapse comparison and the symmetry invariant.
- Next: Day 5 determinism audit — every stochastic function takes an explicit rng,
  no module-level state. That plus this clears the Week 1 gate.
- Unclear: whether the domain still interests me. Deciding tomorrow with Week 1 finished, not tonight.

## 2026-08-16 — Day 7: randomness audit

- Changed: audited all `np.random`, `random.`, `default_rng`, and `seed` hits under `src/errorbar/` and `tests/`; no module-level RNG,
  no generator created inside a function, and no `rng` parameter with a default value was found in the library.
  Tests pass in explicit `default_rng(seed)` form, with no bare generator creation.
  Wrote tests/test_determinism.py — four tests pinning the contract for future work: same-seed reproducibility,
  deterministic functions stable across calls with no seed at all, bit-generator state advancing to
  prove the passed-in rng is genuinely consumed, and a signature check that rejects any function whose rng parameter carries a default.
  Proved the signature test can fail by temporarily defaulting rng on percentile_bootstrap and watching it go red.
- Next: keep the current discipline while implementing the remaining stochastic functions:
  every new random path must accept an explicit `rng` and never hide the seed.
- Unclear: whether errorbar's domain holds my interest. Week 1 is closed, so deciding tonight rather than carrying it.
  The statistics port to neuro/medical eval if the answer is no — clustered data,
  coverage, paired comparison are the same machinery.

## Week 1 gate (Aug 16)

- installs from clean clone: PASS (13 passed from /tmp clone)
- CI green, all five checks: PASS
- two interval methods: PASS (percentile bootstrap, Wilson)
- determinism enforced by test: PASS (tests/test_determinism.py, 4 tests)
Verdict: PASS — all four criteria met, two days late.

## 2026-08-19 — Day 10: v0.1.0 tagged

Shipped in 8 days: models with validation, percentile bootstrap, Wilson score interval,
determinism contract, 17 tests, clean-clone install verified.

Stopping at interval methods rather than the full gate. The statistics are the part I
wanted and got — they port directly to evaluating EEG decoders, where trials within a
subject are correlated the same way seeds within a task are. The domain isn't mine: the
architecture came from a plan I didn't write, which is why I couldn't explain the tool for
the first week.

Not abandoned. Clustered bootstrap and coverage are the interesting half and would make
this a real contribution. Revisit in Blok 1 alongside Statistics & Probability, or not —
decide after the EEG litmus test.

Hours: ~17 in week 1 against 42 planned. The six-hour day was never real.

## 2026-08-19 — Day 10 (later): v0.1.1, documentation-vs-code contradictions

Review of the v0.1.0 tag found four places where the docs and the code disagreed.
All four were the same failure as the old README, just smaller and closer to the
source.

- `stats/intervals.py` module docstring claimed "every estimator takes an explicit
  `rng`". Wilson takes none, deliberately, and METHODOLOGY.md said so correctly.
  The two documents contradicted each other and the wrong one was the one sitting
  next to the code. Rewritten: implemented vs deferred, and the rng rule now states
  what `test_determinism.py` actually enforces — that no `rng` parameter carries a
  default — rather than the stronger thing it does not check.
- `percentile_bootstrap` raised "there must be more than 2 values" on a `n < 2`
  check, so it named the wrong boundary. Now "needs at least 2 values, got {n}".
  The Wilson messages were fixed on Day 4; this one was missed.
- `tests/test_intervals.py` still carried its Day 1 placeholder docstring, listing
  `clustered_bootstrap` tests above twelve real ones. Replaced with a description of
  what is actually tested. `test_coverage.py` and `test_gate.py` keep their
  placeholders, correctly — those files are genuinely unbuilt.

The fourth was worse. `test_models.py` had one test, and it asserted `__version__`.
`models.py` shipped in v0.1.0 with zero tests covering any of the five design
decisions defended on Day 2, under a docstring promising four tests that did not
exist. The Day 1 entry warned about precisely this — "watch that the three skipped
placeholder tests get replaced by real ones rather than accumulating" — and it
happened anyway, unnoticed for six days.

Written now: 17 tests over Interval validation (method required, bound checks,
inclusive point bounds, exclusive alpha bounds), frozen-ness of all three models,
and the RunResult contracts (sorted unique task IDs, KeyError on unknown task,
sorted scores, mean_by_task). Each was mutation-checked — inclusive alpha bounds,
an unfrozen SampleResult, and `scores_for_task` returning `[]` instead of raising
each made the relevant test go red before the source was restored. 34 tests now.

The promised JSON round-trip test was not written, because there is nothing to
test: `models.py` has no serialization at all. That line was promising a test for
unbuilt functionality. Removed from the docstring and noted there instead.

Not fixed: coverage validation. Still the largest gap, still deliberately deferred.
