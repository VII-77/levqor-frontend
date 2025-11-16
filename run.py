from flask import Flask, request, jsonify, Response, redirect
from jsonschema import validate, ValidationError, FormatChecker
from time import time
from uuid import uuid4
from collections import defaultdict, deque
import sqlite3
import json
import os
import logging
import sys
import jwt
import secrets
from datetime import datetime, timedelta

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("levqor")

BUILD = os.environ.get("BUILD_ID", "dev")
VERSION = "1.0.0"
START_TIME = time()

if os.environ.get("SENTRY_DSN"):
    try:
        import sentry_sdk
        from sentry_sdk.integrations.flask import FlaskIntegration
        sentry_sdk.init(
            dsn=os.environ.get("SENTRY_DSN"),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=os.environ.get("ENVIRONMENT", "production"),
            release=f"levqor-backend@{VERSION}"
        )
        log.info("Sentry initialized with Flask integration")
    except ImportError:
        log.warning("SENTRY_DSN set but sentry_sdk not installed")
    except Exception as e:
        log.warning(f"Sentry init failed: {e}")

try:
    import multiprocessing
    # Only initialize scheduler in one worker to prevent job duplication
    # Check if we're in the master process or first worker
    current_process = multiprocessing.current_process()
    worker_id = os.environ.get('GUNICORN_WORKER_ID', '0')
    
    # Initialize scheduler only in worker 0 (or if GUNICORN_WORKER_ID not set, which means single process)
    if worker_id == '0' or not worker_id:
        from monitors.scheduler import get_scheduler
        _scheduler_instance = get_scheduler()
        log.info(f"✅ Scheduler initialized in worker {worker_id or 'main'}")
    else:
        log.info(f"⏭️  Skipping scheduler in worker {worker_id} (preventing duplication)")
        _scheduler_instance = None
except Exception as e:
    log.warning(f"Scheduler initialization skipped: {e}")

app = Flask(__name__, 
    static_folder='public',
    static_url_path='/public')

app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", 512 * 1024))

DB_PATH = os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))

from app import db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{DB_PATH}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 3600,
}
db.init_app(app)

from backend.models.sales_models import Lead, LeadActivity, DFYOrder, DFYActivity, UpsellLog

with app.app_context():
    db.create_all()

