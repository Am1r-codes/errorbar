"""Frozen data models shared across the package.

Planned contents (Day 2):

- ``SampleResult``: one task attempt by one seed, with its score and metadata.
- ``RunResult``: a full evaluation run, i.e. a collection of ``SampleResult``
  grouped by task ID.
- ``Interval``: a point estimate that refuses to travel alone, carrying
  ``(point, low, high, alpha, method)``. ``method`` has no default; the caller
  must state how the interval was computed.
- ``TaskComparison``: per-task baseline-vs-candidate delta and its interval.
- ``GateVerdict``: the final PASS / FAIL / WARN / UNDERPOWERED decision, the
  delta interval that produced it, and the IDs of any tasks dropped because they
  did not match across runs.

All models are frozen dataclasses with full type hints.
"""
