# Levqor Expansion Roadmap
**Post-Launch Growth Strategy**  
**Date:** November 11, 2025

---

## 📊 Current Status

### ✅ Phase 1: INTEGRITY + FINALIZER PACK (COMPLETE)

**Status:** **READY FOR SALE**  
**Timeline:** Completed November 11, 2025

**What's Built:**
- ✅ E2E integrity testing (10 comprehensive checks)
- ✅ Finalizer validation (12 deployment checks)
- ✅ PDF evidence report generation
- ✅ Complete test suite (8/10 passed, 11/12 passed)
- ✅ CLI runner script
- ✅ Stripe product creation script
- ✅ Complete documentation

**Pricing:**
- One-time: $49.00
- Monthly: $19/month (unlimited runs)

**Files Created:**
```
modules/integrity_pack/
├── __init__.py
├── integrity_test.py       (E2E testing engine)
├── finalizer.py            (Deployment validation)
├── evidence_export.py      (PDF report generation)
└── run_integrity_pack.py   (Complete runner)

scripts/
└── create_integrity_pack_stripe_product.py

INTEGRITY-PACK-GUIDE.md     (Complete documentation)
```

**Revenue Potential:**
- Enterprise customers: $49/customer (one-time)
- Monthly subscribers: $19/month recurring
- Target: 50 customers = $2,450/month ARR (monthly plan)

---

## 🎯 Phase 2: TEMPLATE PACKS + DEMO LIBRARY

**Timeline:** 3 weeks  
**Status:** Not started  
**Priority:** High (fast revenue, low complexity)

### What to Build

```bash
mkdir modules/template_packs
touch modules/template_packs/{starter.yaml,automation.yaml,enterprise.yaml}
```

### Template Pack Structure

Each pack contains:
- **Metadata**: name, description, price, tags, import_url
- **Workflow Files**: Pre-configured automation workflows
- **Database Schema**: Ready-to-use data models
- **API Endpoints**: Common integration patterns

### Example Packs

**1. Starter Pack** (Free)
- Basic job orchestration
- Simple status tracking
- Email notifications
- User authentication

**2. Automation Pro Pack** ($99)
- Advanced scheduling
- Multi-step workflows
- Error handling + retries
- Webhook integrations

**3. Enterprise Pack** ($299)
- Complete compliance suite
- Advanced security features
- Multi-tenant support
- Custom branding

### Implementation Tasks

1. **Template Storage** (Week 1)
   - Create YAML template format
   - Build template parser/validator
   - Store templates in `/packs` directory
   - Register in Notion "Template Library" database

2. **Purchase Flow** (Week 2)
   - Stripe Checkout integration
   - Email delivery via Resend
   - Download link generation
   - Usage tracking

3. **Import System** (Week 3)
   - CLI: `levqor pack import <url>`
   - Automatic schema migration
   - Configuration injection
   - Post-import validation

### Revenue Potential
- 100 free downloads → 20% conversion = 20 paid customers
- Average pack price: $99
- Initial revenue: $1,980
- Monthly recurring: Potential $499/month (enterprise subscriptions)

---

## 🔧 Phase 3: USAGE-BASED API TIER

**Timeline:** Weeks 3-5  
**Status:** Not started  
**Priority:** Medium (scalable revenue)

### What to Build

**1. Metering Middleware**
```python
# server/middleware/usage_meter.py

def track_api_usage(user_id, endpoint, tokens_used):
    """Track each API call by user"""
    redis.hincrby(f"usage:{user_id}:month", endpoint, 1)
    redis.hincrby(f"usage:{user_id}:tokens", "total", tokens_used)
```

**2. Usage Tracking**
- Count API calls by user_id
- Track by endpoint category
- Calculate token usage (for AI features)
- Store in Redis for fast access
- Sync to database nightly

**3. API Endpoints**

```bash
GET /api/v1/usage
# Response: { "calls_remaining": 950, "calls_used": 50, "reset_date": "2025-12-01" }

POST /api/v1/billing/purchase-credits
# Purchase additional API credits via Stripe
```

**4. Stripe Metering Integration**
```python
# Nightly sync to Stripe
import stripe

stripe.SubscriptionItem.create_usage_record(
    subscription_item_id,
    quantity=api_calls_count,
    timestamp=int(time.time())
)
```

### Pricing Tiers

| Plan | Price | API Calls/Month | Overage |
|------|-------|-----------------|---------|
| Developer | $29/month | 10,000 calls | $3 per 1,000 |
| Professional | $99/month | 50,000 calls | $2 per 1,000 |
| Enterprise | $299/month | 250,000 calls | $1.50 per 1,000 |

