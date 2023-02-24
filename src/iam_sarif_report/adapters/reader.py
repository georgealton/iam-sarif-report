import sys
from urllib.request import urlopen

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol


class Reader(Protocol):
    def __call__(self, source: str) -> str:
        ...


class URLReader:
    def __call__(self, source: str) -> str:
        with urlopen(source) as data:
            return str(data.read().decode("utf-8"))
