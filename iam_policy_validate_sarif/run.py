from typing import TYPE_CHECKING

from . import converter, validator

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, Callable, Optional

    from mypy_boto3_accessanalyzer.literals import (
        LocaleType,
        PolicyTypeType,
        ValidatePolicyResourceTypeType,
    )


def validate_as_sarif(
    policy_location: "Path",
    policy_document: str,
    policy_type: "PolicyTypeType",
    resource_type: "Optional[ValidatePolicyResourceTypeType]",
    locale: "LocaleType",
    result_writer: "Callable[[str], None]",
) -> None:
    findings = validator.validate(
        locale=locale,
        policy_type=policy_type,
        policy=policy_document,
        resource_type=resource_type,
    )
    converted = converter.SarifConverter(policy_location).convert(findings)
    result_writer(converted)
