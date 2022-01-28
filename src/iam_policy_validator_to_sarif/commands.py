from __future__ import annotations

from attr import define
from pathlib import Path
from typing_extensions import final
from .definitions import POLICY_TYPES, LOCALES, RESOURCE_TYPES


class Command:
    ...


@final
@define(frozen=True)
class GenerateFindingsAndReportSarif(Command):
    policy_path: Path
    policy_document: str
    policy_type: POLICY_TYPES
    locale: LOCALES
    resource_type: RESOURCE_TYPES
    report: str
