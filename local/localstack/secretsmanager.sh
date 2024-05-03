#!/usr/bin/env bash

set -euo pipefail

# enable debug
# set -x

echo "configuring secretsmanager"
echo "==================="
AWS_REGION=us-east-1

# https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/create-secret.html
create_secret() {
    local NAME=$1
    local VALUE=$2
    awslocal secretsmanager create-secret \
        --name "$NAME" \
        --secret-string "$VALUE" \
        --region "$AWS_REGION"
}

create_secret cli/local/secrets '{"foo": "bar"}'
