#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: bin/deploy.sh <cluster env> <component>"
  exit 1
fi

cluster=$1
component=$2

docker-compose run --rm ntpl compile -p envs/base.yaml -p envs/${cluster}.yaml -c $component
