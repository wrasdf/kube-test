#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: bin/e2e_test.sh <cluster env> <component>"
  exit 1
fi

cluster=$1
component=$2

./bin/compile.sh $cluster $component
docker-compose build pytest
docker-compose run --rm pytest
