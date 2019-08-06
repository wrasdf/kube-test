#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: bin/e2e_test.sh <cluster env> <component> <dns_name>"
  exit 1
fi

cluster=$1
component=$2
dns_name=$3

./bin/compile.sh $cluster $component
docker-compose build pytest
docker-compose run --rm -e dns_name=$dns_name -e cluster=$cluster pytest
