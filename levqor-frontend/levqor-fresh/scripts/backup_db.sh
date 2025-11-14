#!/usr/bin/env bash
set -euo pipefail
DB="${1:-levqor.db}"
TS=$(date +%F-%H%M%S)
DST="backups/levqor-${TS}.db"
mkdir -p backups

if command -v sqlite3 >/dev/null 2>&1; then
  sqlite3 "$DB" ".backup '$DST'"
  echo "backup (sqlite3 .backup) -> $DST"
else
  cp "$DB" "$DST"
  [ -f "${DB}-wal" ] && cp "${DB}-wal" "backups/levqor-${TS}.db-wal"
  [ -f "${DB}-shm" ] && cp "${DB}-shm" "backups/levqor-${TS}.db-shm"
  echo "backup (file copy) -> $DST + WAL/SHM"
fi
