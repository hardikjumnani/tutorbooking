#!/usr/bin/env bash
# Generate sustained load so the Horizontal Pod Autoscaler scales the backend up.
#
# Usage:
#   URL=http://tutorslot.local/api/appointments ./scripts/load-test.sh
#   DURATION=180 WORKERS=30 URL=... ./scripts/load-test.sh
set -euo pipefail

URL="${URL:-http://tutorslot.local/api/appointments}"
DURATION="${DURATION:-120}"   # how long to run, in seconds
WORKERS="${WORKERS:-20}"      # how many parallel request loops

echo "Hitting $URL with $WORKERS workers for ${DURATION}s..."
end=$((SECONDS + DURATION))
for _ in $(seq 1 "$WORKERS"); do
  (
    while [ "$SECONDS" -lt "$end" ]; do
      curl -s -o /dev/null "$URL" || true
    done
  ) &
done
wait
echo "Load test completed. Watch scaling with: kubectl get hpa -n tutorslot -w"
