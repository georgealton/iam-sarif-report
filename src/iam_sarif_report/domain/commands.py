from __future__ import annotations

import sys
from pathlib import Path

from attrs import frozen

if sys.version_info >= (3, 8):
    from typing import final
else:
    from typing_extensions import final

from .definitions import LOCALES, POLICY_TYPES, RESOURCE_TYPES, URI


class Command:
    ...


@final
@frozen(kw_only=True)
class GenerateFindingsAndReportSarif(Command):
    policy_locations: list[URI] | URI
    policy_type: POLICY_TYPES
    locale: LOCALES
    resource_type: RESOURCE_TYPES | None
    report: str | Path
