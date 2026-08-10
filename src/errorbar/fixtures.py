"""Synthetic run generation for tests, demos, and coverage simulations.

Planned contents (Day 18):

- ``synthetic_run``: builds a ``RunResult`` with a known ground-truth pass rate,
  a controllable per-task effect, and a tunable amount of within-task
  correlation across seeds.

Because the ground truth is known by construction, these runs are what the
coverage simulations in ``tests/test_coverage.py`` measure the interval
estimators against. Generation takes an explicit ``rng``, so any fixture can be
reproduced byte-for-byte from its seed.
"""
