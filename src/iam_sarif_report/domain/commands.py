from __future__ import annotations

from pathlib import Path
from typing import final

from attrs import frozen

from .definitions import LOCALES, POLICY_TYPES, RESOURCE_TYPES


class Command:
    ...


@final
@frozen(kw_only=True)
class GenerateFindingsAndReportSarif(Command):
    policy_locations: list[str] | str
    policy_type: POLICY_TYPES
    locale: LOCALES
    resource_type: RESOURCE_TYPES | None
    report: str | Path
