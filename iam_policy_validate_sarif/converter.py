from pathlib import Path
from typing import Iterable, List
import sarif_om as sarif
from mypy_boto3_accessanalyzer.type_defs import (
    SpanTypeDef,
    ValidatePolicyFindingTypeDef,
)

Finding = ValidatePolicyFindingTypeDef
Findings = Iterable[Finding]

schema = "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json"
version = "2.1.0"

iam_policy_validator_tool = sarif.Tool(
    driver=sarif.ToolComponent(
        name="ValidatePolicy",
        full_name="IAM Access Analyzer ValidatePolicy",
        information_uri="https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html",
    )
)


class SarifConverter:
    def __init__(self, policy_path: Path) -> None:
        self.policy_path = policy_path

    @staticmethod
    def to_sarif_level(finding: Finding) -> str:
        level_map = {
            "ERROR": "error",
            "SECURITY_WARNING": "warning",
            "SUGGESTION": "note",
            "WARNING": "warning",
        }
        return level_map.get(finding["findingType"], "none")

    @staticmethod
    def build_message_from_finding(finding: Finding) -> str:
        text = finding["findingDetails"]
        return sarif.Message(text=text)

    @staticmethod
    def span_to_region(span: SpanTypeDef) -> sarif.Region:
        start, end = span["start"], span["end"]
        return sarif.Region(
            start_line=start["line"],
            start_column=start["column"],
            end_line=end["line"],
            end_column=end["column"],
        )

    def convert(self, findings: Findings) -> sarif.SarifLog:
        results = self.findings_to_results(findings)
        run = sarif.Run(tool=iam_policy_validator_tool, results=results)
        return sarif.SarifLog(schema_uri=schema, version=version, runs=[run])

    def findings_to_results(self, findings: Findings) -> List[sarif.Run]:
        return [self.finding_to_result(finding) for finding in findings]

    def finding_location(self, finding: Finding) -> sarif.Location:
        uri = self.policy_path.name
        artifact_location = sarif.ArtifactLocation(uri=uri, uri_base_id="EXECUTIONROOT")
        region = SarifConverter.span_to_region(finding["locations"][0]["span"])
        physical_location = sarif.PhysicalLocation(
            artifact_location=artifact_location, region=region
        )
        return sarif.Location(physical_location=physical_location)

    def finding_to_result(self, finding: Finding) -> sarif.Result:
        level = SarifConverter.to_sarif_level(finding)
        message = SarifConverter.build_message_from_finding(finding)
        location = self.finding_location(finding)
        rule_id = finding["issueCode"]
        return sarif.Result(
            rule_id=rule_id, level=level, message=message, locations=[location]
        )
