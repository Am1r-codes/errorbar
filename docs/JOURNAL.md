# Journal

Day 1 is 2026-08-10, the tag is Day 21 (2026-08-30), so Day N falls on August (9 + N).

## Open stubs

A stub past its due date is no longer a plan, it is clutter. Update this table at the
end of each session; anything still `stub` below its due date is a slip, not a backlog.

| File                        | Due            | Status |
| --------------------------- | -------------- | ------ |
| `models.py`                 | Day 2 (Aug 11) | stub   |
| `stats/intervals.py`        | Days 3-11      | stub   |
| `tests/test_coverage.py`    | Day 10 (Aug 19)| stub   |
| `stats/gate.py`             | Days 12, 15    | stub   |
| `stats/power.py`            | Day 16 (Aug 25)| stub   |
| `cli.py` `compare` body     | Day 17 (Aug 26)| stub   |
| `fixtures.py`               | Day 18 (Aug 27)| stub   |
| `docs/METHODOLOGY.md`       | rolling        | outline|

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
