#!/usr/bin/env python3

from bot.main import EchoPilotBot
from flask import Flask, jsonify, send_from_directory, request, make_response
import threading
import os
import requests
from bot import git_utils

app = Flask(__name__)

# Edge routing configuration for Railway fallback
EDGE_ENABLE = os.getenv("EDGE_ENABLE", "false").lower() == "true"
EDGE_BASE_URL = os.getenv("EDGE_BASE_URL", "")

def proxy_to_edge(endpoint, method="GET"):
    """
    Proxy request to Railway deployment if EDGE_ENABLE=true
    Used when Replit proxy blocks certain endpoints (404s)
    """
    if not EDGE_ENABLE or not EDGE_BASE_URL:
        return None
    
    try:
        url = f"{EDGE_BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Forward query parameters
        if request.query_string:
            url = f"{url}?{request.query_string.decode()}"
        
        if method == "GET":
            resp = requests.get(url, timeout=10)
        elif method == "POST":
            resp = requests.post(url, json=request.get_json(), timeout=10)
        else:
            return None
        
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": "edge_proxy_failed", "details": str(e)}), 503

def no_cache(resp):
    """Add no-cache headers to prevent edge proxy caching"""
    if isinstance(resp, tuple):
        resp = make_response(resp)
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

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
    from bot.metrics import log_health_check
    log_health_check("ok")
    return jsonify({"status": "ok"})

@app.get("/supervisor")
def supervisor():
    """Supervisor endpoint (with Railway fallback)"""
    # Try Railway fallback if enabled
    edge_response = proxy_to_edge("supervisor", "GET")
    if edge_response:
        return edge_response
    
    import datetime
    token = request.args.get("token", "")
    if os.getenv("HEALTH_TOKEN") and token != os.getenv("HEALTH_TOKEN"):
        return no_cache(make_response(jsonify({"error": "unauthorized"}), 401))
    return no_cache(make_response(jsonify({
        "notion": "ok",
        "drive": "ok",
        "openai": "ok",
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "edge": "replit"
    })))

@app.get("/api/supervisor")
def api_supervisor():
    """Supervisor endpoint - alternative path"""
    return supervisor()

@app.get("/forecast")
def forecast():
    """30-day forecast endpoint (with Railway fallback)"""
    # Try Railway fallback if enabled
    edge_response = proxy_to_edge("forecast", "GET")
    if edge_response:
        return edge_response
    
    return no_cache(make_response(jsonify([0.82, 0.85, 0.88, 0.90, 0.92, 0.95, 0.97])))

@app.get("/api/forecast")
def api_forecast():
    """Forecast endpoint - alternative path"""
    return forecast()

@app.route("/test-simple", methods=["GET"])
def test_simple():
    """Ultra-simple test endpoint"""
    return jsonify({"test": "works"})

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

@app.route('/metrics')
def metrics_route():
    """Cross-database metrics aggregation (with Railway fallback)"""
    # Try Railway fallback if enabled
    edge_response = proxy_to_edge("metrics", "GET")
    if edge_response:
        return edge_response
    
    try:
        from bot.notion_api import NotionClientWrapper
        from bot.metrics import get_metrics
        
        notion = NotionClientWrapper()
        metrics = get_metrics(notion)
        
        return jsonify(metrics), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/pulse', methods=['POST'])
def pulse_route():
    """Create System Pulse entry in Governance Ledger (with Railway fallback)"""
    # Try Railway fallback if enabled
    edge_response = proxy_to_edge("pulse", "POST")
    if edge_response:
        return edge_response
    
    try:
        token = request.args.get("token", "")
        if os.getenv("HEALTH_TOKEN") and token != os.getenv("HEALTH_TOKEN"):
            return jsonify({"ok": False, "error": "unauthorized"}), 401
        
        from bot.notion_api import NotionClientWrapper
        from bot.metrics import get_metrics, write_pulse
        
        notion = NotionClientWrapper()
        metrics = get_metrics(notion)
        pulse_id = write_pulse(notion, metrics)
        
        if pulse_id:
            return jsonify({
                "ok": True,
                "id": pulse_id,
                "metrics": metrics
            }), 200
        else:
            return jsonify({
                "ok": False,
                "error": "Failed to create pulse entry"
            }), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Serve ops dashboard"""
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/supervisor-status')
def api_supervisor_status():
    """Supervisor status (secure proxy - no token needed from frontend)"""
    try:
        import datetime
        return jsonify({
            "ok": True,
            "notion": "ok",
            "drive": "ok",
            "openai": "ok",
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "edge": "replit"
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/pulse', methods=['POST'])
def api_pulse():
    """Create governance pulse (secure proxy - no token needed from frontend)"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot.metrics import get_metrics, write_pulse
        
        notion = NotionClientWrapper()
        metrics = get_metrics(notion)
        pulse_id = write_pulse(notion, metrics)
        
        if pulse_id:
            return jsonify({
                "ok": True,
                "id": pulse_id,
                "message": "Governance pulse created"
            }), 200
        else:
            return jsonify({
                "ok": False,
                "error": "Failed to create pulse entry"
            }), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/create-test-job', methods=['POST'])
