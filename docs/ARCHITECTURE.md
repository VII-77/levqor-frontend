# EchoPilot Architecture Documentation

## System Overview

EchoPilot is a 100-phase enterprise-ready AI automation platform built on a microservices-inspired architecture with a monolithic Flask backend.

```
┌──────────────────────────────────────────────────────────────┐
│                     User Interface Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Landing Page │  │ Dashboard V2 │  │  About Page  │       │
│  │ (Boss Mode)  │  │  (Mobile)    │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└──────────────────────────────────────────────────────────────┘
                          │ HTTPS
┌──────────────────────────────────────────────────────────────┐
│                    API Layer (Flask)                          │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │
│  │ Public │  │ Secure │  │ Admin  │  │  Edge  │            │
│  │  APIs  │  │  APIs  │  │  APIs  │  │  APIs  │            │
│  └────────┘  └────────┘  └────────┘  └────────┘            │
│         │         │          │           │                   │
│  [Rate Limit] [CSRF] [RBAC] [Audit Log]                     │
└──────────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────────┐
│                     Business Logic Layer                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Task       │  │  Payment   │  │  AI        │            │
│  │ Processing │  │  Engine    │  │  Quality   │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ Scheduler  │  │   SLO      │  │ Multi-     │            │
│  │  Engine    │  │  Tracker   │  │ Tenant     │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└──────────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────────┐
│                    Integration Layer                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Notion  │  │ OpenAI  │  │ Stripe  │  │ Google  │        │
│  │   API   │  │   API   │  │   API   │  │   APIs  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└──────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Flask Application Server

**File:** `run.py` (~5,400 lines)

- **Purpose:** HTTP server handling all requests
- **Framework:** Flask with Gunicorn (production WSGI)
- **Worker Model:** 1 worker, gthread threading
- **Port:** 5000 (bound to 0.0.0.0)

**Key Features:**
- 147+ API endpoints
- Feature flag routing
- Security middleware
- Metrics collection
- Error handling

### 2. Scheduler System

**File:** `scripts/exec_scheduler.py`

- **Purpose:** Autonomous task execution every 60 seconds
- **Execution Model:** Polling-based event loop
- **Concurrency:** Single-threaded with sequential task processing
- **Git Integration:** Commits tracked for every execution

**Scheduled Tasks (46 total):**
- Brief processing (daily 8:00 UTC)
- Daily reports (daily 9:00 UTC)
- Self-heal (every 6 hours)
- Heartbeat (hourly)
- Alerts (every 5 minutes)
- Payment reconciliation (daily 2:10 UTC)
- Compliance checks (weekly Sundays 3:00 UTC)

### 3. AI Processing Engine

**Files:** `bot/main.py`, `bot/ai_quality.py`

- **Primary Model:** GPT-4o (task processing)
- **QA Model:** GPT-4o-mini (quality evaluation)
- **Integration:** Replit AI Integrations connector

**Quality Assurance:**
- 4 criteria scoring (clarity, accuracy, completeness, tone)
- 80% threshold for auto-approval
- Dynamic retry on failure
- Cost tracking per request

### 4. Payment Engine

**Files:** `scripts/payments.py`, `scripts/payment_reconciliation.py`

- **Provider:** Stripe (LIVE mode)
- **Features:**
  - Invoice creation
  - Refund processing
  - Webhook handling
  - Auto-reconciliation
  - Guardrails (max $5,000/transaction)

### 5. Multi-Database Architecture

**Notion Databases (13):**

1. **Automation Queue** - Task intake
2. **Automation Log** - Execution history
3. **Job Log** - Detailed job records
4. **Client** - Customer data
5. **Status** - System health
6. **Finance** - Revenue/cost tracking
7. **Forecast** - ML predictions
8. **Partners** - Marketplace API keys
9. **Referrals** - Growth tracking
10. **Growth Metrics** - KPI dashboard
11. **Governance** - Compliance reports
12. **Ops Monitor** - Incident logs
13. **Region Compliance** - GDPR/CCPA data

**PostgreSQL (Replit):**
- Structured data (future)
- Session storage (future)
- Analytics warehouse (future)

## Data Flow

### Typical Request Flow

```
1. User Request
   ↓
2. Flask receives HTTP request
   ↓
3. Security Middleware
   - Rate limiting check
   - CSRF validation (POST/PUT/DELETE)
   - RBAC authorization
   ↓
4. Route Handler
   - Business logic execution
   - Database queries
   - External API calls
   ↓
5. Response Assembly
   - Security headers applied
   - Audit log written
   - Metrics recorded
   ↓
6. HTTP Response to User
```

### AI Processing Flow

```
1. Brief submitted to Queue DB
   ↓
2. Scheduler polls every 60s
   ↓
3. Task picked up by bot.main.py
   ↓
4. OpenAI API call (GPT-4o)
   - Prompt template applied
   - Cost tracked
   - Latency measured
   ↓
5. Output generated
   ↓
6. QA Evaluation (GPT-4o-mini)
   - 4 criteria scored
   - Pass/fail determined
   ↓
7. Results written to Job Log DB
   ↓
8. Metrics aggregated
   ↓
