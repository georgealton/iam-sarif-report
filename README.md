# IAM Policy Validator To SARIF

[![Open in VSCode](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/georgealton/iam-policy-validator-to-sarif)
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

```yaml
on: [push]
jobs:
  example:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v1
      - uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: arn:aws:iam::111111111111:role/my-github-actions-role-test
          aws-region: eu-west-1
      - uses: georgealton/iam-policy-validator-to-sarif@v1
        with:
          policies: policies/
          results: results
      - uses: github/codeql-action/upload-sarif@v1
        with:
          sarif_file: results
```

### Locally

```sh
pipx run iam-policy-validator-to-sarif "policies/test-policy.json" "test-policy.sarif"
```
