#!/bin/bash -eu
set -o pipefail

rm -f "$1"

for s in molecule/*
do
  docker volume prune -f
  docker system prune -af
  /usr/bin/time -f "$s %e" -ao "$1" make "$s"
done
