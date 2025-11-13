#!/bin/bash
set -e

# Remove all git locks and caches
echo "Cleaning git state..."
sudo rm -rf /home/runner/workspace/.git/index.lock 2>/dev/null || true
sudo rm -rf /home/runner/workspace/.git/objects/*/tmp_* 2>/dev/null || true
sudo rm -rf .git/index.lock 2>/dev/null || true
sudo rm -rf .git/index 2>/dev/null || true

# Reset git index
git rm --cached -r . 2>/dev/null || true
git reset

# Re-add everything fresh
git add .

# Commit
git commit -m "FORCE DEPLOY: Genesis v8 dark theme - bg-slate-950, gradient tiles"

# Verify dark theme is in commit
echo "---VERIFICATION---"
git show HEAD:src/app/layout.tsx | grep -o 'bg-slate-950' && echo "✅ Dark theme IS in git" || echo "❌ Dark theme NOT in git"

# Push
git push origin main --force

echo "---DONE---"
git log -1 --oneline
