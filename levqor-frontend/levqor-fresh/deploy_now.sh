#!/bin/bash
# Deployment wrapper with proper environment setup

set -e

echo "🔧 Setting up Node.js environment..."

# Find Node.js in nix store
NODE_PATH=$(find /nix/store -maxdepth 1 -name "*nodejs-20*" -type d 2>/dev/null | head -1)

if [ -z "$NODE_PATH" ]; then
  echo "❌ Node.js not found. Installing..."
  exit 1
fi

export PATH="$NODE_PATH/bin:$PATH"

echo "✅ Node.js found: $(node --version)"
echo "✅ npm found: $(npm --version)"
echo ""

# Now run the deployment
exec ./deploy_frontend_complete.sh
