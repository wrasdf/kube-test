#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: bin/sh.sh <cluster env> <component>"
  exit 1
fi

cluster=$1
component=$2

docker-compose run --rm ntpl compile -p envs/base.yaml -p envs/${cluster}.yaml -c $component

# Get dns_name from ingress
dns_name=$(docker-compose run --rm yq r _build/$component/ingress.yaml spec.rules[0].host)
docker-compose build sh
docker-compose run --rm -e dns_name=$dns_name -e cluster=$cluster sh
