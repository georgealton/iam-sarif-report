#!/bin/sh
result_path=$4
result=$4
function find_policies(){ find "$1" -type f -maxdepth 1; }
for policy in $(find_policies "$3"); do
    if [[ "$result_path" != "-" ]]; then
        mkdir -p "$result_path"
        result="$result_path/$(basename $policy).sarif"
    fi
    iam-policy-validator-to-sarif \
        --policy-type "$1" \
        --locale "$2" \
        -- \
        "$policy" \
        "$result"
done
