#!/bin/bash
set -e

echo "🔧 Fixing submodule issue and pushing to GitHub..."
echo ""

# Navigate to frontend
cd "$(dirname "$0")"

# Remove parent workspace git tracking
echo "✅ Step 1: Removing parent git tracking..."
git rm --cached . 2>/dev/null || true
cd ../..
git rm --cached levqor/frontend 2>/dev/null || true

# Go back to frontend
cd levqor/frontend

# Add all files
echo ""
echo "✅ Step 2: Adding all frontend files..."
git add -A

# Show what's being added
echo ""
echo "📝 Files ready to commit:"
git status --short | head -20

# Commit
echo ""
echo "✅ Step 3: Committing..."
git commit -m "Add complete Next.js 14 frontend with StatusCard" || echo "Nothing new to commit"

# Push
echo ""
echo "✅ Step 4: Pushing to GitHub..."
git push origin main

echo ""
echo "🎉 SUCCESS! Check: https://github.com/VII-77/levqor-frontend"
echo ""
echo "⏭️  Vercel will auto-deploy in ~2 minutes at: https://levqor-frontend.vercel.app"
