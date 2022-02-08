import json
from pathlib import Path

import jsonschema
import pytest

from iam_policy_validator_to_sarif import checks, converter


@pytest.mark.parametrize(
    "policy",
    [
        ("arn-region-not-allowed"),
        ("redundant-action"),
    ],
)
def test_convertor(policy):
    schema_path = Path("tests/data/sarif-schema-2.1.0.json")
    base_path = Path("tests/data/policy_checks")
    policy_path = Path(base_path, "policies/", f"{policy}.json")
    findings_path = Path(base_path, "findings/", f"{policy}.json")
    sarif_path = Path(base_path, "sarif/", f"{policy}.sarif")

    sarif_schema = json.loads(schema_path.read_text())
    findings = json.loads(findings_path.read_text())["findings"]
    expected_sarif = json.loads(sarif_path.read_text())

    sarif_converter = converter.SarifConverter(checks.ChecksPackageDataRepository())
    sarif = json.loads(sarif_converter(policy_path, findings))
    print(json.dumps(sarif))

    assert sarif == expected_sarif
    jsonschema.validate(sarif, sarif_schema)
