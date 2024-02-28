from typing import Protocol

from click import open_file


class Reader(Protocol):
    def __call__(self, source: str) -> str:
        ...


class LocalFileReader:
    def __call__(self, source: str) -> str:
        with open_file(source) as data:
            return data.read()
