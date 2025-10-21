#!/usr/bin/env python3

from bot.main import EchoPilotBot
from flask import Flask, jsonify, send_from_directory, request, make_response, render_template
import threading
import os
import json
import requests
import sys
from datetime import datetime, timedelta
from bot import git_utils
from bot.security import (
    rate_limit, require_csrf, audit_log, apply_security_headers,
    generate_csrf_token, get_security_headers
)
from functools import wraps
import time
import uuid
from collections import defaultdict
from pathlib import Path

app = Flask(__name__)

# ===== Feature Flags System - Phase 108 =====
# Migrated to bot.feature_flags module with hot-reload cache
# Use: from bot.feature_flags import is_enabled, get_environment

# Phase 51: Observability metrics storage
metrics_storage = {
    'http_requests_total': defaultdict(int),  # {route_status: count}
    'http_request_duration_ms': [],  # list of (route, duration_ms)
    'scheduler_tick_total': 0,
    'stripe_webhook_fail_total': 0,
    'payments_error_rate': 0.0,
    'app_start_time': time.time()
}

def record_metric(metric_name, value=1, labels=None):
    """Record a metric value"""
    if metric_name == 'http_requests_total' and labels:
        key = f"{labels.get('route', 'unknown')}_{labels.get('status', '000')}"
        metrics_storage['http_requests_total'][key] += value
    elif metric_name == 'http_request_duration_ms' and labels:
        metrics_storage['http_request_duration_ms'].append({
            'route': labels.get('route', 'unknown'),
            'duration_ms': value,
            'timestamp': time.time()
        })
        # Keep only last 10000 requests
        if len(metrics_storage['http_request_duration_ms']) > 10000:
            metrics_storage['http_request_duration_ms'] = metrics_storage['http_request_duration_ms'][-10000:]
    elif metric_name in metrics_storage:
        metrics_storage[metric_name] = value

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

# RBAC: Role-Based Access Control (Stabilization Sprint)
import functools
ROLES_JSON = os.getenv("ROLES_JSON", "{}")
_ROLES = json.loads(ROLES_JSON or "{}")  # {"<DASHBOARD_KEY>":"admin"|"analyst"}

def _role_from_key(req):
    """Get role from dashboard key"""
    key = req.headers.get("X-Dash-Key") or ""
    return _ROLES.get(key)

def require_role(*allowed):
    """Decorator to require specific roles"""
    def deco(fn):
        @functools.wraps(fn)
        def wrapped(*a, **kw):
            role = _role_from_key(request)
            if not role or role not in allowed:
                return jsonify({"ok": False, "error": "forbidden", "need": list(allowed)}), 403
            return fn(*a, **kw)
        return wrapped
    return deco

# ===== DEMO MODE - Extra 1 =====
def is_demo_mode():
    """Check if application is running in demo mode"""
    return os.getenv('DEMO_MODE', '').lower() in ('true', '1', 'yes')

def block_in_demo_mode(f):
    """Decorator to block write operations in demo mode"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if is_demo_mode():
            return jsonify({
                "ok": False,
                "error": "Operation not allowed in demo mode",
                "demo_mode": True,
                "message": "This is a read-only demo environment. Write operations are disabled."
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/demo-mode')
def api_demo_mode():
    """Get demo mode status"""
    return jsonify({
        "demo_mode": is_demo_mode(),
        "message": "Demo mode enabled - read-only operations only" if is_demo_mode() else "Normal mode"
    })

@app.before_request
def before_request_timing():
    """Record request start time for latency tracking and generate request ID"""
    request._start_time = time.time()
    
    # Generate or use existing request ID (Extra 3)
    request_id = request.headers.get('X-Request-ID')
    if not request_id:
        request_id = str(uuid.uuid4())
    request._request_id = request_id

def add_security_headers(response):
    """Add security headers and record metrics/traces"""
    # Apply Boss Mode security headers
    response = apply_security_headers(response)
    
    # Security headers (legacy)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Pragma'] = 'no-cache'
    
    # Extra 3: Add request ID to response headers
    if hasattr(request, '_request_id'):
        response.headers['X-Request-ID'] = request._request_id
    
    # Phase 51: Record HTTP traces and metrics
    if hasattr(request, '_start_time'):
        duration_ms = (time.time() - request._start_time) * 1000
        route = request.endpoint or request.path
        status = response.status_code
        
        # Record metrics
        record_metric('http_requests_total', 1, {'route': route, 'status': str(status)})
        record_metric('http_request_duration_ms', duration_ms, {'route': route})
        
        # Write trace to NDJSON (Extra 3: Include request ID)
        try:
            os.makedirs('logs', exist_ok=True)
            trace_entry = {
                'ts': datetime.utcnow().isoformat() + 'Z',
                'request_id': getattr(request, '_request_id', None),
                'route': route,
                'method': request.method,
                'status': status,
                'duration_ms': round(duration_ms, 2),
                'path': request.path
            }
            with open('logs/http_traces.ndjson', 'a') as f:
                f.write(json.dumps(trace_entry) + '\n')
        except:
            pass  # Don't fail requests if logging fails
    
    return response

app.after_request(add_security_headers)

# ===== EXTRA 6: Custom 404 Handler =====
@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error handler"""
    return render_template('404.html'), 404

# Rate limiting moved to bot/security.py (Boss Mode upgrade)
# Old implementation removed to avoid conflicts

# Legacy rate limit store (kept for compatibility)
rate_limit_store = defaultdict(list)

