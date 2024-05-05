#!/bin/bash

# export lambda layer & chromium layer to ./layers folder
# Params:
#   1: requirement file path
# eg:
# $ ./scripts/export_python_layer.sh /path/to/requirements.txt
export DOCKER_DEFAULT_PLATFORM=linux/amd64

BASE_DIR=$(cd $(dirname $(dirname "$0")); pwd)
TMP_DIR="${BASE_DIR}/tmp"
PYTHON_VERSION=${1:-python312}
REQUIREMENTS_FILE=${2:-requirements.txt}

# copy requirements file to tmp folder
mkdir -p "$TMP_DIR"
cp -f "$REQUIREMENTS_FILE" "${TMP_DIR}/requirements.txt"

set -o errexit
set -o nounset
set -o pipefail

echo ------------------------------
echo "Building lambda-python-layer ..."
docker build . -f "compose/lambda/python-layers/${PYTHON_VERSION}.Dockerfile" -t lambda-python-layer:latest
CONTAINER_ID=$(docker run -d lambda-python-layer)
docker cp "$CONTAINER_ID:/layers/" "$TMP_DIR"
docker rm -f "$CONTAINER_ID"

echo ------------------------------
echo "Layer exported"
tree tmp/layers
du -sh tmp/layers/*
