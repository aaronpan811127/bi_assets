#!/usr/bin/env bash
#
# Detect changed DAB bundle folders and emit them for GitHub Actions.
#
# A "DAB folder" is any top-level folder containing a databricks.yml
# (e.g. finance_operations/, supply_chain/, 01_shared_metric_views/).
#
# Usage:
#   detect-changed-dabs.sh <base_ref>
#
# <base_ref> is the git ref to diff against:
#   - CI (pull request): origin/master  -> diff the full feature branch (three-dot)
#   - CD (push to master): HEAD~1        -> diff the most recent merge commit delta
#
# Outputs (to $GITHUB_OUTPUT when set, else stdout):
#   dabs   = JSON array of changed domain bundles  (excludes 01_shared_metric_views)
#   shared = "true"/"false" whether 01_shared_metric_views changed
#   any    = "true"/"false" whether anything deployable changed
#
set -euo pipefail

BASE_REF="${1:-origin/master}"
SHARED_DIR="01_shared_metric_views"

# Three-dot for branch-vs-base (merge-base) diffs; two-dot for a commit delta.
if [[ "$BASE_REF" == *"~"* || "$BASE_REF" == *".."* ]]; then
  DIFF_SPEC="$BASE_REF"
else
  DIFF_SPEC="${BASE_REF}...HEAD"
fi

changed_top=$(git diff --name-only "$DIFF_SPEC" \
  | awk -F/ 'NF>1 {print $1}' \
  | sort -u \
  | while read -r d; do [ -f "$d/databricks.yml" ] && echo "$d"; done)

shared="false"
domains=()
while IFS= read -r d; do
  [ -z "$d" ] && continue
  if [ "$d" = "$SHARED_DIR" ]; then
    shared="true"
  else
    domains+=("$d")
  fi
done <<< "$changed_top"

# Build a JSON array of domain bundles.
if [ "${#domains[@]}" -eq 0 ]; then
  dabs_json="[]"
else
  dabs_json=$(printf '%s\n' "${domains[@]}" | jq -R . | jq -cs .)
fi

any="false"
if [ "$shared" = "true" ] || [ "${#domains[@]}" -gt 0 ]; then
  any="true"
fi

echo "Changed shared metric views: $shared"
echo "Changed domain bundles: $dabs_json"

if [ -n "${GITHUB_OUTPUT:-}" ]; then
  {
    echo "dabs=$dabs_json"
    echo "shared=$shared"
    echo "any=$any"
  } >> "$GITHUB_OUTPUT"
fi
