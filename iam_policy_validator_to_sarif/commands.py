from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from typing_extensions import final
from .definitions import POLICY_TYPES, LOCALES, RESOURCE_TYPES

@final
@dataclass(frozen=True)
class GenerateFindingsAndReportSarif:
    policy_path: Path
    policy_document: str
    policy_type: POLICY_TYPES
    locale: LOCALES
    resource_type: RESOURCE_TYPES
