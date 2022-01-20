from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Callable, final

from . import commands

if TYPE_CHECKING:
    from .converter import Converter
    from .validator import Validator
    from sarif_om import SarifLog
    from typing import Optional

    from mypy_boto3_accessanalyzer.literals import (
        LocaleType,
        PolicyTypeType,
        ValidatePolicyResourceTypeType,
    )

@final
@dataclass(frozen=True)
class GenerateFindingsAndReportSarif:
    validator: Validator
    converter: Converter
    reporter: Callable[]

    def __call__(self,
        policy_document: str,
        policy_type: "PolicyTypeType",
        resource_type: "Optional[ValidatePolicyResourceTypeType]",
        locale: "LocaleType",
    ) -> "SarifLog":
        findings = self.validator(
            locale=locale,
            policy_type=policy_type,
            policy=policy_document,
            resource_type=resource_type,
        )
        results = self.converter(findings)
        self.reporter(results)

COMMAND_HANDLERS = MappingProxyType({
    commands.GenerateFindingsAndReportSarif: GenerateFindingsAndReportSarif
})
