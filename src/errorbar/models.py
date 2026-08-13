"""Frozen data models shared across the package.

Planned contents (Day 2):

- ``SampleResult``: one task attempt by one seed, with its score and metadata. (DONE)
- ``RunResult``: a full evaluation run, i.e. a collection of ``SampleResult`` (DONE)
  grouped by task ID.
- ``Interval``: a point estimate that refuses to travel alone, carrying (DONE)
  ``(point, low, high, alpha, method)``. ``method`` has no default; the caller
  must state how the interval was computed.
- ``TaskComparison``: per-task baseline-vs-candidate delta and its interval.
- ``GateVerdict``: the final PASS / FAIL / WARN / UNDERPOWERED decision, the
  delta interval that produced it, and the IDs of any tasks dropped because they
  did not match across runs.

All models are frozen dataclasses with full type hints.

Note:
----
Not yet implemented: TaskComparison, GateVerdict (Day 15).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SampleResult:
    """A single evaluation of one task at one seed, with it's score and metadata."""

    task_id: str
    seed: int
    score: float
    passed: bool


@dataclass(frozen=True)
class RunResult:
    """A collection of sample results across many tasks and seeds."""

    run_id: str
    samples: list[SampleResult]

    def task_ids(self) -> list[str]:
        """Extracts unique task-IDs and sorts them."""
        unique_task_ids = set()
        for s in self.samples:
            unique_task_ids.add(s.task_id)
        return sorted(unique_task_ids)

    def scores_for_task(self, task_id: str) -> list[float]:
        """Extracts scores of the given task-ID and sorts them."""
        scores = []
        for sample in self.samples:
            if sample.task_id == task_id:
                scores.append(sample.score)

        if not scores:
            raise KeyError(f"task {task_id} not in run; available: {self.task_ids()}")
        return sorted(scores)

    def mean_by_task(self) -> dict[str, float]:
        """Calculates the mean scores and collects them in a dict with task-ID's as keys."""
        result = {}
        for task in self.task_ids():
            scores = self.scores_for_task(task)
            result[task] = sum(scores) / len(scores)
        return result


@dataclass(frozen=True)
class Interval:
    """A point estimate with its uncertainty bounds.

    ``method`` has no default; the caller must state how the interval was computed.
    """

    point: float
    low: float
    high: float
    alpha: float
    method: str

    def __post_init__(self) -> None:
        if self.low > self.high:
            raise ValueError(f"low ({self.low}) exceeds high ({self.high})")
        if not 0 < self.alpha < 1:
            raise ValueError(f"alpha must be in (0, 1), got {self.alpha}")
        if not self.low <= self.point <= self.high:
            raise ValueError(f"point ({self.point}) outside [{self.low}, {self.high}]")
