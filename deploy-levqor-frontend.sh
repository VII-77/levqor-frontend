#!/bin/bash

# === LEVQOR FRONTEND DEPLOYMENT TO VERCEL ===
# Purpose: Deploy levqor-site (frontend) → levqor.ai
# Backend: api.levqor.ai (already live)

set -e  # Exit on error

echo "=== STEP 1: Install Vercel CLI & Log In ==="
npm i -g vercel
vercel login

echo "=== STEP 2: Deploy levqor-site ==="
cd levqor-site
vercel --prod --confirm --name levqor

echo "=== STEP 3: Add Custom Domain ==="
vercel domains add levqor.ai
vercel certs issue levqor.ai

echo "=== STEP 4: Configure DNS on Cloudflare ==="
echo "Please log in to Cloudflare and add this record:"
echo "Type: CNAME | Name: @ | Target: cname.vercel-dns.com | Proxy: DNS only (grey cloud)"
echo "Wait 5–10 minutes for propagation before proceeding."

echo "=== STEP 5: Set Environment Variables in Vercel ==="
vercel env add NEXT_PUBLIC_API_URL production
echo "When prompted, paste: https://api.levqor.ai"

echo "=== STEP 6: Redeploy to Apply Variables ==="
vercel --prod --confirm

echo "=== STEP 7: Verify Deployment ==="
curl -I https://levqor.ai | grep HTTP
echo "✅ Expect: HTTP/2 200 OK"
echo "Check site visually at https://levqor.ai"

echo "=== STEP 8: Confirm Backend Connectivity ==="
curl -fsS https://api.levqor.ai/status
echo "✅ Backend responding correctly"

echo "=== STEP 9: Final Check ==="
echo "Frontend: https://levqor.ai"
echo "Backend:  https://api.levqor.ai"
echo "✅ All systems connected and live!"
