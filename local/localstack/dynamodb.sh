#!/usr/bin/env bash

set -euo pipefail

echo "configuring dynamodb table"
echo "==================="

AWS_REGION=us-east-1

# https://docs.aws.amazon.com/cli/latest/reference/dynamodb/create-table.html
awslocal dynamodb create-table \
  --table-name cli-local \
  --billing-mode PAY_PER_REQUEST \
  --key-schema AttributeName=PK,KeyType=HASH AttributeName=SK,KeyType=RANGE \
  --attribute-definitions AttributeName=PK,AttributeType=S AttributeName=SK,AttributeType=S \
  --region "$AWS_REGION"
