"""Power analysis: how many seeds would this comparison have needed?

Planned contents (Day 16):

- ``required_n``: the number of seeds per task needed to detect an effect of
  size ``min_effect`` at significance ``alpha`` and power ``1 - beta``, given an
  observed per-task variance.

This is what turns an UNDERPOWERED verdict from a refusal into an instruction:
the gate does not just decline to conclude, it reports the sample size that
would let it conclude.
"""
