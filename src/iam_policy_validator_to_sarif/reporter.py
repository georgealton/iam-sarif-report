from __future__ import annotations

try:
    from typing import Protocol, TYPE_CHECKING
except ImportError:
    from typing_extensions import Protocol, TYPE_CHECKING

import click

if TYPE_CHECKING:
    from sarif_om import SarifLog


class Reporter(Protocol):
    def __call__(self, location, sarif: SarifLog):
        ...


class CLIReporter:
    def __call__(self, location, sarif) -> None:
        click.echo(file=location, message=sarif)
