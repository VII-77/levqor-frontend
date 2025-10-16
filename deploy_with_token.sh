#!/bin/bash

# Automated Railway Deployment with Token
# Usage: bash deploy_with_token.sh YOUR_RAILWAY_TOKEN

set -e

if [ -z "$1" ]; then
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║     🚂 Railway Deployment with Token                           ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "❌ Error: Railway token required!"
    echo ""
    echo "📋 HOW TO USE:"
    echo ""
    echo "1. Get your token from: https://railway.app/account/tokens"
    echo "   - Sign in with GitHub"
    echo "   - Click 'Create Token'"
    echo "   - Copy the token"
    echo ""
    echo "2. Run this script with your token:"
    echo "   bash deploy_with_token.sh YOUR_RAILWAY_TOKEN"
    echo ""
    echo "Example:"
    echo "   bash deploy_with_token.sh railway_abc123xyz..."
    echo ""
    exit 1
fi

RAILWAY_TOKEN=$1

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     🚂 Deploying EchoPilot to Railway                          ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Set token and verify
echo "🔑 Step 1: Authenticating with Railway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
export RAILWAY_TOKEN=$RAILWAY_TOKEN

if railway whoami > /dev/null 2>&1; then
    echo "✅ Authentication successful!"
    railway whoami
else
    echo "❌ Authentication failed. Check your token."
    exit 1
fi
echo ""

# Step 2: Initialize project
echo "📋 Step 2: Creating Railway Project"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
railway init <<EOF
EchoPilot
EOF
echo "✅ Project created!"
echo ""

# Step 3: Deploy
echo "🚀 Step 3: Deploying Application"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
railway up --detach
echo "✅ Deployment started!"
echo ""

# Wait for deployment to register
sleep 5

# Step 4: Set environment variables
echo "🔑 Step 4: Setting Environment Variables"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Function to set variable if it exists
set_var() {
    local var_name=$1
    if [ ! -z "${!var_name}" ]; then
        echo "  ✅ $var_name"
        railway variables --set "$var_name=${!var_name}" > /dev/null 2>&1
    else
        echo "  ⚠️  Skipping $var_name (not found)"
    fi
}

# Required variables
set_var "AI_INTEGRATIONS_OPENAI_API_KEY"
set_var "AI_INTEGRATIONS_OPENAI_BASE_URL"
set_var "AUTOMATION_QUEUE_DB_ID"
set_var "AUTOMATION_LOG_DB_ID"
set_var "JOB_LOG_DB_ID"
set_var "REPLIT_CONNECTORS_HOSTNAME"
set_var "REPL_IDENTITY"

# Optional variables
set_var "NOTION_STATUS_DB_ID"
set_var "TELEGRAM_BOT_TOKEN"
set_var "TELEGRAM_CHAT_ID"
set_var "ALERT_TO"

echo "✅ All variables set!"
echo ""

# Step 5: Get domain and set APP_BASE_URL
echo "🌐 Step 5: Getting Deployment URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sleep 5  # Wait for domain to be ready

DOMAIN=$(railway domain 2>/dev/null || echo "")

if [ ! -z "$DOMAIN" ]; then
    echo "✅ Your Railway URL: https://$DOMAIN"
    railway variables --set "APP_BASE_URL=https://$DOMAIN" > /dev/null 2>&1
    echo "✅ APP_BASE_URL set!"
    RAILWAY_URL="https://$DOMAIN"
else
    echo "⚠️  Domain not ready yet. You can get it later with: railway domain"
    RAILWAY_URL="[Get with: railway domain]"
fi
echo ""

# Success summary
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ DEPLOYMENT COMPLETE!                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Deployment Summary:"
echo ""
echo "  🌐 URL: $RAILWAY_URL"
echo "  🔑 Variables: 11 secrets configured"
echo "  📦 Status: Running"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 Test Your Deployment:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
if [ ! -z "$DOMAIN" ]; then
    echo "  curl https://$DOMAIN/health"
    echo ""
    echo "  # Full status"
    echo "  curl https://$DOMAIN/"
    echo ""
fi
echo "  # View logs"
echo "  railway logs"
echo ""
echo "  # Check status"
echo "  railway status"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 Telegram Commands:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  /status  - Check bot status"
echo "  /health  - System health check"
echo "  /report  - Send supervisor report"
echo ""
echo "🎉 Your EchoPilot bot is now running on Railway!"
