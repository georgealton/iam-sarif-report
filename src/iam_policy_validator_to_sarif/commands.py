from __future__ import annotations

from pathlib import Path
import sys

from attr import define

if sys.version_info >= (3, 8):
    from typing import final
else:
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
