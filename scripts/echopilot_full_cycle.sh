#!/usr/bin/env bash
set -euo pipefail

# ---- Config (override via flags) ----
DRY_FINANCE=1
CAPTAIN_TEMP="0.0"
CAPTAIN_RETRIES="1"
CAPTAIN_PAYLOAD=""   # e.g. https://filesamples.com/samples/audio/mp3/sample1.mp3
RUN_FIX=1
RUN_VALIDATE=1
RUN_CAPTAIN=1
RUN_DEPLOY=1

# ---- CLI ----
usage() {
  cat <<EOF
Usage: bash scripts/echopilot_full_cycle.sh [options]

Options:
  --no-fix            Skip Fix Pack
  --no-validate       Skip validation script
  --no-captain        Skip release_captain
  --no-deploy         Skip auto deploy
  --payload URL       Override payload for release_captain
  --dry-finance=0|1   Toggle finance auto-close (default 1 = dry mode)
  --temp FLOAT        Temperature for release_captain (default 0.0)
  --retries N         Max QA retries (default 1)
  -h|--help           Show this help
EOF
}

for arg in "$@"; do
  case "$arg" in
    --no-fix) RUN_FIX=0 ;;
    --no-validate) RUN_VALIDATE=0 ;;
    --no-captain) RUN_CAPTAIN=0 ;;
    --no-deploy) RUN_DEPLOY=0 ;;
    --payload=*) CAPTAIN_PAYLOAD="${arg#*=}" ;;
    --dry-finance=*) DRY_FINANCE="${arg#*=}" ;;
    --temp=*) CAPTAIN_TEMP="${arg#*=}" ;;
    --retries=*) CAPTAIN_RETRIES="${arg#*=}" ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $arg"; usage; exit 1 ;;
  esac
done

log() { printf "\n\033[1;36m[%s]\033[0m %s\n" "$(date '+%H:%M:%S')" "$*"; }
ok()  { printf "\033[1;32m✓\033[0m %s\n" "$*"; }
warn(){ printf "\033[1;33m!\033[0m %s\n" "$*"; }
err() { printf "\033[1;31m✗ %s\033[0m\n" "$*"; }

ROOT_DIR="$(pwd)"
mkdir -p logs

# ---- Step 1: Fix Pack ----
if [[ "$RUN_FIX" -eq 1 ]]; then
  log "RUNNING FIX PACK (non-Stripe backlog hardening)…"
  if [[ -f scripts/echopilot_fixpack.sh ]]; then
    bash scripts/echopilot_fixpack.sh | tee -a logs/full_cycle.log
  else
    bash <(curl -fsSL https://raw.githubusercontent.com/echo-ai-tools/fixpack/main/echopilot_fixpack.sh) | tee -a logs/full_cycle.log
  fi
  ok "Fix Pack complete"
else
  warn "Skipped Fix Pack (--no-fix)"
fi

# ---- Step 2: Validation ----
if [[ "$RUN_VALIDATE" -eq 1 ]]; then
  log "RUNNING VALIDATION (intake → QA → finance → governance)…"
  if [[ -x scripts/validate_system.sh ]]; then
    bash scripts/validate_system.sh | tee -a logs/full_cycle.log
  else
    err "scripts/validate_system.sh not found/executable"; exit 2
  fi
  ok "Validation complete (see logs/e2e_validation.json)"
else
  warn "Skipped Validation (--no-validate)"
fi

# ---- Step 3: Release Captain ----
if [[ "$RUN_CAPTAIN" -eq 1 ]]; then
  log "RUNNING RELEASE CAPTAIN (7-step runbook)…"
  [[ -f scripts/release_captain.py ]] || { err "scripts/release_captain.py not found"; exit 3; }

  CAPTAIN_CMD=( python3 scripts/release_captain.py "--max-retries=$CAPTAIN_RETRIES" "--temperature=$CAPTAIN_TEMP" )
  if [[ "$DRY_FINANCE" -eq 1 ]]; then CAPTAIN_CMD+=( --dry-finance ); fi
  if [[ -n "$CAPTAIN_PAYLOAD" ]]; then CAPTAIN_CMD+=( "--payload=$CAPTAIN_PAYLOAD" ); fi

  printf "→ %s\n" "${CAPTAIN_CMD[*]}"
  "${CAPTAIN_CMD[@]}" | tee -a logs/full_cycle.log
  ok "Release Captain run complete (see logs/release_captain.json)"
else
  warn "Skipped Release Captain (--no-captain)"
fi

# ---- Step 4: Auto commit & deploy ----
if [[ "$RUN_DEPLOY" -eq 1 ]]; then
  log "DEPLOYING (commit + trigger rebuild + ensure app running)…"
  if [[ -x scripts/auto_commit_deploy.sh ]]; then
    bash scripts/auto_commit_deploy.sh | tee -a logs/full_cycle.log
  else
    # Minimal inline deploy fallback
    git add -A || true
    git commit -m "full-cycle: fix+validate+captain $(date -u '+%Y-%m-%dT%H:%M:%SZ')" || true
    touch replit.nix || true
    ok "Committed. Replit will detect changes and redeploy."
  fi
  ok "Deploy step complete"
else
  warn "Skipped Deploy (--no-deploy)"
fi

log "ALL DONE ✅  (Fix:${RUN_FIX} Validate:${RUN_VALIDATE} Captain:${RUN_CAPTAIN} Deploy:${RUN_DEPLOY})"
ok "Logs: logs/full_cycle.log, logs/e2e_validation.json, logs/release_captain.json"
