import boto3


def validate(locale, policy, policy_type):
    client = boto3.client("accessanalyzer")
    paginator = client.get_paginator("validate_policy")
    pages = paginator.paginate(
        locale=locale, policyDocument=policy, policyType=policy_type
    )
    for page in pages:
        yield from page["findings"]
