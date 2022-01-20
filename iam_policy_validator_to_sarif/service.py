from dataclasses import dataclass
from typing import TYPE_CHECKING

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

@dataclass(frozen=True)
class GenerateFindingsAndConvertToSarif:
    validator: Validator
    converter: Converter

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
        return results
