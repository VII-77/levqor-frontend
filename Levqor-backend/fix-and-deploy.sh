#!/bin/bash
# Levqor Stripe Checkout - Complete Fix & Deploy Script
set -e

echo "🔧 LEVQOR STRIPE CHECKOUT - FIX & DEPLOY"
echo "========================================="
echo ""

cd ~/workspace/levqor-site

echo "📝 Step 1: Commit checkout fix..."
rm -f .git/index.lock || true
git add src/app/api/checkout/route.ts
git commit -m "Fix checkout: support both env schemes and POST/GET" || echo "Already committed"
echo ""

echo "🔄 Step 2: Force redeploy..."
date +"%s" > .redeploy
git add .redeploy
git commit -m "trigger deploy" || echo "Already up to date"
echo ""

echo "📤 Step 3: Push to GitHub..."
git push origin main
echo "✅ Pushed!"
echo ""

echo "⏳ Step 4: Waiting 180 seconds for Vercel deploy..."
sleep 180
echo "✅ Wait complete!"
echo ""

echo "🔍 Step 5: Verifying pages..."
echo "Homepage:"
curl -I https://levqor.ai 2>&1 | grep HTTP || true
echo ""
echo "Pricing:"
curl -I https://levqor.ai/pricing 2>&1 | grep HTTP || true
echo ""

echo "🧪 Step 6: Testing checkout endpoints..."
echo ""

echo "Test 1: Starter Monthly (POST)"
curl -s -X POST https://levqor.ai/api/checkout \
  -H "content-type: application/json" \
  --data '{"plan":"starter","term":"monthly"}' | \
  node -e 'let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>{try{const j=JSON.parse(d);console.log(j.url?("✅ URL: "+j.url):("❌ ERR: "+j.error));}catch(e){console.log("❌ ERR: bad_json")}});'
echo ""

echo "Test 2: Pro Monthly (POST)"
curl -s -X POST https://levqor.ai/api/checkout \
  -H "content-type: application/json" \
  --data '{"plan":"pro","term":"monthly"}' | \
  node -e 'let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>{try{const j=JSON.parse(d);console.log(j.url?("✅ URL: "+j.url):("❌ ERR: "+j.error));}catch(e){console.log("❌ ERR: bad_json")}});'
echo ""

echo "Test 3: Starter Yearly (POST)"
curl -s -X POST https://levqor.ai/api/checkout \
  -H "content-type: application/json" \
  --data '{"plan":"starter","term":"yearly"}' | \
  node -e 'let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>{try{const j=JSON.parse(d);console.log(j.url?("✅ URL: "+j.url):("❌ ERR: "+j.error));}catch(e){console.log("❌ ERR: bad_json")}});'
echo ""

echo "Test 4: Pro Yearly (POST)"
curl -s -X POST https://levqor.ai/api/checkout \
  -H "content-type: application/json" \
  --data '{"plan":"pro","term":"yearly"}' | \
  node -e 'let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>{try{const j=JSON.parse(d);console.log(j.url?("✅ URL: "+j.url):("❌ ERR: "+j.error));}catch(e){console.log("❌ ERR: bad_json")}});'
echo ""

echo "Test 5: GET endpoint (backward compatibility)"
curl -I "https://levqor.ai/api/checkout?plan=starter&term=monthly" 2>&1 | grep HTTP || true
echo ""

echo "========================================="
echo "✅ VERIFICATION COMPLETE"
echo ""
echo "If any tests show errors, check environment variables:"
vercel env ls --token "$VERCEL_TOKEN" 2>&1 | grep -E "STRIPE_PRICE|STRIPE_SECRET_KEY|SITE_URL" || true
