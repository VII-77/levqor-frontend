from flask import Flask, request, jsonify, Response
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
    from monitors.scheduler import get_scheduler
    _scheduler_instance = get_scheduler()
except Exception as e:
    log.warning(f"Scheduler initialization skipped: {e}")

app = Flask(__name__, 
    static_folder='public',
    static_url_path='/public')

app.config["MAX_CONTENT_LENGTH"] = int(os.environ.get("MAX_CONTENT_LENGTH", 512 * 1024))

DB_PATH = os.environ.get("SQLITE_PATH", os.path.join(os.getcwd(), "levqor.db"))
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
            marketing_double_opt_in_token TEXT UNIQUE
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
        
        _db_connection.commit()
    return _db_connection

def require_key():
    key = request.headers.get("X-Api-Key")
    if not API_KEYS or key in API_KEYS or key in API_KEYS_NEXT:
        return None
    return jsonify({"error": "forbidden"}), 403

def throttle():
    now = time()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    
    while _ALL_HITS and now - _ALL_HITS[0] > WINDOW:
        _ALL_HITS.popleft()
    dq = _IP_HITS[ip]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    
    if len(dq) >= RATE_BURST or len(_ALL_HITS) >= RATE_GLOBAL:
        resp = jsonify({"error": "rate_limited"})
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
    protected_prefixes = ['/billing/', '/api/partners/', '/api/admin/', '/api/user/', '/webhooks/']
    if not any(request.path.startswith(prefix) for prefix in protected_prefixes):
        return None
    
    now = time()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr) or "unknown"
    key = f"protected:{ip}"
    
    dq = _PROTECTED_PATH_HITS[key]
    while dq and now - dq[0] > WINDOW:
        dq.popleft()
    
    if len(dq) >= 60:
        resp = jsonify({"error": "rate_limited"})
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
    if not request.is_json:
        return bad_request("Content-Type must be application/json")
    
    data = request.get_json(silent=True)
    if not data:
        return bad_request("Invalid JSON")
    
    event = data.get("event", "unknown")
    email = data.get("email", "unknown")
    ip = data.get("ip", "")
    user_agent = data.get("user_agent", "")
    ts = data.get("ts", int(time() * 1000))
    
    audit_entry = json.dumps({
        "event": event,
        "email": email,
        "ip": ip,
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


from monitors.scheduler import init_scheduler
init_scheduler()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
