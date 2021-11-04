#!/bin/bash

find 'tests/data' \
    -name '*.policy.json' \
    -type f \
    -exec sh -c 'aws accessanalyzer validate-policy --policy-document file://{} --policy-type IDENTITY_POLICY > {}.findings' \;
