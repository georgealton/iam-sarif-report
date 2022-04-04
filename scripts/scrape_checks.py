#!/usr/bin/env python3
import json
import re

import html2text
import requests
from bs4 import BeautifulSoup

checks_path = "../src/iam_sarif_report/checks.json"
check_reference = "https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html"
html = requests.get(check_reference).text
reference = BeautifulSoup(html, "html.parser")
id_prefix = "access-analyzer-reference-policy-checks-"

id_prefix_match = re.compile(f"{id_prefix}.*")
checks = reference.find_all(id=id_prefix_match)

finding_type_name_pattern = re.compile(
    r"([a-zA-Z-]*(?:suggestion|error|warning))-([a-zA-Z-]*)"
)


def paragraph_matches_resolving(node) -> bool:
    return node.name == "p" and node.b and node.b.contents[0].startswith("Resolving")


def finding_description_finished(node) -> bool:
    return (
        getattr(node, "attrs", {})
        .get("id", "")
        .startswith("access-analyzer-reference-policy-checks")
    ) or not sib.nextSibling


rules = {}
for check in checks:
    result = finding_type_name_pattern.match(check.attrs["id"])
    if not result:
        continue
    finding_type, finding_name = result.groups()
    rule_id = check.attrs["id"].split(id_prefix)[1]
    rule_id = re.sub("-", "_", rule_id)
    rules[rule_id] = {
        "url": f'{check_reference}#{check.attrs["id"]}',
        "name": re.sub("-", "", finding_name.title()),
    }
    desc = ""
    capture = False
    for sib in check.next_siblings:
        if finding_description_finished(sib):
            capture = False
            full_description = html2text.html2text(desc).strip()
            short_description = full_description.split("\n\n")[0]
            rules[rule_id]["short_description"] = short_description
            rules[rule_id]["description"] = html2text.html2text(desc).strip()
            break
        elif paragraph_matches_resolving(sib):
            capture = True
            continue

        if capture:
            desc += str(sib)


with open(checks_path, "w") as checks:
    json.dump(rules, checks, indent=2)
    print(file=checks)
