#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/run_targets.sh [targets-file]
# Environment:
#   PYTHON - override python executable (default: python3)
#   NO_SUBFINDER=true to pass --no-subfinder to each run
#   ARTIFACT_DIR override (default: artifacts)

TARGETS_FILE="${1:-scans/targets.txt}"
PYTHON_CMD="${PYTHON:-python3}"
NO_SUBFINDER="${NO_SUBFINDER:-false}"
ARTIFACT_DIR="${ARTIFACT_DIR:-artifacts}"

if [ ! -f "$TARGETS_FILE" ]; then
  echo "Targets file not found: $TARGETS_FILE" >&2
  exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
  # trim
  line="$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
  [ -z "$line" ] && continue
  case "$line" in
    \#*) continue ;;
  esac
  echo "[targets] $line"
  if [ "$NO_SUBFINDER" = "true" ]; then
    "$PYTHON_CMD" blackRIFT.py --target "$line" --no-subfinder --artifact-dir "$ARTIFACT_DIR"
  else
    "$PYTHON_CMD" blackRIFT.py --target "$line" --artifact-dir "$ARTIFACT_DIR"
  fi
done < "$TARGETS_FILE"
