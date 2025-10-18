#!/usr/bin/env python3

from bot.main import EchoPilotBot
from flask import Flask, jsonify, send_from_directory, request
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

@app.route('/ops-report')
def ops_report():
    """Auto-operator monitoring report"""
    try:
        from bot.auto_operator import get_operator_report
        report = get_operator_report()
        
        if report.get("overall_ok"):
            return jsonify(report), 200
        else:
            return jsonify(report), 503  # Service unavailable if issues detected
    except Exception as e:
        return jsonify({
            "error": str(e),
            "overall_ok": False
        }), 500

@app.route('/payments/debug')
def payments_debug():
    """Payment system debug information"""
    try:
        stripe_key = os.getenv("STRIPE_SECRET_KEY", "").strip()
        stripe_wh = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()
        paypal_id = os.getenv("PAYPAL_CLIENT_ID", "").strip()
        paypal_sec = os.getenv("PAYPAL_SECRET", "").strip()
        
        return jsonify({
            "stripe": {
                "key_configured": bool(stripe_key),
                "key_prefix": stripe_key[:15] + "..." if stripe_key else None,
                "webhook_secret_configured": bool(stripe_wh),
                "mode": "test" if stripe_key.startswith("sk_test_") else "live" if stripe_key.startswith("sk_live_") else "unknown"
            },
            "paypal": {
                "client_id_configured": bool(paypal_id),
                "secret_configured": bool(paypal_sec),
                "mode": os.getenv("PAYPAL_LIVE", "true").lower()
            },
            "webhook_urls": {
                "stripe": f"{os.getenv('REPLIT_DOMAINS', 'localhost').split(',')[0]}/webhook/stripe",
                "paypal": f"{os.getenv('REPLIT_DOMAINS', 'localhost').split(',')[0]}/webhook/paypal"
            },
            "primary_provider": "stripe" if stripe_key else "paypal" if paypal_id else "none"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    """Handle favicon requests to eliminate 404 errors"""
    return '', 204  # No content response

@app.route('/webhook/stripe', methods=['POST'])
def webhook_stripe():
    """Stripe webhook endpoint for payment status updates"""
    try:
        from bot.payments import stripe_parse_webhook
        from bot.notion_api import update_job_payment_status
        
        sig = request.headers.get("Stripe-Signature", "")
        outcome = stripe_parse_webhook(request.data, sig)
        
        if not outcome.get("ok"):
            return jsonify(outcome), 400
        
        job_id = outcome.get("job_id")
        status = outcome.get("status")
        
        if job_id and status:
            update_job_payment_status(job_id, status)
            print(f"[Stripe Webhook] Updated job {job_id} to status: {status}")
        
        return jsonify({"ok": True})
    except Exception as e:
        print(f"[Stripe Webhook] Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/webhook/paypal', methods=['POST'])
def webhook_paypal():
    """PayPal webhook endpoint for payment status updates"""
    try:
        from bot.payments import paypal_parse_webhook
        from bot.notion_api import update_job_payment_status
        
        body = request.get_json(silent=True) or {}
        outcome = paypal_parse_webhook(body)
        
        job_id = outcome.get("job_id")
        status = outcome.get("status")
        
        if job_id and status:
            update_job_payment_status(job_id, status)
            print(f"[PayPal Webhook] Updated job {job_id} to status: {status}")
        
        return jsonify({"ok": True})
    except Exception as e:
        print(f"[PayPal Webhook] Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/exec-report')
def exec_report_route():
    """Generate and send executive report on-demand"""
    try:
        from bot.executive_report import run_exec_report
        summary = run_exec_report()
        return jsonify({
            "ok": True,
            "summary": summary,
            "message": "Executive report generated and sent"
        }), 200
    except Exception as e:
        print(f"[ExecReport] Error: {e}")
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/refund')
def refund_route():
    """Mark a job as refunded"""
    try:
        from bot.compliance_tools import mark_refund
        
        job_id = request.args.get("job")
        reason = request.args.get("reason", "Manual refund")
        
        if not job_id:
            return jsonify({"ok": False, "error": "job parameter required"}), 400
        
        success = mark_refund(job_id, reason)
        return jsonify({
            "ok": success,
            "job": job_id,
            "reason": reason
        }), (200 if success else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/p95')
def p95_route():
    """Compute p95 latency metric"""
    try:
        from bot.compliance_tools import compute_p95_latency
        
        p95 = compute_p95_latency()
        return jsonify({
            "ok": True,
            "p95_sec": p95,
            "message": f"p95 latency: {p95}s" if p95 else "No data available"
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/backup-config')
def backup_config_route():
    """Create configuration backup"""
    try:
        from bot.compliance_tools import backup_config
        
        path = backup_config()
        return jsonify({
            "ok": True,
            "path": path,
            "message": "Config backup created"
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/dsr', methods=['POST'])
def dsr_route():
    """Create Data Subject Request (DSR) ticket"""
    try:
        from bot.compliance_tools import create_dsr_ticket
        
        data = request.get_json(force=True)
        correlation_id = data.get("cid") or data.get("correlation_id")
        email = data.get("email")
        action = data.get("action", "Erase")
        notes = data.get("notes", "")
        
        if not correlation_id or not email:
            return jsonify({
                "ok": False,
                "error": "cid and email parameters required"
            }), 400
        
        success = create_dsr_ticket(correlation_id, email, action, notes)
        return jsonify({
            "ok": success,
            "correlation_id": correlation_id,
            "action": action
        }), (200 if success else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/payments/scan')
def payments_scan_route():
    """Scan for missed Stripe webhook events and reconcile"""
    try:
        from bot.stripe_events_poller import poll_and_fix
        
        fixed = poll_and_fix()
        return jsonify({
            "ok": True,
            "fixed": fixed,
            "message": f"Reconciled {fixed} missed payment(s)" if fixed > 0 else "No missed payments found"
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/jobs/replay')
def jobs_replay_route():
    """Replay failed jobs by resetting them for retry"""
    try:
        from bot.replay_failed_jobs import replay_once
        
        count = replay_once()
        return jsonify({
            "ok": True,
            "replayed": count,
            "message": f"Replayed {count} failed job(s)" if count > 0 else "No failed jobs found"
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/forecast')
def forecast_route():
    """Generate 30-day forecast"""
    try:
        from bot.forecast_engine import get_forecast_engine
        
        engine = get_forecast_engine()
        forecast = engine.generate_30day_forecast()
        return jsonify(forecast), (200 if forecast['ok'] else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/forecast/chart')
def forecast_chart_route():
    """Get forecast in chart format (JSON + CSV)"""
    try:
        from bot.forecast_engine import get_forecast_engine
        
        engine = get_forecast_engine()
        chart = engine.get_forecast_chart_data()
        return jsonify(chart), (200 if chart['ok'] else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/finance/revenue')
def finance_revenue_route():
    """Get revenue summary"""
    try:
        from bot.finance_system import get_finance_system
        
        days = int(request.args.get('days', 30))
        finance = get_finance_system()
        summary = finance.get_revenue_summary(days)
        return jsonify(summary), (200 if summary['ok'] else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/finance/pl')
def finance_pl_route():
    """Get P&L report"""
    try:
        from bot.finance_system import get_finance_system
        
        days = int(request.args.get('days', 30))
        finance = get_finance_system()
        report = finance.generate_pl_report(days)
        return jsonify(report), (200 if report['ok'] else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/finance/valuation')
def finance_valuation_route():
    """Get valuation pack"""
    try:
        from bot.finance_system import get_finance_system
        
        days = int(request.args.get('days', 30))
        finance = get_finance_system()
        valuation = finance.generate_valuation_pack(days)
        return jsonify(valuation), (200 if valuation['ok'] else 500)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/v1/jobs', methods=['POST'])
def marketplace_submit_job():
    """Marketplace API - Submit job"""
    try:
        from bot.marketplace_api import get_marketplace_api
        
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key:
            return jsonify({"ok": False, "error": "Missing API key"}), 401
        
        job_data = request.get_json(force=True)
        marketplace = get_marketplace_api()
        result = marketplace.submit_job_via_api(api_key, job_data)
        
        return jsonify(result), (200 if result['ok'] else 400)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/v1/results/<job_id>')
def marketplace_get_results(job_id):
    """Marketplace API - Get job results"""
    try:
        from bot.marketplace_api import get_marketplace_api
        
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key:
            return jsonify({"ok": False, "error": "Missing API key"}), 401
        
        marketplace = get_marketplace_api()
        result = marketplace.get_job_results(api_key, job_id)
        
        return jsonify(result), (200 if result['ok'] else 400)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/v1/stats')
def marketplace_stats():
    """Marketplace API - Get partner statistics"""
    try:
        from bot.marketplace_api import get_marketplace_api
        
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key:
            return jsonify({"ok": False, "error": "Missing API key"}), 401
        
        marketplace = get_marketplace_api()
        stats = marketplace.get_partner_stats(api_key)
        
        return jsonify(stats), (200 if stats['ok'] else 400)
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/supervisor')
def supervisor_dashboard():
    """Supervisor dashboard (simple HTML)"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EchoPilot Supervisor Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            .metric { font-size: 24px; font-weight: bold; color: #0066cc; }
            .label { color: #666; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>🤖 EchoPilot Supervisor Dashboard</h1>
        <div class="card">
            <div class="label">System Health</div>
            <div class="metric" id="health">Loading...</div>
        </div>
        <div class="card">
            <div class="label">API Endpoints</div>
            <ul>
                <li><a href="/health">Health Check</a></li>
                <li><a href="/ops-report">Auto-Operator Report</a></li>
                <li><a href="/forecast">30-Day Forecast</a></li>
                <li><a href="/finance/pl">P&L Report</a></li>
                <li><a href="/exec-report">Executive Report</a></li>
            </ul>
        </div>
        <script>
            fetch('/health')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('health').innerHTML = data.status === 'ok' ? '✅ Healthy' : '❌ Unhealthy';
                });
        </script>
    </body>
    </html>
    """

def run_bot():
    """Run the bot in a separate thread"""
    bot = EchoPilotBot()
    bot.run()

# Start bot in background thread (runs with both Gunicorn and Flask dev server)
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

if __name__ == "__main__":
    # Start Flask development server (only used for local testing)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
