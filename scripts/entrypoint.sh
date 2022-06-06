#!/bin/bash

policy_type=$1
locale=$2
policy_path=$3
result_path=$4
result=$4
resource_type=$5

function find_policies(){ find "$1" -type f -maxdepth 1 -print0; }

opts+=( "$policy_type" "$locale" )

if [[ -n "$resource_type" ]]; then
    opts+=( --resource-type "$resource_type" )
fi

while IFS= read -rd '' policy <&3; do
    if [[ "$result_path" != "-" ]]; then
        mkdir -p "$result_path"
        result=$result_path/$(basename "$policy").sarif
    fi
    iam-sarif-report ${opts[@]} -- "$policy" "$result"
done 3< <(find_policies "$policy_path")
