from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from typing import Iterable, Optional

    from mypy_boto3_accessanalyzer.literals import (
        LocaleType,
        PolicyTypeType,
        ValidatePolicyResourceTypeType,
    )
    from mypy_boto3_accessanalyzer.type_defs import ValidatePolicyFindingTypeDef


def validate(
    locale: "LocaleType",
    policy_type: "PolicyTypeType",
    resource_type: "Optional[ValidatePolicyResourceTypeType]",
    policy: str,
) -> "Iterable[ValidatePolicyFindingTypeDef]":
    client = boto3.client("accessanalyzer")
    paginator = client.get_paginator("validate_policy")
    opts = {
        "locale": locale,
        "policyDocument": policy,
        "policyType": policy_type,
    }
    if resource_type:
        opts["resource_type"] = resource_type
    pages = paginator.paginate(**opts)
    for page in pages:
        yield from page["findings"]
