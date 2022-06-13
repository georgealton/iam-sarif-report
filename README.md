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
      security-events: write
      actions: read
      contents: read
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # setup aws access
      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::111111111111:role/my-github-actions-role-test
          aws-region: eu-west-1

      # validate some policies, and get some SARIF back
      # the action creates .sarif file for each policy in the policies directory
      - uses: georgealton/iam-sarif-report@v1
        with:
          policies: policies/
          results: results

      # Public repositories / Organizations with GitHub Advanced Security
      # upload sarif files using CodeQL
      - uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results
```

### Locally

```sh
pipx run iam-sarif-report tests/data/policy_checks/policies/arn-region-not-allowed.json
```
