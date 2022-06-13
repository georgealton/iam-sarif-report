import json
from pathlib import Path

import jsonschema
import pytest


@pytest.fixture(name="policy", params=("arn-region-not-allowed", "redundant-action"))
def _policy(request):
    base_path = Path("tests/data") / "policy_checks"

    policy_path = base_path / "policies" / f"{request.param}.json"
    findings_path = base_path / "findings" / f"{request.param}.json"
    sarif_path = base_path / "sarif" / f"{request.param}.sarif"

    sarif = json.loads(sarif_path.read_text())
    findings = json.loads(findings_path.read_text())["findings"]
    yield policy_path, findings, sarif


def test_converter(policy, sarif_schema, sarif_converter):
    policy_path, findings, expected_sarif = policy
    sarif = json.loads(sarif_converter([(policy_path, findings)]))
    assert sarif == expected_sarif
    jsonschema.validate(sarif, sarif_schema)
