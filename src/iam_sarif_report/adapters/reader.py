from typing import Protocol
from urllib.request import urlopen


class Reader(Protocol):
    def __call__(self, source: str) -> str:
        ...


class URLReader:
    def __call__(self, source: str) -> str:
        with urlopen(source) as data:
            return str(data.read().decode("utf-8"))
