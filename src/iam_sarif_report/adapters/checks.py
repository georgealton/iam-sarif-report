from __future__ import annotations

import json
import sys

if sys.version_info >= (3, 8):
    from typing import Final, Protocol
else:
    from typing_extensions import Final, Protocol

import importlib.resources

from attr import define

CHECKS_DATA_FILE: Final[str] = "checks.json"


@define(frozen=True, slots=True)
class Check:
    id: str
    url: str
    name: str
    short_description: str
    description: str


class ChecksRepository(Protocol):
    def get(self, rule_id: str) -> Check | None:
        ...


class ChecksPackageDataRepository:
    def __init__(self) -> None:
        checks_fp = importlib.resources.open_text(
            __package__.partition(".")[0], CHECKS_DATA_FILE
        )
        self.data = json.load(checks_fp)

    def get(self, rule_id: str) -> Check | None:
        _check = self.data.get(rule_id)
        if _check:
            return Check(id=rule_id, **_check)
        return None
