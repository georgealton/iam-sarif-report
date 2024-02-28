from __future__ import annotations

from pathlib import Path
from typing import Protocol

import click
from sarif_om import SarifLog


class Reporter(Protocol):
    def __call__(self, location: Path | str, sarif: SarifLog) -> None:
        ...


class CLIReporter:
    def __call__(self, location: Path | str, sarif: SarifLog) -> None:
        if not isinstance(location, str) and str(location) != "-":
            location.parent.mkdir(parents=True, exist_ok=True)
        with click.open_file(str(location), "w") as f:
            click.echo(file=f, message=sarif)
