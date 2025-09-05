#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8005}"

# Wait until the port is actually forwarded by Codespaces (appears quickly after attach)
# Try for ~20s
for i in {1..20}; do
  if gh codespace ports list -c "$CODESPACE_NAME" --json port,visibility | grep -q "\"port\": $PORT"; then
    break
  fi
  sleep 1
done

# Set visibility to public (org policy may block this)
gh codespace ports visibility "$PORT:public" -c "$CODESPACE_NAME" || {
  echo "Could not set port ${PORT} to public (policy may restrict)."
}