import json
from types import MappingProxyType
from typing import TYPE_CHECKING
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

import pkg_resources
import sarif_om as sarif
from jschema_to_python.to_json import to_json

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Iterable, Optional

    from mypy_boto3_accessanalyzer.type_defs import (
        LocationTypeDef,
        SpanTypeDef,
        ValidatePolicyFindingTypeDef,
    )

    Finding = ValidatePolicyFindingTypeDef
    Findings = Iterable[Finding]

schema = "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json"
version = "2.1.0"

iam_policy_validator_tool = sarif.Tool(
    driver=sarif.ToolComponent(
        name="IAM Policy Validator",
        full_name="IAM Access Analyzer Policy Validator",
        information_uri="https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html",
    )
)

checks_fp = pkg_resources.resource_stream(__name__, "checks.json")
checks = json.load(checks_fp)

level_map = MappingProxyType(
    {
        "ERROR": "error",
        "SECURITY_WARNING": "warning",
        "SUGGESTION": "note",
        "WARNING": "warning",
    }
)


class Converter(Protocol):
    def __call__(self, policy_path: "Path", findings: "Findings") -> "sarif.SarifLog":
        ...


class SarifConverter(Converter):
    def __init__(self):
        self.policy_path: Optional[Path] = None

    @staticmethod
    def to_rule_id(finding: "Finding") -> str:
        return "_".join(
            [
                "_".join(finding["findingType"].lower().split()),
                "_".join(finding["issueCode"].lower().split()),
            ]
        )

    @staticmethod
    def to_sarif_level(finding: "Finding") -> str:
        return level_map.get(finding["findingType"], "none")

    @staticmethod
    def to_message(finding: "Finding") -> "sarif.Message":
        return sarif.Message(text=finding["findingDetails"])

    @staticmethod
    def to_region(span: "SpanTypeDef") -> "sarif.Region":
        start, end = span["start"], span["end"]
        return sarif.Region(
            start_line=start["line"],
            start_column=start["column"] + 1,
            end_line=end["line"],
            end_column=end["column"] + 1,
        )

    def __call__(self, policy_path: "Path", findings: "Findings") -> "sarif.SarifLog":
        self.policy_path = policy_path
        results = list(self.findings_to_results(findings))
        iam_policy_validator_tool.driver.rules = list(self.get_rules(results))
        run = sarif.Run(tool=iam_policy_validator_tool, results=results)
        return to_json(sarif.SarifLog(schema_uri=schema, version=version, runs=[run]))

    def get_rules(
        self, results: "Iterable[sarif.Result]"
    ) -> "Iterable[sarif.ReportingDescriptor]":
        matched_rules = set(result.rule_id for result in results if result.rule_id)
        for rule_id in matched_rules:
            check = checks.get(rule_id)
            if check:
                yield sarif.ReportingDescriptor(
                    id=rule_id,
                    name=check.get("name"),
                    help=sarif.MultiformatMessageString(
                        text=check.get("short_description"),
                        markdown=check.get("short_description"),
                    ),
                    help_uri=check.get("url"),
                    short_description=sarif.MultiformatMessageString(
                        text=check.get("short_description"),
                        markdown=check.get("short_description"),
                    ),
                    full_description=sarif.MultiformatMessageString(
                        text=check.get("description"),
                        markdown=check.get("description"),
                    ),
                )

    def findings_to_results(self, findings: "Findings") -> "Iterable[sarif.Result]":
        for finding in findings:
            yield from self.to_results(finding)

    def to_location(self, location: "LocationTypeDef") -> "sarif.Location":
        return sarif.Location(
            physical_location=sarif.PhysicalLocation(
                artifact_location=sarif.ArtifactLocation(
                    uri=self.policy_path, uri_base_id="EXECUTIONROOT"
                ),
                region=SarifConverter.to_region(location["span"]),
            )
        )

    def to_results(self, finding: "Finding") -> "Iterable[sarif.Result]":
        for location in finding["locations"]:
            yield sarif.Result(
                rule_id=SarifConverter.to_rule_id(finding),
                level=SarifConverter.to_sarif_level(finding),
                message=SarifConverter.to_message(finding),
                locations=[self.to_location(location)],
                related_locations=list(self.to_related_locations(finding, location))
                or None,
            )

    def to_related_locations(
        self, finding: "Finding", current_location: "LocationTypeDef"
    ) -> "Iterable[sarif.Location]":
        for related_location in finding["locations"]:
            if related_location != current_location:
                yield self.to_location(related_location)
