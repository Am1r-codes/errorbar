"""Command-line interface.

Planned contents (Day 17): the ``compare`` command loads two run files, runs the
gate, renders the verdict as a rich table, and exits with an ``ExitCode`` the CI
system can read.

Only the command surface exists so far; the commands themselves are stubs.
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
    """

    PASS = 0
    FAIL = 10
    WARN = 11
    UNDERPOWERED = 12


app = typer.Typer(
    name="errorbar",
    help="Tell whether a regression in an AI agent's eval scores is real or noise.",
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
    """Statistically rigorous regression testing for AI agents."""


@app.command()
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

    Exits 0 on PASS, 10 on FAIL, 11 on WARN, 12 on UNDERPOWERED. Codes 1 and 2
    belong to click and mean the invocation itself was wrong.
    """
    raise NotImplementedError("compare is not implemented yet; see stats/gate.py")


if __name__ == "__main__":
    app()
