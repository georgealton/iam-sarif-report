# IAM SARIF Report

[![Open in VSCode](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/georgealton/iam-sarif-report)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Validate your IAM Policies and SCPs for best practice, and convert those results into SARIF documents for reporting.

## Use Me

To generate findings, we've got to make API requests to AWS. The AWS Principal you use must be allowed to use the access-analyzer service ValidatePolicy action.

```json
{
  "Effect": "Allow",
  "Action": "access-analyzer:ValidatePolicy",
  "Resource": "*"
}
```

### GitHub Action

See the [action.yaml](action.yaml) for more detailed usage information.

```yaml
on: [push]
jobs:
  example:
    runs-on: ubuntu-latest
    steps:
      # checkout your code
      - uses: actions/checkout@v1
      # setup aws access
      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::111111111111:role/my-github-actions-role-test
          aws-region: eu-west-1
      # validate some policies!
      - uses: georgealton/iam-sarif-report@v0.0.1
        with:
          policies: policies/
          results: results
      # upload results
      - uses: github/codeql-action/upload-sarif@v1
        with:
          sarif_file: results
```

### Locally

```sh
pipx run \
  --spec git+https://github.com/georgealton/iam-sarif-report.git@main \
  iam-sarif-report \
  tests/data/policy_checks/policies/arn-region-not-allowed.json
```
