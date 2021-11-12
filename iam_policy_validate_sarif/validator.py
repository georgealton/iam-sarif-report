from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from typing import Iterable

    from mypy_boto3_accessanalyzer.literals import LocaleType, PolicyTypeType
    from mypy_boto3_accessanalyzer.type_defs import ValidatePolicyFindingTypeDef


def validate(
    locale: LocaleType, policy: str, policy_type: PolicyTypeType
) -> "Iterable[ValidatePolicyFindingTypeDef]":
    client = boto3.client("accessanalyzer")
    paginator = client.get_paginator("validate_policy")
    pages = paginator.paginate(
        locale=locale, policyDocument=policy, policyType=policy_type
    )
    for page in pages:
        yield from page["findings"]
