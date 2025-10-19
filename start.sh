#!/usr/bin/env bash
set -e
echo "🚀 Starting EchoPilot AI Automation Bot..."
exec gunicorn --worker-class gthread --workers 1 --threads 2 --timeout 120 --bind 0.0.0.0:5000 run:app