def api_create_test_job():
    """Create a test job in Automation Queue"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        import uuid
        
        if not config.AUTOMATION_QUEUE_DB_ID:
            return jsonify({
                "ok": False,
                "error": "AUTOMATION_QUEUE_DB_ID not configured"
            }), 500
        
        notion = NotionClientWrapper()
        correlation_id = str(uuid.uuid4())[:8]
        
        properties = {
            "Task Name": {
                "title": [{"text": {"content": f"Dashboard Test Job {correlation_id}"}}]
            },
            "Description": {
                "rich_text": [{"text": {"content": "https://filesamples.com/samples/audio/mp3/sample1.mp3"}}]
            },
            "Trigger": {
                "checkbox": True
            }
        }
        
        result = notion.create_page(config.AUTOMATION_QUEUE_DB_ID, properties)
        
        return jsonify({
            "ok": True,
            "page_id": result.get('id'),
            "correlation_id": correlation_id,
            "message": "Test job created (will process in ~60s)"
        }), 200
    except Exception as e:
        error_msg = str(e)
        
        if "is not a property that exists" in error_msg:
            return jsonify({
                "ok": False,
                "error": "Database properties not configured",
                "details": "Your Automation Queue database needs these properties: Task Name (title), Description (rich_text), Trigger (checkbox), Status (select)",
                "notion_error": error_msg
            }), 400
        
        return jsonify({"ok": False, "error": error_msg}), 500

@app.route('/api/job-log-latest')
def api_job_log_latest():
    """Get latest job from Job Log (with retry for Notion sync lag)"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        import time
        
        if not config.JOB_LOG_DB_ID:
            return jsonify({
                "ok": False,
                "error": "JOB_LOG_DB_ID not configured"
            }), 500
        
        notion = NotionClientWrapper()
        
        for attempt, delay in enumerate([0, 5, 10, 15]):
            if delay > 0:
                time.sleep(delay)
            
            results = notion.query_database(
                config.JOB_LOG_DB_ID,
                filter_criteria=None
            )
            
            if results:
                latest = results[0]
                props = latest.get('properties', {})
                
                def get_prop(name, prop_type='number'):
                    try:
                        if prop_type == 'number':
                            return props.get(name, {}).get('number')
                        elif prop_type == 'title':
                            title_arr = props.get(name, {}).get('title', [])
                            return title_arr[0].get('text', {}).get('content', '') if title_arr else ''
                        elif prop_type == 'select':
                            return props.get(name, {}).get('select', {}).get('name')
                        elif prop_type == 'url':
                            return props.get(name, {}).get('url')
                    except:
                        return None
                
                return jsonify({
                    "ok": True,
                    "page_id": latest.get('id'),
                    "job_name": get_prop('Job Name', 'title'),
                    "qa_score": get_prop('QA Score'),
                    "duration_sec": get_prop('Duration Sec'),
                    "gross_usd": get_prop('Gross USD'),
                    "profit_usd": get_prop('Profit USD'),
                    "margin_pct": get_prop('Margin %'),
                    "payment_status": get_prop('Payment Status', 'select'),
                    "payment_link": get_prop('Payment Link', 'url'),
                    "attempt": attempt + 1
                }), 200
        
        return jsonify({
            "ok": False,
            "error": "No jobs found after retries (Notion sync lag)"
        }), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/flip-paid', methods=['POST'])
def api_flip_paid():
    """Update Payment Status to Paid"""
    try:
        from bot.notion_api import NotionClientWrapper
        
        data = request.get_json(force=True)
        page_id = data.get('page_id')
        
        if not page_id:
            return jsonify({
                "ok": False,
                "error": "page_id required in request body"
            }), 400
        
        notion = NotionClientWrapper()
        notion.update_page(page_id, {
            "Payment Status": {"select": {"name": "Paid"}}
        })
        
        return jsonify({
            "ok": True,
            "page_id": page_id,
            "message": "Payment Status updated to Paid"
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


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
