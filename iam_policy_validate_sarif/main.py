# import boto3
from mypy_boto3_accessanalyzer.type_defs import ValidatePolicyResponseTypeDef
import json
from jschema_to_python.to_json import to_json
from . import converter


def load_findings(path: str) -> ValidatePolicyResponseTypeDef:
    with open(path) as f:
        return json.load(f)


def main(findings):
    converter = converter.SarifConverter('')
    log = converter.convert()
    return to_json(log)
