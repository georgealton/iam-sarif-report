#!/bin/bash

policy_type=$1
locale=$2
policy_path=$3
result_path=$4
resource_type=$5

function find_policies() { find "$1" -type f -maxdepth 1; }

opts+=("$policy_type" "$locale" "$result_path")

if [[ -n "$resource_type" ]]; then
    opts+=(--resource-type "$resource_type")
fi

iam-sarif-report ${opts[@]} -- $(find_policies "$policy_path")
