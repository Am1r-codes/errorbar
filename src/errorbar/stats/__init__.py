"""Statistical machinery: intervals, the regression gate, and power analysis.

Every stochastic function in this subpackage takes an explicit
``rng: numpy.random.Generator`` as a required parameter, and every function that
returns a metric returns an ``Interval`` rather than a bare float.
"""
