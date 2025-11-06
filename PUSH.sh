#!/bin/bash
set -e

echo "🚀 Pushing to GitHub using your token from Secrets..."
echo ""

cd "$(dirname "$0")"

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Add all files
echo "📝 Adding all files..."
git add -A
echo "✅ Files added"
echo ""

# Show what will be committed
echo "Files to commit:"
git status --short | head -15
echo ""

# Commit
echo "💾 Creating commit..."
git commit -m "Complete Next.js 14 frontend with StatusCard and legal pages" || echo "(Nothing new to commit)"
echo ""

# Set branch to main
echo "🌿 Setting branch to main..."
git branch -M main
echo ""

# Add or update remote
echo "🔗 Adding GitHub remote..."
git remote add origin https://github.com/VII-77/levqor-frontend.git 2>/dev/null || \
git remote set-url origin https://github.com/VII-77/levqor-frontend.git
echo "✅ Remote configured"
echo ""

# Push using the token from secrets
echo "🚀 Pushing to GitHub..."
git push -u https://VII-77:${GITHUB_PERSONAL_ACCESS_TOKEN}@github.com/VII-77/levqor-frontend.git main

echo ""
echo "🎉 SUCCESS! Your frontend is now on GitHub!"
echo ""
echo "📍 GitHub: https://github.com/VII-77/levqor-frontend"
echo "📍 Vercel: https://levqor-frontend.vercel.app (wait ~2 minutes)"
echo ""
