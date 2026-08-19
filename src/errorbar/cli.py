"""Command-line interface.

v0.1 ships no working command. ``compare`` depends on the gate, which is not
implemented, so it refuses with ``ExitCode.NOT_IMPLEMENTED`` rather than
pretending to have an opinion. The interval estimators are usable as a library;
see the README.

Deferred (was Day 17): ``compare`` loads two run files, runs the gate, renders
the verdict as a rich table, and exits with an ``ExitCode`` the CI system can
read.
"""

from __future__ import annotations

import logging
from enum import IntEnum
from pathlib import Path
from typing import Annotated

import typer

from errorbar import __version__

logger = logging.getLogger(__name__)


class ExitCode(IntEnum):
    """Process exit codes for ``errorbar compare``.

    Verdicts start at 10 rather than 1 because click already owns the low
    numbers: it exits 1 on an uncaught exception and 2 on a usage error. Mapping
    WARN to 2 would make a mistyped path indistinguishable from a real
    borderline result, which is precisely the kind of quiet lie this tool exists
    to prevent. Leaving 1 and 2 to click keeps "the tool broke" and "the tool
    has an opinion" in disjoint ranges.

    ``NOT_IMPLEMENTED`` sits in a third range for the same reason: "this tool
    has nothing built to answer you with" is neither a crash nor a verdict, and
    a CI system must never read it as one.
    """

    PASS = 0
    FAIL = 10
    WARN = 11
    UNDERPOWERED = 12
    NOT_IMPLEMENTED = 20


app = typer.Typer(
    name="errorbar",
    help="Confidence interval methods for stochastic evaluation data.",
    no_args_is_help=True,
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    """Print the version and exit, when --version is passed."""
    if value:
        typer.echo(f"errorbar {__version__}")
        raise typer.Exit


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Show the version and exit.",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Confidence interval methods for stochastic evaluation data."""


@app.command(short_help="Not implemented in v0.1 (exits 20).")
def compare(
    baseline: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Baseline run, as JSON."),
    ],
    candidate: Annotated[
        Path,
        typer.Argument(exists=True, dir_okay=False, help="Candidate run, as JSON."),
    ],
) -> None:
    """Compare two evaluation runs and report whether the difference is real.

    Not implemented in v0.1: always exits 20. The gate this command reads its
    verdict from does not exist yet, and a command that returns PASS without
    having run a comparison is worse than no command at all.
    """
    typer.secho(
        "errorbar compare is not implemented in v0.1 "
        f"(would have compared {baseline} against {candidate}).\n"
        "v0.1 ships the interval estimators as a library only; "
        "see the Status section of the README.",
        err=True,
        fg=typer.colors.YELLOW,
    )
    raise typer.Exit(code=ExitCode.NOT_IMPLEMENTED)


if __name__ == "__main__":
    app()
