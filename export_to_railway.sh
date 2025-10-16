#!/bin/bash

# Export Railway Environment Variables Helper
# This script shows you what to copy to Railway

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     📋 RAILWAY ENVIRONMENT VARIABLES - COPY THESE               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Copy these to Railway Dashboard → Variables tab"
echo "Replace the values with your actual secrets from Replit"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "⚡ REQUIRED VARIABLES:"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "AI_INTEGRATIONS_OPENAI_API_KEY=<copy from Replit secrets>"
echo "AI_INTEGRATIONS_OPENAI_BASE_URL=<copy from Replit secrets>"
echo "AUTOMATION_QUEUE_DB_ID=<copy from Replit secrets>"
echo "AUTOMATION_LOG_DB_ID=<copy from Replit secrets>"
echo "JOB_LOG_DB_ID=<copy from Replit secrets>"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🔐 REPLIT CONNECTOR VARIABLES (for authentication):"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "REPLIT_CONNECTORS_HOSTNAME=<copy from Replit secrets>"
echo "REPL_IDENTITY=<copy from Replit secrets>"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "📊 OPTIONAL - Monitoring & Alerts:"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "NOTION_STATUS_DB_ID=<copy from Replit secrets>"
echo "TELEGRAM_BOT_TOKEN=<copy from Replit secrets>"
echo "TELEGRAM_CHAT_ID=<copy from Replit secrets>"
echo "ALERT_TO=<copy from Replit secrets>"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🎯 AFTER FIRST DEPLOY:"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "APP_BASE_URL=https://your-railway-url.up.railway.app"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "✅ Variables found in your Replit:"
echo "═══════════════════════════════════════════════════════════════════"

# Check which variables exist
check_var() {
    if [ ! -z "${!1}" ]; then
        echo "✅ $1"
    else
        echo "❌ $1 (not set)"
    fi
}

check_var "AI_INTEGRATIONS_OPENAI_API_KEY"
check_var "AI_INTEGRATIONS_OPENAI_BASE_URL"
check_var "AUTOMATION_QUEUE_DB_ID"
check_var "AUTOMATION_LOG_DB_ID"
check_var "JOB_LOG_DB_ID"
check_var "REPLIT_CONNECTORS_HOSTNAME"
check_var "REPL_IDENTITY"
check_var "NOTION_STATUS_DB_ID"
check_var "TELEGRAM_BOT_TOKEN"
check_var "TELEGRAM_CHAT_ID"
check_var "ALERT_TO"

echo ""
echo "═══════════════════════════════════════════════════════════════════"
