"""errorbar: statistically rigorous regression testing for AI agents.

Compares two evaluation runs and reports whether a score difference is real or
noise, using clustered bootstrap confidence intervals, a paired Welch screen, and
an explicit UNDERPOWERED verdict when the data cannot support a conclusion.

The public surface is assembled here as the package is built out. Nothing is
re-exported yet.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]
