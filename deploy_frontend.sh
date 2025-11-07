#!/bin/bash

set -e

echo "🚀 Deploying Levqor Frontend to Vercel"
echo "======================================="
echo ""

# Check if VERCEL_TOKEN is set
if [ -z "$VERCEL_TOKEN" ]; then
  echo "❌ ERROR: VERCEL_TOKEN environment variable is not set"
  echo "Please add your Vercel token to Replit secrets"
  exit 1
fi

# Check if RESEND_API_KEY is set
if [ -z "$RESEND_API_KEY" ]; then
  echo "❌ ERROR: RESEND_API_KEY environment variable is not set"
  echo "Please add your Resend API key to Replit secrets"
  exit 1
fi

# Navigate to levqor-site directory
cd levqor-site

# Install Vercel CLI if not present
if ! command -v vercel &> /dev/null; then
  echo "📦 Installing Vercel CLI..."
  npm install -g vercel
fi

# Generate a random NEXTAUTH_SECRET if not provided
NEXTAUTH_SECRET=${NEXTAUTH_SECRET:-$(openssl rand -base64 32)}

echo "✅ Environment variables configured"
echo ""
echo "📋 Deploying with the following configuration:"
echo "   - Domain: levqor.ai"
echo "   - API URL: https://api.levqor.ai"
echo "   - Email: no-reply@levqor.ai"
echo ""

# Deploy to Vercel with production flag
echo "🔧 Building and deploying to Vercel..."
vercel --token "$VERCEL_TOKEN" \
  --prod \
  --yes \
  -e NEXTAUTH_URL=https://levqor.ai \
  -e NEXTAUTH_SECRET="$NEXTAUTH_SECRET" \
  -e RESEND_API_KEY="$RESEND_API_KEY" \
  -e NEXT_PUBLIC_API_URL=https://api.levqor.ai

echo ""
echo "✅ Deployment complete!"
echo "🌐 Your site is live at: https://levqor.ai"
echo ""
echo "🔐 NextAuth Secret (save this for future deployments):"
echo "$NEXTAUTH_SECRET"
echo ""
echo "📝 Next steps:"
echo "   1. Visit https://levqor.ai to see your site"
echo "   2. Test the sign-in flow at https://levqor.ai/signin"
echo "   3. Check your Resend dashboard for email delivery"
