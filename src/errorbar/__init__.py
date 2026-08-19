"""errorbar: confidence interval methods for stochastic evaluation data.

Agents are stochastic: the same suite run twice gives different scores. This
package estimates how far those scores move on their own, so a result carries its
uncertainty instead of travelling as a bare point estimate.

v0.1 ships ``percentile_bootstrap`` and ``wilson_interval`` in
``errorbar.stats.intervals``, both returning an ``Interval`` and both bound by an
enforced determinism contract. The clustered bootstrap, the regression gate, the
CLI, and power analysis are deferred -- see ``docs/JOURNAL.md``.

Nothing is re-exported here yet; import from ``errorbar.stats.intervals``.
"""

__version__ = "0.1.1"

__all__ = ["__version__"]
