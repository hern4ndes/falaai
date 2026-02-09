#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required. Install with: pip install uv" >&2
  exit 1
fi

uv sync
uv run alembic upgrade head
