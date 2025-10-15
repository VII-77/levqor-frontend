#!/usr/bin/env python3

from bot.main import EchoPilotBot
from flask import Flask, jsonify
import threading
import os
from bot import git_utils

app = Flask(__name__)

@app.route('/')
def health_check():
    """Health check endpoint for deployment"""
    commit_hash, branch_name, _ = git_utils.get_git_info()
    return jsonify({
        "status": "healthy",
        "service": "EchoPilot AI Automation Bot",
        "commit": commit_hash,
        "branch": branch_name,
        "message": "Bot is running and polling Notion every 60 seconds"
    })

@app.route('/health')
def health():
    """Alternative health endpoint"""
    return jsonify({"status": "ok"})

def run_bot():
    """Run the bot in a separate thread"""
    bot = EchoPilotBot()
    bot.run()

if __name__ == "__main__":
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start Flask server on port 5000 (required for deployment)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
