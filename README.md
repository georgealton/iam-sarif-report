# IAM Policy Validator To Sarif

[![Open in VSCode](https://open.vscode.dev/badges/open-in-vscode.svg)](https://open.vscode.dev/georgealton/iam-policy-validator-to-sarif)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

When you've got IAM Policies and you want to report on Policy issues.

Converts IAM Policy Validator Findings to SARIF.

SARIF (Static Analysis Results Interchange Format)

The motivation for this was to report SARIF results to GitHub

## Use Me

To generate Findings, we've got to make API requests to AWS. The AWS Principal must be allowed to perform

- **iam:ValidatePolicy**

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
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
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
pipx run iam-policy-validator-to-sarif "policies/test-policy.json" "results/test-policy.sarif"
```
