import pathlib
import json
from iam_policy_validate_sarif import converter

finding = {
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
}
def test_findings_to_results():
    assert converter.findingsToResults([]) == []
    assert converter.findingsToResults([finding]) == []

def test_finding_to_result():
    assert converter.findingToResult(finding) == 0


def test_span_to_region():
    span = {
        "end": {"column": 32, "line": 83, "offset": 2574},
        "start": {"column": 8, "line": 83, "offset": 2550},
    }
    assert converter.spanToRegion(span) == 0

def test_to_sarif_level():
    converter.SarifConverter.to_sarif_level()


def test_convertor():
    policy = 'redundant-action'
    policy = f"tests/data/{policy}.policy.json"
    with open(f"{policy}.findings") as data:
        findings = json.load(data)['findings']

    converted_sarif = json.loads(converter.SarifConverter(pathlib.Path(policy)).convert(findings))
    print(json.dumps(converted_sarif))

    with open(f"{policy}.findings.sarif") as data:
        expected_sarif = json.load(data)

    assert converted_sarif == expected_sarif
