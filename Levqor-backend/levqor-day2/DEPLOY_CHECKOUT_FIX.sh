#!/bin/bash
set -e

cd levqor-site

echo "🔧 Committing Stripe checkout fix..."
git add src/app/api/checkout/route.ts
git commit -m "Fix Stripe checkout: support both env naming schemes, validate plan/term, return JSON url"

echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Code pushed successfully!"
echo ""
echo "⏱️  Waiting 150 seconds for Vercel auto-deploy..."
sleep 150

echo ""
echo "🧪 Testing POST /api/checkout (starter + monthly)..."
curl -s -X POST https://levqor.ai/api/checkout \
  -H "content-type: application/json" \
  --data '{"plan":"starter","term":"monthly"}'

echo ""
echo ""
echo "🧪 Testing POST /api/checkout (pro + yearly)..."
curl -s -X POST https://levqor.ai/api/checkout \
  -H "content-type: application/json" \
  --data '{"plan":"pro","term":"yearly"}'

echo ""
echo ""
echo "🧪 Testing GET /api/checkout (backward compat)..."
curl -I "https://levqor.ai/api/checkout?plan=starter&term=monthly" | grep "HTTP"

echo ""
echo "✅ Tests complete!"