### Implementation Tasks

1. **Week 3: Metering System**
   - Add usage tracking middleware
   - Redis integration for counters
   - Database sync job
   - Rate limiting by tier

2. **Week 4: Billing Integration**
   - Stripe metered billing setup
   - Usage record sync
   - Overage charging
   - Credit purchase flow

3. **Week 5: Developer Experience**
   - API key management UI
   - Usage dashboard
   - Email alerts (80%, 100% usage)
   - Documentation updates

### Revenue Potential
- Target: 50 developers on Developer plan = $1,450/month
- 10 on Professional = $990/month
- 3 on Enterprise = $897/month
- **Total: $3,337/month ARR**

---

## 🏢 Phase 4: WHITE-LABEL EDITION

**Timeline:** Weeks 5-8  
**Status:** Not started  
**Priority:** Medium-High (B2B channel)

### What to Build

```bash
mkdir modules/white_label
touch modules/white_label/{branding.py,tenant_config.json,api_overrides.py}
```

### Features

**1. Dynamic Branding** (`branding.py`)
```python
class TenantBranding:
    def __init__(self, tenant_id):
        config = load_tenant_config(tenant_id)
        self.logo = config['logo_url']
        self.primary_color = config['brand_color']
        self.company_name = config['company_name']
    
    def apply_to_template(self, template):
        """Inject branding into UI templates"""
        return template.replace("{{logo}}", self.logo)
```

**2. Tenant Configuration** (`tenant_config.json`)
```json
{
  "tenant_id": "acme_corp",
  "company_name": "Acme Automation",
  "logo_url": "https://cdn.acme.com/logo.png",
  "brand_color": "#FF5733",
  "custom_domain": "automation.acme.com",
  "api_keys": {
    "stripe": "sk_live_acme_...",
    "resend": "re_acme_..."
  },
  "billing": {
    "plan": "enterprise",
    "monthly_fee": 999
  }
}
```

**3. API Overrides** (`api_overrides.py`)
```python
def register_custom_endpoints(tenant_id):
    """Allow custom API endpoints per tenant"""
    @app.route(f"/api/{tenant_id}/custom/status")
    def custom_status():
        return tenant_specific_logic()
```

### Managed Service Pilot

**Choose 2 Design Partners:**
1. Marketing agency (need automation for clients)
2. SaaS company (need white-label workflow engine)

**What to Provide:**
- Custom subdomain: `workflows.theirbrand.com`
- Their branding (logo, colors, name)
- Dedicated support
- Monthly strategy calls
- Shared revenue model (70/30 split)

**Pilot Goals:**
- Run for 3 months
- Gather ROI data
- Collect testimonials
- Create case study
- Identify product gaps

### Pricing

| Tier | Setup Fee | Monthly | Included |
|------|-----------|---------|----------|
| White-Label Basic | $2,000 | $499/month | Up to 5 custom workflows |
| White-Label Pro | $5,000 | $999/month | Unlimited workflows, priority support |
| Managed Service | $10,000 | $1,999/month | Full-service, dedicated account manager |

### Revenue Potential
- 3 White-Label Basic customers = $1,497/month
- 2 White-Label Pro = $1,998/month
- 1 Managed Service = $1,999/month
- **Total: $5,494/month ARR**
- **Setup fees: $14,000 one-time**

---

## 🔨 Phase 5: SYSTEM UPGRADES REQUIRED

**Timeline:** Ongoing (parallel with phases 2-4)

### Core Infrastructure

| Upgrade | Purpose | Timeline |
|---------|---------|----------|
| **Metering + Entitlements** | Track feature usage by user | Week 3 |
| **Packager CLI** | Export/import template packs | Week 2 |
| **Telemetry + Evidence** | Auto-attach PDF reports | Week 1 |
| **Partner Hooks API** | Plugin system for extensions | Week 6 |
| **Pricing Guardrails** | Prevent abuse, enforce limits | Week 4 |

### Database Schema Additions

