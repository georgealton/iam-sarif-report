from __future__ import annotations

from pathlib import Path

from attr import define

try:
    from typing import final
except ImportError:
    from typing_extensions import final

from .definitions import LOCALES, POLICY_TYPES, RESOURCE_TYPES


class Command:
    ...


@final
@define(frozen=True, kw_only=True)
class GenerateFindingsAndReportSarif(Command):
    policy_path: Path
    policy_document: str
    policy_type: POLICY_TYPES
    locale: LOCALES
    resource_type: RESOURCE_TYPES
    report: str
