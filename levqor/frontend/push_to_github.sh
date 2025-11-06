#!/bin/bash
set -e

echo "🔧 Fixing git and pushing to GitHub..."
echo ""

# Remove any stuck git lock files
rm -f /home/runner/workspace/.git/index.lock
rm -f .git/index.lock

# Go to frontend directory
cd "$(dirname "$0")"

echo "✅ Cleaned up lock files"
echo ""

# Add all files
echo "📦 Adding all files..."
git add -A

# Show what will be committed
echo ""
echo "📝 Files to be committed:"
git status --short

# Commit
echo ""
echo "💾 Creating commit..."
git commit -m "Add complete Next.js 14 frontend - all source files" || true

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ DONE! Check your repo at: https://github.com/VII-77/levqor-frontend"
echo ""
echo "⏭️  Next: Wait 2 minutes for Vercel to rebuild at https://levqor-frontend.vercel.app"
