from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

import click

if TYPE_CHECKING:
    from sarif_om import SarifLog


class Reporter(Protocol):
    def __call__(self, location, sarif: SarifLog):
        ...


class CLIReporter:
    def __call__(self, location, sarif) -> None:
        click.echo(file=location, message=sarif)
