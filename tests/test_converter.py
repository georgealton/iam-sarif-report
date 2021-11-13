import json
from pathlib import Path

import jsonschema
import pytest

from iam_policy_validate_sarif import converter


@pytest.mark.parametrize(
    "policy",
    [
        ("arn-region-not-allowed"),
        ("redundant-action"),
    ],
)
def test_convertor(policy):
    base_path = Path("tests/data/policy_checks")
    policy_path = Path(base_path, "policies/", f"{policy}.json")
    findings_path = Path(base_path, "findings/", f"{policy}.json")
    sarif_path = Path(base_path, "sarif/", f"{policy}.sarif")

    with open("tests/data/sarif-schema-2.1.0.json") as schema_file:
        schema = json.load(schema_file)
    with open(findings_path) as data:
        findings = json.load(data)["findings"]
    with open(sarif_path) as data:
        expected_sarif = json.load(data)

    sarif_converter = converter.SarifConverter(policy_path)
    sarif = json.loads(sarif_converter.convert(findings))
    print(json.dumps(sarif))


    assert sarif == expected_sarif
    jsonschema.validate(sarif, schema)
