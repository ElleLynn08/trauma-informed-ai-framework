#!/usr/bin/env bash
#
# Run all Jupyter notebooks in NB_DIR, in alphanumeric order.
# - Skips files that start with "_" (e.g., _template.ipynb).
# - Executes IN PLACE (outputs stay in the .ipynb).
# - Writes per-notebook logs into LOG_DIR.
# - TIMEOUT (seconds) and NB_DIR are configurable via env vars:
#     NB_DIR=notebooks TIMEOUT=900 bash scripts/run_all_notebooks.sh
#
# Exit code: non-zero if any notebook failed (so CI can catch failures).
# If you want to *continue* running all notebooks despite failures (default),
# this script already does that— it just summarizes and returns non-zero at end.

set -euo pipefail

NB_DIR="${NB_DIR:-notebooks}"
TIMEOUT="${TIMEOUT:-600}"
LOG_DIR="${LOG_DIR:-logs/notebook_runs}"

mkdir -p "$LOG_DIR"

if [[ ! -d "$NB_DIR" ]]; then
  echo "Notebook directory '$NB_DIR' not found."
  exit 1
fi

# Collect .ipynb files (may be empty)
shopt -s nullglob
notebooks=( "$NB_DIR"/*.ipynb )
shopt -u nullglob

if [[ ${#notebooks[@]} -eq 0 ]]; then
  echo "No notebooks found in '$NB_DIR'."
  exit 0
fi

fail=0
for nb in "${notebooks[@]}"; do
  base="$(basename "$nb")"

  # Skip hidden/template notebooks
  if [[ "$base" == _* ]]; then
    echo "Skipping template/hidden notebook: $base"
    continue
  fi

  log="$LOG_DIR/${base%.ipynb}.log"
  echo "=== Executing: $nb ==="
  echo "(log: $log)"
  if ! jupyter nbconvert \
        --to notebook \
        --inplace \
        --ExecutePreprocessor.timeout="$TIMEOUT" \
        --execute "$nb" \
        >"$log" 2>&1; then
    echo "!!! FAILED: $nb (see $log)"
    fail=1
  else
    echo "=== Done: $nb ==="
  fi
done

if [[ $fail -ne 0 ]]; then
  echo "One or more notebooks failed. See logs in $LOG_DIR"
  exit 1
fi

echo "All notebooks executed successfully."

