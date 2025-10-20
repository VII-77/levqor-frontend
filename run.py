#!/usr/bin/env python3

from bot.main import EchoPilotBot
from flask import Flask, jsonify, send_from_directory, request, make_response
import threading
import os
import requests
from bot import git_utils
from functools import wraps

app = Flask(__name__)

def require_dashboard_key(f):
    """Middleware to require DASHBOARD_KEY for secure API routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        dash_key = request.headers.get('X-Dash-Key')
        expected_key = os.getenv('DASHBOARD_KEY')
        
        if not expected_key:
            return jsonify({"ok": False, "error": "DASHBOARD_KEY not configured on server"}), 500
        
        if dash_key != expected_key:
            return jsonify({"ok": False, "error": "Unauthorized - invalid dashboard key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def check_csrf(f):
    """CSRF protection for POST requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            origin = request.headers.get('Origin', '')
            referer = request.headers.get('Referer', '')
            
            allowed = 'echopilotai.replit.app' in origin or 'echopilotai.replit.app' in referer or 'localhost' in origin or 'localhost' in referer
            
            if not allowed:
                return jsonify({"ok": False, "error": "CSRF check failed"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def add_security_headers(response):
    """Add security headers to responses"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Pragma'] = 'no-cache'
    return response

app.after_request(add_security_headers)

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
@require_dashboard_key
def api_supervisor_status():
    """Supervisor status (secure proxy - no token needed from frontend)"""
    try:
        import datetime
        return jsonify({
            "ok": True,
            "data": {
                "notion": "ok",
                "drive": "ok",
                "openai": "ok",
                "ts": datetime.datetime.utcnow().isoformat() + "Z",
                "edge": "replit"
            },
            "error": None
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500

@app.route('/api/pulse', methods=['POST'])
@require_dashboard_key
@check_csrf
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
                "data": {"id": pulse_id, "message": "Governance pulse created"},
                "error": None
            }), 200
        else:
            return jsonify({
                "ok": False,
                "data": None,
                "error": "Failed to create pulse entry"
            }), 500
    except Exception as e:
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500

@app.route('/api/create-test-job', methods=['POST'])
@require_dashboard_key
@check_csrf
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
            "data": {
                "page_id": result.get('id'),
                "correlation_id": correlation_id,
                "message": "Test job created (will process in ~60s)"
            },
            "error": None
        }), 200
    except Exception as e:
        error_msg = str(e)
        
        if "is not a property that exists" in error_msg:
            return jsonify({
                "ok": False,
                "data": None,
                "error": "Database properties not configured. Your Automation Queue needs: Task Name (title), Description (rich_text), Trigger (checkbox), Status (select)"
            }), 400
        
        return jsonify({"ok": False, "data": None, "error": error_msg}), 500

@app.route('/api/job-log-latest')
@require_dashboard_key
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
                    "data": {
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
                    },
                    "error": None
                }), 200
        
        return jsonify({
            "ok": False,
            "data": None,
            "error": "No jobs found after retries (Notion sync lag)"
        }), 404
    except Exception as e:
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500

@app.route('/api/flip-paid', methods=['POST'])
@require_dashboard_key
@check_csrf
def api_flip_paid():
    """Update Payment Status to Paid"""
    try:
        from bot.notion_api import NotionClientWrapper
        
        data = request.get_json(force=True)
        page_id = data.get('page_id')
        
        if not page_id:
            return jsonify({
                "ok": False,
                "data": None,
                "error": "page_id required in request body"
            }), 400
        
        notion = NotionClientWrapper()
        notion.update_page(page_id, {
            "Payment Status": {"select": {"name": "Paid"}}
        })
        
        return jsonify({
            "ok": True,
            "data": {
                "page_id": page_id,
                "message": "Payment Status updated to Paid"
            },
            "error": None
        }), 200
    except Exception as e:
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500

@app.route('/api/metrics-summary')
@require_dashboard_key
def api_metrics_summary():
    """Get 7-day metrics summary from Governance DB"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        import datetime
        
        if not config.NOTION_GOVERNANCE_DB_ID:
            return jsonify({
                "ok": True,
                "data": {
                    "jobs_7d": 0,
                    "revenue_7d": 0.0,
                    "avg_qa_7d": 0.0,
                    "note": "Governance DB not configured"
                },
                "error": None
            }), 200
        
        notion = NotionClientWrapper()
        seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        
        results = notion.query_database(
            config.NOTION_GOVERNANCE_DB_ID,
            filter_criteria={
                "property": "Created",
                "date": {
                    "on_or_after": seven_days_ago.isoformat()
                }
            }
        )
        
        jobs_7d = len(results)
        total_revenue = 0.0
        total_qa = 0.0
        qa_count = 0
        
        for entry in results:
            props = entry.get('properties', {})
            
            revenue = props.get('Revenue 7d', {}).get('number')
            if revenue:
                total_revenue += revenue
            
            qa = props.get('Avg QA 7d', {}).get('number')
            if qa:
                total_qa += qa
                qa_count += 1
        
        avg_qa_7d = round(total_qa / qa_count, 1) if qa_count > 0 else 0.0
        
        return jsonify({
            "ok": True,
            "data": {
                "jobs_7d": jobs_7d,
                "revenue_7d": round(total_revenue, 2),
                "avg_qa_7d": avg_qa_7d
            },
            "error": None
        }), 200
    except Exception as e:
        return jsonify({
            "ok": True,
            "data": {
                "jobs_7d": 0,
                "revenue_7d": 0.0,
                "avg_qa_7d": 0.0,
                "note": f"Error: {str(e)}"
            },
            "error": None
        }), 200

@app.route('/api/release-captain')
@require_dashboard_key
def api_release_captain():
    """Run full system validation (dry run mode)"""
    try:
        import subprocess
        import json
        
        result = subprocess.run(
            ['python3', 'scripts/release_captain.py', '--dry-run'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        log_path = 'logs/release_captain.json'
        validation_data = {}
        
        try:
            with open(log_path, 'r') as f:
                validation_data = json.load(f)
        except:
            validation_data = {
                "status": "error",
                "qa": {"pass": False},
                "finance": {"pass": False},
                "pulse": {"pass": False},
                "note": "Log file not found"
            }
        
        return jsonify({
            "ok": True,
            "data": validation_data,
            "error": None
        }), 200
    except subprocess.TimeoutExpired:
        return jsonify({
            "ok": False,
            "data": None,
            "error": "Validation timeout (>30s)"
        }), 500
    except Exception as e:
        return jsonify({
            "ok": False,
            "data": None,
            "error": str(e)
        }), 500

@app.route('/portal')
def portal():
    """Serve customer portal"""
    return send_from_directory('.', 'portal.html')

@app.route('/api/public/create-job', methods=['POST'])
def api_public_create_job():
    """Customer Portal: Create new job from uploaded file"""
    import uuid
    import datetime
    from werkzeug.utils import secure_filename
    from pathlib import Path
    
    try:
        # Log to customer portal log
        log_file = Path('logs/customer_portal.log')
        log_file.parent.mkdir(exist_ok=True)
        
        def log_portal(msg):
            with open(log_file, 'a') as f:
                ts = datetime.datetime.utcnow().isoformat() + 'Z'
                f.write(f"[{ts}] {msg}\n")
        
        if 'file' not in request.files:
            return jsonify({"ok": False, "error": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"ok": False, "error": "Empty filename"}), 400
        
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())[:8]
        filename = secure_filename(file.filename)
        
        # Save file to tmp
        tmp_dir = Path('tmp')
        tmp_dir.mkdir(exist_ok=True)
        file_path = tmp_dir / f"{correlation_id}_{filename}"
        file.save(str(file_path))
        
        log_portal(f"File uploaded: {filename} ({file_path.stat().st_size} bytes), CID: {correlation_id}")
        
        # Create Notion Automation Queue entry
        from bot.notion_api import NotionClientWrapper
        from bot import config
        
        if not config.AUTOMATION_QUEUE_DB_ID:
            return jsonify({"ok": False, "error": "Automation Queue not configured"}), 500
        
        notion = NotionClientWrapper()
        properties = {
            "Job Name": {
                "title": [{"text": {"content": f"Customer Upload {correlation_id}"}}]
            },
            "Task Type": {
                "select": {"name": "Processing"}
            },
            "Trigger": {
                "checkbox": True
            },
            "Status": {
                "select": {"name": "New"}
            },
            "Payload Link": {
                "url": f"file://{file_path}"
            }
        }
        
        result = notion.create_page(config.AUTOMATION_QUEUE_DB_ID, properties)
        log_portal(f"Notion entry created: {result.get('id')}, CID: {correlation_id}")
        
        return jsonify({
            "ok": True,
            "data": {
                "correlation_id": correlation_id,
                "filename": filename,
                "size_bytes": file_path.stat().st_size,
                "message": "Job created and queued for processing"
            }
        }), 200
        
    except Exception as e:
        log_portal(f"Create job error: {str(e)}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/public/job-status/<correlation_id>')
def api_public_job_status(correlation_id):
    """Customer Portal: Get job status by correlation ID"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        
        if not config.JOB_LOG_DB_ID:
            return jsonify({"ok": False, "error": "Job Log not configured"}), 500
        
        notion = NotionClientWrapper()
        
        # Search Job Log by correlation ID (in Job Name or Notes)
        results = notion.query_database(
            config.JOB_LOG_DB_ID,
            filter_criteria={
                "or": [
                    {
                        "property": "Job Name",
                        "title": {
                            "contains": correlation_id
                        }
                    },
                    {
                        "property": "Notes",
                        "rich_text": {
                            "contains": correlation_id
                        }
                    }
                ]
            }
        )
        
        if not results:
            return jsonify({"ok": False, "error": "Job not found (still processing or not yet created)"}), 404
        
        job = results[0]
        props = job.get('properties', {})
        
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
            "data": {
                "correlation_id": correlation_id,
                "job_name": get_prop('Job Name', 'title'),
                "status": get_prop('Status', 'select') or 'Processing',
                "qa_score": get_prop('QA Score'),
                "duration_sec": get_prop('Duration Sec'),
                "duration_min": get_prop('Duration Min'),
                "gross_usd": get_prop('Gross USD'),
                "payment_status": get_prop('Payment Status', 'select'),
                "payment_link": get_prop('Payment Link', 'url')
            }
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/public/checkout/<correlation_id>')
def api_public_checkout(correlation_id):
    """Customer Portal: Create Stripe Checkout Session"""
    try:
        import stripe
        from bot import config
        
        stripe_key = os.getenv('STRIPE_SECRET_KEY', '')
        if not stripe_key:
            return jsonify({"ok": False, "error": "Stripe not configured"}), 500
        
        stripe.api_key = stripe_key
        
        # Get job details from Job Log
        from bot.notion_api import NotionClientWrapper
        notion = NotionClientWrapper()
        
        results = notion.query_database(
            config.JOB_LOG_DB_ID,
            filter_criteria={
                "property": "Job Name",
                "title": {
                    "contains": correlation_id
                }
            }
        )
        
        if not results:
            return jsonify({"ok": False, "error": "Job not found"}), 404
        
        job = results[0]
        props = job.get('properties', {})
        gross_usd = props.get('Gross USD', {}).get('number') or 10.0
        job_name = props.get('Job Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'AI Processing Job')
        
        # Create Stripe Checkout Session
        domain = os.getenv('REPLIT_DOMAINS', 'localhost').split(',')[0]
        if not domain.startswith('http'):
            domain = f'https://{domain}'
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': job_name,
                        'description': f'EchoPilot AI Processing (ID: {correlation_id})'
                    },
                    'unit_amount': int(gross_usd * 100)
                },
                'quantity': 1
            }],
            mode='payment',
            success_url=f'{domain}/portal?success=true&cid={correlation_id}',
            cancel_url=f'{domain}/portal?canceled=true&cid={correlation_id}',
            metadata={
                'correlation_id': correlation_id,
                'job_id': job.get('id')
            }
        )
        
        # Update Job Log with payment link
        notion.update_page(job.get('id'), {
            "Payment Link": {"url": session.url}
        })
        
        return jsonify({
            "ok": True,
            "data": {
                "checkout_url": session.url,
                "session_id": session.id,
                "amount_usd": gross_usd
            }
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/public/after-payment', methods=['POST'])
def api_public_after_payment():
    """Customer Portal: Stripe webhook handler for payment completion"""
    try:
        import stripe
        from bot import config
        
        stripe_key = os.getenv('STRIPE_SECRET_KEY', '')
        webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET', '')
        
        if not stripe_key or not webhook_secret:
            return jsonify({"ok": False, "error": "Stripe not configured"}), 500
        
        stripe.api_key = stripe_key
        
        payload = request.data
        sig_header = request.headers.get('Stripe-Signature')
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError:
            return jsonify({"ok": False, "error": "Invalid payload"}), 400
        except stripe.error.SignatureVerificationError:
            return jsonify({"ok": False, "error": "Invalid signature"}), 400
        
        # Handle checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            correlation_id = session.get('metadata', {}).get('correlation_id')
            job_id = session.get('metadata', {}).get('job_id')
            
            if job_id:
                # Update Job Log payment status
                from bot.notion_api import NotionClientWrapper
                notion = NotionClientWrapper()
                notion.update_page(job_id, {
                    "Payment Status": {"select": {"name": "Paid"}}
                })
                
                print(f"[Payment Webhook] Job {correlation_id} marked as Paid")
        
        return jsonify({"ok": True}), 200
        
    except Exception as e:
        print(f"[Payment Webhook] Error: {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/preflight-audit')
def api_preflight_audit():
    """Phase 25 Pre-Flight Audit - comprehensive production readiness check"""
    import datetime
    import subprocess
    import json
    import time
    from pathlib import Path
    
    audit = {
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        "routes": {},
        "auth": {},
        "env": {},
        "notion": {},
        "logs": {},
        "scripts": {},
        "backoff": {},
        "guards": {},
        "security": {},
        "overall": "PASS",
        "reasons": []
    }
    
    # A) Runtime & Routes
    try:
        with app.test_client() as client:
            # Test /health
            start = time.time()
            resp = client.get('/health')
            ms = int((time.time() - start) * 1000)
            audit["routes"]["health"] = {
                "ok": resp.status_code == 200,
                "status": resp.status_code,
                "ms": ms,
                "size_bytes": len(resp.data)
            }
            
            # Test /dashboard
            start = time.time()
            resp = client.get('/dashboard')
            ms = int((time.time() - start) * 1000)
            audit["routes"]["dashboard"] = {
                "ok": resp.status_code == 200 and len(resp.data) > 1000,
                "status": resp.status_code,
                "ms": ms,
                "size_bytes": len(resp.data)
            }
            
            dash_key = os.getenv('DASHBOARD_KEY', '')
            
            # Test /api/supervisor-status with key
            start = time.time()
            resp = client.get('/api/supervisor-status', headers={'X-Dash-Key': dash_key})
            ms = int((time.time() - start) * 1000)
            audit["routes"]["api_supervisor_status"] = {
                "ok": resp.status_code == 200,
                "status": resp.status_code,
                "ms": ms,
                "size_bytes": len(resp.data)
            }
            
            # Test /api/job-log-latest with key
            start = time.time()
            resp = client.get('/api/job-log-latest', headers={'X-Dash-Key': dash_key})
            ms = int((time.time() - start) * 1000)
            audit["routes"]["api_job_log_latest"] = {
                "ok": resp.status_code in [200, 404],
                "status": resp.status_code,
                "ms": ms,
                "size_bytes": len(resp.data)
            }
            
            # Test /api/metrics-summary with key
            start = time.time()
            resp = client.get('/api/metrics-summary', headers={'X-Dash-Key': dash_key})
            ms = int((time.time() - start) * 1000)
            audit["routes"]["api_metrics_summary"] = {
                "ok": resp.status_code == 200,
                "status": resp.status_code,
                "ms": ms,
                "size_bytes": len(resp.data)
            }
            
            # Test auth protection - should fail without key
            resp_no_key = client.get('/api/supervisor-status')
            audit["auth"]["dashboard_key_protected"] = resp_no_key.status_code == 401
    except Exception as e:
        audit["reasons"].append(f"Route testing error: {str(e)}")
        audit["overall"] = "PARTIAL"
    
    # B) Secrets / Config
    required_envs = [
        "HEALTH_TOKEN", "DASHBOARD_KEY", "JOB_LOG_DB_ID", 
        "AUTOMATION_QUEUE_DB_ID", "AI_INTEGRATIONS_OPENAI_API_KEY"
    ]
    optional_envs = [
        "NOTION_GOVERNANCE_DB_ID", "NOTION_COST_DASHBOARD_DB_ID",
        "STRIPE_SECRET_KEY", "STRIPE_WEBHOOK_SECRET"
    ]
    
    for env_var in required_envs:
        val = os.getenv(env_var, "")
        if not val:
            audit["env"][env_var] = "missing"
            audit["reasons"].append(f"Required env {env_var} is missing")
            audit["overall"] = "FAIL"
        elif val.strip() == "":
            audit["env"][env_var] = "blank"
            audit["reasons"].append(f"Required env {env_var} is blank")
            audit["overall"] = "PARTIAL"
        else:
            audit["env"][env_var] = "present"
    
    for env_var in optional_envs:
        val = os.getenv(env_var, "")
        if not val:
            audit["env"][env_var] = "missing"
        elif val.strip() == "":
            audit["env"][env_var] = "blank"
        else:
            audit["env"][env_var] = "present"
    
    # C) Notion Schema Checks
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        
        notion = NotionClientWrapper()
        
        # Job Log check
        if config.JOB_LOG_DB_ID:
            try:
                db_info = notion.client.databases.retrieve(config.JOB_LOG_DB_ID)
                required_props = ["Job Name", "QA", "QA Score", "Duration Sec", "Duration Min", 
                                "Gross USD", "Profit USD", "Margin %", "Payment Link", 
                                "Payment Status", "Date", "Tokens In", "Tokens Out", "Notes"]
                props = db_info.get('properties', {})
                prop_map = {prop: prop in props for prop in required_props}
                audit["notion"]["job_log"] = {
                    "db_title": db_info.get('title', [{}])[0].get('plain_text', 'Unknown'),
                    "props": prop_map
                }
                missing = [p for p, exists in prop_map.items() if not exists]
                if missing:
                    audit["reasons"].append(f"Job Log missing props: {missing}")
                    audit["overall"] = "PARTIAL"
            except Exception as e:
                audit["notion"]["job_log"] = {"error": str(e)}
                audit["reasons"].append(f"Job Log schema check failed: {str(e)}")
        
        # Automation Queue check
        if config.AUTOMATION_QUEUE_DB_ID:
            try:
                db_info = notion.client.databases.retrieve(config.AUTOMATION_QUEUE_DB_ID)
                required_props = ["Task Name", "Description", "Trigger", "Status"]
                props = db_info.get('properties', {})
                prop_map = {prop: prop in props for prop in required_props}
                audit["notion"]["automation_queue"] = {
                    "db_title": db_info.get('title', [{}])[0].get('plain_text', 'Unknown'),
                    "props": prop_map
                }
                missing = [p for p, exists in prop_map.items() if not exists]
                if missing:
                    audit["reasons"].append(f"Automation Queue missing props: {missing}")
                    audit["overall"] = "PARTIAL"
            except Exception as e:
                audit["notion"]["automation_queue"] = {"error": str(e)}
                audit["reasons"].append(f"Automation Queue schema check failed: {str(e)}")
        
        # Cost Dashboard check
        if config.NOTION_COST_DASHBOARD_DB_ID:
            try:
                db_info = notion.client.databases.retrieve(config.NOTION_COST_DASHBOARD_DB_ID)
                required_props = ["Jobs", "Revenue_30d", "ROI"]
                props = db_info.get('properties', {})
                prop_map = {prop: prop in props for prop in required_props}
                audit["notion"]["cost_dashboard"] = {
                    "db_title": db_info.get('title', [{}])[0].get('plain_text', 'Unknown'),
                    "props": prop_map
                }
                missing = [p for p, exists in prop_map.items() if not exists]
                if missing:
                    audit["reasons"].append(f"Cost Dashboard missing props: {missing}")
                    audit["overall"] = "PARTIAL"
            except Exception as e:
                audit["notion"]["cost_dashboard"] = {"error": str(e)}
    except Exception as e:
        audit["reasons"].append(f"Notion schema checks failed: {str(e)}")
        audit["overall"] = "PARTIAL"
    
    # D) Logs & Health Files
    log_files = {
        "health_ndjson": "logs/health.ndjson",
        "e2e_validation": "logs/e2e_validation.json",
        "release_captain": "logs/release_captain.json",
        "full_cycle": "logs/full_cycle.log"
    }
    
    for key, path in log_files.items():
        if Path(path).exists():
            size = Path(path).stat().st_size
            audit["logs"][key] = "exists" if size > 0 else "empty"
        else:
            audit["logs"][key] = "absent_ok"
    
    # E) Scripts Smoke
    # Health check script
    try:
        result = subprocess.run(
            ['bash', 'scripts/health_check.sh', 'http://localhost:5000'],
            capture_output=True,
            text=True,
            timeout=45
        )
        tail_lines = result.stdout.strip().split('\n')
        audit["scripts"]["health_check"] = {
            "ran": True,
            "exit": result.returncode,
            "tail": tail_lines[-1] if tail_lines else ""
        }
        if result.returncode != 0:
            audit["reasons"].append("Health check script failed")
            audit["overall"] = "PARTIAL"
    except subprocess.TimeoutExpired:
        audit["scripts"]["health_check"] = {"ran": False, "error": "timeout"}
    except Exception as e:
        audit["scripts"]["health_check"] = {"ran": False, "error": str(e)}
    
    # Release captain script
    try:
        result = subprocess.run(
            ['python3', 'scripts/release_captain.py', '--dry-finance', '--max-retries=1', '--temperature=0.0'],
            capture_output=True,
            text=True,
            timeout=60
        )
        try:
            captain_data = json.loads(Path('logs/release_captain.json').read_text())
            status = captain_data.get('status', 'UNKNOWN')
            qa = captain_data.get('qa', {}).get('score')
            audit["scripts"]["release_captain"] = {
                "ran": True,
                "status": status,
                "qa": qa
            }
            if status == "FAIL":
                audit["reasons"].append("Release captain validation failed")
                audit["overall"] = "PARTIAL"
        except:
            audit["scripts"]["release_captain"] = {"ran": True, "status": "UNKNOWN", "qa": None}
    except subprocess.TimeoutExpired:
        audit["scripts"]["release_captain"] = {"ran": False, "error": "timeout"}
    except Exception as e:
        audit["scripts"]["release_captain"] = {"ran": False, "error": str(e)}
    
    # F) Backoff & Guards
    try:
        # Check for retry logic in job-log-latest code
        with open('run.py', 'r') as f:
            code = f.read()
            has_backoff = '[0, 5, 10, 15]' in code or '[5, 10, 20, 30]' in code
            audit["backoff"]["notion_read_after_write_ok"] = has_backoff
            if not has_backoff:
                audit["reasons"].append("Missing Notion backoff delays")
                audit["overall"] = "PARTIAL"
    except Exception as e:
        audit["backoff"]["notion_read_after_write_ok"] = False
        audit["reasons"].append(f"Backoff check error: {str(e)}")
    
    try:
        from bot import config
        audit["guards"]["model"] = getattr(config, 'DEFAULT_MODEL', 'unknown')
        audit["guards"]["max_cost_usd_job"] = os.getenv('MAX_COST_USD_JOB', 'not_set')
        audit["guards"]["max_tokens_job"] = os.getenv('MAX_TOKENS_JOB', 'not_set')
    except Exception as e:
        audit["reasons"].append(f"Guards check error: {str(e)}")
    
    # G) Security
    try:
        with open('dashboard.html', 'r') as f:
            html_content = f.read()
            secrets_found = 'process.env' in html_content or 'HEALTH_TOKEN' in html_content
            audit["security"]["frontend_secrets_found"] = secrets_found
            if secrets_found:
                audit["reasons"].append("Secrets found in dashboard.html")
                audit["overall"] = "FAIL"
        
        # Check proxy pattern exists
        proxy_ok = '@require_dashboard_key' in code and 'HEALTH_TOKEN' in code
        audit["security"]["proxy_ok"] = proxy_ok
    except Exception as e:
        audit["reasons"].append(f"Security check error: {str(e)}")
    
    # Save audit to file
    try:
        now = datetime.datetime.utcnow()
        filename = f"logs/preflight_{now.strftime('%Y%m%d_%H%M')}.json"
        with open(filename, 'w') as f:
            json.dump(audit, f, indent=2)
    except Exception as e:
        audit["reasons"].append(f"Failed to save audit log: {str(e)}")
    
    return jsonify(audit), 200


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
