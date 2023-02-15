from typing import TextIO

from urllib.request import urlopen


class Reader:
    def __call__(self, source):
        ...


class URLReader:
    def __call__(self, source) -> TextIO:
        with urlopen(source) as data:
            return data.read().decode("utf-8")
