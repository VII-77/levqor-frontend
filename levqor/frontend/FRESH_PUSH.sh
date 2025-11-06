#!/bin/bash
set -e

echo "🔧 Fresh Git Setup and Push to GitHub"
echo "======================================"
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")"
PWD=$(pwd)
echo "📁 Working in: $PWD"
echo ""

# Step 1: Initialize git repository
echo "Step 1: Initializing git repository..."
git init
echo "✅ Git initialized"
echo ""

# Step 2: Add all files
echo "Step 2: Adding all files..."
git add -A
echo "✅ Files staged"
echo ""

#Step 3: Show what's being added
echo "📝 Files to be committed:"
git ls-files | head -15
echo ""

# Step 4: Create commit
echo "Step 3: Creating commit..."
git commit -m "Complete Next.js 14 frontend with StatusCard and legal pages"
echo "✅ Commit created"
echo ""

# Step 5: Set branch to main
echo "Step 4: Setting branch to main..."
git branch -M main
echo "✅ Branch set to main"
echo ""

# Step 6: Add remote
echo "Step 5: Adding GitHub remote..."
git remote add origin https://github.com/VII-77/levqor-frontend.git 2>/dev/null || git remote set-url origin https://github.com/VII-77/levqor-frontend.git
echo "✅ Remote added"
echo ""

# Step 7: Push (will ask for credentials)
echo "Step 6: Pushing to GitHub..."
echo ""
echo "⚠️  GitHub will ask for credentials:"
echo "    Username: VII-77"
echo "    Password: [paste your GitHub token]"
echo ""
git push -u origin main

echo ""
echo "🎉 SUCCESS! Frontend is now on GitHub!"
echo ""
echo "Next: Wait 2 minutes for Vercel to auto-deploy"
echo "Then visit: https://levqor-frontend.vercel.app"
