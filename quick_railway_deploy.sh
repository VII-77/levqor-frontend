#!/bin/bash

# One-Command Railway Deployment
# Usage: bash quick_railway_deploy.sh

echo "🚂 Quick Railway Deploy for EchoPilot"
echo ""

# Install Railway CLI if needed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login, init, and deploy in one go
echo "1. Login to Railway (browser will open)..."
railway login

echo ""
echo "2. Creating new project..."
railway init

echo ""
echo "3. Setting all environment variables..."
railway variables --set AI_INTEGRATIONS_OPENAI_API_KEY="$AI_INTEGRATIONS_OPENAI_API_KEY"
railway variables --set AI_INTEGRATIONS_OPENAI_BASE_URL="$AI_INTEGRATIONS_OPENAI_BASE_URL"
railway variables --set AUTOMATION_QUEUE_DB_ID="$AUTOMATION_QUEUE_DB_ID"
railway variables --set AUTOMATION_LOG_DB_ID="$AUTOMATION_LOG_DB_ID"
railway variables --set JOB_LOG_DB_ID="$JOB_LOG_DB_ID"
railway variables --set REPLIT_CONNECTORS_HOSTNAME="$REPLIT_CONNECTORS_HOSTNAME"
railway variables --set REPL_IDENTITY="$REPL_IDENTITY"
railway variables --set NOTION_STATUS_DB_ID="$NOTION_STATUS_DB_ID"
railway variables --set TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN"
railway variables --set TELEGRAM_CHAT_ID="$TELEGRAM_CHAT_ID"
railway variables --set ALERT_TO="$ALERT_TO"

echo ""
echo "4. Deploying to Railway..."
railway up

echo ""
echo "5. Getting your URL..."
DOMAIN=$(railway domain)
echo "Your Railway URL: https://$DOMAIN"

echo ""
echo "6. Setting APP_BASE_URL..."
railway variables --set APP_BASE_URL="https://$DOMAIN"

echo ""
echo "✅ Done! Test your deployment:"
echo "   curl https://$DOMAIN/health"
