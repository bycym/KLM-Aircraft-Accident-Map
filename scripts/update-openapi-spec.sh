#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -gt 0 ]]; then
  changed_backend_files="$(printf '%s\n' "$@")"
else
  changed_backend_files="$(git diff --cached --name-only --diff-filter=ACMR)"
fi

changed_backend_files="$(
  printf '%s\n' "${changed_backend_files}" \
    | grep '^backend/' \
    | grep -v '^backend/openapi-gateway\.json$' \
    || true
)"

if [[ -z "${changed_backend_files}" ]]; then
  exit 0
fi

backend_url="${OPENAPI_BACKEND_URL:-https://backend.example.com}"

(
  cd backend
  PYTHONPATH=src poetry run python -m safety_backend.openapi \
    --backend-url "${backend_url}" \
    --output openapi-gateway.json
)

git add backend/openapi-gateway.json
