import pathlib
import json
from iam_policy_validate_sarif import converter
import pytest

@pytest.mark.parametrize("policy", [("arn-region-not-allowed.policy.json"),("redundant-action.policy.json")])
def test_convertor(policy):
    policy_path = f"tests/data/policy_checks/{policy}"

    with open(f"{policy_path}.findings") as data:
        findings = json.load(data)['findings']

    sarif = converter.SarifConverter(pathlib.Path(policy))
    converted_sarif = json.loads(sarif.convert(findings))
    print(json.dumps(converted_sarif))

    with open(f"{policy_path}.findings.sarif") as data:
        expected_sarif = json.load(data)

    assert converted_sarif == expected_sarif
