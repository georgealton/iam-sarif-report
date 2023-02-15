# Contributing Guide

## Getting Started

### Setup Python

You'll need Python >= 3.9 installed
and pip >= 21.3 to

- support self resolving dependencies
- editable installs pyproject.toml

```console
$ python3 -m venv .venv
$ . .venv/bin/activate
$ python -m pip install --quiet --upgrade 'pip>=21.3'
$ python -m pip install --quiet --editable '.[dev]'
```

Then verify by running the tests

```console
$ pytest -qq
..                                   [100%]
```