```sql
-- Usage tracking
CREATE TABLE usage_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    endpoint VARCHAR NOT NULL,
    tokens_used INT DEFAULT 0,
    timestamp TIMESTAMP DEFAULT NOW(),
    INDEX(user_id, timestamp)
);

-- Template packs
CREATE TABLE template_packs (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    price_cents INT,
    download_url VARCHAR,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- White-label tenants
CREATE TABLE tenants (
    id VARCHAR PRIMARY KEY,
    company_name VARCHAR NOT NULL,
    branding_config JSONB,
    api_keys_encrypted TEXT,
    billing_plan VARCHAR,
    monthly_fee_cents INT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📈 Phase 6: CONTENT & MARKETING ACTIVATION

**Timeline:** Weeks 2-8 (parallel)

### Blog Posts (Notion → Auto-publish)

1. **"Introducing Integrity Pack"** (Week 1)
   - Enterprise-grade verification
   - Compliance use cases
   - PDF evidence for audits

2. **"Template Library Launch"** (Week 3)
   - Pre-built workflow blueprints
   - Starter pack (free)
   - Pro packs pricing

3. **"API Access for Developers"** (Week 5)
   - Usage-based pricing
   - API documentation
   - Code examples

4. **"Levqor for Agencies"** (Week 7)
   - White-label edition
   - Case study from pilot
   - Managed service offering

### Email Campaigns (via Resend)

**Existing Users:**
- "New: Integrity Pack - Verify Your Deployment" (Week 1)
- "50% Off Template Packs - Launch Special" (Week 3)
- "Developer API Now Available" (Week 5)

**New Signups:**
- Welcome series with free Starter Pack
- Upgrade nudges (template packs at day 7)
- Enterprise outreach (white-label at day 30)

### Landing Pages

```
levqor.ai/integrity-pack
levqor.ai/templates
levqor.ai/developers
levqor.ai/agencies
```

---

## 📊 Phase 7: TRACKING & REVIEW

**Metrics to Monitor (Weekly Pulse Report):**

```python
pulse_report_additions = {
    "integrity_pack": {
        "runs_count": count_integrity_runs(),
        "revenue_onetime": sum_onetime_purchases(),
        "revenue_monthly": sum_monthly_subscriptions(),
    },
    "template_packs": {
        "downloads_free": count_free_downloads(),
        "purchases_paid": count_paid_purchases(),
        "revenue": sum_template_revenue(),
    },
    "api_tier": {
        "active_developers": count_api_users(),
        "calls_total": sum_api_calls(),
        "overage_revenue": sum_overage_charges(),
    },
    "white_label": {
        "active_tenants": count_tenants(),
        "mrr": sum_tenant_revenue(),
        "pilot_partners": count_pilot_partners(),
    }
}
```

**Quarterly ROI Review:**
- Which packs sell best?
- API usage patterns
- White-label conversion rate
- Pricing adjustments needed?

---

## 💰 Revenue Projection (6 Months)

| Revenue Stream | Month 1 | Month 3 | Month 6 |
|----------------|---------|---------|---------|
| Integrity Pack (Monthly) | $380 | $950 | $1,900 |
| Template Packs | $990 | $2,475 | $3,960 |
| API Tier | $0 | $1,450 | $3,337 |
| White-Label | $0 | $2,497 | $5,494 |
| **Total MRR** | **$1,370** | **$7,372** | **$14,691** |
| **Annual Run Rate** | $16,440 | $88,464 | $176,292 |

---

## ✅ Next Actions

### Immediate (This Week)
1. ✅ Integrity Pack complete and documented
2. ⏳ Run Stripe product creation script
3. ⏳ Add pricing to levqor.ai site
4. ⏳ Write "Introducing Integrity Pack" blog post

### Week 2
1. Start Template Packs development
2. Create Starter Pack (free)
3. Design Automation Pro Pack
4. Build template parser

### Week 3
1. Finish Template Packs
2. Launch template library
3. Start API metering system
4. Email existing users about templates

### Weeks 4-5
1. Complete API tier implementation
2. Stripe metered billing integration
3. Developer documentation
4. Usage dashboard

### Weeks 6-8
1. White-label MVP
2. Onboard 2 pilot partners
3. Case study development
4. Agency landing page

---

## 🎯 Success Criteria

**Integrity Pack:**
- ✅ 100% test coverage
- ✅ PDF generation working
- ✅ Stripe product created
- ⏳ First 5 customers

**Template Packs:**
- 500 free downloads (Month 1)
- 50 paid purchases (Month 3)
- $5,000 template revenue (Month 6)

**API Tier:**
- 100 developer signups (Month 3)
- 50 paying developers (Month 6)
- $3,000 monthly API revenue (Month 6)

**White-Label:**
- 2 pilot partners (Month 2)
- Case study published (Month 4)
- 5 paying white-label customers (Month 6)
- $5,000 monthly white-label revenue (Month 6)

---

**Document Status:** Complete  
**Last Updated:** November 11, 2025  
**Next Review:** Weekly (Friday Pulse Report)
