from typing import Protocol
import click

class Reporter(Protocol):
    def __call__(self, location, sarif: "SarifLog"): ...

class CLIReporter:
    def __call__(self, location, sarif) -> None:
        click.echo(file=location, message=sarif)