9. User notified (if configured)
```

## Security Architecture

### Defense Layers

1. **Transport Security**
   - HTTPS only (Replit handles TLS)
   - HSTS headers
   - No mixed content

2. **Application Security**
   - Rate limiting (10-30 req/60s)
   - CSRF protection
   - CSP headers
   - Input validation
   - PII redaction in logs

3. **Authentication**
   - Dashboard key (SHA-256 validated)
   - RBAC roles (admin/analyst)
   - JWT tokens (Phase 82)

4. **Audit & Monitoring**
   - NDJSON structured logs
   - Real-time anomaly detection
   - SLO breach alerts
   - Incident paging

## Performance Characteristics

### Latency

- **API Responses:** P50: 150ms, P95: <400ms, P99: <800ms
- **AI Processing:** 2-8 seconds (model dependent)
- **QA Evaluation:** 1-3 seconds
- **Dashboard Load:** <1.5s TTI on 4G

### Throughput

- **Scheduler:** 1 tick/60s = 1,440 ticks/day
- **API Capacity:** ~10,000 requests/hour (rate limited)
- **AI Jobs:** ~100-500 jobs/day (depends on queue)

### Availability

- **Target SLO:** 99.9% uptime
- **Allowed Downtime:** 43 minutes/month
- **Current Uptime:** 99.95% (better than target)

## Scalability

### Current Limitations

- **Single Worker:** Gunicorn runs 1 worker
- **In-Memory State:** Rate limits, CSRF tokens in RAM
- **Synchronous Processing:** No async/await
- **Database:** Notion API rate limits (3 req/s)

### Future Scaling Path

1. **Horizontal Scaling**
   - Multiple Gunicorn workers
   - Redis for shared state
   - Load balancer

2. **Async Processing**
   - Celery task queue
   - Background workers
   - Event-driven architecture

3. **Caching Layer**
   - Redis cache
   - CDN for static assets
   - Database query caching

## Monitoring & Observability

### Metrics Collected

- **HTTP:** Request count, latency, status codes
- **Business:** Jobs processed, revenue, costs
- **System:** CPU, memory, disk usage
- **SLO:** Availability, P95 latency, webhook success

### Logs

**Locations:**
- `logs/ndjson/audit.ndjson` - Security events
- `logs/ndjson/slo_events.ndjson` - SLO tracking
- `logs/ndjson/prompt_usage.ndjson` - AI prompt tracking
- `logs/scheduler.log` - Scheduler events
- `logs/stripe_webhooks.log` - Payment events

**Format:** NDJSON (newline-delimited JSON) for machine parsing

### Alerting

**Channels:**
- Telegram (instant notifications)
- Email (reports and summaries)
- Notion (log entries)

**Alert Types:**
- SLO breaches
- Payment failures
- Scheduler errors
- Security violations

## Deployment

### Current Setup

- **Platform:** Replit Reserved VM
- **URL:** https://echopilotai.replit.app
- **Workflows:**
  1. EchoPilot Bot (Flask server)
  2. Scheduler (background polling)

### Configuration

**Environment Variables (26):**
- API keys: OpenAI, Stripe, Telegram
- Database IDs: 13 Notion databases
- Feature flags: ALLOW_DIRTY, etc.
- Secrets: Dashboard keys, webhook secrets

### Disaster Recovery

- **Backups:** Daily compressed backups
- **Retention:** 30 days
- **Verification:** Automated integrity checks
- **Restore Time:** <30 minutes (manual)

## Technology Stack

### Backend

- **Language:** Python 3.11
- **Framework:** Flask
- **WSGI:** Gunicorn
- **Database:** Notion API (primary), PostgreSQL (secondary)

### Frontend

- **HTML/CSS/JS:** Vanilla (no framework)
- **Design System:** Custom CSS (~800 lines)
- **Mobile-First:** Optimized for 360-430px
- **Accessibility:** WCAG 2.2 AA compliant

### External Services

- **AI:** OpenAI (via Replit AI Integrations)
- **Payments:** Stripe
- **Storage:** Notion, Google Drive
- **Email:** Gmail API
- **Notifications:** Telegram Bot API

### DevOps

- **Version Control:** Git
- **Deployment:** Replit Workflows
- **Monitoring:** Custom (SLO tracker, metrics)
- **Logging:** NDJSON structured logs

## Code Organization

```
/
├── run.py                    # Main Flask app (5,400 lines)
├── bot/
│   ├── main.py              # AI processing engine
│   ├── security.py          # Security utilities (Boss Mode)
│   ├── slo.py               # SLO tracking
│   ├── status_summary.py   # Status aggregation
│   ├── ai_quality.py        # Prompt management
│   └── notion_api.py        # Notion wrapper
├── scripts/
│   ├── exec_scheduler.py    # Main scheduler loop
│   ├── payments.py          # Stripe integration
│   ├── feature_flags.json   # Feature flag config
│   └── [65+ other scripts]
├── templates/
│   ├── landing.html         # Boss Mode landing page
│   └── about.html           # Boss Mode about page
├── static/
│   └── app.css              # Boss Mode design system
├── docs/
│   ├── GET_STARTED.md
│   ├── SECURITY.md
│   ├── RUNBOOK.md
│   ├── CHANGELOG.md
│   └── ARCHITECTURE.md (this file)
├── dashboard_v2.html        # Boss Mode dashboard
└── dashboard.html           # Legacy dashboard
```

**Stats:**
- Total files: ~120
- Python scripts: 78
- Lines of code: ~20,000
- API endpoints: 147+
- Autonomous tasks: 46

---

**Last Updated:** October 20, 2025  
**Version:** Boss Mode UI v2.0  
**Author:** EchoPilot Development Team
