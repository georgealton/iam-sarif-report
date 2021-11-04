from pathlib import Path
from typing import List
import sarif_om as sarif
from mypy_boto3_accessanalyzer.type_defs import (
    SpanTypeDef,
    ValidatePolicyFindingTypeDef,
)

Finding = ValidatePolicyFindingTypeDef
Findings = List[Finding]


class SarifConverter:
    def to_sarif_level(self, finding: Finding) -> str:
        level_map = {
            "ERROR": "error",
            "SECURITY_WARNING": "warning",
            "SUGGESTION": "note",
            "WARNING": "warning",
        }
        return level_map.get(finding["findingType"], "none")

    def build_message_from_finding(self, finding: Finding) -> str:
        text = finding["findingDetails"]
        return sarif.Message(text=text)

    def __init__(self, policy_path) -> None:
        self.policy_path = policy_path

    def convert(self, findings: Findings) -> sarif.SarifLog:
        tool_name = "ValidatePolicy"
        tool_full_name = "IAM Access Analyzer ValidatePolicy"
        tool_info_uri = "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html"
        schema = "https://docs.oasis-open.org/sarif/sarif/v2.1.0/cos02/schemas/sarif-schema-2.1.0.json"
        version = "2.1.0"
        driver = sarif.ToolComponent(
            name=tool_name, full_name=tool_full_name, information_uri=tool_info_uri
        )
        tool = sarif.Tool(driver=driver)
        results = self.findings_to_results(findings)
        run = sarif.Run(tool=tool, results=results)
        log = sarif.SarifLog(schema_uri=schema, version=version, runs=[run])
        return log

    def findings_to_results(self, findings: Findings) -> List[sarif.Run]:
        return [self.finding_to_result(finding) for finding in findings]

    def finding_location(self, policy_path: Path, finding: Finding) -> sarif.Location:
        uri = policy_path.name
        artifact_location = sarif.ArtifactLocation(uri=uri, uri_base_id="EXECUTIONROOT")
        region = self.span_to_region(finding["locations"][0]["span"])
        physical_location = sarif.PhysicalLocation(
            artifact_location=artifact_location, region=region
        )
        return sarif.Location(physical_location=physical_location)

    def span_to_region(self, span: SpanTypeDef) -> sarif.Region:
        start, end = span["start"], span["end"]
        return sarif.Region(
            start_line=start["line"],
            start_column=start["column"],
            end_line=end["line"],
            end_column=end["column"],
        )

    def finding_to_result(self, finding: Finding) -> sarif.Result:
        level = self.to_sarif_level(finding)
        message = self.build_message_from_finding(finding)
        location = self.finding_location(Path(self.policy_path), finding)
        rule_id = finding["issueCode"]
        return sarif.Result(
            rule_id=rule_id, level=level, message=message, locations=[location]
        )
