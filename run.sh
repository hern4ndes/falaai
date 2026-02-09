#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$script_dir/docker"
exec docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
