#!/usr/bin/env bash
# levqor_fix_all.sh — final end-to-end fixer for Git + Vercel + Checkout
# Safe to re-run. No jq. Exits non-zero on actionable faults.

set -euo pipefail

REPO=~/workspace/levqor-site
APP_URL="https://levqor.ai"
REQUIRED_VARS=(
  STRIPE_SECRET_KEY
  SITE_URL
  STRIPE_PRICE_STARTER
  STRIPE_PRICE_STARTER_YEAR
  STRIPE_PRICE_PRO
  STRIPE_PRICE_PRO_YEAR
  STRIPE_PRICE_BUSINESS
  STRIPE_PRICE_BUSINESS_YEAR
)

echo "== 0) Context ==============================================="
echo "Repo    : $REPO"
echo "App URL : $APP_URL"
echo "Token   : ${VERCEL_TOKEN:-<none>}"

echo "== 1) Git: snapshot and reconcile ============================"
cd "$REPO"

# Snapshot local edits (if any) so we can always roll back
git add -A || true
git stash push -m "backup before levqor_fix_all" || true

git fetch --all --prune

# Ensure main exists and aligns to remote
git checkout main 2>/dev/null || git checkout -b main
git reset --hard origin/main || true

# Merge Replit working branch in, preferring Replit edits on conflict
if git show-ref --verify --quiet refs/heads/replit-agent || git show-ref --verify --quiet refs/remotes/origin/replit-agent; then
  echo "Merging replit-agent into main (prefer theirs)…"
  git merge replit-agent --strategy-option=theirs --no-edit || true
else
  echo "replit-agent not present; skipping merge"
fi

# Ensure the checkout code is present (route + optional debug)
if [ ! -f src/app/api/checkout/route.ts ]; then
  echo "FATAL: src/app/api/checkout/route.ts missing. Commit it, then re-run."
  exit 2
fi

echo "Pushing unified state to GitHub main (force)…"
git push origin main --force

echo "== 2) Vercel: env audit ======================================"
if [ -z "${VERCEL_TOKEN:-}" ]; then
  echo "WARN: VERCEL_TOKEN not set. Env audit will still run using current session if logged in."
fi

echo "Listing current Production env…"
vercel env ls --token "${VERCEL_TOKEN:-}" 2>/dev/null | sed -n '1,120p' || true

MISSING=()
for v in "${REQUIRED_VARS[@]}"; do
  if ! vercel env ls --token "${VERCEL_TOKEN:-}" 2>/dev/null | grep -q -E "^\s*${v}\b.*Production"; then
    MISSING+=("$v")
  fi
done

if [ "${#MISSING[@]}" -gt 0 ]; then
  echo
  echo "FATAL: Missing required Production env vars:"
  for v in "${MISSING[@]}"; do echo "  - $v"; done
  cat <<'TIP'

Fix:
  For each missing var run:
    vercel env add <VAR_NAME> production --token "$VERCEL_TOKEN"
  Paste the live Stripe price_id value (looks like price_XXXXXXXXX) when prompted.
  SITE_URL must be https://levqor.ai

Re-run:  ./levqor_fix_all.sh
TIP
  exit 3
fi

echo "== 3) Trigger clean Production deploy ========================"
# Empty commit to ensure a new build if auto-build stalls
git commit --allow-empty -m "ci: force production rebuild (levqor_fix_all)" || true
git push origin main

# Try CLI deploy; if rate-limited, fall back to auto-build from push
if vercel --version >/dev/null 2>&1; then
  echo "Attempting Vercel production deploy…"
  set +e
  vercel --prod --token "${VERCEL_TOKEN:-}" >/tmp/levqor_vercel.out 2>&1
  VC=$?
  set -e
  if [ $VC -ne 0 ]; then
    echo "NOTE: Vercel CLI deploy skipped/limited. The push above will still trigger a build when quota allows."
  fi
else
  echo "NOTE: vercel CLI not installed. Relying on Git push to trigger build."
fi

echo "== 4) Post-deploy checks (poll up to ~5 min) ================="
# Lightweight poll without jq. Stop early on success.
deadline=$(( $(date +%s) + 300 ))
while :; do
  if curl -sI "$APP_URL" | grep -q "HTTP/2 200"; then break; fi
  now=$(date +%s); [ $now -gt $deadline ] && break
  echo "Waiting for site…"; sleep 10
done

echo "Homepage:"
curl -sI "$APP_URL" | sed -n '1p'

echo "Pricing:"
curl -sI "$APP_URL/pricing" | sed -n '1p'

echo "== 5) Checkout functional test ==============================="
# Source of truth is POST JSON
resp=$(curl -s -X POST "$APP_URL/api/checkout" -H "content-type: application/json" \
       --data '{"plan":"starter","term":"monthly"}' || true)

echo "Checkout response:"
echo "$resp"

if echo "$resp" | grep -q '"url"'; then
  echo "SUCCESS: Checkout session created."
  exit 0
fi

echo "FAIL: Checkout did not return a session URL."

echo
echo "== 6) Quick diagnostics ====================================="
echo "Debug endpoint (if implemented):"
curl -s "$APP_URL/api/checkout/_debug" || true
echo
echo "Vercel env (grep STRIPE & SITE_URL):"
vercel env ls --token "${VERCEL_TOKEN:-}" | grep -E 'STRIPE|SITE_URL' || true

cat <<'NEXT'
Next steps if still failing:
  1) Ensure the values for STRIPE_PRICE_* are live Stripe price IDs:
       price_1….  Monthly/yearly must be distinct.
  2) Confirm the code uses STRIPE_PRICE_* names.
  3) If Vercel shows HTTP/2 200 for pages but checkout fails, it is env-mismatch.
  4) After correcting env, run this script again to force rebuild and verify.

DONE.
NEXT
