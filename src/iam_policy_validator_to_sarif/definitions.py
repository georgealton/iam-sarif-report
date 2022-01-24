from enum import unique, Enum


@unique
class POLICY_TYPES(str, Enum):
    identity = "IDENTITY_POLICY"
    resource = "RESOURCE_POLICY"
    scp = "SERVICE_CONTROL_POLICY"


@unique
class LOCALES(str, Enum):
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
class RESOURCE_TYPES(str, Enum):
    s3_bucket = "AWS::S3::Bucket"
    s3_access_point = "AWS::S3::AccessPoint"
    s3_multi_region_acess_point = "AWS::S3::MultiRegionAccessPoint"
    s3_object_lambda_access_point = "AWS::S3ObjectLambda::AccessPoint"