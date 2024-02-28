from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, Protocol

import boto3.session

if TYPE_CHECKING:
    from mypy_boto3_accessanalyzer.literals import (
        LocaleType,
        PolicyTypeType,
        ValidatePolicyResourceTypeType,
    )
    from mypy_boto3_accessanalyzer.type_defs import (
        ValidatePolicyFindingTypeDef,
        ValidatePolicyRequestRequestTypeDef,
    )


class Validator(Protocol):
    def __call__(
        self,
        locale: LocaleType,
        policy_type: PolicyTypeType,
        resource_type: ValidatePolicyResourceTypeType | None,
        policy: str,
    ) -> Iterable[ValidatePolicyFindingTypeDef]:
        ...


class AWSAccessAnalyzerValidator:
    def __init__(self) -> None:
        self.session = boto3.session.Session()

    def __call__(
        self,
        locale: LocaleType,
        policy_type: PolicyTypeType,
        resource_type: ValidatePolicyResourceTypeType | None,
        policy: str,
    ) -> Iterable[ValidatePolicyFindingTypeDef]:
        client = self.session.client("accessanalyzer")
        paginator = client.get_paginator("validate_policy")
        opts: ValidatePolicyRequestRequestTypeDef = {
            "locale": locale,
            "policyDocument": policy,
            "policyType": policy_type,
        }
        if resource_type:
            opts["validatePolicyResourceType"] = resource_type

        pages = paginator.paginate(**opts)

        for page in pages:
            yield from page["findings"]
