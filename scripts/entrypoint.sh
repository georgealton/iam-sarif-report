#!/bin/sh
function find_policies(){ find $1 -type f -maxdepth 1; }
for policy in $(find_policies "$3"); do
    result=$4/$(basename "$policy").sarif
    iam-policy-validator-to-sarif \
        --policy-type "$1" \
        --locale "$2" \
        "$policy"
done