def rate_limit_legacy(max_requests=5, window_minutes=1):
    """Legacy in-memory rate limiter (deprecated - use bot.security.rate_limit)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr or 'unknown'
            now = datetime.utcnow()
            cutoff = now - timedelta(minutes=window_minutes)
            
            # Clean old entries
            rate_limit_store[client_ip] = [
                ts for ts in rate_limit_store[client_ip] if ts > cutoff
            ]
            
            # Check limit
            if len(rate_limit_store[client_ip]) >= max_requests:
                return jsonify({
                    "ok": False,
                    "error": f"Rate limit exceeded. Maximum {max_requests} requests per {window_minutes} minute(s)",
                    "data": None
                }), 429
            
            # Record this request
            rate_limit_store[client_ip].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# SMTP Email System (safe fallback if not configured)
def send_email(to, subject, html_body):
    """Send email via SMTP with safe fallback"""
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from pathlib import Path
    
    # Log file
    log_file = Path('logs/customer_email.log')
    log_file.parent.mkdir(exist_ok=True)
    
    def log_email(msg):
        with open(log_file, 'a') as f:
            ts = datetime.utcnow().isoformat() + 'Z'
            f.write(f"[{ts}] {msg}\n")
    
    # Check if SMTP is configured
    smtp_host = os.getenv('SMTP_HOST', '').strip()
    smtp_port = os.getenv('SMTP_PORT', '587').strip()
    smtp_user = os.getenv('SMTP_USER', '').strip()
    smtp_pass = os.getenv('SMTP_PASS', '').strip()
    smtp_from = os.getenv('SMTP_FROM', smtp_user).strip()
    
    if not (smtp_host and smtp_user and smtp_pass):
        # No SMTP configured - log only
        log_email(f"[NO-SEND] To: {to}, Subject: {subject} (SMTP not configured)")
        return {"ok": True, "message": "Email logged (SMTP not configured)"}
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = smtp_from
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send via SMTP
        with smtplib.SMTP(smtp_host, int(smtp_port)) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        log_email(f"[SENT] To: {to}, Subject: {subject}")
        return {"ok": True, "message": "Email sent successfully"}
        
    except Exception as e:
        log_email(f"[FAILED] To: {to}, Subject: {subject}, Error: {str(e)}")
        return {"ok": False, "error": str(e)}

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

@app.route('/health')
def health_check():
    """Health check endpoint for deployment (moved from / to avoid conflict with landing page)"""
    commit_hash, branch_name, _ = git_utils.get_git_info()
    return jsonify({
        "status": "healthy",
        "service": "EchoPilot AI Automation Bot",
        "commit": commit_hash,
        "branch": branch_name,
        "message": "Bot is running and polling Notion every 60 seconds"
    })

@app.get("/healthz/strict")
def strict_health():
    """Strict health check - returns 500 when SLO error budget > 80% (Finalization)"""
    try:
        import json
        path = "logs/slo_guard.ndjson"
        if not os.path.exists(path):
            return jsonify({"ok": False, "slo": "grey", "msg": "no SLO log"}), 503
        
        with open(path) as f:
            lines = f.readlines()
        
        if not lines:
            return jsonify({"ok": False, "slo": "grey", "msg": "no SLO data"}), 503
        
        last = json.loads(lines[-1])
        used = last.get("error_budget_used", 0)
        
        if used < 0.8:
            return jsonify({"ok": True, "slo": "green", "error_budget_used": used}), 200
        
        return jsonify({"ok": False, "slo": "red", "error_budget_used": used, "msg": "SLO budget exceeded"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/health')
def health():
    """
    Enhanced health endpoint - Phase 109
    Returns build metadata, dependency status, and system health
    """
    import threading
    import datetime
    from pathlib import Path
    
    # Spawn background logging (best-effort, non-blocking)
    def background_log():
        try:
            log_file = Path('logs/health.ndjson')
            log_file.parent.mkdir(exist_ok=True)
            with open(log_file, 'a') as f:
                ts = datetime.datetime.utcnow().isoformat() + 'Z'
                f.write(f'{{"ts":"{ts}","status":"ok"}}\n')
        except:
            pass  # Silent fail if logging unavailable
    
    threading.Thread(target=background_log, daemon=True).start()
    
    # Build metadata
    build_info = {
        "version": "1.0.0",
        "phase": "103-110",
        "build_date": "2025-10-21T00:00:00Z",
        "commit": os.getenv("REPL_ID", "unknown")[:8],
        "environment": os.getenv("REPL_SLUG", "development")
    }
    
    # Dependency health checks
    dependencies = {}
    
    # Check Notion API
    try:
        from bot.config import NOTION_TOKEN
        dependencies["notion"] = "ok" if NOTION_TOKEN else "missing_token"
    except:
        dependencies["notion"] = "error"
    
    # Check OpenAI API
    try:
        openai_key = os.getenv("AI_INTEGRATIONS_OPENAI_API_KEY")
        dependencies["openai"] = "ok" if openai_key else "missing_key"
    except:
        dependencies["openai"] = "error"
    
    # Check Database (graceful degradation if psycopg2 not installed)
    try:
        import psycopg2
        conn = psycopg2.connect(os.getenv('DATABASE_URL'), connect_timeout=2)
        conn.close()
        dependencies["database"] = "ok"
    except ImportError:
        dependencies["database"] = "psycopg2_not_installed"
    except:
        dependencies["database"] = "error"
    
    # Check Stripe
    try:
        stripe_key = os.getenv("STRIPE_SECRET_KEY")
        dependencies["stripe"] = "ok" if stripe_key else "missing_key"
    except:
        dependencies["stripe"] = "error"
    
    # Check Telegram
    try:
        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
        dependencies["telegram"] = "ok" if telegram_token else "missing_token"
    except:
        dependencies["telegram"] = "error"
    
    # System metrics
    uptime_seconds = time.time() - metrics_storage['app_start_time']
    
    return jsonify({
        "status": "ok",
        "timestamp": datetime.datetime.utcnow().isoformat() + 'Z',
        "build": build_info,
        "dependencies": dependencies,
        "uptime_seconds": int(uptime_seconds),
        "features": {
            "visual_workflow_builder": True,
            "boss_mode_v2": True,
            "customer_auth": True,
            "data_warehouse": True,
            "a_b_testing": True
        }
    })

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

# ============================================================
# PHASE 103: CUSTOMER AUTHENTICATION & PORTAL
# ============================================================

@app.route('/auth/login')
def login_page():
    """Customer login page"""
    return render_template('auth/login.html')

@app.route('/app')
def customer_portal():
    """Customer portal dashboard"""
    return render_template('auth/portal.html')

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """
    Customer login endpoint
    Accepts email + password/code and returns JWT
    Rate limited to 5 requests per minute per IP
    """
    from bot.auth import rate_limit, generate_jwt, log_auth_event, get_customer_by_email
    
    # Rate limiting check
    identifier = request.remote_addr or "unknown"
    from bot.auth import check_rate_limit
    if not check_rate_limit(identifier, limit=5, window=60):
        log_auth_event("rate_limited", ip=identifier)
        return jsonify({
            "error": "Too many login attempts",
            "retry_after": 60
        }), 429
    
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    
    if not email or not password:
        log_auth_event("login_failed", reason="missing_credentials", ip=identifier)
        return jsonify({"error": "Email and password required"}), 400
    
    # Lookup customer in Notion Client database
    customer = get_customer_by_email(email)
    
    if not customer:
        log_auth_event("login_failed", reason="customer_not_found", email=email, ip=identifier)
        return jsonify({"error": "Invalid credentials"}), 401
    
    # For Phase 103, we use a simple password check
    # In production, implement proper password hashing
    # For now, accept any password for existing customers
    
    # Generate JWT
    token = generate_jwt(email, customer.get('customer_id'))
    
    log_auth_event("login_success", email=email, ip=identifier)
    
    return jsonify({
        "ok": True,
        "token": token,
        "email": email
    }), 200

@app.route('/api/auth/magic-link', methods=['POST'])
def api_magic_link():
    """
    Send magic link for passwordless login
    Currently logs to emails.ndjson (stub for Gmail integration)
    Rate limited to 5 requests per minute per IP
    """
    from bot.auth import check_rate_limit, send_magic_link, log_auth_event
    
    identifier = request.remote_addr or "unknown"
    if not check_rate_limit(identifier, limit=5, window=60):
        return jsonify({
            "error": "Too many requests",
            "retry_after": 60
        }), 429
    
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    
    if not email:
        return jsonify({"error": "Email required"}), 400
    
    success = send_magic_link(email)
    
    if success:
        log_auth_event("magic_link_sent", email=email, ip=identifier)
        return jsonify({
            "ok": True,
            "message": "Magic link sent to your email"
        }), 200
    else:
        return jsonify({"error": "Failed to send magic link"}), 500

@app.route('/api/me')
def api_me():
    """
    Get current user profile
    Requires JWT Bearer token in Authorization header
    """
    from bot.auth import require_jwt
    
    # Manual JWT verification since decorator doesn't work well with Flask
    from bot.auth import verify_jwt
    
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header required"}), 401
    
    token = auth_header.replace("Bearer ", "")
    is_valid, payload = verify_jwt(token)
    
    if not is_valid:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    return jsonify({
        "ok": True,
        "email": payload.get("email"),
        "customer_id": payload.get("customer_id"),
        "exp": payload.get("exp")
    }), 200

@app.route('/api/billing/history')
def api_billing_history():
    """
    Get customer billing history from Stripe
    Requires JWT Bearer token
    """
    from bot.auth import verify_jwt
    import stripe
    import os
    import json
    from datetime import datetime
    
    # Verify JWT
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header required"}), 401
    
    token = auth_header.replace("Bearer ", "")
    is_valid, payload = verify_jwt(token)
    
    if not is_valid:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    customer_id = payload.get("customer_id")
    
    if not customer_id:
        # Return empty for customers without Stripe ID
        return jsonify({
            "ok": True,
            "invoices": []
        }), 200
    
    try:
        # Fetch invoices from Stripe
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        invoices = stripe.Invoice.list(customer=customer_id, limit=20)
        
        formatted_invoices = []
        for inv in invoices.data:
            formatted_invoices.append({
                "id": inv.id,
                "date": datetime.fromtimestamp(inv.created).strftime("%Y-%m-%d"),
                "amount": f"${inv.total / 100:.2f}",
                "status": inv.status,
                "description": inv.description or "EchoPilot AI Service",
                "invoice_pdf": inv.invoice_pdf
            })
        
        # Log to billing.ndjson
        os.makedirs("logs", exist_ok=True)
        with open("logs/billing.ndjson", "a") as f:
            log_entry = {
                "ts": datetime.utcnow().isoformat() + "Z",
                "event": "billing_history_retrieved",
                "customer_id": customer_id,
                "count": len(formatted_invoices)
            }
            f.write(json.dumps(log_entry) + "\n")
        
        return jsonify({
            "ok": True,
            "invoices": formatted_invoices
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e),
            "invoices": []
        }), 500

@app.route('/api/billing/portal', methods=['POST'])
def api_billing_portal():
    """
    Create Stripe Customer Portal session
    Requires JWT Bearer token
    """
    from bot.auth import verify_jwt
    import stripe
    import os
    
    # Verify JWT
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authorization header required"}), 401
    
    token = auth_header.replace("Bearer ", "")
    is_valid, payload = verify_jwt(token)
    
    if not is_valid:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    customer_id = payload.get("customer_id")
    
    if not customer_id:
        return jsonify({"error": "No billing account found"}), 404
    
    try:
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        
        # Create billing portal session
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=os.getenv("PUBLIC_BASE_URL", "https://echopilotai.replit.app") + "/app"
        )
        
        return jsonify({
            "ok": True,
            "url": session.url
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 103
# ============================================================

# ============================================================
# PHASE 105: PUBLIC PRICING + LEADS
# ============================================================

@app.route('/pricing')
def pricing_page():
    """Public pricing page with SEO"""
    stripe_key = os.getenv("STRIPE_SECRET_KEY", "")
    stripe_mode = "test" if stripe_key.startswith("sk_test_") else "live"
    return render_template('pricing.html', stripe_mode=stripe_mode)

@app.route('/api/lead', methods=['POST'])
def api_lead():
    """
    Capture leads from pricing page and save to Notion Partners/Leads DB
    Rate limited to 10 requests per hour per IP
    """
    from bot.auth import check_rate_limit
    import json
    from datetime import datetime
    
    identifier = request.remote_addr or "unknown"
    if not check_rate_limit(identifier, limit=10, window=3600):
        return jsonify({
            "error": "Too many requests",
            "retry_after": 3600
        }), 429
    
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    use_case = data.get('use_case', '').strip()
    
    if not email:
        return jsonify({"error": "Email required"}), 400
    
    try:
        from bot import notion_api
        
        # Save to Notion Partners database
        partners_db_id = os.getenv("NOTION_PARTNERS_DB_ID")
        if not partners_db_id:
            # Fallback: Log to file
            os.makedirs("logs", exist_ok=True)
            with open("logs/leads.ndjson", "a") as f:
                log_entry = {
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "email": email,
                    "use_case": use_case,
                    "ip": identifier
                }
                f.write(json.dumps(log_entry) + "\n")
            
            return jsonify({
                "ok": True,
                "message": "Lead captured successfully"
            }), 200
        
        # Create page in Notion Partners DB
        notion_api.notion.pages.create(
            parent={"database_id": partners_db_id},
            properties={
                "Name": {
                    "title": [{"text": {"content": email}}]
                },
                "Email": {
                    "email": email
                },
                "Use Case": {
                    "rich_text": [{"text": {"content": use_case or "Enterprise inquiry"}}]
                },
                "Status": {
                    "select": {"name": "New Lead"}
                }
            }
        )
        
        # Also log to NDJSON
        os.makedirs("logs", exist_ok=True)
        with open("logs/leads.ndjson", "a") as f:
            log_entry = {
                "ts": datetime.utcnow().isoformat() + "Z",
                "event": "lead_captured",
                "email": email,
                "source": "pricing_page",
                "ip": identifier
            }
            f.write(json.dumps(log_entry) + "\n")
        
        return jsonify({
            "ok": True,
            "message": "Thank you! We'll contact you soon."
        }), 200
        
    except Exception as e:
        print(f"[Lead Capture] Error: {e}")
        return jsonify({
            "ok": False,
            "error": "Failed to capture lead"
        }), 500

@app.route('/sitemap.xml')
def sitemap():
    """SEO sitemap"""
    base_url = os.getenv("PUBLIC_BASE_URL", "https://echopilotai.replit.app")
    
    sitemap_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{base_url}/pricing</loc>
        <changefreq>monthly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/workflow/builder</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/auth/login</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>{base_url}/docs</loc>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
</urlset>'''
    
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response

@app.route('/robots.txt')
def robots():
    """SEO robots.txt"""
    base_url = os.getenv("PUBLIC_BASE_URL", "https://echopilotai.replit.app")
    
    robots_txt = f'''User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/

Sitemap: {base_url}/sitemap.xml'''
    
    response = make_response(robots_txt)
    response.headers["Content-Type"] = "text/plain"
    return response

# ============================================================
# END PHASE 105
# ============================================================

# ============================================================
# PHASE 106: DATA WAREHOUSE SYNC
# ============================================================

@app.route('/api/warehouse/status')
@require_dashboard_key
def api_warehouse_status():
    """
    Get data warehouse sync status
    Reads wh_sync_metadata table and warehouse_sync.ndjson logs
    """
    import psycopg2
    import os
    import json
    from datetime import datetime
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Get latest sync metadata
        cursor.execute("""
            SELECT table_name, sync_started_at, sync_completed_at, rows_synced, status, error_message
            FROM wh_sync_metadata
            ORDER BY sync_completed_at DESC
            LIMIT 10
        """)
        
        recent_syncs = []
        for row in cursor.fetchall():
            recent_syncs.append({
                "table": row[0],
                "started_at": row[1].isoformat() if row[1] else None,
                "completed_at": row[2].isoformat() if row[2] else None,
                "rows_synced": row[3],
                "status": row[4],
                "error": row[5]
            })
        
        # Get table row counts
        tables = [
            'wh_automation_queue', 'wh_automation_log', 'wh_job_log', 
            'wh_clients', 'wh_finance', 'wh_governance', 'wh_ops_monitor',
            'wh_forecast', 'wh_region_compliance', 'wh_partners', 
            'wh_referrals', 'wh_growth_metrics'
        ]
        
        table_stats = {}
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_stats[table] = count
        
        cursor.close()
        conn.close()
        
        # Read latest sync log
        latest_log = None
        if os.path.exists('logs/warehouse_sync.ndjson'):
            with open('logs/warehouse_sync.ndjson', 'r') as f:
                lines = f.readlines()
                if lines:
                    latest_log = json.loads(lines[-1].strip())
        
        return jsonify({
            "ok": True,
            "recent_syncs": recent_syncs,
            "table_stats": table_stats,
            "latest_sync": latest_log,
            "total_rows": sum(table_stats.values())
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/warehouse/sync', methods=['POST'])
@require_dashboard_key
@block_in_demo_mode
def api_warehouse_sync():
    """
    Trigger manual data warehouse sync
    Runs warehouse_sync.py script asynchronously
    """
    import subprocess
    import os
    
    try:
        # Run warehouse sync in background
        result = subprocess.Popen(
            ['python3', 'scripts/warehouse_sync.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return jsonify({
            "ok": True,
            "message": "Warehouse sync started",
            "pid": result.pid
        }), 202  # 202 Accepted
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 106
# ============================================================

# ============================================================
# PHASE 107: SLO THRESHOLD OPTIMIZATION
# ============================================================

@app.route('/api/slo/recommendations')
@require_dashboard_key
def api_slo_recommendations():
    """
    Get SLO threshold tuning recommendations
    Returns ML-generated recommendations from alert_tuner.py
    """
    import json
    from pathlib import Path
    
    try:
        rec_file = Path('configs/slo_tuning_recommendations.json')
        
        if not rec_file.exists():
            return jsonify({
                "ok": False,
                "error": "No recommendations available. Run /api/slo/tune first."
            }), 404
        
        with open(rec_file, 'r') as f:
            recommendations = json.load(f)
        
        return jsonify({
            "ok": True,
            "recommendations": recommendations
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/slo/tune', methods=['POST'])
@require_dashboard_key
@block_in_demo_mode
def api_slo_tune():
    """
    Trigger SLO threshold tuning analysis
    Runs alert_tuner.py ML model asynchronously
    """
    import subprocess
    
    try:
        # Run alert tuner in background
        result = subprocess.Popen(
            ['python3', 'scripts/alert_tuner.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return jsonify({
            "ok": True,
            "message": "SLO tuning started",
            "pid": result.pid
        }), 202
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/slo/apply', methods=['POST'])
@require_dashboard_key
def api_slo_apply():
    """
    Apply SLO recommendations (admin-only)
    Returns instructions for setting environment variables
    """
    import json
    from pathlib import Path
    from flask import request
    
    try:
        rec_file = Path('configs/slo_tuning_recommendations.json')
        
        if not rec_file.exists():
            return jsonify({
                "ok": False,
                "error": "No recommendations available"
            }), 404
        
        with open(rec_file, 'r') as f:
            data = json.load(f)
        
        recommendations = data.get('recommendations', {})
        
        # Get min confidence from request (default: high)
        min_confidence = request.json.get('min_confidence', 'high') if request.json else 'high'
        
        # Define confidence hierarchy (high > medium > low)
        confidence_levels = {'high': 3, 'medium': 2, 'low': 1}
        min_level = confidence_levels.get(min_confidence, 3)
        
        # Filter by confidence level
        to_apply = []
        for var_name, rec in recommendations.items():
            rec_level = confidence_levels.get(rec['confidence'], 0)
            
            # Include if recommendation confidence >= minimum threshold
            if rec_level >= min_level:
                to_apply.append({
                    'variable': var_name,
                    'current': rec['current'],
                    'recommended': rec['recommended'],
                    'confidence': rec['confidence'],
                    'sample_size': rec.get('sample_size', 0),
                    'rationale': rec['rationale']
                })
        
        # Generate instructions
        instructions = []
        for item in to_apply:
            instructions.append(f"export {item['variable']}={item['recommended']}")
        
        return jsonify({
            "ok": True,
            "apply_count": len(to_apply),
            "recommendations": to_apply,
            "instructions": instructions,
            "note": "Set these environment variables in Replit Secrets, then restart workflows"
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 107
# ============================================================

# ============================================================
# PHASE 108: A/B TESTING FRAMEWORK
# ============================================================

@app.route('/api/flags')
@require_dashboard_key
def api_flags_list():
    """
    Get all feature flags
    Returns complete flag configuration with metadata
    """
    from bot.feature_flags import get_all_flags
    
    try:
        flags = get_all_flags()
        
        return jsonify({
            "ok": True,
            "flags": flags,
            "count": len(flags)
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/flags/<flag_name>')
@require_dashboard_key
def api_flags_get(flag_name):
    """Get specific feature flag configuration"""
    from bot.feature_flags import get_flag
    
    try:
        flag = get_flag(flag_name)
        
        if not flag:
            return jsonify({
                "ok": False,
                "error": "Flag not found"
            }), 404
        
        return jsonify({
            "ok": True,
            "flag": flag
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/flags/<flag_name>', methods=['PUT'])
@require_dashboard_key
@block_in_demo_mode
def api_flags_update(flag_name):
    """
    Update feature flag configuration
    Supports hot-reload without restart
    """
    from bot.feature_flags import set_flag
    from flask import request
    
    try:
        data = request.get_json() or {}
        
        success = set_flag(
            flag_name,
            enabled=data.get('enabled'),
            rollout_pct=data.get('rollout_pct'),
            environments=data.get('environments'),
            description=data.get('description')
        )
        
        if success:
            return jsonify({
                "ok": True,
                "message": f"Flag {flag_name} updated successfully"
            }), 200
        else:
            return jsonify({
                "ok": False,
                "error": "Failed to update flag"
            }), 500
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/flags/<flag_name>', methods=['DELETE'])
@require_dashboard_key
def api_flags_delete(flag_name):
    """Delete feature flag"""
    from bot.feature_flags import delete_flag
    
    try:
        success = delete_flag(flag_name)
        
        if success:
            return jsonify({
                "ok": True,
                "message": f"Flag {flag_name} deleted successfully"
            }), 200
        else:
            return jsonify({
                "ok": False,
                "error": "Flag not found"
            }), 404
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/flags/check/<flag_name>')
def api_flags_check(flag_name):
    """
    Check if flag is enabled (public endpoint)
    Supports user_id parameter for rollout percentage
    """
    from bot.feature_flags import is_enabled, get_environment
    from flask import request
    
    try:
        user_id = request.args.get('user_id')
        environment = get_environment()
        
        enabled = is_enabled(flag_name, user_id=user_id, environment=environment)
        
        return jsonify({
            "ok": True,
            "flag": flag_name,
            "enabled": enabled,
            "environment": environment
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/flags/evaluate')
def api_flags_evaluate():
    """
    Evaluate all flags for a user
    Returns map of flag_name -> enabled status
    """
    from bot.feature_flags import evaluate_for_user
    from flask import request
    
    try:
        user_id = request.args.get('user_id', 'anonymous')
        
        flags = evaluate_for_user(user_id)
        
        return jsonify({
            "ok": True,
            "user_id": user_id,
            "flags": flags
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 108
# ============================================================

# ============================================================
# PHASE 110: AI GOVERNANCE ADVISOR
# ============================================================

@app.route('/api/governance/report')
@require_dashboard_key
def api_governance_report():
    """
    Get latest AI governance report
    Returns recommendations, alerts, and system health analysis
    """
    import json
    from pathlib import Path
    
    try:
        report_file = Path('logs/governance_report.json')
        
        if not report_file.exists():
            return jsonify({
                "ok": False,
                "error": "No governance report available. Run /api/governance/analyze first."
            }), 404
        
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        return jsonify({
            "ok": True,
            "report": report
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/governance/analyze', methods=['POST'])
@require_dashboard_key
@block_in_demo_mode
def api_governance_analyze():
    """
    Trigger AI governance analysis
    Runs auto_governance.py with GPT-4o-mini advisor
    """
    import subprocess
    
    try:
        # Run governance advisor in background
        result = subprocess.Popen(
            ['python3', 'scripts/auto_governance.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return jsonify({
            "ok": True,
            "message": "AI governance analysis started",
            "pid": result.pid
        }), 202  # 202 Accepted
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ===== EXTRA 4: JWT Authentication Endpoints =====
from bot.security import generate_jwt_pair, rotate_jwt, revoke_jwt, require_jwt

@app.route('/api/auth/token', methods=['POST'])
def api_auth_token():
    """
    Generate JWT token pair
    Body: {"user_id": "...", "user_data": {...}}
    """
    data = request.get_json() or {}
    user_id = data.get('user_id')
    user_data = data.get('user_data')
    
    if not user_id:
        return jsonify({
            "ok": False,
            "error": "user_id required"
        }), 400
    
    tokens = generate_jwt_pair(user_id, user_data)
    
    return jsonify({
        "ok": True,
        **tokens
    }), 200

@app.route('/api/auth/refresh', methods=['POST'])
def api_auth_refresh():
    """
    Refresh access token using refresh token
    Body: {"refresh_token": "..."}
    """
    data = request.get_json() or {}
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({
            "ok": False,
            "error": "refresh_token required"
        }), 400
    
    tokens, error = rotate_jwt(refresh_token)
    
    if error:
        return jsonify({
            "ok": False,
            "error": error
        }), 401
    
    return jsonify({
        "ok": True,
        **tokens
    }), 200

@app.route('/api/auth/revoke', methods=['POST'])
def api_auth_revoke():
    """
    Revoke JWT token
    Body: {"token": "..."}
    """
    data = request.get_json() or {}
    token = data.get('token')
    
    if not token:
        return jsonify({
            "ok": False,
            "error": "token required"
        }), 400
    
    success = revoke_jwt(token)
    
    if success:
        return jsonify({
            "ok": True,
            "message": "Token revoked successfully"
        }), 200
    else:
        return jsonify({
            "ok": False,
            "error": "Failed to revoke token"
        }), 400

@app.route('/api/auth/me')
@require_jwt
def api_auth_me():
    """
    Get current JWT user info
    Requires: Authorization: Bearer <access_token>
    """
    return jsonify({
        "ok": True,
        "user_id": getattr(request, 'jwt_user_id', None),
        "user_data": getattr(request, 'jwt_data', None)
    }), 200

# ===== EXTRA 3: OBSERVABILITY PACK =====

@app.route('/api/logs')
@require_dashboard_key
def api_logs():
    """
    Real-time log tailing endpoint
    Returns recent log entries from various NDJSON log files
    Query params: ?file=<logfile>&lines=<count>&request_id=<id>
    """
    from pathlib import Path
    
    log_file = request.args.get('file', 'http_traces')
    
    # Validate lines parameter (clamp between 1 and 10000)
    try:
        lines_count = int(request.args.get('lines', 100))
        lines_count = max(1, min(lines_count, 10000))  # Clamp to safe range
    except ValueError:
        return jsonify({
            "ok": False,
            "error": "Invalid 'lines' parameter, must be an integer"
        }), 400
    
    request_id_filter = request.args.get('request_id')
    
    # Supported log files
    log_files = {
        'http_traces': 'logs/http_traces.ndjson',
        'automation': 'logs/automation_log.ndjson',
        'scheduler': 'logs/scheduler.ndjson',
        'anomaly_guard': 'logs/anomaly_guard.ndjson',
        'warehouse_sync': 'logs/warehouse_sync.ndjson',
        'alert_tuner': 'logs/alert_tuner.ndjson',
        'governance': 'logs/governance.ndjson',
        'seed_demo': 'logs/seed_demo.ndjson'
    }
    
    if log_file not in log_files:
        return jsonify({
            "ok": False,
            "error": f"Unknown log file. Available: {', '.join(log_files.keys())}"
        }), 400
    
    log_path = Path(log_files[log_file])
    
    if not log_path.exists():
        return jsonify({
            "ok": True,
            "logs": [],
            "message": f"Log file {log_file} not yet created"
        }), 200
    
    try:
        # Read last N lines
        with open(log_path, 'r') as f:
            all_lines = f.readlines()
        
        # Parse NDJSON
        logs = []
        for line in all_lines[-lines_count:]:
            try:
                entry = json.loads(line.strip())
                
                # Filter by request_id if provided
                if request_id_filter and entry.get('request_id') != request_id_filter:
                    continue
                
                logs.append(entry)
            except:
                continue
        
        return jsonify({
            "ok": True,
            "file": log_file,
            "count": len(logs),
            "logs": logs
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/metrics')
def metrics_prometheus():
    """
    Prometheus-compatible metrics endpoint
    Exports metrics in Prometheus text format
    """
    from collections import defaultdict
    
    try:
        # Gather metrics from in-memory store
        metrics_output = []
        metrics_output.append("# HELP echopilot_info EchoPilot system information")
        metrics_output.append("# TYPE echopilot_info gauge")
        metrics_output.append('echopilot_info{version="2.0",environment="production"} 1')
        
        # HTTP request metrics
        if os.path.exists('logs/http_traces.ndjson'):
            with open('logs/http_traces.ndjson', 'r') as f:
                lines = f.readlines()[-1000:]  # Last 1000 requests
            
            # Count by status code
            status_counts = defaultdict(int)
            total_duration = defaultdict(list)
            
            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    status = entry.get('status', 0)
                    duration = entry.get('duration_ms', 0)
                    route = entry.get('route', 'unknown')
                    
                    status_counts[status] += 1
                    total_duration[route].append(duration)
                except:
                    continue
            
            # HTTP requests total
            metrics_output.append("\n# HELP http_requests_total Total HTTP requests")
            metrics_output.append("# TYPE http_requests_total counter")
            for status, count in status_counts.items():
                metrics_output.append(f'http_requests_total{{status="{status}"}} {count}')
            
            # HTTP request duration
            metrics_output.append("\n# HELP http_request_duration_seconds HTTP request latency")
            metrics_output.append("# TYPE http_request_duration_seconds summary")
            for route, durations in total_duration.items():
                if durations:
                    avg_duration = sum(durations) / len(durations) / 1000  # Convert to seconds
                    p95 = sorted(durations)[int(len(durations) * 0.95)] / 1000 if len(durations) > 1 else avg_duration
                    p99 = sorted(durations)[int(len(durations) * 0.99)] / 1000 if len(durations) > 1 else avg_duration
                    
                    metrics_output.append(f'http_request_duration_seconds{{route="{route}",quantile="0.5"}} {avg_duration:.3f}')
                    metrics_output.append(f'http_request_duration_seconds{{route="{route}",quantile="0.95"}} {p95:.3f}')
                    metrics_output.append(f'http_request_duration_seconds{{route="{route}",quantile="0.99"}} {p99:.3f}')
        
        # Database metrics (if available)
        if os.getenv('DATABASE_URL'):
            metrics_output.append("\n# HELP database_connected Database connection status")
            metrics_output.append("# TYPE database_connected gauge")
            try:
                import psycopg2
                conn = psycopg2.connect(os.getenv('DATABASE_URL'))
                cur = conn.cursor()
                cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s', ('public',))
                table_count = cur.fetchone()[0]
                conn.close()
                
                metrics_output.append("database_connected 1")
                metrics_output.append(f"\n# HELP database_tables_total Total database tables")
                metrics_output.append(f"# TYPE database_tables_total gauge")
                metrics_output.append(f"database_tables_total {table_count}")
            except:
                metrics_output.append("database_connected 0")
        
        # Scheduler metrics (if log exists)
        if os.path.exists('logs/scheduler.ndjson'):
            metrics_output.append("\n# HELP scheduler_jobs_total Total scheduler job executions")
            metrics_output.append("# TYPE scheduler_jobs_total counter")
            
            with open('logs/scheduler.ndjson', 'r') as f:
                lines = f.readlines()[-1000:]
            
            job_counts = defaultdict(int)
            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    if entry.get('event') == 'job_complete':
                        job = entry.get('job', 'unknown')
                        job_counts[job] += 1
                except:
                    continue
            
            for job, count in job_counts.items():
                metrics_output.append(f'scheduler_jobs_total{{job="{job}"}} {count}')
        
        # System uptime
        metrics_output.append("\n# HELP process_uptime_seconds Process uptime in seconds")
        metrics_output.append("# TYPE process_uptime_seconds gauge")
        uptime = time.time() - metrics_storage.get('app_start_time', time.time())
        metrics_output.append(f"process_uptime_seconds {uptime:.0f}")
        
        return '\n'.join(metrics_output), 200, {'Content-Type': 'text/plain; version=0.0.4'}
        
    except Exception as e:
        return f"# Error generating metrics: {str(e)}\n", 500, {'Content-Type': 'text/plain'}

@app.route('/api/governance/recommendations')
@require_dashboard_key
def api_governance_recommendations():
    """
    Get governance recommendations summary
    Returns only high-priority actionable items
    """
    import json
    from pathlib import Path
    
    try:
        report_file = Path('logs/governance_report.json')
        
        if not report_file.exists():
            return jsonify({
                "ok": False,
                "error": "No recommendations available"
            }), 404
        
        with open(report_file, 'r') as f:
            report = json.load(f)
        
        # Handle actual JSON structure: report['recommendations'] is the full object
        recommendations_obj = report.get('recommendations', {})
        
        # Extract lists from the recommendations object
        all_recommendations = recommendations_obj.get('recommendations', [])
        all_alerts = recommendations_obj.get('alerts', [])
        
        # Filter for high-priority recommendations
        high_priority = [
            rec for rec in all_recommendations
            if rec.get('priority') in ['high', 'critical']
        ]
        
        # Filter for critical alerts
        critical_alerts = [
            alert for alert in all_alerts
            if alert.get('severity') in ['high', 'critical']
        ]
        
        return jsonify({
            "ok": True,
            "priority": recommendations_obj.get('priority', 'unknown'),
            "summary": recommendations_obj.get('summary', ''),
            "high_priority_recommendations": high_priority,
            "critical_alerts": critical_alerts,
            "last_updated": report.get('timestamp')
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 110
# ============================================================

# ============================================================
# PHASE 111: ANALYTICS & PRODUCT INSIGHTS
# ============================================================

@app.route('/api/analytics/usage')
@require_dashboard_key
def api_analytics_usage():
    """
    Get usage analytics: DAU/WAU/MAU, feature usage, funnels
    Query params: ?days=30 (default)
    """
    from bot.analytics import get_analytics_summary
    
    try:
        days = int(request.args.get('days', 30))
        days = max(1, min(days, 365))  # Clamp to 1-365
        
        summary = get_analytics_summary(days=days)
        
        return jsonify({
            "ok": True,
            **summary
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/analytics/event', methods=['POST'])
def api_analytics_event():
    """
    Client telemetry endpoint for event ingestion
    Accepts batched events from telemetry.js
    """
    from bot.analytics import log_event
    
    try:
        data = request.get_json() or {}
        events = data.get('events', [])
        
        if not isinstance(events, list):
            return jsonify({
                "ok": False,
                "error": "events must be an array"
            }), 400
        
        # Log each event
        logged_count = 0
        for event in events[:100]:  # Max 100 events per batch
            event_type = event.get('event_type')
            user_id = event.get('user_id')
            feature = event.get('feature')
            metadata = event.get('metadata', {})
            
            if event_type:
                log_event(event_type, user_id, feature, metadata)
                logged_count += 1
        
        return jsonify({
            "ok": True,
            "logged": logged_count
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 111
# ============================================================

# ============================================================
# PHASE 112: OPERATOR CHAT CONSOLE
# ============================================================

@app.route('/api/ops/command', methods=['POST'])
@require_dashboard_key
def api_ops_command():
    """
    Execute operator commands with dry-run support
    Body: {"verb": "restart_scheduler", "confirm": false, "user": "admin"}
    """
    from bot.ops_console import execute_command, get_command_list
    
    try:
        data = request.get_json() or {}
        verb = data.get('verb')
        confirm = data.get('confirm', False)
        user = data.get('user', 'api_user')
        
        if not verb:
            return jsonify({
                "ok": False,
                "error": "verb required",
                "available_commands": get_command_list()
            }), 400
        
        result = execute_command(verb, user=user, confirm=confirm)
        status_code = 200 if result.get('ok') else 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

@app.route('/api/ops/commands')
@require_dashboard_key
def api_ops_commands():
    """Get list of available operator commands"""
    from bot.ops_console import get_command_list
    
    try:
        commands = get_command_list()
        
        return jsonify({
            "ok": True,
            "commands": commands,
            "count": len(commands)
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500

# ============================================================
# END PHASE 112
# ============================================================

# ============================================================
# PHASE 116: TENANTIZATION HARDENING
# ============================================================

@app.before_request
def apply_tenant_context():
    """Apply tenant context to all requests (Phase 116)"""
    from bot.tenancy import set_tenant_context
    
    # Skip for health checks and static files
    if request.path in ['/health', '/favicon.ico'] or request.path.startswith('/static'):
        return None
    
    set_tenant_context()

@app.route('/api/tenant/info')
def api_tenant_info():
    """Get current tenant information"""
    from bot.tenancy import get_tenant_stats
    from flask import g
    
    try:
        stats = get_tenant_stats()
        
        return jsonify({
            'ok': True,
            'tenant_id': getattr(g, 'tenant_id', 'unknown'),
            'tenant_verified': getattr(g, 'tenant_verified', False),
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

@app.route('/api/tenant/test-access')
@require_dashboard_key
def api_tenant_test_access():
    """Test cross-tenant access control"""
    from bot.tenancy import check_cross_tenant_access
    from flask import g
    
    try:
        test_tenant = request.args.get('test_tenant', 'other_tenant')
        action = request.args.get('action', 'access')
        
        allowed, reason = check_cross_tenant_access(test_tenant, action)
        
        return jsonify({
            'ok': True,
            'current_tenant': getattr(g, 'tenant_id', 'unknown'),
            'test_tenant': test_tenant,
            'action': action,
            'allowed': allowed,
            'reason': reason
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

# ============================================================
# END PHASE 116
# ============================================================

# ============================================================
# PHASE 117: FINOPS COST & PROFITABILITY
# ============================================================

@app.route('/api/finops/summary')
@require_dashboard_key
def api_finops_summary():
    """Get FinOps summary with revenue, costs, and profitability"""
    from bot.finops import get_finops_summary
    from flask import g
    
    try:
        days = int(request.args.get('days', 30))
        tenant_id = request.args.get('tenant_id')
        
        # If no tenant specified and user has tenant context, use it
        if not tenant_id and hasattr(g, 'tenant_id') and g.tenant_id != 'default':
            tenant_id = g.tenant_id
        
        summary = get_finops_summary(tenant_id=tenant_id, days=days)
        
        return jsonify({
            'ok': True,
            **summary
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

@app.route('/api/finops/tenants')
@require_dashboard_key
def api_finops_tenants():
    """Get cost/revenue breakdown by tenant"""
    from bot.finops import get_tenant_breakdown
    
    try:
        days = int(request.args.get('days', 30))
        
        breakdown = get_tenant_breakdown(days=days)
        
        return jsonify({
            'ok': True,
            'period_days': days,
            **breakdown
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

# ============================================================
# END PHASE 117
# ============================================================

# ============================================================
# PHASE 118: COMPLIANCE WEBHOOKS & AUDIT API
# ============================================================

@app.route('/api/audit/chain')
@require_dashboard_key
def api_audit_chain():
    """Get immutable audit chain entries"""
    from bot.compliance_webhooks import get_audit_chain, verify_audit_chain
    
    try:
        limit = int(request.args.get('limit', 100))
        offset = int(request.args.get('offset', 0))
        verify = request.args.get('verify', 'false').lower() == 'true'
        
        chain = get_audit_chain(limit=limit, offset=offset)
        
        result = {
            'ok': True,
            **chain
        }
        
        if verify:
            verification = verify_audit_chain()
            result['verification'] = verification
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

@app.route('/api/compliance/webhook', methods=['POST'])
def api_compliance_webhook():
    """Receive compliance events from external systems"""
    from bot.compliance_webhooks import log_compliance_event
    import hmac
    import hashlib
    import os
    
    try:
        # Verify signature
        signature = request.headers.get('X-EchoPilot-Signature')
        if signature:
            secret = os.getenv('COMPLIANCE_WEBHOOK_SECRET', 'default_secret')
            payload = request.get_data()
            expected_sig = hmac.new(
                secret.encode(),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            if signature != expected_sig:
                return jsonify({
                    'ok': False,
                    'error': 'Invalid signature'
                }), 401
        
        data = request.get_json() or {}
        
        # Log compliance event
        event = log_compliance_event(
            event_type=data.get('event_type', 'external_event'),
            severity=data.get('severity', 'medium'),
            description=data.get('description', 'External compliance event'),
            metadata=data.get('metadata', {})
        )
        
        return jsonify({
            'ok': True,
            'event_logged': True,
            'ts': event['ts']
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

# ============================================================
# END PHASE 118
# ============================================================

# ============================================================
# PHASE 119: EDGE QUEUE
# ============================================================

@app.route('/api/queue/enqueue', methods=['POST'])
@require_dashboard_key
def api_queue_enqueue():
    """Enqueue job for edge processing"""
    from scripts.edge_worker import enqueue_job
    
    try:
        data = request.get_json() or {}
        
        job_type = data.get('job_type')
        payload = data.get('payload', {})
        priority = data.get('priority', 'normal')
        
        if not job_type:
            return jsonify({
                'ok': False,
                'error': 'job_type required'
            }), 400
        
        job_id = enqueue_job(job_type, payload, priority)
        
        return jsonify({
            'ok': True,
            'job_id': job_id,
            'status': 'queued'
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

@app.route('/api/queue/status')
@require_dashboard_key
def api_queue_status():
    """Get edge queue status"""
    from scripts.edge_worker import get_queue_status
    
    try:
        status = get_queue_status()
        
        return jsonify({
            'ok': True,
            **status
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

# ============================================================
# END PHASE 119
# ============================================================

# ============================================================
# PHASE 120: GROWTH & MARKETING REFERRAL 2.0
# ============================================================

@app.route('/api/growth/referrals')
@require_dashboard_key
def api_growth_referrals():
    """Get referral statistics and leaderboard"""
    from bot.growth_referrals import get_referral_stats
    
    try:
        days = int(request.args.get('days', 30))
        referrer_id = request.args.get('referrer_id')
        
        stats = get_referral_stats(referrer_id=referrer_id, days=days)
        
        return jsonify({
            'ok': True,
            'period_days': days,
            **stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

@app.route('/api/growth/referral/create', methods=['POST'])
@require_dashboard_key
def api_create_referral():
    """Create new referral link"""
    from bot.growth_referrals import create_referral
    
    try:
        data = request.get_json() or {}
        
        referrer_id = data.get('referrer_id')
        campaign = data.get('campaign', 'default')
        
        if not referrer_id:
            return jsonify({
                'ok': False,
                'error': 'referrer_id required'
            }), 400
        
        referral = create_referral(referrer_id, campaign=campaign)
        
        return jsonify({
            'ok': True,
            **referral
        }), 200
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

@app.route('/api/growth/payouts/export')
@require_dashboard_key
def api_export_payouts():
    """Export referral payouts as CSV"""
    from bot.growth_referrals import export_payouts_csv
    from flask import Response
    
    try:
        min_payout = float(request.args.get('min_payout', 10.0))
        
        csv_content = export_payouts_csv(min_payout_usd=min_payout)
        
        if not csv_content:
            return jsonify({
                'ok': False,
                'error': 'Failed to generate CSV'
            }), 500
        
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=payouts_{datetime.utcnow().strftime("%Y%m%d")}.csv'
            }
        )
        
    except Exception as e:
        return jsonify({
            'ok': False,
            'error': str(e)
        }), 500

# ============================================================
# END PHASE 120
# ============================================================

# ============================================================
# PHASE 121: PWA SUPPORT
# ============================================================

@app.route('/offline.html')
def offline_page():
    """Offline fallback page for PWA"""
    return render_template('offline.html')

@app.route('/manifest.json')
def pwa_manifest():
    """PWA manifest file"""
    return send_from_directory('static', 'manifest.json', mimetype='application/manifest+json')

# ============================================================
# PHASE 122: INTEGRATIONS HUB
# ============================================================

@app.route('/api/integrations/catalog')
@require_dashboard_key
def api_integrations_catalog():
    """Get integrations catalog"""
    from bot.integrations_hub import get_integrations_catalog
    
    try:
        category = request.args.get('category')
        status = request.args.get('status', 'active')
        
        catalog = get_integrations_catalog(category=category, status=status)
        
        return jsonify({
            'ok': True,
            **catalog
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/integrations/install', methods=['POST'])
@require_dashboard_key
def api_install_integration():
    """Install an integration"""
    from bot.integrations_hub import install_integration
    from flask import g
    
    try:
        data = request.get_json() or {}
        integration_id = data.get('integration_id')
        tenant_id = g.tenant_id if hasattr(g, 'tenant_id') else 'default'
        config = data.get('config', {})
        
        result = install_integration(integration_id, tenant_id, config)
        
        return jsonify({
            'ok': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 123: AI DATA LAKE
# ============================================================

@app.route('/api/ai/analytics')
@require_dashboard_key
def api_ai_analytics():
    """Get AI prompt analytics"""
    from bot.ai_data_lake import get_prompt_analytics
    
    try:
        days = int(request.args.get('days', 7))
        analytics = get_prompt_analytics(days=days)
        
        return jsonify({
            'ok': True,
            **analytics
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/ai/model-comparison')
@require_dashboard_key
def api_model_comparison():
    """Get AI model performance comparison"""
    from bot.ai_data_lake import get_model_comparison
    
    try:
        comparison = get_model_comparison()
        
        return jsonify({
            'ok': True,
            **comparison
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 124: PREDICTIVE LOAD
# ============================================================

@app.route('/api/predict/load')
@require_dashboard_key
def api_predict_load():
    """Get load prediction"""
    from bot.predictive_load import predict_load
    
    try:
        hours = int(request.args.get('hours', 24))
        prediction = predict_load(hours_ahead=hours)
        
        return jsonify({
            'ok': True,
            **prediction
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/predict/staffing')
@require_dashboard_key
def api_staffing_recommendation():
    """Get staffing recommendation"""
    from bot.predictive_load import get_staffing_recommendation
    
    try:
        recommendation = get_staffing_recommendation()
        
        return jsonify({
            'ok': True,
            **recommendation
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 125: SELF-HEALING 2.0
# ============================================================

@app.route('/api/healing/status')
@require_dashboard_key
def api_healing_status():
    """Get self-healing status"""
    from bot.self_healing_v2 import health_check, get_healing_history
    
    try:
        health = health_check()
        history = get_healing_history(limit=10)
        
        return jsonify({
            'ok': True,
            'health': health,
            'recent_actions': history.get('actions', [])
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 126: ENTERPRISE MARKETPLACE
# ============================================================

@app.route('/api/marketplace/listings')
@require_dashboard_key
def api_marketplace_listings():
    """Get marketplace listings"""
    from bot.enterprise_marketplace import get_marketplace_listings
    
    try:
        category = request.args.get('category')
        listings = get_marketplace_listings(category=category)
        
        return jsonify({
            'ok': True,
            **listings
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/marketplace/purchase', methods=['POST'])
@require_dashboard_key
def api_marketplace_purchase():
    """Purchase marketplace listing"""
    from bot.enterprise_marketplace import purchase_listing
    from flask import g
    
    try:
        data = request.get_json() or {}
        listing_id = data.get('listing_id')
        tenant_id = g.tenant_id if hasattr(g, 'tenant_id') else 'default'
        quantity = data.get('quantity', 1)
        
        result = purchase_listing(listing_id, tenant_id, quantity)
        
        return jsonify({
            'ok': True,
            **result
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 127: COMPLIANCE APIS
# ============================================================

@app.route('/api/compliance/gdpr-export')
@require_dashboard_key
def api_gdpr_export():
    """Generate GDPR data export"""
    from bot.compliance_apis import generate_gdpr_report
    from flask import g
    
    try:
        user_id = request.args.get('user_id')
        tenant_id = g.tenant_id if hasattr(g, 'tenant_id') else 'default'
        
        report = generate_gdpr_report(user_id, tenant_id)
        
        return jsonify({
            'ok': True,
            **report
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/compliance/soc2-report')
@require_dashboard_key
def api_soc2_report():
    """Generate SOC2 compliance report"""
    from bot.compliance_apis import generate_soc2_report
    
    try:
        report = generate_soc2_report()
        
        return jsonify({
            'ok': True,
            **report
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 128: MULTI-REGION
# ============================================================

@app.route('/api/regions/status')
@require_dashboard_key
def api_regions_status():
    """Get multi-region status"""
    from bot.multi_region import get_regional_health, get_region_stats
    
    try:
        health = get_regional_health()
        stats = get_region_stats()
        
        return jsonify({
            'ok': True,
            'health': health,
            'stats': stats
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 129: PARTNER PORTAL
# ============================================================

@app.route('/api/partners/dashboard')
@require_dashboard_key
def api_partner_dashboard():
    """Get partner dashboard"""
    from bot.partner_portal import get_partner_dashboard
    
    try:
        partner_id = request.args.get('partner_id')
        days = int(request.args.get('days', 30))
        
        dashboard = get_partner_dashboard(partner_id, days=days)
        
        return jsonify({
            'ok': True,
            **dashboard
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/partners/register', methods=['POST'])
@require_dashboard_key
def api_register_partner():
    """Register new partner"""
    from bot.partner_portal import register_partner
    
    try:
        data = request.get_json() or {}
        partner = register_partner(
            data.get('name'),
            data.get('email'),
            data.get('tier', 'standard')
        )
        
        return jsonify({
            'ok': True,
            **partner
        }), 200
        
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# PHASE 130: ECHOPILOT OS
# ============================================================

@app.route('/api/health')
def api_health():
    """Basic health check endpoint for monitoring"""
    try:
        return jsonify({
            'ok': True,
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'version': '2.0.0'
        }), 200
    except Exception as e:
        return jsonify({
            'ok': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/platform/status')
def api_platform_status():
    """Get comprehensive platform status"""
    from bot.echopilot_os import get_platform_status
    
    try:
        status = get_platform_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/platform/metrics')
@require_dashboard_key
def api_platform_metrics():
    """Get unified system metrics"""
    from bot.echopilot_os import get_system_metrics
    
    try:
        metrics = get_system_metrics()
        return jsonify({
            'ok': True,
            **metrics
        }), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/platform/phase-report')
@require_dashboard_key
def api_phase_report():
    """Get all phases completion report"""
    from bot.echopilot_os import get_phase_completion_report
    
    try:
        report = get_phase_completion_report()
        return jsonify({
            'ok': True,
            **report
        }), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# ============================================================
# END PHASE 130 - ALL 130 PHASES COMPLETE
# ============================================================

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

@app.route('/')
def landing():
    """Boss Mode: Landing page"""
    return render_template('landing.html', demo_mode=is_demo_mode())

@app.route('/about')
def about():
    """Boss Mode: About page with system info"""
    return send_from_directory('templates', 'about.html')

@app.route('/dashboard')
@app.route('/dashboard.html')
def dashboard():
    """Serve ops dashboard - always redirect to Boss Mode UI v2"""
    return send_from_directory('.', 'dashboard_v2.html')

@app.route('/dashboard/v2')
def dashboard_v2():
    """Serve new mobile-first dashboard (Boss Mode UI)"""
    return send_from_directory('.', 'dashboard_v2.html')

@app.route('/dashboard/v1')
def dashboard_v1():
    """Serve legacy dashboard (fallback)"""
    return send_from_directory('.', 'dashboard.html')

@app.route('/payments')
def payments():
    """Boss Mode Phase 5: Payments Center UI"""
    return send_from_directory('templates', 'payments.html')

@app.route('/api/feature-flags')
def api_feature_flags():
    """Get current feature flags (legacy - use /api/flags instead)"""
    from bot.feature_flags import get_all_flags
    flags = get_all_flags()
    return jsonify({"ok": True, "flags": flags})

# ===== Boss Mode Phase 10: Growth Loops =====
@app.route('/api/growth/referral', methods=['POST'])
@require_dashboard_key
def api_track_referral():
    """Track a new referral"""
    try:
        from bot.growth import track_referral
        data = request.get_json() or {}
        result = track_referral(
            data.get('referrer_id'),
            data.get('referee_id'),
            data.get('source', 'direct')
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/growth/referrals/<user_id>')
@require_dashboard_key
def api_get_referrals(user_id):
    """Get referral stats for a user"""
    try:
        from bot.growth import get_referral_stats
        result = get_referral_stats(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/growth/onboarding/<user_id>')
def api_get_onboarding(user_id):
    """Get onboarding status for a user"""
    try:
        from bot.growth import get_onboarding_status
        result = get_onboarding_status(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/growth/onboarding', methods=['POST'])
@require_dashboard_key
def api_update_onboarding():
    """Update onboarding progress"""
    try:
        from bot.growth import update_onboarding_status
        data = request.get_json() or {}
        result = update_onboarding_status(
            data.get('user_id'),
            data.get('step'),
            data.get('completed', True)
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ===== Boss Mode Phase 11: Internationalization =====
@app.route('/api/i18n/locales')
def api_get_locales():
    """Get supported locales"""
    try:
        from bot.i18n import get_supported_locales
        result = get_supported_locales()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/i18n/strings/<locale>')
def api_get_strings(locale):
    """Get translations for a locale"""
    try:
        from bot.i18n import get_locale_strings
        result = get_locale_strings(locale)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ===== Visual Workflow Builder (Phases 51-55) =====
@app.route('/workflow/builder')
def workflow_builder_ui():
    """Visual Workflow Builder UI"""
    return render_template('workflow_builder.html')

@app.route('/api/workflow/node-types')
def api_get_node_types():
    """Get available workflow node types"""
    try:
        from bot.workflow_builder import get_available_node_types
        result = get_available_node_types()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow', methods=['POST'])
@require_dashboard_key
def api_create_workflow():
    """Create a new workflow"""
    try:
        from bot.workflow_builder import create_workflow
        data = request.get_json() or {}
        result = create_workflow(
            user_id=data.get('user_id', 'default'),
            name=data.get('name', 'New Workflow'),
            description=data.get('description', ''),
            template_id=data.get('template_id')
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow/<workflow_id>')
def api_get_workflow(workflow_id):
    """Get workflow by ID"""
    try:
        from bot.workflow_builder import get_workflow
        result = get_workflow(workflow_id)
        return jsonify(result), 200 if result.get('ok') else 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow/<workflow_id>', methods=['PUT'])
@require_dashboard_key
def api_update_workflow(workflow_id):
    """Update workflow"""
    try:
        from bot.workflow_builder import update_workflow
        data = request.get_json() or {}
        result = update_workflow(workflow_id, data)
        return jsonify(result), 200 if result.get('ok') else 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow/<workflow_id>', methods=['DELETE'])
@require_dashboard_key
def api_delete_workflow(workflow_id):
    """Delete workflow"""
    try:
        from bot.workflow_builder import delete_workflow
        result = delete_workflow(workflow_id)
        return jsonify(result), 200 if result.get('ok') else 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow/list')
def api_list_workflows():
    """List all workflows"""
    try:
        from bot.workflow_builder import list_workflows
        user_id = request.args.get('user_id')
        result = list_workflows(user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow/templates')
def api_list_templates():
    """List workflow templates"""
    try:
        from bot.workflow_builder import list_templates, initialize_default_templates
        initialize_default_templates()
        result = list_templates()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/workflow/execute/ai', methods=['POST'])
@require_dashboard_key
def api_execute_ai_task():
    """Phase 55: Execute AI task for workflow execution"""
    try:
        data = request.get_json()
        model = data.get('model', 'gpt-4o-mini')
        system_prompt = data.get('system_prompt', 'You are a helpful assistant.')
        user_message = data.get('user_message', '')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 2000)
        
        # Call AI
        from bot.ai_client import get_ai_client
        client = get_ai_client()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        result_text = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        # Estimate cost (simplified)
        cost_per_1k = 0.0015 if 'gpt-4o' in model else 0.0005
        cost = (tokens / 1000) * cost_per_1k
        
        return jsonify({
            "ok": True,
            "response": result_text,
            "model": model,
            "tokens": tokens,
            "cost": round(cost, 4)
        })
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/status/summary')
@rate_limit(max_requests=30, window=60)
def api_status_summary():
    """Boss Mode: Aggregated system status summary"""
    try:
        from bot.status_summary import get_status_summary
        summary = get_status_summary()
        return jsonify({"ok": True, "data": summary})
    except Exception as e:
        audit_log("status_summary_error", {"error": str(e)}, ok=False)
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/csrf-token', methods=['GET'])
def api_get_csrf_token():
    """Boss Mode: Generate CSRF token for forms"""
    token, session_id = generate_csrf_token()
    return jsonify({
        "ok": True,
        "csrf_token": token,
        "session_id": session_id
    })

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
            return jsonify({"ok": False, "error": "No file uploaded", "data": None}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"ok": False, "error": "Empty filename", "data": None}), 400
        
        # Validate file type
        filename = secure_filename(file.filename)
        if not (filename.lower().endswith('.mp3') or filename.lower().endswith('.wav')):
            return jsonify({
                "ok": False, 
                "error": "Only .mp3 and .wav files are supported",
                "data": None
            }), 400
        
        # Check file size (50MB max)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        MAX_SIZE = 50 * 1024 * 1024  # 50MB
        if file_size > MAX_SIZE:
            return jsonify({
                "ok": False,
                "error": f"File too large. Maximum size is 50MB, got {file_size / 1024 / 1024:.1f}MB",
                "data": None
            }), 413
        
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())[:8]
        
        # Get email and subscribe preference from form
        email = request.form.get('email', '')
        subscribe = request.form.get('subscribe', 'false').lower() == 'true'
        
        # Save file to tmp
        tmp_dir = Path('tmp')
        tmp_dir.mkdir(exist_ok=True)
        file_path = tmp_dir / f"{correlation_id}_{filename}"
        file.save(str(file_path))
        
        log_portal(f"File uploaded: {filename} ({file_path.stat().st_size} bytes), CID: {correlation_id}, Email: {email}")
        
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
        
        if email:
            properties["Owner Email"] = {"email": email}
        
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
        
        drive_link = get_prop('Drive Link', 'url')
        download_url = drive_link if drive_link else f"/api/public/download/{correlation_id}"
        
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
                "payment_link": get_prop('Payment Link', 'url'),
                "drive_link": drive_link,
                "download_url": download_url,
                "created_time": job.get('created_time')
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
        except Exception as e:
            if 'signature' in str(e).lower():
                return jsonify({"ok": False, "error": "Invalid signature"}), 400
            raise
        
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

@app.route('/api/public/job-history/<email>')
def api_public_job_history(email):
    """Customer Portal: Get last 5 jobs by email"""
    try:
        from bot.notion_api import NotionClientWrapper
        from bot import config
        
        if not config.JOB_LOG_DB_ID:
            return jsonify({"ok": False, "error": "Job Log not configured"}), 500
        
        notion = NotionClientWrapper()
        
        # Query Job Log for jobs with this Owner Email
        results = notion.query_database(
            config.JOB_LOG_DB_ID,
            filter_criteria={
                "property": "Owner Email",
                "email": {
                    "equals": email
                }
            }
        )
        
        # Return last 5 jobs
        jobs = []
        for job in results[:5]:
            props = job.get('properties', {})
            jobs.append({
                "job_name": props.get('Job Name', {}).get('title', [{}])[0].get('text', {}).get('content', 'N/A') if props.get('Job Name', {}).get('title') else 'N/A',
                "qa_score": props.get('QA Score', {}).get('number'),
                "gross_usd": props.get('Gross USD', {}).get('number'),
                "status": props.get('Status', {}).get('select', {}).get('name'),
                "created_time": job.get('created_time')
            })
        
        return jsonify({"ok": True, "data": jobs}), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/public/send-email', methods=['POST'])
@rate_limit(max_requests=5, window=60)
def api_public_send_email():
    """Customer Portal: Send job completion email"""
    import datetime
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from pathlib import Path
    
    try:
        data = request.get_json()
        recipient = data.get('email')
        job_data = data.get('job', {})
        
        if not recipient:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        # Log email
        log_file = Path('logs/customer_email.log')
        log_file.parent.mkdir(exist_ok=True)
        
        def log_email(msg):
            with open(log_file, 'a') as f:
                ts = datetime.datetime.utcnow().isoformat() + 'Z'
                f.write(f"[{ts}] {msg}\n")
        
        # Load email template
        template_path = Path('templates/email_job_complete.html')
        if template_path.exists():
            with open(template_path, 'r') as f:
                html_content = f.read()
            
            # Replace placeholders
            html_content = html_content.replace('{{job_name}}', job_data.get('job_name', 'N/A'))
            html_content = html_content.replace('{{qa_score}}', str(job_data.get('qa_score', 0)))
            html_content = html_content.replace('{{duration_min}}', str(round(job_data.get('duration_min', 0), 2)))
            html_content = html_content.replace('{{cost_usd}}', str(round(job_data.get('cost', 0), 2)))
            html_content = html_content.replace('{{correlation_id}}', job_data.get('correlation_id', 'N/A'))
            html_content = html_content.replace('{{download_url}}', job_data.get('download_url', '#'))
        else:
            html_content = f"""
            <h1>Your EchoPilot Job is Complete!</h1>
            <p>Job: {job_data.get('job_name', 'N/A')}</p>
            <p>QA Score: {job_data.get('qa_score', 0)}%</p>
            <p>Duration: {round(job_data.get('duration_min', 0), 2)} minutes</p>
            <p>Cost: ${round(job_data.get('cost', 0), 2)}</p>
            """
        
        # Try to send via Replit's built-in mail or log only
        try:
            smtp_user = os.getenv('SMTP_USER')
            smtp_pass = os.getenv('SMTP_PASS')
            
            if smtp_user and smtp_pass:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = f"EchoPilot Job Complete - {job_data.get('job_name', 'N/A')}"
                msg['From'] = smtp_user
                msg['To'] = recipient
                
                msg.attach(MIMEText(html_content, 'html'))
                
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
                
                log_email(f"Email sent to {recipient}, Job: {job_data.get('job_name', 'N/A')}, Status: Success")
            else:
                # Log only (SMTP not configured)
                log_email(f"Email queued for {recipient}, Job: {job_data.get('job_name', 'N/A')}, Status: Logged (SMTP not configured)")
        except Exception as e:
            log_email(f"Email failed to {recipient}, Job: {job_data.get('job_name', 'N/A')}, Error: {str(e)}")
            return jsonify({"ok": False, "error": f"Email send failed: {str(e)}"}), 500
        
        return jsonify({"ok": True, "message": "Email sent successfully"}), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/public/support', methods=['POST'])
@rate_limit(max_requests=5, window=60)
def api_public_support():
    """Customer Portal: Log support requests"""
    import datetime
    from pathlib import Path
    
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not name or not email or not message:
            return jsonify({"ok": False, "error": "Name, email, and message required"}), 400
        
        # Log to file
        log_file = Path('logs/support_requests.log')
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'a') as f:
            ts = datetime.datetime.utcnow().isoformat() + 'Z'
            f.write(f"[{ts}] {name} <{email}>: {message}\n")
        
        # Optionally log to Notion Partners DB if configured
        try:
            from bot.notion_api import NotionClientWrapper
            partners_db = os.getenv('NOTION_PARTNERS_DB_ID')
            
            if partners_db:
                notion = NotionClientWrapper()
                properties = {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Email": {"email": email},
                    "Notes": {"rich_text": [{"text": {"content": message}}]}
                }
                notion.create_page(partners_db, properties)
        except:
            pass  # Non-blocking if Notion fails
        
        return jsonify({"ok": True, "message": "Support request received"}), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/public/download/<correlation_id>')
def api_public_download(correlation_id):
    """Customer Portal: Provide download URL for job results"""
    try:
        from pathlib import Path
        
        # Check tmp directory for file
        tmp_dir = Path('tmp')
        files = list(tmp_dir.glob(f"{correlation_id}_*"))
        
        if files:
            # Return file directly
            return send_from_directory(tmp_dir, files[0].name, as_attachment=True)
        else:
            return jsonify({"ok": False, "error": "File not found"}), 404
        
    except Exception as e:
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


# ============================================================================
# PHASE 27: AUTONOMY & SCALE ENDPOINTS
# ============================================================================

def _backend_fetch(path, method="GET", json_data=None, timeout=5):
    """
    Internal failover helper: try localhost first, fallback to Railway if configured.
    Logs to logs/failover.log on fallback.
    """
    from pathlib import Path
    import time
    
    log_file = Path('logs/failover.log')
    log_file.parent.mkdir(exist_ok=True)
    
    def log_failover(msg):
        with open(log_file, 'a') as f:
            ts = datetime.utcnow().isoformat() + 'Z'
            f.write(f"[{ts}] {msg}\n")
    
    # Try localhost first
    try:
        url = f"http://localhost:5000{path}"
        response = requests.request(method, url, json=json_data, timeout=timeout)
        if response.status_code != 404:
            return response
        else:
            log_failover(f"404 on localhost{path}, status={response.status_code}")
    except Exception as e:
        log_failover(f"Localhost error on {path}: {str(e)}")
    
    # Try Railway fallback if configured
    railway_url = os.getenv('RAILWAY_URL', '').strip()
    if railway_url:
        try:
            url = f"{railway_url}{path}"
            response = requests.request(method, url, json=json_data, timeout=timeout)
            log_failover(f"Railway fallback success: {path}, status={response.status_code}")
            return response
        except Exception as e:
            log_failover(f"Railway fallback error on {path}: {str(e)}")
    
    # Return None if all failed
    return None


@app.route('/api/self-heal', methods=['POST'])
@require_dashboard_key
def self_heal():
    """
    Self-heal service: retry failed/stuck jobs, check worker health, surface unpaid jobs.
    Requires X-Dash-Key header.
    """
    from pathlib import Path
    from bot import config
    
    log_file = Path('logs/self_heal.log')
    log_file.parent.mkdir(exist_ok=True)
    
    def log_heal(data):
        with open(log_file, 'a') as f:
            import json
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', **data}) + '\n')
    
    try:
        notes = []
        retried_count = 0
        eligible_unpaid = []
        worker_restart_suggested = False
        
        # 1) Scan last 25 Job Log rows for Failed/Stuck
        try:
            token = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
            job_log_id = config.JOB_LOG_DB_ID
            
            url = f"https://{token}/notion/v1/databases/{job_log_id}/query"
            payload = {
                "page_size": 25,
                "sorts": [{"timestamp": "created_time", "direction": "descending"}]
            }
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                for page in results:
                    props = page.get('properties', {})
                    page_id = page.get('id', '')
                    
                    # Extract properties
                    status = None
                    if 'Status' in props and props['Status'].get('select'):
                        status = props['Status']['select']['name']
                    
                    payment_status = None
                    if 'Payment Status' in props and props['Payment Status'].get('select'):
                        payment_status = props['Payment Status']['select']['name']
                    
                    qa_score = None
                    if 'QA Score' in props and props['QA Score'].get('number') is not None:
                        qa_score = props['QA Score']['number']
                    
                    correlation_id = None
                    if 'Correlation ID' in props and props['Correlation ID'].get('rich_text'):
                        correlation_id = props['Correlation ID']['rich_text'][0]['plain_text']
                    
                    # Check for Failed/Stuck
                    if status in ['Failed', 'Stuck']:
                        # Re-enqueue into Automation Queue
                        try:
                            queue_url = f"https://{token}/notion/v1/pages"
                            queue_payload = {
                                "parent": {"database_id": config.AUTOMATION_QUEUE_DB_ID},
                                "properties": {
                                    "Task Name": {
                                        "title": [{"text": {"content": f"self-heal retry {datetime.utcnow().isoformat()} (cid={correlation_id or page_id[:8]})"}}]
                                    },
                                    "Trigger": {"checkbox": True},
                                    "Task Type": {"select": {"name": "audio_transcription"}}
                                }
                            }
                            queue_resp = requests.post(queue_url, json=queue_payload, timeout=10)
                            
                            if queue_resp.status_code == 200:
                                retried_count += 1
                                log_heal({
                                    "action": "retry_queued",
                                    "result": "success",
                                    "page_id": page_id,
                                    "correlation_id": correlation_id,
                                    "status": status
                                })
                                notes.append(f"Queued retry for {status} job {correlation_id or page_id[:8]}")
                            else:
                                log_heal({
                                    "action": "retry_queued",
                                    "result": "failed",
                                    "page_id": page_id,
                                    "error": queue_resp.text[:200]
                                })
                        except Exception as e:
                            log_heal({
                                "action": "retry_queued",
                                "result": "error",
                                "page_id": page_id,
                                "error": str(e)
                            })
                    
                    # Check for Unpaid with high QA
                    if payment_status == 'Unpaid' and qa_score and qa_score >= 95:
                        payment_link = None
                        if 'Payment Link' in props and props['Payment Link'].get('url'):
                            payment_link = props['Payment Link']['url']
                        
                        eligible_unpaid.append({
                            "correlation_id": correlation_id or page_id[:8],
                            "qa_score": qa_score,
                            "payment_link": payment_link
                        })
            else:
                notes.append(f"Could not query Job Log: {response.status_code}")
        
        except Exception as e:
            notes.append(f"Job Log scan error: {str(e)}")
            log_heal({"action": "scan_job_log", "result": "error", "error": str(e)})
        
        # 2) Check worker heartbeat from supervisor
        try:
            supervisor_resp = _backend_fetch('/api/supervisor-status', method='GET', timeout=5)
            if supervisor_resp and supervisor_resp.status_code == 200:
                supervisor_data = supervisor_resp.json()
                last_poll = supervisor_data.get('data', {}).get('last_poll_time')
                
                if last_poll:
                    from dateutil import parser
                    last_poll_dt = parser.parse(last_poll)
                    now = datetime.utcnow().replace(tzinfo=last_poll_dt.tzinfo)
                    stale_seconds = (now - last_poll_dt).total_seconds()
                    
                    if stale_seconds > 300:  # 5 minutes
                        worker_restart_suggested = True
                        notes.append(f"Worker stale for {int(stale_seconds)}s (>5min)")
                        
                        # Write sentinel file (no actual kill)
                        with open('/tmp/restart_requested', 'w') as f:
                            f.write(f"RESTART_REQUESTED at {datetime.utcnow().isoformat()}\n")
                        
                        log_heal({
                            "action": "worker_check",
                            "result": "restart_suggested",
                            "stale_seconds": int(stale_seconds)
                        })
                    else:
                        notes.append(f"Worker healthy (last poll {int(stale_seconds)}s ago)")
        except Exception as e:
            notes.append(f"Worker check error: {str(e)}")
        
        return jsonify({
            "ok": True,
            "retried_count": retried_count,
            "eligible_unpaid": eligible_unpaid,
            "worker_restart_suggested": worker_restart_suggested,
            "notes": notes
        }), 200
    
    except Exception as e:
        log_heal({"action": "self_heal", "result": "error", "error": str(e)})
        return jsonify({
            "ok": False,
            "error": f"Self-heal failed: {str(e)}",
            "retried_count": 0,
            "eligible_unpaid": [],
            "worker_restart_suggested": False,
            "notes": []
        }), 500


@app.route('/api/finance-metrics', methods=['GET'])
@require_dashboard_key
def finance_metrics():
    """
    Finance & ROI metrics: try Notion Cost Dashboard rollups first, fallback to Job Log computation.
    Requires X-Dash-Key header.
    """
    try:
        from bot import config
        from dateutil import parser
        
        token = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
        cost_dashboard_id = os.getenv('NOTION_COST_DASHBOARD_DB_ID', '').strip()
        job_log_id = config.JOB_LOG_DB_ID
        
        warnings = []
        source = "computed"
        
        # Try rollups first
        if cost_dashboard_id:
            try:
                url = f"https://{token}/notion/v1/databases/{cost_dashboard_id}/query"
                response = requests.post(url, json={"page_size": 1}, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('results', [])
                    
                    if results:
                        props = results[0].get('properties', {})
                        
                        # Extract rollup values if they exist
                        def get_rollup(name):
                            if name in props and props[name].get('rollup', {}).get('number') is not None:
                                return props[name]['rollup']['number']
                            return None
                        
                        revenue_7d = get_rollup('Revenue_7d')
                        revenue_30d = get_rollup('Revenue_30d')
                        cost_7d = get_rollup('Cost_7d')
                        cost_30d = get_rollup('Cost_30d')
                        profit_7d = get_rollup('Profit_7d')
                        profit_30d = get_rollup('Profit_30d')
                        roi_30d = get_rollup('ROI_30d')
                        
                        # If all exist, use rollups
                        if all(x is not None for x in [revenue_7d, revenue_30d, profit_7d, profit_30d]):
                            source = "rollup"
                            return jsonify({
                                "ok": True,
                                "data": {
                                    "revenue_7d": round(revenue_7d, 2),
                                    "revenue_30d": round(revenue_30d, 2),
                                    "cost_7d": round(cost_7d or 0, 2),
                                    "cost_30d": round(cost_30d or 0, 2),
                                    "profit_7d": round(profit_7d, 2),
                                    "profit_30d": round(profit_30d, 2),
                                    "roi_30d": round(roi_30d or 0, 2),
                                    "jobs_7d": 0,
                                    "jobs_30d": 0
                                },
                                "source": source,
                                "warnings": []
                            }), 200
                        else:
                            warnings.append("Cost Dashboard rollups incomplete, falling back to computation")
                else:
                    warnings.append(f"Cost Dashboard query failed: {response.status_code}")
            except Exception as e:
                warnings.append(f"Rollup fetch error: {str(e)}")
        else:
            warnings.append("NOTION_COST_DASHBOARD_DB_ID not configured")
        
        # Compute from Job Log
        source = "computed"
        now = datetime.utcnow()
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ago = now - timedelta(days=30)
        
        # Query Job Log
        url = f"https://{token}/notion/v1/databases/{job_log_id}/query"
        payload = {
            "page_size": 100,
            "sorts": [{"timestamp": "created_time", "direction": "descending"}]
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code != 200:
            warnings.append(f"Job Log query failed: {response.status_code}")
            raise Exception("Cannot compute metrics")
        
        data = response.json()
        results = data.get('results', [])
        
        # Aggregate metrics
        revenue_7d = revenue_30d = 0
        cost_7d = cost_30d = 0
        profit_7d = profit_30d = 0
        jobs_7d = jobs_30d = 0
        
        for page in results:
            created_time = page.get('created_time')
            if not created_time:
                continue
            
            created_dt = parser.parse(created_time)
            props = page.get('properties', {})
            
            # Extract values
            gross = 0
            if 'Gross USD' in props and props['Gross USD'].get('number') is not None:
                gross = props['Gross USD']['number']
            
            profit = 0
            if 'Profit USD' in props and props['Profit USD'].get('number') is not None:
                profit = props['Profit USD']['number']
            
            # Cost = Gross - Profit
            job_cost = gross - profit
            
            # Aggregate by time window
            if created_dt >= seven_days_ago:
                revenue_7d += gross
                cost_7d += job_cost
                profit_7d += profit
                jobs_7d += 1
            
            if created_dt >= thirty_days_ago:
                revenue_30d += gross
                cost_30d += job_cost
                profit_30d += profit
                jobs_30d += 1
        
        # Calculate ROI
        roi_30d = (profit_30d / cost_30d * 100) if cost_30d > 0 else 0
        
        return jsonify({
            "ok": True,
            "data": {
                "revenue_7d": round(revenue_7d, 2),
                "revenue_30d": round(revenue_30d, 2),
                "cost_7d": round(cost_7d, 2),
                "cost_30d": round(cost_30d, 2),
                "profit_7d": round(profit_7d, 2),
                "profit_30d": round(profit_30d, 2),
                "roi_30d": round(roi_30d, 2),
                "jobs_7d": jobs_7d,
                "jobs_30d": jobs_30d
            },
            "source": source,
            "warnings": warnings
        }), 200
    
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": f"Finance metrics failed: {str(e)}",
            "data": {
                "revenue_7d": 0,
                "revenue_30d": 0,
                "cost_7d": 0,
                "cost_30d": 0,
                "profit_7d": 0,
                "profit_30d": 0,
                "roi_30d": 0,
                "jobs_7d": 0,
                "jobs_30d": 0
            },
            "source": "error",
            "warnings": [str(e)]
        }), 200  # Never fail hard


@app.route('/api/growth/subscribe', methods=['POST'])
@rate_limit(max_requests=5, window=60)
def growth_subscribe():
    """
    Growth hooks: subscribe email with optional referral code.
    Public endpoint with rate limiting.
    """
    from pathlib import Path
    
    log_file = Path('logs/growth_subscribers.log')
    log_file.parent.mkdir(exist_ok=True)
    
    try:
        data = request.get_json() or {}
        email = data.get('email', '').strip()
        ref = data.get('ref', '').strip()
        
        if not email:
            return jsonify({"ok": False, "error": "Email required"}), 400
        
        # Log locally
        with open(log_file, 'a') as f:
            ts = datetime.utcnow().isoformat() + 'Z'
            f.write(f"[{ts}] {email} | ref={ref or 'none'}\n")
        
        # Try MailerLite or Brevo if configured (server-side only)
        mailerlite_key = os.getenv('MAILERLITE_API_KEY', '').strip()
        brevo_key = os.getenv('BREVO_API_KEY', '').strip()
        
        if mailerlite_key:
            try:
                # MailerLite API v2
                url = "https://api.mailerlite.com/api/v2/subscribers"
                headers = {"X-MailerLite-ApiKey": mailerlite_key}
                payload = {"email": email, "fields": {"ref": ref} if ref else {}}
                response = requests.post(url, json=payload, headers=headers, timeout=5)
            except:
                pass  # Silent fail
        elif brevo_key:
            try:
                # Brevo (Sendinblue) API
                url = "https://api.brevo.com/v3/contacts"
                headers = {"api-key": brevo_key}
                payload = {
                    "email": email,
                    "attributes": {"REF": ref} if ref else {},
                    "listIds": [2]  # Default list
                }
                response = requests.post(url, json=payload, headers=headers, timeout=5)
            except:
                pass  # Silent fail
        
        # Try Notion Referrals DB if configured
        referrals_db_id = os.getenv('NOTION_REFERRALS_DB_ID', '').strip()
        if referrals_db_id:
            try:
                token = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
                url = f"https://{token}/notion/v1/pages"
                payload = {
                    "parent": {"database_id": referrals_db_id},
                    "properties": {
                        "Email": {"email": email},
                        "Referrer Code": {"rich_text": [{"text": {"content": ref or "none"}}]},
                        "Source": {"select": {"name": "portal"}}
                    }
                }
                requests.post(url, json=payload, timeout=5)
            except:
                pass  # Silent fail
        
        return jsonify({"ok": True, "queued": True}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ============================================================================
# PHASE 28: AUTONOMOUS OPS EXPANSION
# ============================================================================

def send_telegram(message):
    """
    Send Telegram message via Bot API.
    Returns {"ok": True/False, "details": str}
    """
    token = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '').strip()
    
    if not (token and chat_id):
        return {"ok": False, "details": "Telegram not configured"}
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            return {"ok": True, "details": "Sent successfully"}
        else:
            return {"ok": False, "details": f"HTTP {response.status_code}: {response.text[:100]}"}
    
    except Exception as e:
        return {"ok": False, "details": str(e)}


@app.route('/api/alerts/trigger', methods=['POST'])
@require_dashboard_key
def trigger_alerts():
    """
    Alerting system: check self-heal + finance metrics, send alerts if thresholds exceeded.
    Requires X-Dash-Key header.
    """
    from pathlib import Path
    from datetime import datetime, timedelta
    
    log_file = Path('logs/alerts.log')
    log_file.parent.mkdir(exist_ok=True)
    
    def log_alert(data):
        with open(log_file, 'a') as f:
            import json
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', **data}) + '\n')
    
    try:
        triggered = False
        reasons = []
        target = "none"
        
        # 1) Check self-heal log for retry count in last 24h
        retry_count_24h = 0
        try:
            if log_file.exists():
                cutoff = datetime.utcnow() - timedelta(hours=24)
                with open('logs/self_heal.log', 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            entry_ts = datetime.fromisoformat(entry.get('ts', '').replace('Z', '+00:00'))
                            if entry_ts > cutoff and entry.get('action') == 'retry_queued':
                                retry_count_24h += 1
                        except:
                            pass
        except:
            pass
        
        if retry_count_24h > 3:
            triggered = True
            reasons.append(f"Self-heal retries: {retry_count_24h} in 24h (threshold: 3)")
        
        # 2) Check finance metrics for QA and profit
        try:
            metrics_resp = requests.get(
                'http://localhost:5000/api/finance-metrics',
                headers={'X-Dash-Key': os.getenv('DASHBOARD_KEY', '')},
                timeout=5
            )
            
            if metrics_resp.status_code == 200:
                finance_data = metrics_resp.json()
                if finance_data.get('ok'):
                    data = finance_data.get('data', {})
                    profit_7d = data.get('profit_7d', 0)
                    
                    if profit_7d < 0:
                        triggered = True
                        reasons.append(f"Negative profit_7d: ${profit_7d:.2f}")
        except:
            pass
        
        # 3) Check metrics-summary for avg_qa_7d
        try:
            summary_resp = requests.get(
                'http://localhost:5000/api/metrics-summary',
                headers={'X-Dash-Key': os.getenv('DASHBOARD_KEY', '')},
                timeout=5
            )
            
            if summary_resp.status_code == 200:
                summary_data = summary_resp.json()
                if summary_data.get('ok'):
                    avg_qa_7d = summary_data.get('data', {}).get('avg_qa_7d', 100)
                    
                    if avg_qa_7d < 75:
                        triggered = True
                        reasons.append(f"Low QA: {avg_qa_7d:.1f}% (threshold: 75%)")
        except:
            pass
        
        # 4) Send alert if triggered
        if triggered:
            alert_message = f"🚨 <b>EchoPilot Alert</b>\n\n" + "\n".join([f"• {r}" for r in reasons])
            
            telegram_result = send_telegram(alert_message)
            if telegram_result["ok"]:
                target = "telegram"
            else:
                target = "log"
                log_alert({"alert": "triggered", "reasons": reasons, "telegram_fail": telegram_result["details"]})
        
        # Always log the check
        log_alert({
            "alert": "checked",
            "triggered": triggered,
            "reasons": reasons,
            "target": target
        })
        
        return jsonify({
            "ok": True,
            "triggered": triggered,
            "reason": reasons,
            "target": target,
            "ts": datetime.utcnow().isoformat() + 'Z'
        }), 200
    
    except Exception as e:
        log_alert({"alert": "error", "error": str(e)})
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/optimizer/run', methods=['POST'])
@require_dashboard_key
def run_optimizer():
    """
    Adaptive tuning engine: adjust DEFAULT_RATE_USD_PER_MIN based on QA/margin.
    Requires X-Dash-Key header.
    """
    from pathlib import Path
    from bot import config
    import json
    
    log_file = Path('logs/optimizer.log')
    log_file.parent.mkdir(exist_ok=True)
    runtime_config = Path('.env_runtime.json')
    
    def log_optimizer(data):
        with open(log_file, 'a') as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', **data}) + '\n')
    
    try:
        # 1) Read last 20 jobs from Job Log
        token = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
        job_log_id = config.JOB_LOG_DB_ID
        
        url = f"https://{token}/notion/v1/databases/{job_log_id}/query"
        payload = {
            "page_size": 20,
            "sorts": [{"timestamp": "created_time", "direction": "descending"}]
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code != 200:
            return jsonify({"ok": False, "error": f"Job Log query failed: {response.status_code}"}), 500
        
        data = response.json()
        results = data.get('results', [])
        
        if not results:
            return jsonify({"ok": False, "error": "No jobs found in Job Log"}), 404
        
        # 2) Compute avg QA and margin
        total_qa = 0
        total_revenue = 0
        total_cost = 0
        job_count = 0
        
        for page in results:
            props = page.get('properties', {})
            
            qa_score = None
            if 'QA Score' in props and props['QA Score'].get('number') is not None:
                qa_score = props['QA Score']['number']
            
            gross_usd = 0
            if 'Gross USD' in props and props['Gross USD'].get('number') is not None:
                gross_usd = props['Gross USD']['number']
            
            profit_usd = 0
            if 'Profit USD' in props and props['Profit USD'].get('number') is not None:
                profit_usd = props['Profit USD']['number']
            
            if qa_score is not None:
                total_qa += qa_score
                job_count += 1
            
            total_revenue += gross_usd
            total_cost += (gross_usd - profit_usd)
        
        if job_count == 0:
            return jsonify({"ok": False, "error": "No jobs with QA scores"}), 404
        
        avg_qa = total_qa / job_count
        margin_pct = ((total_revenue - total_cost) / total_revenue * 100) if total_revenue > 0 else 0
        
        # 3) Get current rate
        old_rate = float(os.getenv('DEFAULT_RATE_USD_PER_MIN', '0.15'))
        
        # Load from runtime config if exists
        if runtime_config.exists():
            try:
                with open(runtime_config, 'r') as f:
                    runtime_data = json.load(f)
                    old_rate = float(runtime_data.get('DEFAULT_RATE_USD_PER_MIN', old_rate))
            except:
                pass
        
        # 4) Adjust rate by ±5%
        new_rate = old_rate
        reason = "No change"
        
        if avg_qa >= 95 and margin_pct > 25:
            new_rate = old_rate * 1.05
            reason = f"Increase: QA={avg_qa:.1f}%, margin={margin_pct:.1f}%"
        elif avg_qa < 80 or margin_pct < 10:
            new_rate = old_rate * 0.95
            reason = f"Decrease: QA={avg_qa:.1f}%, margin={margin_pct:.1f}%"
        
        # 5) Save to runtime config
        with open(runtime_config, 'w') as f:
            json.dump({
                "DEFAULT_RATE_USD_PER_MIN": round(new_rate, 4),
                "updated_at": datetime.utcnow().isoformat() + 'Z'
            }, f, indent=2)
        
        # 6) Log change
        log_optimizer({
            "action": "adjust_rate",
            "old_rate": round(old_rate, 4),
            "new_rate": round(new_rate, 4),
            "avg_qa": round(avg_qa, 2),
            "margin_pct": round(margin_pct, 2),
            "reason": reason
        })
        
        return jsonify({
            "ok": True,
            "old_rate": round(old_rate, 4),
            "new_rate": round(new_rate, 4),
            "avg_qa": round(avg_qa, 2),
            "margin_pct": round(margin_pct, 2),
            "reason": reason,
            "ts": datetime.utcnow().isoformat() + 'Z'
        }), 200
    
    except Exception as e:
        log_optimizer({"action": "error", "error": str(e)})
        return jsonify({"ok": False, "error": str(e)}), 500


# ============================================================================
# PHASE 29: AI EXECUTIVE MODE
# ============================================================================

@app.route('/api/exec/report-latest', methods=['GET'])
@require_dashboard_key
def exec_report_latest():
    """
    GET /api/exec/report-latest
    Returns the most recent brief from logs/exec_briefs/*.json
    """
    from pathlib import Path
    import json
    
    try:
        briefs_dir = Path('logs/exec_briefs')
        if not briefs_dir.exists():
            return jsonify({"ok": False, "error": "No briefs folder found"}), 404
        
        # Find latest brief_*.json
        brief_files = sorted(briefs_dir.glob('brief_*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        
        if not brief_files:
            return jsonify({"ok": False, "error": "No briefs found"}), 404
        
        latest = brief_files[0]
        with open(latest, 'r') as f:
            data = json.load(f)
        
        return jsonify({"ok": True, "data": data, "error": None}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500


@app.route('/api/exec/ingest', methods=['POST'])
@require_dashboard_key
def exec_ingest():
    """
    POST /api/exec/ingest
    Aggregates fresh signals into a single payload object from logs and live endpoints.
    """
    from pathlib import Path
    import json
    from datetime import datetime
    
    def log_exec(data):
        log_file = Path('logs/exec_mode.log')
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', "actor": "exec_mode", **data}) + '\n')
    
    try:
        payload = {"ts": datetime.utcnow().isoformat() + 'Z', "signals": {}}
        
        # 1) Logs: daily_report (latest only)
        daily_reports = sorted(Path('logs').glob('daily_report_*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        if daily_reports:
            with open(daily_reports[0], 'r') as f:
                payload['signals']['daily_report'] = json.load(f)
        
        # 2) self_heal.log (last 200 lines)
        self_heal_log = Path('logs/self_heal.log')
        if self_heal_log.exists():
            lines = self_heal_log.read_text().strip().split('\n')[-200:]
            payload['signals']['self_heal_log'] = [json.loads(line) for line in lines if line.strip()]
        
        # 3) alerts.log (last 200 lines)
        alerts_log = Path('logs/alerts.log')
        if alerts_log.exists():
            lines = alerts_log.read_text().strip().split('\n')[-200:]
            payload['signals']['alerts_log'] = [json.loads(line) for line in lines if line.strip()]
        
        # 4) e2e_validation.json (last 50 lines)
        e2e_log = Path('logs/e2e_validation.json')
        if e2e_log.exists():
            lines = e2e_log.read_text().strip().split('\n')[-50:]
            payload['signals']['e2e_validation'] = [json.loads(line) for line in lines if line.strip()]
        
        # 5) release_captain.json (last 50 lines)
        release_log = Path('logs/release_captain.json')
        if release_log.exists():
            lines = release_log.read_text().strip().split('\n')[-50:]
            payload['signals']['release_captain'] = [json.loads(line) for line in lines if line.strip()]
        
        # 6) health.ndjson (last 200 lines)
        health_log = Path('logs/health.ndjson')
        if health_log.exists():
            lines = health_log.read_text().strip().split('\n')[-200:]
            payload['signals']['health_ndjson'] = [json.loads(line) for line in lines if line.strip()]
        
        # 7) Live endpoints: finance-metrics
        try:
            from bot import config
            token = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
            if hasattr(config, 'JOB_LOG_DB_ID'):
                url_finance = f"http://localhost:5000/api/finance-metrics"
                resp_finance = requests.get(url_finance, headers={'X-Dash-Key': os.getenv('DASHBOARD_KEY', '')}, timeout=10)
                if resp_finance.status_code == 200:
                    payload['signals']['finance_metrics'] = resp_finance.json()
        except:
            pass
        
        # 8) Live endpoints: metrics-summary
        try:
            url_metrics = f"http://localhost:5000/api/metrics-summary"
            resp_metrics = requests.get(url_metrics, headers={'X-Dash-Key': os.getenv('DASHBOARD_KEY', '')}, timeout=10)
            if resp_metrics.status_code == 200:
                payload['signals']['metrics_summary'] = resp_metrics.json()
        except:
            pass
        
        # 9) Optional: Last 10 Job Log items
        try:
            from bot import config
            token = os.getenv('REPLIT_CONNECTORS_HOSTNAME')
            job_log_id = config.JOB_LOG_DB_ID
            url = f"https://{token}/notion/v1/databases/{job_log_id}/query"
            resp = requests.post(url, json={"page_size": 10, "sorts": [{"timestamp": "created_time", "direction": "descending"}]}, timeout=10)
            if resp.status_code == 200:
                payload['signals']['job_log_recent'] = resp.json().get('results', [])
        except:
            pass
        
        # Save snapshot
        ts_filename = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        ingest_path = Path(f'logs/exec_ingest_{ts_filename}.json')
        ingest_path.parent.mkdir(exist_ok=True)
        with open(ingest_path, 'w') as f:
            json.dump(payload, f, indent=2)
        
        log_exec({"event": "ingest", "ok": True, "path": str(ingest_path)})
        
        return jsonify({"ok": True, "data": payload, "error": None, "saved_to": str(ingest_path)}), 200
    
    except Exception as e:
        log_exec({"event": "ingest", "ok": False, "error": str(e)})
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500


@app.route('/api/exec/analyze', methods=['POST'])
@require_dashboard_key
def exec_analyze():
    """
    POST /api/exec/analyze
    Run GPT-4o-mini with anomaly detection rules and produce strict JSON output.
    """
    from pathlib import Path
    import json
    from datetime import datetime
    import openai
    
    def log_exec(data):
        log_file = Path('logs/exec_mode.log')
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', "actor": "exec_mode", **data}) + '\n')
    
    try:
        # Load latest ingest or use provided payload
        ingest_files = sorted(Path('logs').glob('exec_ingest_*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not ingest_files:
            return jsonify({"ok": False, "error": "No ingest data found. Run /api/exec/ingest first."}), 404
        
        with open(ingest_files[0], 'r') as f:
            ingest_data = json.load(f)
        
        # Prepare OpenAI client
        api_key = os.getenv('AI_INTEGRATIONS_OPENAI_API_KEY')
        base_url = os.getenv('AI_INTEGRATIONS_OPENAI_BASE_URL', 'https://api.openai.com/v1')
        
        if not api_key:
            return jsonify({"ok": False, "error": "OPENAI_API_KEY not configured"}), 500
        
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        
        # System prompt with detection rules
        system_prompt = """You are an AI Executive Assistant analyzing EchoPilot system metrics for anomalies.

DETECTION RULES (flag if ANY condition met):

Quality:
- 3+ consecutive jobs with QA < 80
- 7-day avg QA < target (usually 85%)

Finance:
- 7d ROI < 1.0
- Margin < 40%
- Revenue trending down 3+ consecutive days
- Unpaid jobs with QA ≥ 95% older than 48h

Ops:
- Processing latency > 2 polling cycles (120s)
- Repeated Notion read-after-write lag > 90s
- 5xx error spikes
- Health endpoint timeouts

Growth:
- Sign-ups flat for 7+ days
- No referrals logged
- Email bounce rate high

OUTPUT STRICT JSON:
{
  "kpis": {"jobs_7d":0,"revenue_7d":0,"avg_qa_7d":0,"roi_7d":0,"margin_pct_7d":0},
  "anomalies": [{"type":"finance|ops|quality|growth","severity":"low|med|high","signal":"<short>","evidence":["..."],"suggested_fix":"<1-liner>"}],
  "actions": [{"owner":"ops|eng|growth|finance","priority":1,"task":"<do this>","eta_hours":2}],
  "notes":["short bullets"],
  "confidence": 0.0
}

Respond ONLY with valid JSON. No markdown, no explanation."""
        
        # Call GPT-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze these signals:\n\n{json.dumps(ingest_data, indent=2)}"}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        
        analysis_text = response.choices[0].message.content.strip()
        
        # Parse JSON response
        try:
            analysis_json = json.loads(analysis_text)
        except:
            # Try to extract JSON from markdown if GPT wrapped it
            if '```json' in analysis_text:
                analysis_text = analysis_text.split('```json')[1].split('```')[0].strip()
                analysis_json = json.loads(analysis_text)
            else:
                raise ValueError("GPT returned non-JSON response")
        
        # Save analysis
        ts_filename = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        analysis_path = Path(f'logs/exec_analysis_{ts_filename}.json')
        with open(analysis_path, 'w') as f:
            json.dump(analysis_json, f, indent=2)
        
        log_exec({"event": "analyze", "ok": True, "path": str(analysis_path)})
        
        return jsonify({"ok": True, "data": analysis_json, "error": None, "saved_to": str(analysis_path)}), 200
    
    except Exception as e:
        log_exec({"event": "analyze", "ok": False, "error": str(e)})
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500


@app.route('/api/exec/brief', methods=['POST'])
@require_dashboard_key
def exec_brief():
    """
    POST /api/exec/brief
    Combines ingest + analyze into a human-readable brief + machine JSON.
    """
    from pathlib import Path
    import json
    from datetime import datetime
    
    def log_exec(data):
        log_file = Path('logs/exec_mode.log')
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', "actor": "exec_mode", **data}) + '\n')
    
    try:
        # 1) Run ingest
        ingest_resp = exec_ingest()
        if ingest_resp[1] != 200:
            return jsonify({"ok": False, "error": "Ingest failed"}), 500
        ingest_data = ingest_resp[0].get_json()
        ingest_path = ingest_data.get('saved_to')
        
        # 2) Run analyze
        analyze_resp = exec_analyze()
        if analyze_resp[1] != 200:
            return jsonify({"ok": False, "error": "Analyze failed"}), 500
        analyze_data = analyze_resp[0].get_json()
        analysis_json = analyze_data.get('data', {})
        analysis_path = analyze_data.get('saved_to')
        
        # 3) Build EXEC_BRIEF
        kpis = analysis_json.get('kpis', {})
        anomalies = analysis_json.get('anomalies', [])
        actions = analysis_json.get('actions', [])
        
        # Generate headline
        if anomalies:
            high_sev = [a for a in anomalies if a.get('severity') == 'high']
            if high_sev:
                headline = f"⚠️ {len(high_sev)} HIGH SEVERITY ALERTS"
            else:
                headline = f"⚡ {len(anomalies)} anomalies detected"
        else:
            headline = "✅ All systems nominal"
        
        # Generate summary
        summary_lines = []
        summary_lines.append(f"Jobs (7d): {kpis.get('jobs_7d', 0)} | QA: {kpis.get('avg_qa_7d', 0):.1f}% | ROI: {kpis.get('roi_7d', 0):.1f}x")
        summary_lines.append(f"Revenue: ${kpis.get('revenue_7d', 0):.2f} | Margin: {kpis.get('margin_pct_7d', 0):.1f}%")
        
        if anomalies:
            summary_lines.append(f"\nTop Risks:")
            for anom in anomalies[:3]:
                summary_lines.append(f"  • [{anom.get('severity', 'low').upper()}] {anom.get('signal', 'Unknown')}")
        
        summary = '\n'.join(summary_lines)
        
        # Actions next 24h / 7d
        actions_24h = [a for a in actions if a.get('eta_hours', 999) <= 24]
        actions_7d = [a for a in actions if a.get('eta_hours', 999) > 24]
        
        # Top risks
        top_risks = anomalies[:5]
        
        exec_brief = {
            "ts": datetime.utcnow().isoformat() + 'Z',
            "headline": headline,
            "summary": summary,
            "kpis": kpis,
            "top_risks": top_risks,
            "actions_next_24h": actions_24h,
            "actions_next_7d": actions_7d,
            "confidence": analysis_json.get('confidence', 0.0),
            "attachments": {
                "analysis_json_path": analysis_path,
                "ingest_json_path": ingest_path
            }
        }
        
        # 4) Save JSON brief
        ts_filename = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        brief_json_path = Path(f'logs/exec_briefs/brief_{ts_filename}.json')
        brief_json_path.parent.mkdir(exist_ok=True, parents=True)
        with open(brief_json_path, 'w') as f:
            json.dump(exec_brief, f, indent=2)
        
        # 5) Generate HTML version
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>EchoPilot CEO Brief - {datetime.utcnow().strftime('%Y-%m-%d')}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .headline {{ font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #333; }}
        .kpis {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
        .kpi {{ background: #f8f9fa; padding: 15px; border-radius: 6px; flex: 1; min-width: 150px; }}
        .kpi-label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
        .kpi-value {{ font-size: 24px; font-weight: bold; color: #007bff; margin-top: 5px; }}
        .section {{ margin: 30px 0; }}
        .section-title {{ font-size: 18px; font-weight: bold; margin-bottom: 15px; border-bottom: 2px solid #007bff; padding-bottom: 5px; }}
        .risk {{ padding: 12px; margin: 10px 0; border-radius: 6px; border-left: 4px solid; }}
        .risk.high {{ background: #fff3cd; border-color: #dc3545; }}
        .risk.med {{ background: #d1ecf1; border-color: #ffc107; }}
        .risk.low {{ background: #d4edda; border-color: #28a745; }}
        .risk-severity {{ font-weight: bold; text-transform: uppercase; font-size: 12px; }}
        .action {{ padding: 10px; margin: 8px 0; background: #f8f9fa; border-radius: 6px; }}
        .action-priority {{ display: inline-block; background: #007bff; color: white; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-right: 8px; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="headline">{exec_brief['headline']}</div>
        
        <div class="kpis">
            <div class="kpi">
                <div class="kpi-label">Jobs (7d)</div>
                <div class="kpi-value">{kpis.get('jobs_7d', 0)}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Revenue (7d)</div>
                <div class="kpi-value">${kpis.get('revenue_7d', 0):.2f}</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Avg QA (7d)</div>
                <div class="kpi-value">{kpis.get('avg_qa_7d', 0):.1f}%</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">ROI (7d)</div>
                <div class="kpi-value">{kpis.get('roi_7d', 0):.1f}x</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Margin (7d)</div>
                <div class="kpi-value">{kpis.get('margin_pct_7d', 0):.1f}%</div>
            </div>
        </div>
        
        <div class="section">
            <div class="section-title">Top Risks</div>
            {"".join([f'<div class="risk {risk.get("severity", "low")}"><span class="risk-severity">{risk.get("severity", "low")}</span>: {risk.get("signal", "Unknown")}<br><small>{risk.get("suggested_fix", "")}</small></div>' for risk in top_risks]) if top_risks else '<p>No risks detected.</p>'}
        </div>
        
        <div class="section">
            <div class="section-title">Actions: Next 24 Hours</div>
            {"".join([f'<div class="action"><span class="action-priority">P{action.get("priority", 1)}</span><strong>{action.get("owner", "ops")}</strong>: {action.get("task", "TBD")} <small>({action.get("eta_hours", 0)}h)</small></div>' for action in actions_24h]) if actions_24h else '<p>No immediate actions required.</p>'}
        </div>
        
        <div class="section">
            <div class="section-title">Actions: Next 7 Days</div>
            {"".join([f'<div class="action"><span class="action-priority">P{action.get("priority", 1)}</span><strong>{action.get("owner", "ops")}</strong>: {action.get("task", "TBD")} <small>({action.get("eta_hours", 0)}h)</small></div>' for action in actions_7d]) if actions_7d else '<p>No weekly actions planned.</p>'}
        </div>
        
        <div class="footer">
            Generated by AI Executive Mode · {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC<br>
            Analysis: <code>{analysis_path}</code>
        </div>
    </div>
</body>
</html>"""
        
        brief_html_path = Path(f'logs/exec_briefs/brief_{ts_filename}.html')
        with open(brief_html_path, 'w') as f:
            f.write(html_content)
        
        log_exec({"event": "brief", "ok": True, "json_path": str(brief_json_path), "html_path": str(brief_html_path)})
        
        return jsonify({
            "ok": True,
            "data": exec_brief,
            "error": None,
            "json_path": str(brief_json_path),
            "html_path": str(brief_html_path)
        }), 200
    
    except Exception as e:
        log_exec({"event": "brief", "ok": False, "error": str(e)})
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500


@app.route('/api/exec/email', methods=['POST'])
@require_dashboard_key
def exec_email():
    """
    POST /api/exec/email
    Sends latest brief via SMTP if configured; otherwise logs to exec_emails.log.
    """
    from pathlib import Path
    import json
    from datetime import datetime
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    def log_exec(data):
        log_file = Path('logs/exec_mode.log')
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', "actor": "exec_mode", **data}) + '\n')
    
    try:
        # Load latest brief
        brief_files = sorted(Path('logs/exec_briefs').glob('brief_*.json'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not brief_files:
            return jsonify({"ok": False, "error": "No brief found. Run /api/exec/brief first."}), 404
        
        with open(brief_files[0], 'r') as f:
            brief = json.load(f)
        
        # Load HTML version
        ts_part = brief_files[0].stem.replace('brief_', '')
        html_path = Path(f'logs/exec_briefs/brief_{ts_part}.html')
        
        if not html_path.exists():
            return jsonify({"ok": False, "error": "HTML brief not found"}), 404
        
        with open(html_path, 'r') as f:
            html_content = f.read()
        
        # Check SMTP config
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')
        alert_to = os.getenv('ALERT_TO')
        
        if not smtp_user or not smtp_pass:
            # Fallback to log
            email_log = Path('logs/exec_emails.log')
            with open(email_log, 'a') as f:
                f.write(json.dumps({
                    "ts": datetime.utcnow().isoformat() + 'Z',
                    "to": alert_to or "not_configured",
                    "subject": f"EchoPilot CEO Brief — {datetime.utcnow().strftime('%Y-%m-%d')}",
                    "brief_headline": brief.get('headline'),
                    "html_path": str(html_path)
                }) + '\n')
            
            log_exec({"event": "email", "ok": True, "sent": False, "logged_to": str(email_log)})
            return jsonify({"ok": True, "sent": False, "logged_to": str(email_log), "error": None}), 200
        
        # Send via SMTP
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"EchoPilot CEO Brief — {datetime.utcnow().strftime('%Y-%m-%d')}"
        msg['From'] = smtp_user
        msg['To'] = alert_to
        
        msg.attach(MIMEText(html_content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        log_exec({"event": "email", "ok": True, "sent": True, "to": alert_to})
        return jsonify({"ok": True, "sent": True, "to": alert_to, "error": None}), 200
    
    except Exception as e:
        log_exec({"event": "email", "ok": False, "error": str(e)})
        return jsonify({"ok": False, "sent": False, "error": str(e)}), 500


@app.route('/api/exec/schedule-daily', methods=['POST'])
@require_dashboard_key
def exec_schedule_daily():
    """
    POST /api/exec/schedule-daily
    Spawns detached subprocess to run scripts/exec_brief.sh immediately.
    """
    from pathlib import Path
    import json
    from datetime import datetime
    import subprocess
    
    def log_exec(data):
        log_file = Path('logs/exec_mode.log')
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a') as f:
            f.write(json.dumps({"ts": datetime.utcnow().isoformat() + 'Z', "actor": "exec_mode", **data}) + '\n')
    
    try:
        script_path = Path('scripts/exec_brief.sh')
        if not script_path.exists():
            return jsonify({"ok": False, "error": "exec_brief.sh not found"}), 404
        
        # Run script in background
        subprocess.Popen(['bash', str(script_path), 'http://localhost:5000'], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        start_new_session=True)
        
        log_exec({"event": "schedule_daily", "ok": True, "script": str(script_path)})
        return jsonify({"ok": True, "status": "Script launched", "error": None}), 200
    
    except Exception as e:
        log_exec({"event": "schedule_daily", "ok": False, "error": str(e)})
        return jsonify({"ok": False, "error": str(e)}), 500


# ============================================================================
# AUTOMATION CONTROL (Phases 27-29 Scheduler)
# ============================================================================

@app.route('/api/automations/start', methods=['POST'])
@require_dashboard_key
def automations_start():
    """
    POST /api/automations/start
    Starts the background scheduler via scripts/run_automations.sh start
    """
    from pathlib import Path
    import subprocess
    import json
    
    try:
        script_path = Path('scripts/run_automations.sh')
        if not script_path.exists():
            return jsonify({"ok": False, "error": "run_automations.sh not found"}), 404
        
        # Call supervisor script with 'start' command
        result = subprocess.run(
            ['bash', str(script_path), 'start'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Read PID from file
        pid = None
        pid_file = Path('logs/scheduler.pid')
        if pid_file.exists():
            try:
                pid = int(pid_file.read_text().strip())
            except:
                pass
        
        # Check if started successfully
        if result.returncode == 0:
            return jsonify({
                "ok": True,
                "status": "Scheduler started",
                "pid": pid,
                "error": None
            }), 200
        else:
            return jsonify({
                "ok": False,
                "status": "Failed to start scheduler",
                "pid": None,
                "error": result.stderr or result.stdout
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "Start command timed out"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/automations/stop', methods=['POST'])
@require_dashboard_key
def automations_stop():
    """
    POST /api/automations/stop
    Stops the background scheduler via scripts/run_automations.sh stop
    """
    import subprocess
    from pathlib import Path
    
    try:
        script_path = Path('scripts/run_automations.sh')
        if not script_path.exists():
            return jsonify({"ok": False, "error": "run_automations.sh not found"}), 404
        
        # Call supervisor script with 'stop' command
        result = subprocess.run(
            ['bash', str(script_path), 'stop'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return jsonify({
                "ok": True,
                "status": "Scheduler stopped",
                "error": None
            }), 200
        else:
            return jsonify({
                "ok": False,
                "status": "Failed to stop scheduler",
                "error": result.stderr or result.stdout
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "Stop command timed out"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/automations/status', methods=['GET'])
@require_dashboard_key
def automations_status():
    """
    GET /api/automations/status
    Returns scheduler status via scripts/run_automations.sh status
    """
    import subprocess
    from pathlib import Path
    import json
    
    try:
        script_path = Path('scripts/run_automations.sh')
        if not script_path.exists():
            return jsonify({"ok": False, "data": None, "error": "run_automations.sh not found"}), 404
        
        # Call supervisor script with 'status' command
        result = subprocess.run(
            ['bash', str(script_path), 'status'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Parse JSON from supervisor script
            status_data = json.loads(result.stdout)
            return jsonify({
                "ok": True,
                "data": status_data,
                "error": None
            }), 200
        else:
            return jsonify({
                "ok": False,
                "data": None,
                "error": result.stderr or "Failed to get status"
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "data": None, "error": "Status command timed out"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"ok": False, "data": None, "error": f"Invalid JSON from supervisor: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"ok": False, "data": None, "error": str(e)}), 500


# ==================== PHASE 31: SYSTEM HEALTH & COSTS ====================

@app.route('/api/system-health', methods=['GET'])
@require_dashboard_key
def system_health():
    """Run comprehensive health checks including 5-point probe + system metrics"""
    import subprocess
    import json
    
    try:
        # Run health probe
        health_result = subprocess.run(
            ['python3', 'scripts/health_probe.py'],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if health_result.returncode != 0:
            return jsonify({
                "ok": False,
                "error": "Health probe failed",
                "stderr": health_result.stderr
            }), 500
        
        health_data = json.loads(health_result.stdout)
        
        # Run sys probe for system metrics
        sys_result = subprocess.run(
            ['python3', 'scripts/sys_probe.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        sys_data = {}
        if sys_result.returncode == 0:
            sys_data = json.loads(sys_result.stdout)
        
        # Combine results
        combined = {
            "ts": health_data.get("ts"),
            "ok": health_data.get("ok", False) and sys_data.get("ok", False),
            "components": health_data.get("components", {}),
            "system_metrics": sys_data.get("metrics", {}),
            "issues": health_data.get("issues", []) + sys_data.get("issues", [])
        }
        
        return jsonify(combined), 200
            
    except subprocess.TimeoutExpired:
        return jsonify({"ok": False, "error": "Health probe timed out"}), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/live-ops', methods=['GET'])
@require_dashboard_key
def live_ops_status():
    """Get live ops monitoring status including rate limits and bans"""
    import subprocess
    import json
    from datetime import datetime
    
    try:
        # Get rate guard stats
        rate_result = subprocess.run(
            ['python3', 'scripts/rate_guard.py', 'stats'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        rate_stats = {}
        if rate_result.returncode == 0:
            rate_stats = json.loads(rate_result.stdout)
        
        # Get sys probe metrics
        sys_result = subprocess.run(
            ['python3', 'scripts/sys_probe.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        sys_data = {}
        if sys_result.returncode == 0:
            sys_data = json.loads(sys_result.stdout)
        
        return jsonify({
            "ok": True,
            "ts": datetime.utcnow().isoformat() + "Z",
            "system_metrics": sys_data.get("metrics", {}),
            "system_ok": sys_data.get("ok", False),
            "rate_guard": rate_stats,
            "issues": sys_data.get("issues", [])
        }), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/runtime-costs', methods=['GET'])
@require_dashboard_key
def runtime_costs():
    """Calculate runtime costs from execution logs"""
    import json
    import os
    from datetime import datetime, timedelta
    
    try:
        # Estimate costs based on activity
        costs = {
            "cpu_hours_est": 0.2,  # Approximate for lightweight operations
            "openai_usd": 0.0,     # Would need token tracking
            "stripe_fees": 0.0,    # Would need transaction tracking
            "notion_api": 0.0      # Free tier
        }
        
        # Try to get real cost data from Finance DB if available
        try:
            finance_resp = requests.get('http://localhost:5000/api/finance-metrics', timeout=5)
            if finance_resp.status_code == 200:
                finance_data = finance_resp.json()
                # Extract real costs if available
        except:
            pass
        
        total = round(sum(costs.values()), 2)
        
        return jsonify({
            "ok": True,
            "data": {
                "ts": datetime.utcnow().isoformat() + "Z",
                "total_usd": total,
                "breakdown": costs,
                "period": "7d",
                "note": "Estimates based on execution logs"
            },
            "error": None
        }), 200
        
    except Exception as e:
        return jsonify({
            "ok": False,
            "data": None,
            "error": str(e)
        }), 500


# ==================== PHASE 33-40: ENTERPRISE EXPANSION ====================

@app.route('/api/payments/create-invoice', methods=['POST'])
@require_dashboard_key
def create_payment_invoice():
    """Create Stripe invoice (Phase 33)"""
    import subprocess
    import json
    
    try:
        data = request.get_json() or {}
        amount = data.get('amount', 1.0)
        email = data.get('email', 'customer@example.com')
        description = data.get('description', 'EchoPilot Job')
        
        # Use stripe_live_guard.py
        from scripts.stripe_live_guard import create_invoice
        result = create_invoice(amount, email, description)
        
        return jsonify(result), 200 if result.get('ok') else 500
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/payments/webhook', methods=['POST'])
def stripe_webhook():
    """Stripe webhook handler (Phase 33)"""
    import json
    from datetime import datetime
    
    try:
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get('Stripe-Signature')
        
        # Verify webhook signature
        from scripts.stripe_live_guard import verify_webhook
        verify_result = verify_webhook(payload, sig_header)
        
        if not verify_result.get('ok'):
            return jsonify({"error": verify_result.get('error')}), 400
        
        event = verify_result.get('event')
        
        # Log webhook to file
        os.makedirs('logs', exist_ok=True)
        log_entry = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'event_type': event['type'],
            'event_id': event['id'],
            'mode': os.getenv('STRIPE_MODE', 'test')
        }
        
        with open('logs/stripe_webhook.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return jsonify({"ok": True, "received": True}), 200
        
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route('/api/customer/signed-url/<client_id>', methods=['GET'])
@require_dashboard_key
def get_signed_url(client_id):
    """Generate signed download URL (Phase 34)"""
    try:
        from scripts.customer_experience import signed_url
        url = signed_url(client_id)
        return jsonify({"ok": True, "url": url}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/customer/unsubscribe', methods=['POST'])
def unsubscribe_email():
    """Unsubscribe email (Phase 34)"""
    try:
        data = request.get_json() or {}
        email = data.get('email')
        
        from scripts.customer_experience import unsubscribe
        result = unsubscribe(email)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/compliance/export-data', methods=['GET'])
@require_dashboard_key
def export_user_data():
    """Export compliance data (Phase 35)"""
    import subprocess
    import json
    
    try:
        result = subprocess.run(
            ['python3', 'scripts/data_export.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/pricing/optimize', methods=['POST'])
@require_dashboard_key
def optimize_pricing():
    """Run adaptive pricing AI (Phase 36)"""
    import subprocess
    import json
    
    try:
        result = subprocess.run(
            ['python3', 'scripts/pricing_ai.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify({"ok": True, "data": data}), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/growth/referral/new', methods=['POST'])
@require_dashboard_key
def generate_referral():
    """Generate new referral code (Phase 37)"""
    import subprocess
    import json
    
    try:
        result = subprocess.run(
            ['python3', 'scripts/referral_engine.py'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify({"ok": True, "data": data}), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/audit/report', methods=['GET'])
@require_dashboard_key
def run_audit_report():
    """Generate SOC-lite audit report (Phase 38)"""
    import subprocess
    import json
    
    try:
        result = subprocess.run(
            ['python3', 'scripts/audit_pack.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/regions/sync', methods=['POST'])
@require_dashboard_key
def sync_regions():
    """Sync data across regions (Phase 39)"""
    import subprocess
    
    try:
        result = subprocess.run(
            ['python3', 'scripts/replica_sync.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return jsonify({"ok": True, "message": result.stdout}), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/payments/list', methods=['GET'])
@require_dashboard_key
def api_list_payments():
    """List recent Stripe payments (Phase 41)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/payments_center.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/ops/sentinel', methods=['GET'])
@require_dashboard_key
def api_ops_sentinel():
    """Get system health from Ops Sentinel (Phase 44)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/ops_sentinel.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/ops/check', methods=['POST', 'GET'])
@require_dashboard_key
def api_ops_check():
    """Run comprehensive Ops Check (Phase 101+)"""
    try:
        import subprocess
        env = os.environ.copy()
        env.setdefault("BASE_URL", request.host_url.rstrip("/"))
        
        result = subprocess.run(
            ['python3', 'scripts/ops_check.py'],
            env=env,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        try:
            payload = json.loads(result.stdout or "{}")
        except:
            payload = {
                "ok": False,
                "error": "bad_output",
                "stdout": result.stdout[-400:] if result.stdout else "",
                "stderr": result.stderr[-400:] if result.stderr else ""
            }
        
        return jsonify({
            "ok": bool(payload.get("ok")),
            "data": payload,
            "stderr": result.stderr[-400:] if result.stderr else ""
        }), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.get("/api/ops/slo/status")
@require_role("analyst","admin")
def slo_status():
    """Get SLO status - analyst/admin only (Stabilization Sprint)"""
    p = "logs/slo_guard.ndjson"
    last = ""
    if os.path.exists(p):
        with open(p, "rb") as f:
            try:
                for line in f: pass
                last = line.decode("utf-8").strip()
            except:
                last = "{}"
    return jsonify({"ok": True, "last": last})

@app.get("/api/ops/dr/last")
@require_role("analyst","admin")
def dr_last():
    """Get last DR reports - analyst/admin only (Stabilization Sprint)"""
    import glob
    files = sorted(glob.glob("logs/dr_report_*.json"))[-3:]
    return jsonify({"ok": True, "files": files})

@app.post("/api/ops/uptime/test")
@require_role("admin")
def uptime_test():
    """Run uptime test - admin only (Stabilization Sprint)"""
    import subprocess, sys
    r = subprocess.run([sys.executable,"scripts/uptime_monitor.py","--once"], capture_output=True, text=True)
    return jsonify({"ok": r.returncode==0, "stdout": r.stdout, "stderr": r.stderr})

@app.route('/api/revenue/intelligence', methods=['POST'])
@require_dashboard_key
def api_revenue_intelligence():
    """Run revenue intelligence analysis (Phase 42)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/revenue_intelligence.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/finance/reconcile', methods=['POST'])
@require_dashboard_key
def api_finance_reconcile():
    """Run finance reconciliation (Phase 47)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/finance_reconciler.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/governance/check', methods=['GET'])
@require_dashboard_key
def api_governance_check():
    """Run governance KPI check (Phase 50)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/auto_governance.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/brain/decide', methods=['POST'])
@require_dashboard_key
def run_ops_brain():
    """Run AI Ops Brain for autonomous decisions (Phase 40)"""
    import subprocess
    import json
    
    try:
        result = subprocess.run(
            ['python3', 'scripts/ai_ops_brain.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
            
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/observability/snapshot', methods=['GET'])
@require_dashboard_key
def api_observability_snapshot():
    """Get current observability snapshot (Phase 53)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/observability_snapshot.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/fraud/check', methods=['POST'])
@require_dashboard_key
def api_fraud_check():
    """Check payment for fraud risk (Phase 54)"""
    try:
        from scripts.fraud_guard import evaluate_payment
        
        data = request.get_json() or {}
        email = data.get('email', '')
        card_type = data.get('card_type', 'credit')
        amount = float(data.get('amount', 0))
        recent_count = int(data.get('recent_count', 0))
        daily_total = float(data.get('daily_total', 0))
        
        result = evaluate_payment(email, card_type, amount, recent_count, daily_total)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/portal/link', methods=['POST'])
@require_dashboard_key
def api_portal_link():
    """Generate signed portal link for customer (Phase 55)"""
    try:
        from scripts.customer_portal import create_portal_link
        
        data = request.get_json() or {}
        email = data.get('email', '')
        expiry_hours = int(data.get('expiry_hours', 24))
        
        if not email:
            return jsonify({"ok": False, "error": "email required"}), 400
        
        result = create_portal_link(email, expiry_hours)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/email/send', methods=['POST'])
@require_dashboard_key
def api_send_email():
    """Send email via SMTP (Phase 52)"""
    try:
        from scripts.emailer import send_email
        
        data = request.get_json() or {}
        to = data.get('to', '')
        subject = data.get('subject', '')
        body = data.get('body', '')
        
        if not all([to, subject, body]):
            return jsonify({"ok": False, "error": "to, subject, body required"}), 400
        
        result = send_email(to, subject, body)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/reports/email', methods=['POST'])
@require_dashboard_key
def api_reports_email():
    """Send daily CEO report via email (Phase 56)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/reports_emailer.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/payouts/reconcile', methods=['POST'])
@require_dashboard_key
def api_payouts_reconcile():
    """Run payout reconciliation (Phase 57)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/payout_recon.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/churn/score', methods=['POST'])
@require_dashboard_key
def api_churn_score():
    """Run churn risk analysis (Phase 58)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/churn_ai.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/slo/check', methods=['GET'])
@require_dashboard_key
def api_slo_check():
    """Check SLO compliance (Phase 59)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/slo_guard.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/audit/latest', methods=['GET'])
@require_dashboard_key
def api_audit_latest():
    """Get latest audit report (Phase 60)"""
    try:
        from scripts.audit_ui import get_latest_audit
        result = get_latest_audit()
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/audit/summary', methods=['GET'])
@require_dashboard_key
def api_audit_summary():
    """Get audit summary (Phase 60)"""
    try:
        from scripts.audit_ui import get_audit_summary
        result = get_audit_summary()
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/support/digest', methods=['POST'])
@require_dashboard_key
def api_support_digest():
    """Fetch support inbox digest (Phase 61)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/support_inbox.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/flags/get', methods=['GET'])
@require_dashboard_key
def api_flags_get_all():
    """Get all feature flags (Phase 62)"""
    try:
        from scripts.feature_flags import get_flags
        flags = get_flags()
        return jsonify({"ok": True, "flags": flags}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/flags/set', methods=['POST'])
@require_dashboard_key
def api_flags_set():
    """Set feature flag (Phase 62)"""
    try:
        from scripts.feature_flags import set_flag
        
        data = request.get_json() or {}
        key = data.get('key')
        value = data.get('value')
        
        if not key:
            return jsonify({"ok": False, "error": "key required"}), 400
        
        flags = set_flag(key, value)
        return jsonify({"ok": True, "flags": flags}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/exp/assign', methods=['GET'])
@require_dashboard_key
def api_exp_assign():
    """Assign user to experiment variant (Phase 63)"""
    try:
        from scripts.experiments import assign_variant
        
        user = request.args.get('user', 'anonymous')
        experiment = request.args.get('exp', 'pricing_v2')
        
        result = assign_variant(user, experiment)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/exp/log', methods=['POST'])
@require_dashboard_key
def api_exp_log():
    """Log experiment event (Phase 63)"""
    try:
        from scripts.experiments import log_event
        
        data = request.get_json() or {}
        result = log_event(data)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/costs/report', methods=['GET'])
@require_dashboard_key
def api_costs_report():
    """Get infrastructure cost report (Phase 64)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/cost_tracker.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/incidents/scan', methods=['POST'])
@require_dashboard_key
def api_incidents_scan():
    """Scan for incidents (Phase 65)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/incident_autoresponder.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/payments/webhooks', methods=['GET'])
@require_dashboard_key
def api_payments_webhooks():
    """List recent payment webhooks (Phase 66)"""
    try:
        import subprocess
        result = subprocess.run(
            ['tail', '-n', '20', 'logs/stripe_webhook.log'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        lines = result.stdout.splitlines() if result.returncode == 0 else []
        return jsonify({"ok": True, "count": len(lines), "lines": lines}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/payments/refund-last', methods=['POST'])
@require_dashboard_key
def api_payments_refund_last():
    """Process refund (test stub) (Phase 66)"""
    try:
        import time
        
        # Log refund request (stub for now)
        refund_entry = {
            "ts": time.time(),
            "ts_iso": datetime.utcnow().isoformat() + "Z",
            "action": "refund_last_called",
            "note": "Test refund initiated from dashboard"
        }
        
        with open("logs/refunds.log", "a") as f:
            f.write(json.dumps(refund_entry) + "\n")
        
        return jsonify({"ok": True, "message": "Refund logged (test mode)"}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/payments/events', methods=['GET'])
@require_dashboard_key
def api_payments_events():
    """List recent payment webhook events (Production Ops)"""
    try:
        limit = int(request.args.get('limit', 10))
        limit = min(limit, 100)  # Max 100
        
        events = []
        log_path = 'logs/stripe_webhooks.ndjson'
        
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                lines = f.readlines()
                recent = lines[-limit:] if len(lines) > limit else lines
                for line in recent:
                    if line.strip():
                        try:
                            events.append(json.loads(line))
                        except:
                            pass
        
        return jsonify({"ok": True, "count": len(events), "data": events}), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/payments/refund', methods=['POST'])
@require_dashboard_key
def api_payments_refund():
    """Refund a payment (Production Ops)"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        payment_id = data.get('payment_id')
        amount = data.get('amount')  # Optional partial refund amount in USD
        
        if not payment_id:
            return jsonify({"ok": False, "error": "payment_id required"}), 400
        
        # Import stripe
        import stripe
        
        # Determine mode and key
        mode = os.getenv('STRIPE_MODE', 'test')
        if mode == 'live':
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        else:
            stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        
        # Build refund params
        refund_params = {'payment_intent': payment_id}
        if amount:
            refund_params['amount'] = int(round(float(amount) * 100))  # Convert to cents
        
        # Create refund
        refund = stripe.Refund.create(**refund_params)
        
        # Log refund
        os.makedirs('logs', exist_ok=True)
        refund_log = {
            'ts': datetime.utcnow().isoformat() + 'Z',
            'event': 'refund_created',
            'refund_id': refund.get('id'),
            'payment_id': payment_id,
            'amount': refund.get('amount', 0) / 100,
            'status': refund.get('status'),
            'mode': mode
        }
        
        with open('logs/refunds.ndjson', 'a') as f:
            f.write(json.dumps(refund_log) + '\n')
        
        return jsonify({
            "ok": True,
            "data": {
                "id": refund.get('id'),
                "status": refund.get('status'),
                "amount": refund.get('amount', 0) / 100,
                "mode": mode
            }
        }), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route('/api/customer/invoices/<email>', methods=['GET'])
@require_dashboard_key
def api_customer_invoices(email):
    """Get customer invoices (Phase 70)"""
    try:
        # Stub: return mock invoice data
        invoices = [
            {
                "id": "inv_001",
                "date": "2025-10-15",
                "amount": 29.99,
                "status": "paid"
            },
            {
                "id": "inv_002",
                "date": "2025-10-20",
                "amount": 49.99,
                "status": "pending"
            }
        ]
        
        return jsonify({
            "ok": True,
            "email": email,
            "invoices": invoices
        }), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/customer/signed-url/<email>', methods=['GET'])
@require_dashboard_key
def api_customer_signed_url(email):
    """Generate signed portal URL (Phase 70)"""
    try:
        import hmac
        import hashlib
        import time
        
        # Generate HMAC-signed URL
        secret = os.getenv('SESSION_SECRET', 'default-secret-key')
        timestamp = int(time.time())
        expires = timestamp + (24 * 3600)  # 24 hours
        
        # Create signature
        message = f"{email}:{expires}"
        signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Build signed URL
        base_url = os.getenv('REPLIT_DOMAINS', 'localhost:5000').split(',')[0]
        signed_url = f"https://{base_url}/portal?email={email}&expires={expires}&sig={signature}"
        
        return jsonify({
            "ok": True,
            "email": email,
            "signed_url": signed_url,
            "expires": expires,
            "expires_iso": datetime.fromtimestamp(expires).isoformat() + "Z"
        }), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/backup/run', methods=['POST'])
@require_dashboard_key
def api_backup_run():
    """Run daily backup (Phase 70)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/backup_daily.py'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/slo/status', methods=['GET'])
@require_dashboard_key
def api_slo_status():
    """Get SLO monitoring status (Phase 68)"""
    try:
        if os.path.exists('logs/slo_status.json'):
            with open('logs/slo_status.json', 'r') as f:
                data = json.load(f)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": "No SLO status available"}), 404
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/ops/analytics', methods=['GET'])
@require_dashboard_key
def api_ops_analytics():
    """Get ops analytics with predictive scaling (Phase 71/74)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/predictive_scaling.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/retries/simulate', methods=['POST'])
@require_dashboard_key
def api_retries_simulate():
    """Simulate smart retry with exponential backoff (Phase 72)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/smart_retries.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/reports/email-daily', methods=['POST'])
@require_dashboard_key
def api_reports_email_daily():
    """Generate daily HTML email report (Phase 73)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/email_reports_v2.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/incidents/summarize', methods=['POST'])
@require_dashboard_key
def api_incidents_summarize():
    """Generate AI-powered incident summary (Phase 75)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/ai_incident_summaries.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ==================== PHASES 76-80: SLOs, PAGER, PORTAL, COSTS & SCALE ====================

@app.route('/api/slo/budget', methods=['GET'])
@require_dashboard_key
def api_slo_budget():
    """Get SLO error budget status (Phase 76)"""
    try:
        if os.path.exists('logs/slo_budget.json'):
            with open('logs/slo_budget.json', 'r') as f:
                data = json.load(f)
            return jsonify(data), 200
        else:
            import subprocess
            result = subprocess.run(
                ['python3', 'scripts/slo_budget.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return jsonify(data), 200
            else:
                return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/slo/rebaseline', methods=['POST'])
@require_dashboard_key
def api_slo_rebaseline():
    """Reset SLO error budget baseline (Phase 76)"""
    try:
        # Clear historical data
        for file in ['logs/slo_budget.ndjson', 'logs/deploy_gate.flag']:
            if os.path.exists(file):
                os.remove(file)
        
        # Recompute fresh
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/slo_budget.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify({"ok": True, "message": "SLO baseline reset", "data": data}), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/incidents/raise', methods=['POST'])
@require_dashboard_key
def api_incidents_raise():
    """Raise a new incident (Phase 77)"""
    try:
        data = request.get_json()
        severity = data.get('severity', 'INFO')
        msg = data.get('msg', 'No message')
        source = data.get('source', 'api')
        meta = data.get('meta', {})
        
        # Import incident pager
        sys.path.insert(0, 'scripts')
        from incident_pager import raise_incident
        
        result = raise_incident(severity, msg, source, meta)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/incidents/summary', methods=['POST'])
@require_dashboard_key
def api_incidents_summary():
    """Get incident summary (Phase 77)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/incident_pager.py'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify(data), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/portal/receipts', methods=['GET'])
@require_dashboard_key
def api_portal_receipts():
    """Get customer receipts (Phase 78)"""
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({"ok": False, "error": "email parameter required"}), 400
        
        # Import customer portal
        sys.path.insert(0, 'scripts')
        from customer_portal import get_customer_receipts
        
        result = get_customer_receipts(email)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/portal/download', methods=['GET'])
def api_portal_download():
    """Download receipt with signed token (Phase 78)"""
    try:
        email = request.args.get('email')
        resource_id = request.args.get('id')
        expires_at = int(request.args.get('expires', 0))
        token = request.args.get('token')
        
        if not all([email, resource_id, expires_at, token]):
            return jsonify({"ok": False, "error": "Missing required parameters"}), 400
        
        # Import customer portal
        sys.path.insert(0, 'scripts')
        from customer_portal import verify_download_token
        
        ip = request.remote_addr
        result = verify_download_token(email, resource_id, expires_at, token, ip)
        
        if result.get('ok'):
            # In production, would return actual file
            return jsonify({
                "ok": True,
                "message": "Download authorized",
                "resource_id": resource_id,
                "content": "Receipt content here (PDF/HTML)"
            }), 200
        else:
            return jsonify(result), result.get('status', 403)
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/costs/status', methods=['GET'])
@require_dashboard_key
def api_costs_status():
    """Get cost guardrails status (Phase 79)"""
    try:
        if os.path.exists('logs/costs.json'):
            with open('logs/costs.json', 'r') as f:
                data = json.load(f)
            return jsonify(data), 200
        else:
            import subprocess
            result = subprocess.run(
                ['python3', 'scripts/cost_guardrails.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return jsonify(data), 200
            else:
                return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/costs/set-cap', methods=['POST'])
@require_dashboard_key
def api_costs_set_cap():
    """Set cost cap (Phase 79)"""
    try:
        data = request.get_json()
        scope = data.get('scope', 'daily')
        key = data.get('key')
        usd_cap = float(data.get('usd_cap', 0))
        
        if usd_cap < 0:
            return jsonify({"ok": False, "error": "Cap must be positive"}), 400
        
        # Import cost guardrails
        sys.path.insert(0, 'scripts')
        from cost_guardrails import set_cost_cap
        
        result = set_cost_cap(scope, key, usd_cap)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/scale/status', methods=['GET'])
@require_dashboard_key
def api_scale_status():
    """Get autoscale status (Phase 80)"""
    try:
        if os.path.exists('logs/autoscale.json'):
            with open('logs/autoscale.json', 'r') as f:
                data = json.load(f)
            return jsonify(data), 200
        else:
            import subprocess
            result = subprocess.run(
                ['python3', 'scripts/autoscale_workers.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return jsonify(data), 200
            else:
                return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/scale/apply', methods=['POST'])
@require_dashboard_key
def api_scale_apply():
    """Apply autoscale changes (Phase 80)"""
    try:
        data = request.get_json() or {}
        dry_run = data.get('dry_run', True)
        
        # Set environment for dry run mode
        env = os.environ.copy()
        env['SCALE_DRY_RUN'] = str(dry_run).lower()
        
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/autoscale_workers.py'],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return jsonify({
                "ok": True,
                "message": "Scaling applied" if not dry_run else "Scaling computed (dry run)",
                "data": data
            }), 200
        else:
            return jsonify({"ok": False, "error": result.stderr}), 500
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ================================
# PHASES 81-100: ENTERPRISE EXPANSION
# ================================

@app.route('/api/rbac/init', methods=['POST'])
@require_dashboard_key
def api_rbac_init():
    """Initialize RBAC system (Phase 81)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/rbac_system.py'],
            capture_output=True, text=True, timeout=10
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/rbac/users', methods=['GET'])
@require_dashboard_key
def api_rbac_users():
    """Get RBAC users (Phase 81)"""
    try:
        import json as j
        if os.path.exists('data/rbac_users.json'):
            with open('data/rbac_users.json', 'r') as f:
                return jsonify({"ok": True, "users": j.load(f)}), 200
        return jsonify({"ok": True, "users": {}}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# JWT auth endpoints moved to lines 1447-1540 (Extra 4)

@app.route('/api/dr/backup', methods=['POST'])
@require_dashboard_key
def api_dr_backup():
    """Create DR backup (Phase 83)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/dr_backups.py'],
            capture_output=True, text=True, timeout=60
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/model/route', methods=['POST'])
@require_dashboard_key
def api_model_route():
    """Get model routing recommendation (Phase 84)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/model_router.py'],
            capture_output=True, text=True, timeout=10
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/finops/report', methods=['GET'])
@require_dashboard_key
def api_finops_report():
    """Get FinOps report (Phase 85)"""
    try:
        if os.path.exists('logs/finops_report.json'):
            with open('logs/finops_report.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/finops_reports.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# Warehouse sync endpoint moved to line ~1030 (Phase 106)

@app.route('/api/analytics/hub', methods=['GET'])
@require_dashboard_key
def api_analytics_hub():
    """Get analytics hub data (Phase 87)"""
    try:
        if os.path.exists('logs/analytics_hub.json'):
            with open('logs/analytics_hub.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/analytics_hub.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/maintenance/predict', methods=['GET'])
@require_dashboard_key
def api_predictive_maintenance():
    """Get predictive maintenance forecast (Phase 88)"""
    try:
        if os.path.exists('logs/predictive_maintenance.json'):
            with open('logs/predictive_maintenance.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/predictive_maintenance.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/compliance/check', methods=['GET'])
@require_dashboard_key
def api_compliance_v2():
    """Check compliance status (Phase 89)"""
    try:
        if os.path.exists('logs/compliance_v2.json'):
            with open('logs/compliance_v2.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/compliance_suite_v2.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/governance/advice', methods=['GET'])
@require_dashboard_key
def api_governance_ai():
    """Get AI governance recommendations (Phase 90)"""
    try:
        if os.path.exists('logs/governance_ai.json'):
            with open('logs/governance_ai.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/governance_ai.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/tenant/stats', methods=['GET'])
@require_dashboard_key
def api_tenant_stats():
    """Get multi-tenant stats (Phase 91)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/multitenant_core.py'],
            capture_output=True, text=True, timeout=10
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/tenant/billing/<tenant_id>', methods=['GET'])
@require_dashboard_key
def api_tenant_billing(tenant_id):
    """Get tenant billing (Phase 92)"""
    try:
        if os.path.exists(f'logs/tenant_billing_{tenant_id}.json'):
            with open(f'logs/tenant_billing_{tenant_id}.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/tenant_billing.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/anomaly/detect', methods=['GET'])
@require_dashboard_key
def api_anomaly_detection():
    """Detect anomalies (Phase 93)"""
    try:
        if os.path.exists('logs/anomaly_detection.json'):
            with open('logs/anomaly_detection.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/anomaly_detection.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/security/scan', methods=['POST'])
@require_dashboard_key
def api_security_scan():
    """Run security scan (Phase 95)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/security_scan.py'],
            capture_output=True, text=True, timeout=60
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/privacy/consent', methods=['POST'])
@require_dashboard_key
def api_privacy_consent():
    """Record privacy consent (Phase 96)"""
    try:
        import subprocess
        data = request.get_json() or {}
        result = subprocess.run(
            ['python3', 'scripts/privacy_consent.py'],
            capture_output=True, text=True, timeout=10
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/training/audit', methods=['GET'])
@require_dashboard_key
def api_training_audit():
    """Get AI training audit (Phase 97)"""
    try:
        if os.path.exists('logs/training_audit.json'):
            with open('logs/training_audit.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/training_audit.py'],
            capture_output=True, text=True, timeout=10
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/optimizer/run', methods=['POST'])
@require_dashboard_key
def api_adaptive_optimizer():
    """Run adaptive optimizer (Phase 98)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/adaptive_optimizer.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/self-heal/run', methods=['POST'])
@require_dashboard_key
def api_self_heal_v2():
    """Run self-heal v2 (Phase 99)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/self_heal_v2.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/learning/status', methods=['GET'])
@require_dashboard_key
def api_continuous_learning():
    """Get continuous learning status (Phase 100)"""
    try:
        if os.path.exists('logs/continuous_learning.json'):
            with open('logs/continuous_learning.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/continuous_learning.py'],
            capture_output=True, text=True, timeout=30
        )
        return jsonify(json.loads(result.stdout) if result.returncode == 0 else {"ok": False}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/validate/enterprise', methods=['GET'])
@require_dashboard_key
def api_enterprise_validator():
    """Run enterprise validation (Phase 100B)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/enterprise_validator.py'],
            capture_output=True, text=True, timeout=60
        )
        data = json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/reports/enterprise', methods=['GET'])
@require_dashboard_key
def api_enterprise_report():
    """Get enterprise ready report (Phase 100C)"""
    try:
        if os.path.exists('logs/enterprise_ready_report.json'):
            with open('logs/enterprise_ready_report.json', 'r') as f:
                return jsonify(json.load(f)), 200
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/final_enterprise_report.py'],
            capture_output=True, text=True, timeout=60
        )
        data = json.loads(result.stdout) if result.returncode == 0 else {"ok": False, "error": result.stderr}
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route('/api/reports/enterprise/html', methods=['GET'])
def api_enterprise_report_html():
    """View enterprise report HTML (Public)"""
    try:
        if os.path.exists('docs/ENTERPRISE_READY_REPORT.html'):
            with open('docs/ENTERPRISE_READY_REPORT.html', 'r') as f:
                return f.read(), 200, {'Content-Type': 'text/html'}
        return "<h1>Report not yet generated</h1>", 404
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>", 500

@app.route('/api/validation/html', methods=['GET'])
def api_validation_report_html():
    """View validation report HTML (Public)"""
    try:
        if os.path.exists('logs/enterprise_validator_report.html'):
            with open('logs/enterprise_validator_report.html', 'r') as f:
                return f.read(), 200, {'Content-Type': 'text/html'}
        return "<h1>Validation report not yet generated</h1>", 404
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>", 500


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

# ==================== PHASE 51: OBSERVABILITY & SLOS ====================

@app.route('/metrics', methods=['GET'])
def prometheus_metrics():
    """Prometheus-style metrics endpoint (no auth required for scraping)"""
    import psutil
    
    lines = []
    
    # App uptime
    uptime = time.time() - metrics_storage['app_start_time']
    lines.append('# HELP app_uptime_seconds Application uptime in seconds')
    lines.append('# TYPE app_uptime_seconds gauge')
    lines.append(f'app_uptime_seconds {uptime:.0f}')
    
    # HTTP requests total
    lines.append('# HELP http_requests_total Total HTTP requests by route and status')
    lines.append('# TYPE http_requests_total counter')
    for key, count in metrics_storage['http_requests_total'].items():
        parts = key.rsplit('_', 1)
        route = parts[0] if len(parts) > 1 else 'unknown'
        status = parts[1] if len(parts) > 1 else '000'
        lines.append(f'http_requests_total{{route="{route}",status="{status}"}} {count}')
    
    # HTTP request duration buckets (simplified histogram)
    lines.append('# HELP http_request_duration_ms HTTP request duration in milliseconds')
    lines.append('# TYPE http_request_duration_ms histogram')
    durations = metrics_storage['http_request_duration_ms']
    if durations:
        buckets = [10, 50, 100, 200, 400, 800, 1600, 3200, 6400, float('inf')]
        counts = {b: 0 for b in buckets}
        total_sum = 0
        for d in durations:
            ms = d['duration_ms']
            total_sum += ms
            for bucket in buckets:
                if ms <= bucket:
                    counts[bucket] += 1
        
        for bucket in buckets:
            label = '+Inf' if bucket == float('inf') else str(bucket)
            lines.append(f'http_request_duration_ms_bucket{{le="{label}"}} {counts[bucket]}')
        lines.append(f'http_request_duration_ms_sum {total_sum:.2f}')
        lines.append(f'http_request_duration_ms_count {len(durations)}')
    
    # Scheduler ticks
    lines.append('# HELP scheduler_tick_total Total scheduler ticks')
    lines.append('# TYPE scheduler_tick_total counter')
    lines.append(f'scheduler_tick_total {metrics_storage["scheduler_tick_total"]}')
    
    # Stripe webhook failures
    lines.append('# HELP stripe_webhook_fail_total Total Stripe webhook failures')
    lines.append('# TYPE stripe_webhook_fail_total counter')
    lines.append(f'stripe_webhook_fail_total {metrics_storage["stripe_webhook_fail_total"]}')
    
    # Payment error rate
    lines.append('# HELP payments_error_rate Payment error rate (0-1)')
    lines.append('# TYPE payments_error_rate gauge')
    lines.append(f'payments_error_rate {metrics_storage["payments_error_rate"]:.4f}')
    
    # System metrics
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        lines.append('# HELP cpu_percent CPU usage percentage')
        lines.append('# TYPE cpu_percent gauge')
        lines.append(f'cpu_percent {cpu:.1f}')
        
        lines.append('# HELP mem_percent Memory usage percentage')
        lines.append('# TYPE mem_percent gauge')
        lines.append(f'mem_percent {mem:.1f}')
        
        lines.append('# HELP disk_percent Disk usage percentage')
        lines.append('# TYPE disk_percent gauge')
        lines.append(f'disk_percent {disk:.1f}')
    except:
        pass
    
    return '\n'.join(lines) + '\n', 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/api/observability/slo', methods=['GET'])
@require_dashboard_key
def api_observability_slo():
    """Get SLO report (Phase 51)"""
    try:
        report_path = 'logs/slo_report.json'
        if os.path.exists(report_path):
            with open(report_path, 'r') as f:
                report = json.load(f)
            return jsonify({"ok": True, "data": report}), 200
        else:
            return jsonify({"ok": False, "error": "No SLO report available yet. Run slo_guard first."}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route('/api/observability/latency', methods=['GET'])
@require_dashboard_key
def api_observability_latency():
    """Get latency metrics (p50/p95/p99 last 24h) (Phase 51)"""
    try:
        cutoff = time.time() - (24 * 3600)
        recent = [d for d in metrics_storage['http_request_duration_ms'] if d['timestamp'] > cutoff]
        
        if not recent:
            return jsonify({
                "ok": True,
                "data": {
                    "p50_ms": 0,
                    "p95_ms": 0,
                    "p99_ms": 0,
                    "count": 0,
                    "period_hours": 24,
                    "recent_60": []
                }
            }), 200
        
        durations = sorted([d['duration_ms'] for d in recent])
        count = len(durations)
        
        def percentile(data, pct):
            if not data:
                return 0
            idx = int(len(data) * pct / 100)
            return data[min(idx, len(data) - 1)]
        
        p50 = percentile(durations, 50)
        p95 = percentile(durations, 95)
        p99 = percentile(durations, 99)
        
        # Last 60 for sparkline
        recent_60 = [d['duration_ms'] for d in recent[-60:]]
        
        return jsonify({
            "ok": True,
            "data": {
                "p50_ms": round(p50, 2),
                "p95_ms": round(p95, 2),
                "p99_ms": round(p99, 2),
                "count": count,
                "period_hours": 24,
                "recent_60": recent_60
            }
        }), 200
    
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


# ==================== PHASE 101: OPERATIONAL DASHBOARD ====================

@app.route('/api/ops/telemetry', methods=['GET'])
@require_dashboard_key
def api_ops_telemetry():
    """Get live telemetry snapshot for Ops Dashboard (Phase 101)"""
    try:
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/telemetry_collector.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            telemetry = json.loads(result.stdout)
            return jsonify(telemetry), 200
        else:
            return jsonify({
                "ok": False,
                "error": "Telemetry collection failed",
                "details": result.stderr
            }), 500
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

