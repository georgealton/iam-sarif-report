from iam_policy_validate_sarif import main

findings = [{
    "findingDetails": "The action sqs:DeleteMessageBatch does not exist.",
    "findingType": "ERROR",
    "issueCode": "INVALID_ACTION",
    "learnMoreLink": "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html#access-analyzer-reference-policy-checks-error-invalid-action",
    "locations": [
        {
            "path": [
                {"value": "Statement"},
                {"index": 0},
                {"value": "Action"},
                {"index": 77},
            ],
            "span": {
                "end": {"column": 32, "line": 83, "offset": 2574},
                "start": {"column": 8, "line": 83, "offset": 2550},
            },
        }
    ],
}]

def test_main():
    assert main.main(findings) == 1
