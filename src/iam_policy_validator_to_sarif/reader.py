from typing import TextIO

import click


class Reader:
    def __call__(self):
        ...


class CLIReader:
    def __call__(self, source) -> TextIO:
        with click.open_file(source) as data:
            return data.read()
