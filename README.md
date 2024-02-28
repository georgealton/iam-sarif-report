# IAM SARIF Report

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Validate your IAM Policies and SCPs with AWS Policy Validator, and convert those results into SARIF documents for reporting.

## Use Me

To generate findings, iam-sarif-report makes AWS API requests. The AWS Principal you use must be allowed to use the `access-analyzer:ValidatePolicy` command.

```json
{
  "Effect": "Allow",
  "Action": "access-analyzer:ValidatePolicy",
  "Resource": "*"
}
```

### GitHub Action

See the [action.yaml](action.yaml) for detailed usage information.

```yaml
on: [push]
jobs:
  example:
    permissions:
      id-token: write
      security-events: write # When using GitHub Advanced Security
      actions: read
      contents: read
      checks: write # When using SARIF annotator
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # setup aws access
      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::111111111111:role/my-github-actions-role-test
          aws-region: eu-west-1

      # validate some policies and write a SARIF result file
      - uses: georgealton/iam-sarif-report@v2
        with:
          policies: policies/
          result: results/iam.sarif

      # Public repositories and Organizations with GitHub Advanced Security
      # can upload sarif files using CodeQL
      - uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results

      # Without GitHub Advanced Security use sarif-annotator
      - uses: SirYwell/sarif-annotator@v0.2.1
        with:
          report-path: results/iam.sarif
          source: qodana
```

### Locally

```sh
pipx run iam-sarif-report tests/data/policy_checks/policies/*
```
