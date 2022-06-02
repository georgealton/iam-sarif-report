from __future__ import annotations

from enum import Enum, unique


class StrEnum(str, Enum):
    def __str__(self) -> str:
        return str.__str__(self)


@unique
class POLICY_TYPES(StrEnum):
    identity = "IDENTITY_POLICY"
    resource = "RESOURCE_POLICY"
    scp = "SERVICE_CONTROL_POLICY"


@unique
class LOCALES(StrEnum):
    de = "DE"
    en = "EN"
    es = "ES"
    fr = "FR"
    it = "IT"
    ja = "JA"
    ko = "KO"
    pt_br = "PT_BR"
    zh_cn = "ZH_CN"
    zh_tw = "ZH_TW"


@unique
class RESOURCE_TYPES(StrEnum):
    s3_bucket = "AWS::S3::Bucket"
    s3_access_point = "AWS::S3::AccessPoint"
    s3_multi_region_access_point = "AWS::S3::MultiRegionAccessPoint"
    s3_object_lambda_access_point = "AWS::S3ObjectLambda::AccessPoint"
