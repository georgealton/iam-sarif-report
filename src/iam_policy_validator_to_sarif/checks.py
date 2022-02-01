from __future__ import annotations

import json
from typing import Optional

try:
    from typing import Final, Protocol
except ImportError:
    from typing_extensions import Protocol, Final

import pkg_resources
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
    def get(self, rule_id: str) -> Optional[Check]:
        ...


class ChecksPackageDataRepository:
    def __init__(self) -> None:
        checks_fp = pkg_resources.resource_stream(__name__, CHECKS_DATA_FILE)
        self.data = json.load(checks_fp)

    def get(self, rule_id: str) -> Optional[Check]:
        _check = self.data.get(rule_id)
        if _check:
            return Check(id=rule_id, **_check)
        return None
