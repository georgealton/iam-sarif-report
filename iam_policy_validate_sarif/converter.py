from pathlib import Path
from typing import Iterable, List
import sarif_om as sarif
from mypy_boto3_accessanalyzer.type_defs import (
    SpanTypeDef,
    ValidatePolicyFindingTypeDef,
    LocationTypeDef,
)
from jschema_to_python.to_json import to_json
import itertools
import json

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

with open("checks.json") as f:
    checks = json.load(f)


class SarifConverter:
    def __init__(self, policy_path: Path) -> None:
        self.policy_path = policy_path

    @staticmethod
    def to_rule_id(finding: Finding) -> str:
        return "_".join(
            [
                "_".join(finding["findingType"].lower().split()),
                "_".join(finding["issueCode"].lower().split()),
            ]
        )

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
    def build_message_from_finding(finding: Finding) -> sarif.Message:
        details, moreInfo = finding["findingDetails"], finding["learnMoreLink"]
        text_fmt = "{0} - {1}"
        return sarif.Message(text=text_fmt, arguments=[details, moreInfo])

    @staticmethod
    def span_to_region(span: SpanTypeDef) -> sarif.Region:
        start, end = span["start"], span["end"]
        return sarif.Region(
            start_line=start["line"],
            start_column=start["column"] + 1,
            end_line=end["line"],
            end_column=end["column"] + 1,
        )

    def convert(self, findings: Findings) -> sarif.SarifLog:
        """Converts Findings to a SARIF Log

        :param findings: [description]
        :return: [description]
        """
        results = list(self.findings_to_results(findings))
        matched_rules = set(result.rule_id for result in results if result.rule_id)
        rules = [
            sarif.ReportingDescriptor(
                id=rule_id,
                name=checks.get(rule_id).get("name"),
                help_uri=checks.get(rule_id).get("url"),
                full_description=sarif.MultiformatMessageString(text=checks.get(rule_id).get("description")),
            )
            for rule_id in matched_rules
        ]
        iam_policy_validator_tool.driver.rules = rules
        run = sarif.Run(tool=iam_policy_validator_tool, results=results)
        return to_json(sarif.SarifLog(schema_uri=schema, version=version, runs=[run]))

    def findings_to_results(self, findings: Findings) -> Iterable[sarif.Result]:
        return itertools.chain.from_iterable(
            self.finding_to_results(finding) for finding in findings
        )

    def finding_location(self, location: LocationTypeDef) -> sarif.Location:
        """[summary]

        :param location: [description]
        :return: [description]
        """
        uri = self.policy_path.name
        artifact_location = sarif.ArtifactLocation(uri=uri, uri_base_id="EXECUTIONROOT")
        region = SarifConverter.span_to_region(location["span"])
        physical_location = sarif.PhysicalLocation(
            artifact_location=artifact_location, region=region
        )
        return sarif.Location(physical_location=physical_location)

    def finding_to_results(self, finding: Finding) -> Iterable[sarif.Result]:
        """Generates SARIF Results from a Finding

        Produces multiple Results when we have more than 1 Location in Finding. SARIF Results
        should only have multiple locations when **every** location needs changing. Findings with
        issueCode REDUNDANT_ACTION may only need correct in 1 location to resolve.

        https://docs.oasis-open.org/sarif/sarif/v2.1.0/csprd01/sarif-v2.1.0-csprd01.html#_Toc10541088

        :param finding: [description]
        :return: [description]]
        """
        for location in finding["locations"]:
            level = SarifConverter.to_sarif_level(finding)
            message = SarifConverter.build_message_from_finding(finding)
            location = self.finding_location(location)
            rule_id = SarifConverter.to_rule_id(finding)
            yield sarif.Result(
                rule_id=rule_id, level=level, message=message, locations=[location]
            )