from backend.routes.dsar import dsar_bp
from backend.routes.dsar_admin import dsar_admin_bp
from backend.routes.gdpr_optout import gdpr_optout_bp
from backend.routes.legal import legal_bp
from backend.routes.legal_enhanced import legal_enhanced_bp
from backend.routes.marketing import marketing_bp
from backend.routes.marketing_enhanced import marketing_enhanced_bp
from backend.routes.compliance_dashboard import compliance_dashboard_bp
from backend.routes.billing_webhooks import billing_webhooks_bp
from backend.routes.stripe_checkout_webhook import stripe_checkout_bp
from backend.routes.daily_tasks import daily_tasks_bp
from backend.routes.sales import sales_bp
from backend.routes.ase import ase_bp
from backend.routes.dfy_engine import dfy_engine_bp
from backend.routes.followup_endpoints import followup_bp
from backend.routes.support_chat import support_chat_bp
from backend.routes.stripe_check import stripe_check_bp
from backend.routes.stripe_webhook_test import bp as stripe_webhook_test_bp
app.register_blueprint(dsar_bp)
app.register_blueprint(dsar_admin_bp)
app.register_blueprint(gdpr_optout_bp)
app.register_blueprint(legal_bp)
app.register_blueprint(legal_enhanced_bp)
app.register_blueprint(marketing_bp)
app.register_blueprint(marketing_enhanced_bp)
app.register_blueprint(compliance_dashboard_bp)
app.register_blueprint(billing_webhooks_bp)
app.register_blueprint(stripe_checkout_bp)
app.register_blueprint(daily_tasks_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(ase_bp)
app.register_blueprint(dfy_engine_bp)
app.register_blueprint(followup_bp)
app.register_blueprint(support_chat_bp, url_prefix="/api/support")
app.register_blueprint(stripe_check_bp)
app.register_blueprint(stripe_webhook_test_bp, url_prefix="/api/stripe")

_db_connection = None

API_KEYS = set((os.environ.get("API_KEYS") or "").split(",")) - {""}
API_KEYS_NEXT = set((os.environ.get("API_KEYS_NEXT") or "").split(",")) - {""}
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-in-prod")

RATE_BURST = int(os.environ.get("RATE_BURST", 20))
RATE_GLOBAL = int(os.environ.get("RATE_GLOBAL", 200))
WINDOW = 60

_IP_HITS = defaultdict(deque)
_ALL_HITS = deque()
_PROTECTED_PATH_HITS = defaultdict(deque)

def get_db():
    global _db_connection
    if _db_connection is None:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        _db_connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS users(
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            locale TEXT,
            currency TEXT,
            meta TEXT,
            created_at REAL,
            updated_at REAL,
            terms_accepted_at REAL,
            terms_version TEXT,
            terms_accepted_ip TEXT,
            marketing_consent INTEGER DEFAULT 0,
            marketing_consent_at REAL,
            marketing_consent_ip TEXT,
            marketing_double_opt_in INTEGER DEFAULT 0,
            marketing_double_opt_in_at REAL,
            marketing_double_opt_in_token TEXT UNIQUE,
            gdpr_opt_out_marketing INTEGER DEFAULT 0,
            gdpr_opt_out_profiling INTEGER DEFAULT 0,
            gdpr_opt_out_automation INTEGER DEFAULT 0,
            gdpr_opt_out_analytics INTEGER DEFAULT 0,
            gdpr_opt_out_all INTEGER DEFAULT 0,
            gdpr_opt_out_at REAL
          )
        """)
        _db_connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS referrals(
            id TEXT PRIMARY KEY,
            user_id TEXT,
            email TEXT,
            source TEXT NOT NULL,
            campaign TEXT,
            medium TEXT,
            created_at REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
          )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_referrals_user_id ON referrals(user_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_referrals_source ON referrals(source)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_referrals_created_at ON referrals(created_at)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS analytics_aggregates(
            day DATE PRIMARY KEY,
            dau INTEGER NOT NULL DEFAULT 0,
            wau INTEGER NOT NULL DEFAULT 0,
            mau INTEGER NOT NULL DEFAULT 0,
            computed_at TEXT NOT NULL
          )
        """)
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS developer_keys(
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            key_hash TEXT UNIQUE NOT NULL,
            key_prefix TEXT NOT NULL,
            tier TEXT NOT NULL DEFAULT 'sandbox',
            is_active INTEGER NOT NULL DEFAULT 1,
            calls_used INTEGER NOT NULL DEFAULT 0,
            calls_limit INTEGER NOT NULL DEFAULT 1000,
            reset_at REAL NOT NULL,
            created_at REAL NOT NULL,
            last_used_at REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
          )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_developer_keys_user_id ON developer_keys(user_id)")
        _db_connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_developer_keys_key_hash ON developer_keys(key_hash)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_developer_keys_tier ON developer_keys(tier)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS api_usage_log(
            id TEXT PRIMARY KEY,
            key_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            method TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            response_time_ms INTEGER,
            created_at REAL NOT NULL,
            FOREIGN KEY (key_id) REFERENCES developer_keys(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
          )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_api_usage_log_key_id ON api_usage_log(key_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_api_usage_log_created_at ON api_usage_log(created_at)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS partners(
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            webhook_url TEXT,
            revenue_share REAL NOT NULL DEFAULT 0.7,
            is_verified INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            stripe_connect_id TEXT,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            metadata TEXT
          )
        """)
        _db_connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_partners_email ON partners(email)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_partners_verified ON partners(is_verified)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_partners_active ON partners(is_active)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS listings(
            id TEXT PRIMARY KEY,
            partner_id TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            price_cents INTEGER NOT NULL DEFAULT 0,
            is_verified INTEGER NOT NULL DEFAULT 0,
            is_active INTEGER NOT NULL DEFAULT 1,
            downloads INTEGER NOT NULL DEFAULT 0,
            rating REAL,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            metadata TEXT,
            FOREIGN KEY (partner_id) REFERENCES partners(id)
          )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_listings_partner_id ON listings(partner_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_listings_verified ON listings(is_verified)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_listings_category ON listings(category)")
        
        _db_connection.execute("""
          CREATE TABLE IF NOT EXISTS marketplace_orders(
            id TEXT PRIMARY KEY,
            listing_id TEXT NOT NULL,
            partner_id TEXT NOT NULL,
            user_id TEXT,
            amount_cents INTEGER NOT NULL,
            partner_share_cents INTEGER NOT NULL,
            platform_fee_cents INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            stripe_payment_intent_id TEXT,
            created_at REAL NOT NULL,
            completed_at REAL,
            FOREIGN KEY (listing_id) REFERENCES listings(id),
            FOREIGN KEY (partner_id) REFERENCES partners(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
          )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_orders_listing_id ON marketplace_orders(listing_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_orders_partner_id ON marketplace_orders(partner_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_marketplace_orders_status ON marketplace_orders(status)")
        
        _db_connection.execute("PRAGMA journal_mode=WAL")
        _db_connection.execute("PRAGMA synchronous=NORMAL")
        
        # Initialize DSAR tables
        from dsar.models import init_dsar_tables
        init_dsar_tables(_db_connection)
        
        # Initialize compliance tables (SLA, disputes, incidents)
        from compliance.models import init_compliance_tables
        init_compliance_tables(_db_connection)
        
        # Initialize dunning tables
        from dunning.models import init_dunning_tables
        init_dunning_tables(_db_connection)
        
        # Deletion jobs table
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS deletion_jobs(
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                email TEXT NOT NULL,
                requested_at REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                deleted_at REAL,
                error TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_deletion_jobs_status ON deletion_jobs(status)")
        
        # Status snapshots table for historical tracking
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS status_snapshots(
                id TEXT PRIMARY KEY,
                timestamp REAL NOT NULL,
                overall_status TEXT NOT NULL,
                api_status TEXT NOT NULL,
                frontend_status TEXT NOT NULL,
                db_status TEXT NOT NULL,
                stripe_status TEXT NOT NULL,
                notes TEXT
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_status_snapshots_timestamp ON status_snapshots(timestamp)")
        
        # Marketing consent tracking (PECR/GDPR compliant)
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS user_marketing_consent(
                id TEXT PRIMARY KEY,
                user_id TEXT,
                email TEXT NOT NULL,
                scope TEXT NOT NULL,
                status TEXT NOT NULL,
                source TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                confirmed_at REAL,
                token TEXT,
                token_expires_at REAL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_marketing_consent_email ON user_marketing_consent(email)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_marketing_consent_status ON user_marketing_consent(status)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_marketing_consent_token ON user_marketing_consent(token)")
        
        # High-risk data blocks audit table (GDPR/ICO compliance)
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS risk_blocks(
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                blocked_terms TEXT NOT NULL,
                payload_snippet TEXT,
                ip_address TEXT,
                created_at REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_risk_blocks_user ON risk_blocks(user_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_risk_blocks_created ON risk_blocks(created_at)")
        
        # GDPR objection log (Right to Object audit trail)
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS gdpr_objection_log(
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                scope TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_gdpr_objection_user ON gdpr_objection_log(user_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_gdpr_objection_scope ON gdpr_objection_log(scope)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_gdpr_objection_created ON gdpr_objection_log(created_at)")
        
        # Billing dunning state (Stripe payment failure tracking)
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS billing_dunning_state(
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT,
                status TEXT NOT NULL DEFAULT 'none',
                last_event_at REAL,
                next_action_at REAL,
                created_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        _db_connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_dunning_user ON billing_dunning_state(user_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_status ON billing_dunning_state(status)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_next_action ON billing_dunning_state(next_action_at)")
        
        # Billing events (Stripe webhook audit log)
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS billing_events(
                id TEXT PRIMARY KEY,
                user_id TEXT,
                stripe_customer_id TEXT,
                stripe_subscription_id TEXT,
                event_type TEXT NOT NULL,
                attempt_count INTEGER,
                event_payload_snippet TEXT,
                created_at REAL NOT NULL
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_billing_events_user ON billing_events(user_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_billing_events_type ON billing_events(event_type)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_billing_events_customer ON billing_events(stripe_customer_id)")
        
        # Billing dunning events (NEW: Stripe payment recovery email scheduler)
        # Created via migration: db/migrations/008_add_billing_dunning_events.sql
        # Do NOT manually create - run migration for proper schema
        _db_connection.execute("""
            CREATE TABLE IF NOT EXISTS billing_dunning_events(
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                stripe_customer_id TEXT NOT NULL,
                stripe_subscription_id TEXT NOT NULL,
                invoice_id TEXT NOT NULL,
                email TEXT NOT NULL,
                plan TEXT,
                attempt_number INTEGER NOT NULL CHECK(attempt_number IN (1, 2, 3)),
                scheduled_for TEXT NOT NULL,
                sent_at TEXT,
                status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'sent', 'skipped', 'error')),
                error_message TEXT
            )
        """)
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_events_customer ON billing_dunning_events(stripe_customer_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_events_subscription ON billing_dunning_events(stripe_subscription_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_events_invoice ON billing_dunning_events(invoice_id)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_events_status ON billing_dunning_events(status)")
        _db_connection.execute("CREATE INDEX IF NOT EXISTS idx_dunning_events_scheduled ON billing_dunning_events(scheduled_for, status)")
        
        # Migration: Add GDPR opt-out columns if they don't exist
        try:
            cursor = _db_connection.cursor()
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'gdpr_opt_out_marketing' not in columns:
                _db_connection.execute("ALTER TABLE users ADD COLUMN gdpr_opt_out_marketing INTEGER DEFAULT 0")
            if 'gdpr_opt_out_profiling' not in columns:
                _db_connection.execute("ALTER TABLE users ADD COLUMN gdpr_opt_out_profiling INTEGER DEFAULT 0")
            if 'gdpr_opt_out_automation' not in columns:
                _db_connection.execute("ALTER TABLE users ADD COLUMN gdpr_opt_out_automation INTEGER DEFAULT 0")
            if 'gdpr_opt_out_analytics' not in columns:
                _db_connection.execute("ALTER TABLE users ADD COLUMN gdpr_opt_out_analytics INTEGER DEFAULT 0")
            if 'gdpr_opt_out_all' not in columns:
                _db_connection.execute("ALTER TABLE users ADD COLUMN gdpr_opt_out_all INTEGER DEFAULT 0")
            if 'gdpr_opt_out_at' not in columns:
                _db_connection.execute("ALTER TABLE users ADD COLUMN gdpr_opt_out_at REAL")
        except Exception as e:
            log.warning(f"GDPR opt-out migration warning: {e}")
        
        _db_connection.commit()
    return _db_connection

def require_key():
    key = request.headers.get("X-Api-Key")
    if not API_KEYS or key in API_KEYS or key in API_KEYS_NEXT:
        return None
    return jsonify({"error": "forbidden"}), 403

def throttle():
    """
    SECURITY NOTE: Global rate limiting for all endpoints.
    Limits: 20 req/min per IP (burst), 200 req/min global.
    Logs rate limit violations for abuse detection.
    """
    from backend.security import log_security_event
    
    now = time()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    
    while _ALL_HITS and now - _ALL_HITS[0] > WINDOW:
        _ALL_HITS.popleft()
    dq = _IP_HITS[ip]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    
    if len(dq) >= RATE_BURST or len(_ALL_HITS) >= RATE_GLOBAL:
        # Log rate limit violation
        log_security_event(
            "rate_limit",
            ip=ip,
            details={"endpoint": request.path, "method": request.method, "limit_type": "global"},
            severity="warning"
        )
        
        resp = jsonify({"ok": False, "error": "rate_limited", "retry_after": 60})
        resp.status_code = 429
        resp.headers["Retry-After"] = "60"
        resp.headers["X-RateLimit-Limit"] = str(RATE_BURST)
        resp.headers["X-RateLimit-Remaining"] = "0"
        resp.headers["X-RateLimit-Reset"] = str(int(now) + WINDOW)
        return resp
    
    dq.append(now)
    _ALL_HITS.append(now)
    return None

def protected_path_throttle():
    """
    SECURITY NOTE: Stricter rate limiting for sensitive endpoints.
    Protected paths: billing, admin, partners, webhooks.
    Limit: 60 req/min per IP. Logs violations.
    """
    from backend.security import log_security_event
    
    protected_prefixes = ['/billing/', '/api/partners/', '/api/admin/', '/api/user/', '/webhooks/', '/api/legal/', '/api/marketing/']
    if not any(request.path.startswith(prefix) for prefix in protected_prefixes):
        return None
    
    now = time()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    key = f"protected:{ip}"
    
    dq = _PROTECTED_PATH_HITS[key]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    
    if len(dq) >= 60:
        # Log protected path rate limit
        log_security_event(
            "rate_limit_protected",
            ip=ip,
            details={"endpoint": request.path, "method": request.method, "limit": "60/min"},
            severity="warning"
        )
        
        resp = jsonify({"ok": False, "error": "rate_limited", "retry_after": 60})
        resp.status_code = 429
        resp.headers["Retry-After"] = "60"
        return resp
    
    dq.append(now)
    return None

@app.before_request
def _log_in():
    log.info("in %s %s ip=%s ua=%s", request.method, request.path,
             request.headers.get("X-Forwarded-For", request.remote_addr),
             request.headers.get("User-Agent", "-"))
    
    rate_check = protected_path_throttle()
    if rate_check:
        return rate_check

@app.after_request
def add_headers(r):
    r.headers["Access-Control-Allow-Origin"] = "https://levqor.ai"
    r.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS,PATCH"
    r.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Api-Key"
    r.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    r.headers["Content-Security-Policy"] = "default-src 'none'; connect-src https://levqor.ai https://api.levqor.ai; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    r.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    r.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    r.headers["X-Content-Type-Options"] = "nosniff"
    r.headers["X-Frame-Options"] = "DENY"
    r.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    r.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
    return r

@app.errorhandler(Exception)
def on_error(e):
    """Global error handler with correlation ID support"""
    from werkzeug.exceptions import HTTPException
    import os
    
    cid = request.headers.get("X-Request-ID") or request.headers.get("X-Correlation-ID", "unknown")
    debug = os.getenv("INTEL_DEBUG_ERRORS", "false").lower() in ("1", "true", "yes", "on")
    
    # Pass through HTTP exceptions (404, etc.)
    if isinstance(e, HTTPException):
        log.warning(f"HTTP {e.code}: {e.description} [cid={cid}]")
        return jsonify({
            "error": {
                "type": e.__class__.__name__,
                "message": e.description,
                "status": e.code,
                "correlation_id": cid
            }
        }), e.code
    
    # Log full exception details
    log.exception("error: %s [cid=%s]", e, cid)
    
    # Return structured error response
    error_payload = {
        "error": {
            "type": e.__class__.__name__,
            "message": str(e)[:500],
            "status": 500,
            "correlation_id": cid
        }
    }
    
    if debug:
        import traceback
        error_payload["error"]["trace"] = traceback.format_exc().splitlines()[-10:]
    
    return jsonify(error_payload), 500

@app.get("/")
def root():
    return jsonify({"ok": True, "service": "levqor-backend", "version": VERSION, "build": BUILD}), 200

@app.get("/health")
def health():
    return jsonify({"ok": True, "ts": int(time())})

@app.get("/status")
def system_status():
    return jsonify({"status": "pass", "timestamp": int(time())})

@app.get("/public/metrics")
def public_metrics():
    return jsonify({
        "uptime_rolling_7d": 99.99,
        "jobs_today": 0,
        "audit_coverage": 100,
        "last_updated": int(time())
    })

@app.post("/audit")
def audit():
    """
    SECURITY NOTE: Audit logging endpoint with lockout detection.
    Tracks signin events, records failed attempts, implements account lockout.
    Called by NextAuth frontend after successful OAuth authentication.
    """
    from backend.security import (
        log_security_event, 
        record_failed_attempt,
        record_successful_login,
        is_locked_out
    )
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    data = request.get_json(silent=True)
    if not data:
        return bad_request("Invalid JSON")
    
    event = data.get("event", "unknown")
    email = data.get("email", "unknown")
    ip_address = data.get("ip") or request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    user_agent = data.get("user_agent", "")
    ts = data.get("ts", int(time() * 1000))
    
    # Check if account is locked out (even for successful sign-ins)
    if email != "unknown":
        locked, remaining = is_locked_out(email)
        if locked and event == "sign_in":
            log_security_event(
                "signin_blocked_lockout",
                email=email,
                ip=ip_address,
                details={"remaining_seconds": remaining},
                severity="warning"
            )
            return jsonify({
                "ok": False,
                "error": "account_temporarily_locked",
                "retry_after": remaining
            }), 429
    
    # Handle different event types
    if event == "sign_in":
        # Successful sign-in - clear lockout
        if email != "unknown":
            record_successful_login(email)
        log_security_event("signin_success", email=email, ip=ip_address, severity="info")
    
    elif event == "sign_out":
        log_security_event("signout", email=email, ip=ip_address, severity="info")
    
    elif event == "auth_failed":
        # Failed authentication - record attempt
        if email != "unknown":
            record_failed_attempt(email)
        log_security_event("auth_failed", email=email, ip=ip_address, severity="warning")
    
    # Log to file (legacy format for compatibility)
    audit_entry = json.dumps({
        "event": event,
        "email": email,
        "ip": ip_address,
        "user_agent": user_agent,
        "ts": ts
    }, separators=(',', ':'))
    
    audit_file = os.path.join("logs", "audit.log")
    try:
        with open(audit_file, "a") as f:
            f.write(audit_entry + "\n")
    except Exception as e:
        log.warning(f"Failed to write audit log: {e}")
    
    return jsonify({"ok": True}), 200

@app.post("/api/admin/impersonate")
def admin_impersonate():
    admin_token = request.headers.get("X-ADMIN-TOKEN")
    if not ADMIN_TOKEN or admin_token != ADMIN_TOKEN:
        return jsonify({"error": "forbidden"}), 403
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    data = request.get_json(silent=True)
    if not data or "email" not in data:
        return bad_request("email required")
    
    email = data["email"]
    exp = datetime.utcnow() + timedelta(minutes=15)
    
    token = jwt.encode({
        "email": email,
        "exp": exp,
        "impersonated": True
    }, JWT_SECRET, algorithm="HS256")
    
    audit_entry = json.dumps({
        "event": "admin_impersonate",
        "email": email,
        "admin_ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "ts": int(time() * 1000)
    }, separators=(',', ':'))
    
    audit_file = os.path.join("logs", "audit.log")
    try:
        with open(audit_file, "a") as f:
            f.write(audit_entry + "\n")
    except Exception as e:
        log.warning(f"Failed to write audit log: {e}")
    
    return jsonify({"token": token}), 200

JOBS = {}

INTAKE_SCHEMA = {
    "type": "object",
    "properties": {
        "workflow": {"type": "string", "minLength": 1, "maxLength": 128},
        "payload": {"type": "object"},
        "callback_url": {"type": "string", "minLength": 1, "maxLength": 1024},
        "priority": {"type": "string", "enum": ["low", "normal", "high"]},
    },
    "required": ["workflow", "payload"],
    "additionalProperties": False,
}

STATUS_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["queued","running","succeeded","failed"]},
        "created_at": {"type": "number"},
        "result": {},
        "error": {},
    },
    "required": ["status","created_at"],
    "additionalProperties": True,
}

USER_UPSERT_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 3},
        "name": {"type": "string"},
        "locale": {"type": "string"},
        "currency": {"type": "string", "enum": ["GBP", "USD", "EUR"]},
        "meta": {"type": "object"}
    },
    "required": ["email"],
    "additionalProperties": False
}

USER_PATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "locale": {"type": "string"},
        "currency": {"type": "string", "enum": ["GBP", "USD", "EUR"]},
        "meta": {"type": "object"}
    },
    "additionalProperties": False
}

def bad_request(message, details=None):
    return jsonify({"error": message, "details": details}), 400

def row_to_user(row):
    if not row:
        return None
    (id_, email, name, locale, currency, meta, created_at, updated_at, terms_accepted_at, terms_version, terms_accepted_ip, 
     marketing_consent, marketing_consent_at, marketing_consent_ip, marketing_double_opt_in, marketing_double_opt_in_at, marketing_double_opt_in_token) = row
    return {
        "id": id_,
        "email": email,
        "name": name,
        "locale": locale,
        "currency": currency,
        "meta": json.loads(meta) if meta else {},
        "created_at": created_at,
        "updated_at": updated_at,
        "terms_accepted_at": terms_accepted_at,
        "terms_version": terms_version,
        "terms_accepted_ip": terms_accepted_ip,
        "marketing_consent": bool(marketing_consent),
        "marketing_consent_at": marketing_consent_at,
        "marketing_consent_ip": marketing_consent_ip,
        "marketing_double_opt_in": bool(marketing_double_opt_in),
        "marketing_double_opt_in_at": marketing_double_opt_in_at,
        "marketing_double_opt_in_token": marketing_double_opt_in_token
    }

def fetch_user_by_email(email):
    cur = get_db().execute("SELECT id,email,name,locale,currency,meta,created_at,updated_at,terms_accepted_at,terms_version,terms_accepted_ip,marketing_consent,marketing_consent_at,marketing_consent_ip,marketing_double_opt_in,marketing_double_opt_in_at,marketing_double_opt_in_token FROM users WHERE email = ?", (email,))
    return row_to_user(cur.fetchone())

def fetch_user_by_id(uid):
    cur = get_db().execute("SELECT id,email,name,locale,currency,meta,created_at,updated_at,terms_accepted_at,terms_version,terms_accepted_ip,marketing_consent,marketing_consent_at,marketing_consent_ip,marketing_double_opt_in,marketing_double_opt_in_at,marketing_double_opt_in_token FROM users WHERE id = ?", (uid,))
    return row_to_user(cur.fetchone())

def fetch_user_by_marketing_token(token):
    cur = get_db().execute("SELECT id,email,name,locale,currency,meta,created_at,updated_at,terms_accepted_at,terms_version,terms_accepted_ip,marketing_consent,marketing_consent_at,marketing_consent_ip,marketing_double_opt_in,marketing_double_opt_in_at,marketing_double_opt_in_token FROM users WHERE marketing_double_opt_in_token = ?", (token,))
    return row_to_user(cur.fetchone())

@app.post("/api/v1/intake")
def intake():
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    # Check for account suspension (billing dunning)
    api_key = request.headers.get("X-Api-Key")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT user_id FROM api_keys WHERE key_hash = ?", (hashlib.sha256(api_key.encode()).hexdigest(),))
    key_record = cursor.fetchone()
    
    if key_record and key_record[0]:
        user_id = key_record[0]
        if is_account_suspended(user_id):
            return jsonify({
                "ok": False,
                "error": "ACCOUNT_SUSPENDED",
                "message": "Account access suspended due to payment failure. Please update your billing details to restore service."
            }), 403
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    data = request.get_json(silent=True)
    if data is None:
        return bad_request("Invalid JSON")
    try:
        validate(instance=data, schema=INTAKE_SCHEMA, format_checker=FormatChecker())
    except ValidationError as e:
        return bad_request("Invalid request body", e.message)
    
    if len(json.dumps(data["payload"])) > 200 * 1024:
        return bad_request("payload too large")
    
    if "callback_url" in data:
        url = data["callback_url"]
        if not url.startswith(("http://", "https://")):
            return bad_request("callback_url must be a valid HTTP(S) URL")
    
    # High-risk data firewall (GDPR/ICO compliance)
    from compliance.high_risk_firewall import validate_workflow_content, log_high_risk_block
    is_valid, error_msg, blocked_terms = validate_workflow_content(data)
    
    if not is_valid:
        # Log the block attempt
        api_key = request.headers.get("X-Api-Key", "")
        user_id = api_key[:8] if api_key else "anonymous"
        ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
        payload_snippet = json.dumps(data)[:200]
        
        log_high_risk_block(get_db(), user_id, blocked_terms, payload_snippet, ip_address)
        
        return jsonify({
            "ok": False,
            "category": "high_risk_data",
            "error": error_msg
        }), 400

    job_id = uuid4().hex
    JOBS[job_id] = {
        "status": "queued",
        "created_at": time(),
        "input": data,
        "result": None,
        "error": None,
    }

    return jsonify({"job_id": job_id, "status": "queued"}), 202

@app.get("/api/v1/status/<job_id>")
def status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "not_found", "job_id": job_id}), 404

    public_view = {
        "status": job["status"],
        "created_at": job["created_at"],
        "result": job["result"],
        "error": job["error"],
    }
    try:
        validate(instance=public_view, schema=STATUS_SCHEMA)
    except ValidationError:
        pass

    return jsonify({"job_id": job_id, **public_view}), 200

@app.post("/api/v1/_dev/complete/<job_id>")
def dev_complete(job_id):
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"error": "not_found"}), 404
    body = request.get_json(silent=True) or {}
    job["status"] = "succeeded"
    job["result"] = body.get("result", {"ok": True})
    return jsonify({"ok": True})

@app.post("/api/v1/users/upsert")
def users_upsert():
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    body = request.get_json(silent=True) or {}
    try:
        validate(instance=body, schema=USER_UPSERT_SCHEMA, format_checker=FormatChecker())
    except ValidationError as e:
        return bad_request("Invalid user payload", e.message)

    now = time()
    email = body["email"].strip().lower()
    name = body.get("name")
    locale = body.get("locale")
    currency = body.get("currency")
    meta = json.dumps(body.get("meta", {}))

    existing = fetch_user_by_email(email)
    if existing:
        get_db().execute(
            "UPDATE users SET name=?, locale=?, currency=?, meta=?, updated_at=? WHERE email=?",
            (name, locale, currency, meta, now, email)
        )
        get_db().commit()
        return jsonify({"updated": True, "user": fetch_user_by_email(email)}), 200
    else:
        uid = uuid4().hex
        get_db().execute(
            "INSERT INTO users(id,email,name,locale,currency,meta,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?)",
            (uid, email, name, locale, currency, meta, now, now)
        )
        get_db().commit()
        return jsonify({"created": True, "user": fetch_user_by_id(uid)}), 201

@app.patch("/api/v1/users/<user_id>")
def users_patch(user_id):
    guard = require_key()
    if guard:
        return guard
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    body = request.get_json(silent=True) or {}
    try:
        validate(instance=body, schema=USER_PATCH_SCHEMA, format_checker=FormatChecker())
    except ValidationError as e:
        return bad_request("Invalid patch payload", e.message)

    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404

    name = body.get("name", u["name"])
    locale = body.get("locale", u["locale"])
    currency = body.get("currency", u["currency"])
    meta = u["meta"].copy()
    meta.update(body.get("meta", {}))
    get_db().execute(
        "UPDATE users SET name=?, locale=?, currency=?, meta=?, updated_at=? WHERE id=?",
        (name, locale, currency, json.dumps(meta), time(), user_id)
    )
    get_db().commit()
    return jsonify({"updated": True, "user": fetch_user_by_id(user_id)}), 200

@app.get("/api/v1/users/<user_id>")
def users_get(user_id):
    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404
    return jsonify(u), 200

@app.post("/api/v1/users/<user_id>/accept-terms")
def accept_terms(user_id):
    """Record TOS acceptance for a user"""
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    body = request.get_json(silent=True) or {}
    version = body.get("version", "2025-11-14")
    
    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404
    
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr or "unknown"
    
    redacted_ip = ".".join(ip.split(".")[:3]) + ".xxx" if "." in ip else ip[:12] + "..."
    
    now = time()
    get_db().execute(
        "UPDATE users SET terms_accepted_at=?, terms_version=?, terms_accepted_ip=?, updated_at=? WHERE id=?",
        (now, version, ip, now, user_id)
    )
    get_db().commit()
    
    print(f"[TOS] User {user_id} accepted terms v{version} at {now} from {redacted_ip}")
    
    return jsonify({
        "ok": True,
        "version": version,
        "at": datetime.fromtimestamp(now).isoformat()
    }), 200

@app.post("/api/v1/users/<user_id>/marketing-consent")
def marketing_consent(user_id):
    """Set marketing consent and generate double opt-in token"""
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    body = request.get_json(silent=True) or {}
    consent = body.get("consent", False)
    
    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404
    
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr or "unknown"
    
    redacted_ip = ".".join(ip.split(".")[:3]) + ".xxx" if "." in ip else ip[:12] + "..."
    now = time()
    
    if consent:
        token = secrets.token_urlsafe(32)
        get_db().execute(
            """UPDATE users SET 
               marketing_consent=1, 
               marketing_consent_at=?, 
               marketing_consent_ip=?, 
               marketing_double_opt_in=0,
               marketing_double_opt_in_at=NULL,
               marketing_double_opt_in_token=?,
               updated_at=? 
               WHERE id=?""",
            (now, ip, token, now, user_id)
        )
        get_db().commit()
        
        print(f"[MARKETING] User {user_id} ({u['email']}) opted in for marketing at {now} from {redacted_ip}")
        print(f"[MARKETING] Action: opt_in | User: {user_id} | Email: {u['email']} | IP: {redacted_ip} | Timestamp: {now}")
        
        return jsonify({
            "ok": True,
            "consent": True,
            "token": token,
            "email": u["email"],
            "name": u.get("name", "")
        }), 200
    else:
        get_db().execute(
            """UPDATE users SET 
               marketing_consent=0,
               marketing_consent_at=NULL,
               marketing_consent_ip=NULL,
               marketing_double_opt_in=0,
               marketing_double_opt_in_at=NULL,
               marketing_double_opt_in_token=NULL,
               updated_at=? 
               WHERE id=?""",
            (now, user_id)
        )
        get_db().commit()
        
        print(f"[MARKETING] User {user_id} ({u['email']}) opted out of marketing at {now} from {redacted_ip}")
        print(f"[MARKETING] Action: opt_out | User: {user_id} | Email: {u['email']} | IP: {redacted_ip} | Timestamp: {now}")
        
        return jsonify({
            "ok": True,
            "consent": False
        }), 200

@app.post("/api/v1/marketing/confirm")
def marketing_confirm_token():
    """Confirm marketing double opt-in via token"""
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    body = request.get_json(silent=True) or {}
    token = body.get("token", "").strip()
    
    if not token:
        return jsonify({"error": "token_required"}), 400
    
    u = fetch_user_by_marketing_token(token)
    if not u:
        return jsonify({"error": "invalid_token"}), 404
    
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr or "unknown"
    
    redacted_ip = ".".join(ip.split(".")[:3]) + ".xxx" if "." in ip else ip[:12] + "..."
    now = time()
    
    get_db().execute(
        """UPDATE users SET 
           marketing_double_opt_in=1,
           marketing_double_opt_in_at=?,
           marketing_double_opt_in_token=NULL,
           updated_at=? 
           WHERE id=?""",
        (now, now, u["id"])
    )
    get_db().commit()
    
    print(f"[MARKETING] User {u['id']} ({u['email']}) confirmed double opt-in at {now} from {redacted_ip}")
    print(f"[MARKETING] Action: double_opt_in_confirmed | User: {u['id']} | Email: {u['email']} | IP: {redacted_ip} | Timestamp: {now}")
    
    return jsonify({
        "ok": True,
        "confirmed": True,
        "email": u["email"]
    }), 200

@app.post("/api/v1/users/<user_id>/marketing-unsubscribe")
def marketing_unsubscribe(user_id):
    """Unsubscribe from marketing emails"""
    u = fetch_user_by_id(user_id)
    if not u:
        return jsonify({"error": "not_found", "user_id": user_id}), 404
    
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.remote_addr or "unknown"
    
    redacted_ip = ".".join(ip.split(".")[:3]) + ".xxx" if "." in ip else ip[:12] + "..."
    now = time()
    
    get_db().execute(
        """UPDATE users SET 
           marketing_consent=0,
           marketing_double_opt_in=0,
           marketing_consent_at=NULL,
           marketing_consent_ip=NULL,
           marketing_double_opt_in_at=NULL,
           marketing_double_opt_in_token=NULL,
           updated_at=? 
           WHERE id=?""",
        (now, user_id)
    )
    get_db().commit()
    
    print(f"[MARKETING] User {user_id} ({u['email']}) unsubscribed at {now} from {redacted_ip}")
    print(f"[MARKETING] Action: unsubscribe | User: {user_id} | Email: {u['email']} | IP: {redacted_ip} | Timestamp: {now}")
    
    return jsonify({
        "ok": True,
        "unsubscribed": True
    }), 200

@app.post("/api/v1/referrals/track")
def track_referral():
    """Track a referral source (public endpoint for analytics)"""
    rate_check = throttle()
    if rate_check:
        return rate_check
    
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()
    source = body.get("source", "direct").strip()
    campaign = body.get("campaign", "").strip()
    medium = body.get("medium", "").strip()
    
    if not email or not source:
        return jsonify({"error": "email and source required"}), 400
    
    user = fetch_user_by_email(email)
    user_id = user["id"] if user else None
    
    referral_id = uuid4().hex
    now = time()
    
    get_db().execute(
        "INSERT INTO referrals(id, user_id, email, source, campaign, medium, created_at) VALUES (?,?,?,?,?,?,?)",
        (referral_id, user_id, email, source, campaign, medium, now)
    )
    get_db().commit()
    
    return jsonify({"ok": True, "referral_id": referral_id}), 201

@app.get("/admin/analytics")
def admin_analytics():
    """Get retention and referral analytics (requires admin token)"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "unauthorized"}), 401
    
    token = auth_header.split(" ")[1]
    if token != ADMIN_TOKEN:
        return jsonify({"error": "forbidden"}), 403
    
    now = time()
    seven_days_ago = now - (7 * 24 * 60 * 60)
    thirty_days_ago = now - (30 * 24 * 60 * 60)
    
    db = get_db()
    
    cursor = db.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT COUNT(*) FROM users WHERE created_at >= ?", (seven_days_ago,))
    new_users_7d = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT COUNT(*) FROM users WHERE created_at >= ?", (thirty_days_ago,))
    new_users_30d = cursor.fetchone()[0]
    
    cursor = db.execute("""
        SELECT source, COUNT(*) as count 
        FROM referrals 
        WHERE created_at >= ? 
        GROUP BY source 
        ORDER BY count DESC 
        LIMIT 10
    """, (thirty_days_ago,))
    top_referrals = [{"source": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    cursor = db.execute("SELECT COUNT(*) FROM referrals WHERE created_at >= ?", (seven_days_ago,))
    referrals_7d = cursor.fetchone()[0]
    
    cursor = db.execute("SELECT COUNT(*) FROM referrals WHERE created_at >= ?", (thirty_days_ago,))
    referrals_30d = cursor.fetchone()[0]
    
    return jsonify({
        "users": {
            "total": total_users,
            "new_7d": new_users_7d,
            "new_30d": new_users_30d,
        },
        "referrals": {
            "total_7d": referrals_7d,
            "total_30d": referrals_30d,
            "top_sources": top_referrals
        },
        "timestamp": int(now)
    }), 200

@app.get("/api/v1/users")
def users_lookup():
    email = request.args.get("email", "").strip().lower()
    if not email:
        return bad_request("email query param required")
    u = fetch_user_by_email(email)
    if not u:
        return jsonify({"error": "not_found", "email": email}), 404
    return jsonify(u), 200

@app.get("/api/v1/ops/health")
def ops_health():
    guard = require_key()
    if guard:
        return guard
    return jsonify({"ok": True, "ts": int(time())}), 200

@app.get("/ops/uptime")
def ops_uptime():
    """Public endpoint for system uptime metrics"""
    uptime_seconds = int(time() - START_TIME)
    return jsonify({
        "uptime_seconds": uptime_seconds,
        "start_time": int(START_TIME),
        "current_time": int(time()),
        "version": VERSION,
        "build": BUILD
    }), 200

@app.get("/ops/queue_health")
def ops_queue_health():
    """Public endpoint for job queue health monitoring"""
    queued = sum(1 for j in JOBS.values() if j["status"] == "queued")
    running = sum(1 for j in JOBS.values() if j["status"] == "running")
    completed = sum(1 for j in JOBS.values() if j["status"] == "succeeded")
    failed = sum(1 for j in JOBS.values() if j["status"] == "failed")
    total = len(JOBS)
    
    return jsonify({
        "healthy": True,
        "queue_stats": {
            "queued": queued,
            "running": running,
            "completed": completed,
            "failed": failed,
            "total": total
        },
        "timestamp": int(time())
    }), 200

@app.get("/billing/health")
def billing_health():
    """Public endpoint to verify Stripe integration health"""
    stripe_key = os.environ.get("STRIPE_SECRET_KEY", "")
    stripe_webhook = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    
    has_stripe_key = bool(stripe_key and stripe_key.startswith("sk_"))
    has_webhook_secret = bool(stripe_webhook and len(stripe_webhook) > 10)
    
    healthy = has_stripe_key and has_webhook_secret
    
    return jsonify({
        "healthy": healthy,
        "stripe_key_configured": has_stripe_key,
        "webhook_secret_configured": has_webhook_secret,
        "timestamp": int(time())
    }), 200 if healthy else 503

@app.get("/ops/autoscale/dryrun")
def autoscale_dryrun():
    """Dry-run autoscale decision based on current metrics"""
    from monitors.autoscale import get_controller
    
    queue_depth = int(request.args.get("queue_depth", 0))
    p95_latency = float(request.args.get("p95_latency_ms", 0))
    error_rate = float(request.args.get("error_rate", 0))
    
    controller = get_controller()
    decision = controller.decide_action(queue_depth, p95_latency, error_rate)
    
    return jsonify(decision), 200

@app.post("/ops/autoscale/apply")
def autoscale_apply():
    """Apply autoscale action"""
    from monitors.autoscale import get_controller
    
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json() or {}
    queue_depth = int(data.get("queue_depth", 0))
    p95_latency = float(data.get("p95_latency_ms", 0))
    error_rate = float(data.get("error_rate", 0))
    
    controller = get_controller()
    decision = controller.decide_action(queue_depth, p95_latency, error_rate)
    result = controller.apply_action(decision)
    
    return jsonify(result), 200

@app.post("/ops/recover")
def ops_recover():
    """Execute incident recovery"""
    from monitors.incident_response import get_responder
    
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json() or {}
    error_rate = float(data.get("error_rate", 0))
    recent_failures = int(data.get("recent_failures", 0))
    dry_run = bool(data.get("dry_run", False))
    
    responder = get_responder()
    result = responder.recover(error_rate, recent_failures, dry_run)
    
    return jsonify(result), 200

@app.get("/admin/retention")
def admin_retention():
    """Get retention metrics (DAU/WAU/MAU)"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT day, dau, wau, mau, computed_at
        FROM analytics_aggregates
        ORDER BY day DESC
        LIMIT 30
    """)
    
    rows = cursor.fetchall()
    metrics = [
        {
            "day": row[0],
            "dau": row[1],
            "wau": row[2],
            "mau": row[3],
            "computed_at": row[4]
        }
        for row in rows
    ]
    
    return jsonify({
        "ok": True,
        "metrics": metrics,
        "count": len(metrics)
    }), 200

@app.get("/ops/cost/forecast")
def cost_forecast():
    """Get 30-day cost forecast"""
    from scripts.cost_predict import load_cached_forecast, forecast_next_30d
    from scripts.cost_predict import get_stripe_charges_last_30d, estimate_infra_costs, estimate_openai_usage
    
    cached = load_cached_forecast()
    if cached:
        return jsonify(cached), 200
    
    stripe_charges = get_stripe_charges_last_30d()
    infra = estimate_infra_costs()
    openai = estimate_openai_usage()
    
    forecast = forecast_next_30d(stripe_charges, infra, openai)
    
    return jsonify(forecast), 200

OPENAPI = {
    "openapi": "3.0.0",
    "info": {"title": "Levqor API", "version": VERSION},
    "paths": {
        "/api/v1/intake": {"post": {"summary": "Submit job", "responses": {"202": {"description": "Queued"}}}},
        "/api/v1/status/{job_id}": {"get": {"summary": "Get status", "responses": {"200": {"description": "OK"}}}},
        "/api/v1/users/upsert": {"post": {"summary": "Create or update user", "responses": {"201": {"description": "Created"}}}},
        "/api/v1/users/{user_id}": {"get": {"summary": "Get user by ID", "responses": {"200": {"description": "OK"}}}},
        "/api/v1/users": {"get": {"summary": "Lookup user by email", "responses": {"200": {"description": "OK"}}}}
    }
}

@app.get("/public/openapi.json")
def openapi():
    return jsonify(OPENAPI)

from api.admin.flags import bp as flags_bp
from api.admin.ledger import bp as ledger_bp
from api.admin.growth import bp as growth_bp
from api.billing.pricing import bp as pricing_bp
from api.billing.discounts import bp as discounts_bp
from api.billing.checkout import bp as billing_checkout_bp
from api.admin.insights import bp as admin_insights_bp
from api.admin.runbooks import bp as admin_runbooks_bp
from api.admin.postmortem import bp as admin_postmortem_bp
from ops.admin.insights import bp as ops_insights_bp
from ops.admin.runbooks import bp as ops_runbooks_bp
from ops.admin.postmortem import bp as ops_postmortem_bp
from monitors.auto_tune import suggest_tuning
from api.developer.keys import bp as developer_keys_bp
from api.developer.sandbox import bp as developer_sandbox_bp
from api.routes.insights.preview import bp as insights_preview_bp
from api.routes.insights.report import bp as insights_report_bp
from modules.partner_api.registry import bp as partner_registry_bp
from modules.marketplace.listings import bp as marketplace_listings_bp
from api.routes.intelligence import bp as intelligence_bp

app.register_blueprint(flags_bp)
app.register_blueprint(ledger_bp)
app.register_blueprint(growth_bp)
app.register_blueprint(pricing_bp)
app.register_blueprint(discounts_bp)
app.register_blueprint(billing_checkout_bp)
app.register_blueprint(admin_insights_bp)
app.register_blueprint(admin_runbooks_bp)
app.register_blueprint(admin_postmortem_bp)
app.register_blueprint(ops_insights_bp)
app.register_blueprint(ops_runbooks_bp)
app.register_blueprint(ops_postmortem_bp)
app.register_blueprint(developer_keys_bp)
app.register_blueprint(developer_sandbox_bp)
app.register_blueprint(insights_preview_bp)
app.register_blueprint(insights_report_bp)
app.register_blueprint(partner_registry_bp)
app.register_blueprint(marketplace_listings_bp)
app.register_blueprint(intelligence_bp)

@app.get("/ops/auto_tune")
def auto_tune_endpoint():
    current_p95 = request.args.get("current_p95", type=float, default=100.0)
    current_queue = request.args.get("current_queue", type=int, default=1)
    suggestions = suggest_tuning(current_p95, current_queue)
    return jsonify({"status": "ok", "suggestions": suggestions}), 200

# ============================================================================
# DSAR (Data Subject Access Request) Endpoints - GDPR Compliance
# ============================================================================

@app.post("/api/data-export/request")
def dsar_request_export():
    """Request a data export (GDPR Article 15 - Right of Access)"""
    from dsar.exporter import generate_user_export
    from dsar.security import create_download_token_and_otp
    from dsar.email import send_export_ready_email
    from dsar.audit import log_dsar_event
    
    # Get user from session (X-User-Email header set by frontend proxy)
    user_email = request.headers.get("X-User-Email")
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # Get user
    cursor.execute("SELECT id, email, name FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id, email, name = user_row
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    
    # Rate limiting: Check for recent requests
    twenty_four_hours_ago = time() - (24 * 60 * 60)
    cursor.execute("""
        SELECT id FROM dsar_requests 
        WHERE user_id = ? 
        AND requested_at >= ? 
        AND status IN ('pending', 'processing', 'ready', 'emailed')
    """, (user_id, twenty_four_hours_ago))
    
    if cursor.fetchone():
        log_dsar_event(db, user_id, email, "request_rate_limited", ip_address, user_agent)
        return jsonify({
            "ok": False,
            "error": "RATE_LIMITED",
            "message": "You already requested an export in the last 24 hours. Please wait before requesting again."
        }), 429
    
    # Create DSAR request
    request_id = str(uuid4())
    now = time()
    
    cursor.execute("""
        INSERT INTO dsar_requests (id, user_id, email, requested_at, status, type, ip_address)
        VALUES (?, ?, ?, ?, 'processing', 'export', ?)
    """, (request_id, user_id, email, now, ip_address))
    db.commit()
    
    log_dsar_event(db, user_id, email, "request_created", ip_address, user_agent, request_id)
    
    try:
        # Generate export
        export_result = generate_user_export(db, user_id)
        
        # Create export record with tokens
        export_id = str(uuid4())
        created_at = time()
        expires_at = created_at + (24 * 60 * 60)  # 24 hours
        
        download_token, otp, otp_hash = create_download_token_and_otp()
        otp_expires_at = created_at + (15 * 60)  # 15 minutes
        
        cursor.execute("""
            INSERT INTO dsar_exports 
            (id, request_id, user_id, created_at, expires_at, storage_path, 
             download_token, download_token_expires_at, otp_hash, otp_expires_at, data_categories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (export_id, request_id, user_id, created_at, expires_at, 
              export_result["storage_path"], download_token, expires_at, 
              otp_hash, otp_expires_at, export_result["data_categories"]))
        
        # Update request status
        cursor.execute("UPDATE dsar_requests SET status = 'ready' WHERE id = ?", (request_id,))
        db.commit()
        
        log_dsar_event(db, user_id, email, "export_generated", ip_address, user_agent, request_id, export_id)
        
        # Send email
        email_result = send_export_ready_email(email, name, download_token, otp)
        
        if email_result["ok"]:
            cursor.execute("UPDATE dsar_requests SET status = 'emailed' WHERE id = ?", (request_id,))
            db.commit()
            log_dsar_event(db, user_id, email, "email_sent", ip_address, user_agent, request_id, export_id)
            
            return jsonify({
                "ok": True,
                "message": "If an export is available, you will receive an email shortly with download instructions."
            }), 202
        else:
            log_dsar_event(db, user_id, email, "email_failed", ip_address, user_agent, request_id, export_id, json.dumps(email_result))
            return jsonify({
                "ok": True,
                "message": "Export generated but email failed. Contact privacy@levqor.ai",
                "warning": "EMAIL_FAILED"
            }), 202
    
    except Exception as e:
        cursor.execute("UPDATE dsar_requests SET status = 'failed', notes = ? WHERE id = ?", (str(e), request_id))
        db.commit()
        log_dsar_event(db, user_id, email, "export_failed", ip_address, user_agent, request_id, details=str(e))
        log.error(f"DSAR export failed for user {user_id}: {e}", exc_info=True)
        return jsonify({
            "ok": False,
            "error": "EXPORT_FAILED",
            "message": "Export generation failed. Please try again later or contact privacy@levqor.ai"
        }), 500


@app.post("/api/data-export/download")
def dsar_download():
    """Download export with token + OTP verification"""
    from dsar.security import verify_download_token_and_otp
    from dsar.audit import log_dsar_event
    import os
    
    data = request.get_json() or {}
    token = data.get("token")
    otp = data.get("otp")
    
    if not token or not otp:
        return jsonify({"ok": False, "error": "MISSING_CREDENTIALS"}), 400
    
    db = get_db()
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    
    # Verify token and OTP
    export_data, error_reason = verify_download_token_and_otp(db, token, otp)
    
    if error_reason:
        log_dsar_event(db, None, None, "download_failed", ip_address, user_agent, details=error_reason)
        return jsonify({"ok": False, "error": error_reason}), 403
    
    # Get user info for logging
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (export_data["user_id"],))
    user_row = cursor.fetchone()
    user_email = user_row[0] if user_row else "unknown"
    
    log_dsar_event(db, export_data["user_id"], user_email, "download_attempt", ip_address, user_agent, export_id=export_data["export_id"])
    
    # Check if file exists
    storage_path = export_data["storage_path"]
    if not os.path.exists(storage_path):
        log_dsar_event(db, export_data["user_id"], user_email, "file_not_found", ip_address, user_agent, export_id=export_data["export_id"])
        return jsonify({"ok": False, "error": "FILE_NOT_FOUND"}), 404
    
    # Update downloaded_at timestamp
    cursor.execute("UPDATE dsar_exports SET downloaded_at = ? WHERE id = ?", (time(), export_data["export_id"]))
    cursor.execute("UPDATE dsar_requests SET status = 'downloaded' WHERE id = (SELECT request_id FROM dsar_exports WHERE id = ?)", (export_data["export_id"],))
    db.commit()
    
    log_dsar_event(db, export_data["user_id"], user_email, "download_success", ip_address, user_agent, export_id=export_data["export_id"])
    
    # Stream file
    from datetime import datetime
    filename = f"levqor-data-export-{datetime.utcnow().strftime('%Y%m%d')}.zip"
    
    return Response(
        open(storage_path, 'rb').read(),
        mimetype='application/zip',
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )


@app.post("/api/privacy/delete-my-data")
def delete_my_data():
    """
    Delete all user data (GDPR Article 17 - Right to Erasure)
    
    SAFETY: Preserves billing/financial records required by law
    """
    from dsar.audit import log_dsar_event
    from uuid import uuid4
    
    # Get authenticated user (from session or API key)
    user_email = request.args.get("email")  # TODO: Replace with actual session/auth
    
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED", "message": "Authentication required"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # Find user
    cursor.execute("SELECT id, email FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id, email = user_row
    
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    
    # Log deletion request
    log_dsar_event(db, user_id, email, "delete_my_data_requested", ip_address, user_agent, details="User requested full data deletion")
    
    deleted_counts = {}
    
    try:
        # Delete API usage logs
        cursor.execute("DELETE FROM api_usage_log WHERE user_id = ?", (user_id,))
        deleted_counts["api_usage_log"] = cursor.rowcount
        
        # Delete risk blocks
        cursor.execute("DELETE FROM risk_blocks WHERE user_id = ?", (user_id,))
        deleted_counts["risk_blocks"] = cursor.rowcount
        
        # Delete referrals
        cursor.execute("DELETE FROM referrals WHERE user_id = ?", (user_id,))
        deleted_counts["referrals"] = cursor.rowcount
        
        # Delete developer keys
        cursor.execute("DELETE FROM developer_keys WHERE user_id = ?", (user_id,))
        deleted_counts["developer_keys"] = cursor.rowcount
        
        # Delete DSAR requests and exports (physical files too)
        cursor.execute("SELECT storage_path FROM dsar_exports WHERE user_id = ?", (user_id,))
        export_paths = [row[0] for row in cursor.fetchall()]
        
        for path in export_paths:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    log.warning(f"Failed to delete export file {path}: {e}")
        
        cursor.execute("DELETE FROM dsar_exports WHERE user_id = ?", (user_id,))
        deleted_counts["dsar_exports"] = cursor.rowcount
        
        cursor.execute("DELETE FROM dsar_requests WHERE user_id = ?", (user_id,))
        deleted_counts["dsar_requests"] = cursor.rowcount
        
        # Delete marketing consent (anonymize if PECR requires keeping denials)
        cursor.execute("UPDATE user_marketing_consent SET user_id = NULL, email = 'deleted@deleted.local' WHERE user_id = ?", (user_id,))
        deleted_counts["marketing_consent_anonymized"] = cursor.rowcount
        
        # Delete marketplace orders (anonymize user_id, keep financial data)
        cursor.execute("UPDATE marketplace_orders SET user_id = NULL WHERE user_id = ?", (user_id,))
        deleted_counts["marketplace_orders_anonymized"] = cursor.rowcount
        
        # DO NOT DELETE:
        # - billing_events (legal requirement)
        # - billing_dunning_state (financial record)
        # - users table (anonymized below)
        
        # Anonymize user record (keep for billing reference)
        cursor.execute("""
            UPDATE users 
            SET email = ?, 
                name = 'Deleted User',
                locale = NULL,
                currency = NULL,
                meta = NULL,
                updated_at = ?
            WHERE id = ?
        """, (f"deleted_{user_id}@deleted.local", time(), user_id))
        
        db.commit()
        
        log_dsar_event(db, user_id, email, "delete_my_data_completed", ip_address, user_agent, 
                      details=f"Deleted {sum(deleted_counts.values())} records")
        
        log.info(f"[DELETE_MY_DATA] User {email} deleted their data: {deleted_counts}")
        
        return jsonify({
            "ok": True,
            "message": "Your data has been deleted. Billing records are retained as required by law.",
            "deleted": deleted_counts
        }), 200
    
    except Exception as e:
        db.rollback()
        log.error(f"[DELETE_MY_DATA] Error deleting data for {email}: {e}")
        log_dsar_event(db, user_id, email, "delete_my_data_failed", ip_address, user_agent, details=str(e))
        
        return jsonify({
            "ok": False,
            "error": "DELETION_FAILED",
            "message": "An error occurred while deleting your data. Please contact support."
        }), 500


# ============================================================================
# DSAR (via Email Attachment) - Simplified endpoint for GDPR/UK-GDPR compliance
# ============================================================================

@app.post("/api/dsar/request")
def dsar_request_via_email():
    """
    Request data export sent directly via email attachment (no download links)
    GDPR/UK-GDPR Article 15 - Right of Access
    """
    from dsar.exporter import generate_user_export_bytes
    from dsar.email import send_export_as_attachment
    from dsar.audit import log_dsar_event
    
    # Get user from session or request body
    user_email = request.headers.get("X-User-Email")
    
    # Allow email-only requests (for users not signed in)
    if not user_email:
        data = request.get_json() or {}
        user_email = data.get("email")
    
    if not user_email:
        return jsonify({"ok": False, "error": "Email required"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Get user
    cursor.execute("SELECT id, email, name FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    
    if not user_row:
        # For privacy, don't reveal if user exists - just say request received
        return jsonify({
            "ok": True,
            "status": "processing",
            "message": "If an account exists with this email, you'll receive your data export shortly."
        }), 202
    
    user_id, email, name = user_row
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    
    # Rate limiting: Check for recent requests (24 hours)
    twenty_four_hours_ago = time() - (24 * 60 * 60)
    cursor.execute("""
        SELECT id FROM dsar_requests 
        WHERE user_id = ? 
        AND requested_at >= ? 
        AND status IN ('pending', 'processing', 'completed')
    """, (user_id, twenty_four_hours_ago))
    
    if cursor.fetchone():
        log_dsar_event(db, user_id, email, "request_rate_limited", ip_address, user_agent)
        return jsonify({
            "ok": False,
            "error": "RATE_LIMITED",
            "message": "You already requested an export in the last 24 hours. Please wait before requesting again."
        }), 429
    
    # Create DSAR request record
    request_id = str(uuid4())
    now = time()
    
    cursor.execute("""
        INSERT INTO dsar_requests (id, user_id, email, requested_at, status, type, ip_address)
        VALUES (?, ?, ?, ?, 'processing', 'email_export', ?)
    """, (request_id, user_id, email, now, ip_address))
    db.commit()
    
    log_dsar_event(db, user_id, email, "request_created", ip_address, user_agent, request_id)
    
    # Generate export and send via email (synchronous for now)
    # TODO: Move to background worker for production at scale
    try:
        # Generate ZIP in memory
        zip_bytes, filename, size_bytes, data_categories = generate_user_export_bytes(db, user_id)
        
        # Send via email as attachment
        email_result = send_export_as_attachment(email, name, zip_bytes, filename, request_id[:8])
        
        if email_result["ok"]:
            cursor.execute("""
                UPDATE dsar_requests 
                SET status = 'completed', notes = ? 
                WHERE id = ?
            """, (f"Email sent successfully. Size: {size_bytes} bytes", request_id))
            db.commit()
            
            log_dsar_event(db, user_id, email, "email_export_sent", ip_address, user_agent, request_id, 
                          details=f"size={size_bytes}, filename={filename}")
            log.info(f"[DSAR] Export email sent to {email}, size {size_bytes} bytes, ref {request_id[:8]}")
            
            return jsonify({
                "ok": True,
                "status": "completed",
                "reference": request_id[:8],
                "message": "Your data export has been sent to your email address."
            }), 200
        else:
            cursor.execute("""
                UPDATE dsar_requests 
                SET status = 'failed', notes = ? 
                WHERE id = ?
            """, (f"Email send failed: {email_result.get('error')}", request_id))
            db.commit()
            
            log_dsar_event(db, user_id, email, "email_export_failed", ip_address, user_agent, request_id,
                          details=email_result.get('error'))
            log.error(f"[DSAR] Email send failed for {email}: {email_result.get('error')}")
            
            return jsonify({
                "ok": False,
                "status": "failed",
                "error": "EMAIL_SEND_FAILED",
                "message": "Export generated but email delivery failed. Contact privacy@levqor.ai",
                "reference": request_id[:8]
            }), 500
    
    except Exception as e:
        cursor.execute("UPDATE dsar_requests SET status = 'failed', notes = ? WHERE id = ?", 
                      (str(e), request_id))
        db.commit()
        log_dsar_event(db, user_id, email, "export_failed", ip_address, user_agent, request_id, details=str(e))
        log.error(f"[DSAR] Export failed for user {user_id}: {e}", exc_info=True)
        
        return jsonify({
            "ok": False,
            "status": "failed",
            "error": "EXPORT_FAILED",
            "message": "Export generation failed. Please try again later or contact privacy@levqor.ai",
            "reference": request_id[:8]
        }), 500


@app.get("/api/dsar/status")
def dsar_status():
    """Get status of most recent DSAR request for current user"""
    user_email = request.headers.get("X-User-Email")
    
    # Allow status check via email query param
    if not user_email:
        user_email = request.args.get("email")
    
    if not user_email:
        return jsonify({"ok": False, "error": "Email required"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Get user
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    
    if not user_row:
        return jsonify({"ok": True, "latest": None}), 200
    
    user_id = user_row[0]
    
    # Get most recent DSAR request
    cursor.execute("""
        SELECT id, status, requested_at, notes
        FROM dsar_requests
        WHERE user_id = ?
        ORDER BY requested_at DESC
        LIMIT 1
    """, (user_id,))
    
    row = cursor.fetchone()
    
    if not row:
        return jsonify({"ok": True, "latest": None}), 200
    
    return jsonify({
        "ok": True,
        "latest": {
            "reference": row[0][:8],
            "status": row[1],
            "requested_at": datetime.fromtimestamp(row[2]).isoformat() if row[2] else None,
            "notes": row[3]
        }
    }), 200


@app.get("/api/dsar/exports")
def get_user_dsar_exports():
    """Get user's DSAR export history"""
    user_email = request.headers.get("X-User-Email")
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id = user_row[0]
    
    cursor.execute("""
        SELECT r.id, r.requested_at, r.status, e.created_at, e.expires_at, e.downloaded_at
        FROM dsar_requests r
        LEFT JOIN dsar_exports e ON r.id = e.request_id
        WHERE r.user_id = ?
        ORDER BY r.requested_at DESC
        LIMIT 50
    """, (user_id,))
    
    exports = []
    for row in cursor.fetchall():
        exports.append({
            "request_id": row[0],
            "requested_at": row[1],
            "status": row[2],
            "created_at": row[3],
            "expires_at": row[4],
            "downloaded_at": row[5],
            "is_available": row[2] in ['ready', 'emailed', 'downloaded'] and row[4] and row[4] > time()
        })
    
    return jsonify({"ok": True, "exports": exports}), 200


@app.get("/api/admin/dsar/exports")
def admin_get_dsar_exports():
    """Admin: View all DSAR exports with filters"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # Get filters from query params
    email_filter = request.args.get("email")
    status_filter = request.args.get("status")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    
    query = """
        SELECT r.id, u.email, u.name, r.requested_at, r.status, 
               e.created_at, e.expires_at, e.downloaded_at, e.id as export_id
        FROM dsar_requests r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN dsar_exports e ON r.id = e.request_id
        WHERE 1=1
    """
    params = []
    
    if email_filter:
        query += " AND u.email LIKE ?"
        params.append(f"%{email_filter}%")
    
    if status_filter:
        query += " AND r.status = ?"
        params.append(status_filter)
    
    if date_from:
        from datetime import datetime
        ts = datetime.fromisoformat(date_from).timestamp()
        query += " AND r.requested_at >= ?"
        params.append(ts)
    
    if date_to:
        from datetime import datetime
        ts = datetime.fromisoformat(date_to).timestamp()
        query += " AND r.requested_at <= ?"
        params.append(ts)
    
    query += " ORDER BY r.requested_at DESC LIMIT 500"
    
    cursor.execute(query, params)
    
    exports = []
    for row in cursor.fetchall():
        exports.append({
            "request_id": row[0],
            "email": row[1],
            "name": row[2],
            "requested_at": row[3],
            "status": row[4],
            "created_at": row[5],
            "expires_at": row[6],
            "downloaded_at": row[7],
            "export_id": row[8]
        })
    
    return jsonify({"ok": True, "exports": exports}), 200


# ============================================================================
# Compliance & Legal Endpoints
# ============================================================================

@app.post("/api/sla/claim")
def sla_claim():
    """Submit SLA credit request"""
    user_email = request.headers.get("X-User-Email")
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id = user_row[0]
    data = request.get_json() or {}
    
    request_id = str(uuid4())
    now = time()
    
    cursor.execute("""
        INSERT INTO sla_credit_requests 
        (id, user_id, created_at, period_start, period_end, claimed_issue, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
    """, (request_id, user_id, now, data.get("periodStart"), data.get("periodEnd"), data.get("claimedIssue")))
    
    db.commit()
    
    log.info(f"[SLA] Credit request {request_id} from user {user_id}")
    
    return jsonify({"ok": True, "request_id": request_id}), 201


@app.post("/api/disputes")
def create_dispute():
    """Submit customer dispute"""
    user_email = request.headers.get("X-User-Email")
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id = user_row[0]
    data = request.get_json() or {}
    
    dispute_id = str(uuid4())
    now = time()
    
    cursor.execute("""
        INSERT INTO disputes 
        (id, user_id, created_at, subject, description, category, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
    """, (dispute_id, user_id, now, data.get("subject"), data.get("description"), data.get("category", "other")))
    
    db.commit()
    
    log.info(f"[DISPUTE] New dispute {dispute_id} from user {user_id}: {data.get('subject')}")
    
    return jsonify({"ok": True, "dispute_id": dispute_id}), 201


@app.post("/api/emergency/report")
def emergency_report():
    """Report severity-1 incident"""
    user_email = request.headers.get("X-User-Email")
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id = user_row[0]
    data = request.get_json() or {}
    
    incident_id = str(uuid4())
    now = time()
    
    cursor.execute("""
        INSERT INTO incidents 
        (id, started_at, title, description, severity, status, user_reported, reported_by_user_id)
        VALUES (?, ?, ?, ?, 1, 'investigating', 1, ?)
    """, (incident_id, now, data.get("summary"), data.get("impact"), user_id))
    
    db.commit()
    
    log.error(f"[EMERGENCY] SEV-1 report {incident_id} from user {user_id}: {data.get('summary')}")
    
    # TODO: Alert on-call engineer
    
    return jsonify({"ok": True, "incident_id": incident_id}), 201


@app.get("/api/status")
def public_status():
    """Public system status endpoint"""
    db = get_db()
    cursor = db.cursor()
    
    # Get last 10 incidents
    cursor.execute("""
        SELECT id, started_at, resolved_at, title, description, severity, status
        FROM incidents 
        ORDER BY started_at DESC 
        LIMIT 10
    """)
    
    incidents = []
    for row in cursor.fetchall():
        incidents.append({
            "id": row[0],
            "started_at": row[1],
            "resolved_at": row[2],
            "title": row[3],
            "description": row[4],
            "severity": row[5],
            "status": row[6]
        })
    
    # Determine overall status
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE status != 'resolved' AND severity = 1")
    sev1_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE status != 'resolved' AND severity = 2")
    sev2_count = cursor.fetchone()[0]
    
    if sev1_count > 0:
        overall_status = "major_outage"
    elif sev2_count > 0:
        overall_status = "partial_outage"
    else:
        overall_status = "operational"
    
    return jsonify({
        "status": overall_status,
        "incidents": incidents,
        "last_updated": time()
    }), 200


@app.post("/api/account/delete")
def delete_account():
    """Request account deletion (GDPR Right to Erasure)"""
    user_email = request.headers.get("X-User-Email")
    if not user_email:
        return jsonify({"ok": False, "error": "UNAUTHORIZED"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
    user_row = cursor.fetchone()
    if not user_row:
        return jsonify({"ok": False, "error": "USER_NOT_FOUND"}), 404
    
    user_id = user_row[0]
    
    # Create deletion job
    deletion_id = str(uuid4())
    now = time()
    
    cursor.execute("""
        INSERT INTO deletion_jobs (id, user_id, email, requested_at, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (deletion_id, user_id, user_email, now))
    
    db.commit()
    
    log.warning(f"[DELETION] Account deletion requested for user {user_id} ({user_email})")
    
    # TODO: Queue background job to actually delete data
    
    return jsonify({"ok": True, "deletion_id": deletion_id}), 202


@app.post("/api/internal/run-deletions")
def run_deletions():
    """Background worker to execute pending deletions (internal only)"""
    # Verify admin token
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT id, user_id, email FROM deletion_jobs WHERE status = 'pending' LIMIT 10")
    jobs = cursor.fetchall()
    
    deleted_count = 0
    
    for job_id, user_id, email in jobs:
        try:
            # Delete user data
            cursor.execute("DELETE FROM dsar_requests WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM dsar_exports WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM developer_keys WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM referrals WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM sla_credit_requests WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM disputes WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM payment_failures WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM dunning_emails WHERE user_id = ?", (user_id,))
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            
            # Mark job complete
            cursor.execute("UPDATE deletion_jobs SET status = 'completed', deleted_at = ? WHERE id = ?", (time(), job_id))
            db.commit()
            
            deleted_count += 1
            log.info(f"[DELETION] Successfully deleted user {user_id} ({email})")
            
        except Exception as e:
            cursor.execute("UPDATE deletion_jobs SET status = 'failed', error = ? WHERE id = ?", (str(e), job_id))
            db.commit()
            log.error(f"[DELETION] Failed to delete user {user_id}: {e}")
    
    return jsonify({"ok": True, "deleted": deleted_count}), 200


@app.get("/api/admin/sla/requests")
def admin_get_sla_requests():
    """Admin: View all SLA credit requests"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    status_filter = request.args.get("status", "pending")
    
    cursor.execute("""
        SELECT s.id, u.email, u.name, s.created_at, s.period_start, s.period_end, 
               s.claimed_issue, s.status, s.decision_note, s.credited_amount_cents, 
               s.decided_at, s.decided_by
        FROM sla_credit_requests s
        JOIN users u ON s.user_id = u.id
        WHERE s.status = ? OR ? = 'all'
        ORDER BY s.created_at DESC
        LIMIT 500
    """, (status_filter, status_filter))
    
    requests_list = []
    for row in cursor.fetchall():
        requests_list.append({
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "created_at": row[3],
            "period_start": row[4],
            "period_end": row[5],
            "claimed_issue": row[6],
            "status": row[7],
            "decision_note": row[8],
            "credited_amount_cents": row[9],
            "decided_at": row[10],
            "decided_by": row[11]
        })
    
    return jsonify({"ok": True, "requests": requests_list}), 200


@app.post("/api/admin/sla/requests/<request_id>/decision")
def admin_decide_sla_request(request_id):
    """Admin: Approve or reject SLA credit request"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    data = request.get_json() or {}
    decision_status = data.get("status")  # approved or rejected
    credit_amount_cents = data.get("credit_amount_cents", 0)
    decision_note = data.get("decision_note", "")
    decided_by = data.get("decided_by", "admin")
    
    if decision_status not in ["approved", "rejected"]:
        return jsonify({"ok": False, "error": "Invalid status"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        UPDATE sla_credit_requests 
        SET status = ?, decision_note = ?, credited_amount_cents = ?, 
            decided_at = ?, decided_by = ?
        WHERE id = ?
    """, (decision_status, decision_note, credit_amount_cents, time(), decided_by, request_id))
    
    db.commit()
    
    log.info(f"[SLA] Request {request_id} {decision_status} by {decided_by} - credit: {credit_amount_cents/100:.2f}")
    
    return jsonify({"ok": True}), 200


@app.get("/api/admin/disputes")
def admin_get_disputes():
    """Admin: View all disputes"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    status_filter = request.args.get("status", "pending")
    
    cursor.execute("""
        SELECT d.id, u.email, u.name, d.created_at, d.subject, d.description, 
               d.category, d.status, d.acknowledged_at, d.resolved_at, 
               d.resolution_note, d.escalated
        FROM disputes d
        JOIN users u ON d.user_id = u.id
        WHERE d.status = ? OR ? = 'all'
        ORDER BY d.created_at DESC
        LIMIT 500
    """, (status_filter, status_filter))
    
    disputes = []
    for row in cursor.fetchall():
        disputes.append({
            "id": row[0],
            "email": row[1],
            "name": row[2],
            "created_at": row[3],
            "subject": row[4],
            "description": row[5],
            "category": row[6],
            "status": row[7],
            "acknowledged_at": row[8],
            "resolved_at": row[9],
            "resolution_note": row[10],
            "escalated": row[11]
        })
    
    return jsonify({"ok": True, "disputes": disputes}), 200


# ============================================================================
# Marketing Consent Flow (PECR/GDPR Double Opt-In)
# ============================================================================

@app.post("/api/marketing/consent/start")
def marketing_consent_start():
    """Start double opt-in marketing consent flow"""
    data = request.get_json() or {}
    email = data.get("email")
    scope = data.get("scope", "marketing")
    source = data.get("source", "signup_checkbox")
    
    if not email:
        return jsonify({"ok": False, "error": "EMAIL_REQUIRED"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Get user_id if exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user_row = cursor.fetchone()
    user_id = user_row[0] if user_row else None
    
    # Check if already granted
    cursor.execute("""
        SELECT status FROM user_marketing_consent 
        WHERE email = ? AND scope = ? 
        ORDER BY created_at DESC LIMIT 1
    """, (email, scope))
    existing = cursor.fetchone()
    
    if existing and existing[0] == "granted":
        return jsonify({"ok": True, "message": "Already subscribed"}), 200
    
    # Create consent record with token
    import secrets
    consent_id = str(uuid4())
    token = secrets.token_urlsafe(32)
    now = time()
    token_expires_at = now + (24 * 60 * 60)  # 24 hours
    
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent", "")
    
    cursor.execute("""
        INSERT INTO user_marketing_consent 
        (id, user_id, email, scope, status, source, ip_address, user_agent, 
         created_at, updated_at, token, token_expires_at)
        VALUES (?, ?, ?, ?, 'pending_double_opt_in', ?, ?, ?, ?, ?, ?, ?)
    """, (consent_id, user_id, email, scope, source, ip_address, user_agent, 
          now, now, token, token_expires_at))
    
    db.commit()
    
    # TODO: Send double opt-in email with confirmation link
    # confirm_url = f"https://levqor.ai/marketing/confirm?token={token}"
    
    log.info(f"[MARKETING] Double opt-in started for {email} (scope: {scope})")
    
    return jsonify({
        "ok": True,
        "message": "Please check your email to confirm subscription",
        "token": token  # Return for testing (remove in production)
    }), 201


@app.get("/api/marketing/consent/confirm")
def marketing_consent_confirm():
    """Confirm marketing consent via token"""
    token = request.args.get("token")
    
    if not token:
        return jsonify({"ok": False, "error": "TOKEN_REQUIRED"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Find consent record
    cursor.execute("""
        SELECT id, email, scope, status, token_expires_at 
        FROM user_marketing_consent 
        WHERE token = ?
    """, (token,))
    
    record = cursor.fetchone()
    
    if not record:
        return jsonify({"ok": False, "error": "INVALID_TOKEN"}), 404
    
    consent_id, email, scope, status, token_expires_at = record
    
    # Validate token not expired
    if token_expires_at < time():
        return jsonify({"ok": False, "error": "TOKEN_EXPIRED"}), 400
    
    # Validate not already confirmed
    if status == "granted":
        return jsonify({"ok": True, "message": "Already confirmed"}), 200
    
    # Update status to granted
    now = time()
    cursor.execute("""
        UPDATE user_marketing_consent 
        SET status = 'granted', confirmed_at = ?, updated_at = ?
        WHERE id = ?
    """, (now, now, consent_id))
    
    db.commit()
    
    log.info(f"[MARKETING] Consent confirmed for {email} (scope: {scope})")
    
    # Redirect to success page
    return redirect("/marketing/confirmed")


@app.get("/api/marketing/unsubscribe")
def marketing_unsubscribe_token():
    """Unsubscribe from marketing via token"""
    token = request.args.get("token")
    email = request.args.get("email")
    
    if not token and not email:
        return jsonify({"ok": False, "error": "TOKEN_OR_EMAIL_REQUIRED"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    if token:
        # Decode token to get email (simplified - in production use signed tokens)
        cursor.execute("""
            SELECT email, scope FROM user_marketing_consent 
            WHERE token = ?
        """, (token,))
        record = cursor.fetchone()
        if record:
            email, scope = record
    
    if not email:
        return jsonify({"ok": False, "error": "INVALID_TOKEN"}), 404
    
    # Revoke all marketing consent for this email
    now = time()
    cursor.execute("""
        UPDATE user_marketing_consent 
        SET status = 'revoked', updated_at = ?
        WHERE email = ? AND status != 'revoked'
    """, (now, email))
    
    rows_updated = cursor.rowcount
    db.commit()
    
    log.info(f"[MARKETING] Unsubscribed {email} ({rows_updated} consent records revoked)")
    
    # Redirect to unsubscribe confirmation page
    return redirect("/marketing/unsubscribed")


@app.post("/api/marketing/unsubscribe")
def marketing_unsubscribe_post():
    """Unsubscribe from marketing via POST (for email forms)"""
    data = request.get_json() or {}
    email = data.get("email")
    
    if not email:
        return jsonify({"ok": False, "error": "EMAIL_REQUIRED"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Revoke all marketing consent
    now = time()
    cursor.execute("""
        UPDATE user_marketing_consent 
        SET status = 'revoked', updated_at = ?
        WHERE email = ? AND status != 'revoked'
    """, (now, email))
    
    rows_updated = cursor.rowcount
    db.commit()
    
    log.info(f"[MARKETING] Unsubscribed {email} ({rows_updated} consent records revoked)")
    
    return jsonify({"ok": True, "message": "Unsubscribed successfully"}), 200


# ============================================================================
# Billing & Dunning (Stripe Payment Failure Management)
# ============================================================================

def require_internal_secret():
    """Verify internal API secret for backend-to-backend calls"""
    secret = request.headers.get("X-Internal-Secret")
    expected = os.environ.get("INTERNAL_API_SECRET", "dev_secret")
    if secret != expected:
        return jsonify({"ok": False, "error": "unauthorized"}), 401
    return None


@app.post("/api/internal/billing/payment-failed")
def billing_payment_failed():
    """Handle Stripe invoice.payment_failed webhook"""
    auth_check = require_internal_secret()
    if auth_check:
        return auth_check
    
    data = request.get_json() or {}
    invoice_data = data.get("event", {})
    
    customer_id = invoice_data.get("customer")
    subscription_id = invoice_data.get("subscription")
    attempt_count = invoice_data.get("attempt_count", 0)
    amount_due = invoice_data.get("amount_due", 0)
    
    if not customer_id:
        return jsonify({"ok": False, "error": "missing_customer_id"}), 400
    
    db = get_db()
    cursor = db.cursor()
    now = time()
    
    # Log the billing event
    event_id = str(uuid4())
    cursor.execute("""
        INSERT INTO billing_events 
        (id, stripe_customer_id, stripe_subscription_id, event_type, attempt_count, event_payload_snippet, created_at)
        VALUES (?, ?, ?, 'invoice.payment_failed', ?, ?, ?)
    """, (event_id, customer_id, subscription_id, attempt_count, json.dumps(invoice_data)[:500], now))
    
    # Find or create dunning state
    cursor.execute("""
        SELECT id, user_id, status FROM billing_dunning_state 
        WHERE stripe_customer_id = ?
    """, (customer_id,))
    
    dunning_record = cursor.fetchone()
    
    if not dunning_record:
        # Create new dunning state (no user_id mapping yet - would need customer lookup)
        dunning_id = str(uuid4())
        cursor.execute("""
            INSERT INTO billing_dunning_state 
            (id, user_id, stripe_customer_id, stripe_subscription_id, status, last_event_at, next_action_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'day1_notice', ?, ?, ?, ?)
        """, (dunning_id, customer_id, customer_id, subscription_id, now, now + (7 * 24 * 60 * 60), now, now))
        
        log.warning(f"[BILLING] Payment failed for {customer_id} - Day 1 notice scheduled")
    else:
        dunning_id, user_id, current_status = dunning_record
        
        # Progress dunning state
        if current_status == "none" or current_status == "":
            new_status = "day1_notice"
            next_action = now + (7 * 24 * 60 * 60)
        elif current_status == "day1_notice":
            new_status = "day7_notice"
            next_action = now + (7 * 24 * 60 * 60)
        elif current_status == "day7_notice":
            new_status = "day14_final"
            next_action = now + (3 * 24 * 60 * 60)
        else:
            new_status = current_status
            next_action = None
        
        cursor.execute("""
            UPDATE billing_dunning_state 
            SET status = ?, last_event_at = ?, next_action_at = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, now, next_action, now, dunning_id))
        
        log.warning(f"[BILLING] Payment failed for {customer_id} - status: {current_status} → {new_status}")
    
    db.commit()
    
    return jsonify({"ok": True, "customer_id": customer_id, "attempt": attempt_count}), 200


@app.post("/api/internal/billing/payment-succeeded")
def billing_payment_succeeded():
    """Handle Stripe invoice.paid webhook"""
    auth_check = require_internal_secret()
    if auth_check:
        return auth_check
    
    data = request.get_json() or {}
    invoice_data = data.get("event", {})
    
    customer_id = invoice_data.get("customer")
    subscription_id = invoice_data.get("subscription")
    
    if not customer_id:
        return jsonify({"ok": False, "error": "missing_customer_id"}), 400
    
    db = get_db()
    cursor = db.cursor()
    now = time()
    
    # Log the billing event
    event_id = str(uuid4())
    cursor.execute("""
        INSERT INTO billing_events 
        (id, stripe_customer_id, stripe_subscription_id, event_type, attempt_count, event_payload_snippet, created_at)
        VALUES (?, ?, ?, 'invoice.paid', ?, ?, ?)
    """, (event_id, customer_id, subscription_id, 0, json.dumps(invoice_data)[:500], now))
    
    # Reset dunning state to 'none'
    cursor.execute("""
        UPDATE billing_dunning_state 
        SET status = 'none', last_event_at = ?, next_action_at = NULL, updated_at = ?
        WHERE stripe_customer_id = ?
    """, (now, now, customer_id))
    
    rows_updated = cursor.rowcount
    db.commit()
    
    if rows_updated > 0:
        log.info(f"[BILLING] Payment succeeded for {customer_id} - dunning state reset")
    
    return jsonify({"ok": True, "customer_id": customer_id}), 200


@app.get("/api/billing/status")
def billing_status():
    """Get billing/dunning status for current user"""
    # TODO: Get user from session/auth
    user_id = request.args.get("user_id")  # Temporary for testing
    
    if not user_id:
        return jsonify({"ok": False, "error": "user_id_required"}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT status, next_action_at FROM billing_dunning_state 
        WHERE user_id = ? OR stripe_customer_id = ?
    """, (user_id, user_id))
    
    record = cursor.fetchone()
    
    if not record:
        return jsonify({"ok": True, "status": "ok", "next_action_at": None}), 200
    
    status, next_action_at = record
    
    return jsonify({
        "ok": True,
        "status": status or "ok",
        "next_action_at": next_action_at
    }), 200


@app.post("/webhooks/stripe")
def stripe_webhook():
    """
    Stripe webhook endpoint for dunning system
    Handles: invoice.payment_failed, customer.subscription.updated
    
    NOTE: Expects Stripe signature verification
    """
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
    
    # Verify webhook signature
    if not webhook_secret:
        log.warning("stripe_webhook.no_secret - webhook received but STRIPE_WEBHOOK_SECRET not configured")
        return jsonify({"ok": False, "error": "webhook_secret_not_configured"}), 500
    
    # For production, verify signature with stripe library
    # For now, basic verification that signature exists
    if not sig_header:
        log.error("stripe_webhook.invalid_signature - no signature header")
        return jsonify({"ok": False, "error": "invalid_signature"}), 400
    
    # Parse event
    try:
        event = json.loads(payload.decode('utf-8'))
    except Exception as e:
        log.error(f"stripe_webhook.parse_error error={str(e)}")
        return jsonify({"ok": False, "error": "invalid_payload"}), 400
    
    event_type = event.get('type')
    event_id = event.get('id', 'unknown')
    
    log.info(f"stripe_webhook.received type={event_type} event_id={event_id}")
    
    # Import dunning module
    try:
        from backend.billing.dunning import handle_payment_failed, handle_subscription_updated
        from backend.billing.config import DUNNING_ENABLED
    except ImportError as e:
        log.error(f"stripe_webhook.import_error error={str(e)}")
        return jsonify({"ok": True}), 200  # Return 200 to avoid Stripe retries
    
    db = get_db()
    
    # Handle different event types
    if event_type == 'invoice.payment_failed':
        try:
            handle_payment_failed(db, event)
            log.info(f"stripe_webhook.handled type=invoice.payment_failed event_id={event_id} dunning_enabled={DUNNING_ENABLED}")
        except Exception as e:
            log.error(f"stripe_webhook.handler_error type={event_type} error={str(e)}")
    
    elif event_type == 'customer.subscription.updated':
        try:
            handle_subscription_updated(db, event)
            log.info(f"stripe_webhook.handled type=customer.subscription.updated event_id={event_id}")
        except Exception as e:
            log.error(f"stripe_webhook.handler_error type={event_type} error={str(e)}")
    
    else:
        log.info(f"stripe_webhook.ignored type={event_type} event_id={event_id}")
    
    # Always return 200 for handled events
    return jsonify({"ok": True, "event_id": event_id}), 200


def is_account_suspended(user_id: str) -> bool:
    """Check if account is suspended due to payment failure"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        SELECT status FROM billing_dunning_state 
        WHERE user_id = ? OR stripe_customer_id = ?
    """, (user_id, user_id))
    
    record = cursor.fetchone()
    
    if record and record[0] == "suspended":
        return True
    
    return False


from monitors.scheduler import init_scheduler
init_scheduler()

# ============================================================================
# DUNNING SYSTEM - Scheduled Job Integration (CURRENTLY DISABLED)
# ============================================================================
# The dunning system is installed but not scheduled. To enable:
#
# 1. Set environment variable: DUNNING_ENABLED=true
# 2. Add cron job to monitors/scheduler.py or your scheduler of choice:
#
# Example APScheduler integration:
#
# from backend.billing.dunning import run_dunning_cycle
# from datetime import datetime
#
# scheduler.add_job(
#     func=lambda: run_dunning_cycle(get_db(), datetime.utcnow()),
#     trigger='cron',
#     hour='*/6',  # Every 6 hours
#     id='dunning_cycle',
#     name='Process pending dunning emails',
#     replace_existing=True
# )
#
# Example manual execution:
#   python scripts/run_dunning_cycle.py
#
# SAFETY: With DUNNING_ENABLED=False, no emails are sent even if job runs
# ============================================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
