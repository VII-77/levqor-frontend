#!/bin/bash

# Automated Railway Deployment Script for EchoPilot
# This script automates most of the Railway deployment process

set -e  # Exit on any error

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     🚂 Automated Railway Deployment for EchoPilot              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."
    npm install -g @railway/cli
    echo "✅ Railway CLI installed!"
    echo ""
fi

# Step 1: Login to Railway
echo "🔐 Step 1: Login to Railway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Please login to Railway in your browser..."
railway login
echo ""

# Step 2: Create new project or link existing
echo "📋 Step 2: Initialize Railway Project"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Choose an option:"
echo "  1) Create new Railway project"
echo "  2) Link to existing Railway project"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    railway init
elif [ "$choice" = "2" ]; then
    railway link
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi
echo ""

# Step 3: Set environment variables from Replit secrets
echo "🔑 Step 3: Setting Environment Variables"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Function to set variable if it exists in environment
set_var() {
    local var_name=$1
    if [ ! -z "${!var_name}" ]; then
        echo "  ✅ Setting $var_name"
        railway variables --set "$var_name=${!var_name}"
    else
        echo "  ⚠️  Skipping $var_name (not found in environment)"
    fi
}

# Required variables
echo "Setting required variables..."
set_var "AI_INTEGRATIONS_OPENAI_API_KEY"
set_var "AI_INTEGRATIONS_OPENAI_BASE_URL"
set_var "AUTOMATION_QUEUE_DB_ID"
set_var "AUTOMATION_LOG_DB_ID"
set_var "JOB_LOG_DB_ID"
set_var "REPLIT_CONNECTORS_HOSTNAME"
set_var "REPL_IDENTITY"

# Optional variables
echo ""
echo "Setting optional variables..."
set_var "NOTION_STATUS_DB_ID"
set_var "TELEGRAM_BOT_TOKEN"
set_var "TELEGRAM_CHAT_ID"
set_var "ALERT_TO"

echo ""
echo "✅ Environment variables set!"
echo ""

# Step 4: Deploy
echo "🚀 Step 4: Deploying to Railway"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
railway up --detach
echo ""

# Step 5: Get the deployment URL
echo "🌐 Step 5: Getting Deployment URL"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
sleep 5  # Wait for deployment to register
RAILWAY_URL=$(railway domain)

if [ ! -z "$RAILWAY_URL" ]; then
    echo "✅ Your Railway URL: $RAILWAY_URL"
    echo ""
    
    # Set APP_BASE_URL
    echo "🔧 Setting APP_BASE_URL..."
    railway variables --set "APP_BASE_URL=https://$RAILWAY_URL"
    echo "✅ APP_BASE_URL set!"
else
    echo "⚠️  Could not get Railway URL automatically."
    echo "Please run: railway domain"
    echo "Then set: railway variables --set APP_BASE_URL=https://your-url"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ DEPLOYMENT COMPLETE!                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Next Steps:"
echo ""
echo "1. Check deployment status:"
echo "   railway status"
echo ""
echo "2. View logs:"
echo "   railway logs"
echo ""
echo "3. Open your app:"
echo "   railway open"
echo ""
echo "4. Test health endpoint:"
if [ ! -z "$RAILWAY_URL" ]; then
    echo "   curl https://$RAILWAY_URL/health"
    echo ""
    echo "5. Test full status:"
    echo "   curl https://$RAILWAY_URL/"
fi
echo ""
echo "🎉 Your EchoPilot bot is now running on Railway!"
