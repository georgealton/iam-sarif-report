from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import boto3.session

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

if TYPE_CHECKING:
    from typing import Iterable

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
    ):
        ...


class AWSAccessAnalyzerValidator:
    def __init__(self):
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
