from . import validator
from . import converter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import TextIO
    from mypy_boto3_accessanalyzer.literals import LocaleType, PolicyTypeType


def validate_as_sarif(
    policy_location: str,
    policy_document: str,
    policy_type: PolicyTypeType,
    locale: LocaleType,
    output_location: TextIO,
) -> None:
    findings = validator.validate(
        policy_type=policy_type, locale=locale, policy=policy_document
    )
    converted = converter.SarifConverter(policy_path=policy_location).convert(findings)
    output_location.write(converted)
