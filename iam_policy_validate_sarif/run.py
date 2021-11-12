from typing import TYPE_CHECKING

from . import converter, validator

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Callable

    from mypy_boto3_accessanalyzer.literals import LocaleType, PolicyTypeType


def validate_as_sarif(
    policy_location: "Path",
    policy_document: str,
    policy_type: "PolicyTypeType",
    locale: "LocaleType",
    result_writer: "Callable[[str], Any]",
) -> None:
    findings = validator.validate(
        locale=locale, policy_type=policy_type, policy=policy_document
    )
    converted = converter.SarifConverter(policy_location).convert(findings)
    result_writer(converted)
