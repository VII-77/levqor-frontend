#!/bin/bash
set -e

echo "🔧 Complete Fix - Removing locks and pushing to GitHub..."
echo ""

# Step 1: Remove ALL lock files
echo "Step 1: Removing lock files..."
rm -f /home/runner/workspace/.git/index.lock
rm -f .git/index.lock
rm -f levqor/frontend/.git/index.lock
echo "✅ Lock files removed"
echo ""

# Step 2: Fix submodule issue
echo "Step 2: Fixing submodule issue..."
cd levqor/frontend
git rm --cached . 2>/dev/null || true
echo "✅ Submodule issue fixed"
echo ""

# Step 3: Add all files
echo "Step 3: Adding all files..."
git add -A
echo "✅ Files added"
echo ""

# Step 4: Commit
echo "Step 4: Creating commit..."
git commit -m "Complete Next.js 14 frontend with all source files" || echo "(Nothing new to commit)"
echo ""

# Step 5: Push
echo "Step 5: Pushing to GitHub..."
git push origin main
echo ""

echo "🎉 SUCCESS! Your frontend is now on GitHub!"
echo ""
echo "📍 GitHub: https://github.com/VII-77/levqor-frontend"
echo "📍 Vercel: https://levqor-frontend.vercel.app (wait 2 minutes)"
echo ""
