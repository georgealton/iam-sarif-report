import pathlib
import json
from iam_policy_validate_sarif import converter

def test_convertor():
    policy = 'arn-region-not-allowed'
    policy = f"tests/data/{policy}.policy.json"

    with open(f"{policy}.findings") as data:
        findings = json.load(data)['findings']

    sarif = converter.SarifConverter(pathlib.Path(policy))
    converted_sarif = json.loads(sarif.convert(findings))
    print(json.dumps(converted_sarif))

    with open(f"{policy}.findings.sarif") as data:
        expected_sarif = json.load(data)

    assert converted_sarif == expected_sarif
