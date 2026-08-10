# Methodology

Why each method in `errorbar` was chosen, and what it assumes. This is the trust
document: if you are deciding whether to believe a verdict this tool produced, this is
the page that has to convince you.

> **Status:** outline only. Each section gets written as its method lands.

## The problem

<!-- Why a point estimate on eval scores is not a measurement. -->

## Wilson intervals for pass rates

<!-- Wilson (1927). Why not Wald: coverage collapse at small n and at p near 0 or 1. -->

## Clustered bootstrap

<!-- Repeated seeds on one task are correlated. Resampling samples instead of tasks
     understates variance and produces intervals that are too narrow. -->

## BCa correction

<!-- Efron & Tibshirani (1993), ch. 14. Skewed sampling distributions near the
     pass-rate boundaries. -->

## The paired Welch screen

<!-- Why Welch and not Student: the two runs have no reason to share a variance. -->

## The four verdicts

<!-- Why FAIL requires the upper bound below -min_effect, and why UNDERPOWERED exists
     rather than defaulting to PASS. -->

## Coverage validation

<!-- How `tests/test_coverage.py` checks these claims empirically, and what the
     [0.92, 0.97] band on a nominal 95% interval means. -->

## Known limitations

<!-- What this tool does not tell you. -->
