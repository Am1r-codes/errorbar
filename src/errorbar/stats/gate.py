"""The regression gate: from two runs to a verdict.

Planned contents (Days 12, 15):

- ``paired_deltas``: per-task candidate-minus-baseline differences, pairing on
  task ID. Tasks present in only one run are never silently dropped; their IDs
  are carried through to the verdict.

- ``welch_screen``: a paired Welch test used as a cheap screen before the
  bootstrap. Welch rather than Student because the two runs have no reason to
  share a variance.

- ``delta_interval``: the clustered bootstrap interval on the mean paired delta.
  This is the number the verdict is actually read off.

- ``compare``: the top-level entry point returning a ``GateVerdict``.

The four verdicts:

- ``UNDERPOWERED`` -- the seed count cannot detect ``min_effect`` at ``alpha``.
  Returned with a required-n. An underpowered comparison never returns PASS;
  reporting "no regression detected" from a run that could not have detected one
  is the specific lie this tool exists to prevent.
- ``FAIL`` -- conservative by construction: requires the *upper* bound of the
  delta interval to fall below ``-min_effect``, so statistical and practical
  significance must both fire.
- ``WARN`` -- signal is present but the interval straddles the threshold.
- ``PASS`` -- no regression, from a comparison that had the power to find one.
"""
