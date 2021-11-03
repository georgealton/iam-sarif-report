from . import validator
from . import converter


def validate_as_sarif(
    policy_location,
    policy_document,
    policy_type,
    locale,
    output_location,
):
    findings = validator.validate(
        policy_type=policy_type, locale=locale, policy=policy_document
    )
    converted = converter.SarifConverter(policy_path=policy_location).convert(findings)
    output_location.write(converted)
