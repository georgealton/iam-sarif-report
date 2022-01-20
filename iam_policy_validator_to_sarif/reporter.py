from typing import Protocol
import click

class Reporter(Protocol):
    def __init__(self, location): ...
    def __call__(self, sarif): ...

class CLIReporter:
    def __init__(self, location):
        self.location = location

    def __call__(self, sarif):
        click.echo(file=self.location, message=sarif)
