# Technical & Organizational Controls

**Version:** 1.0  
**Date:** 14 November 2025  
**Owner:** Data Protection Officer (privacy@levqor.ai)  
**Part of:** [Compliance Pack v1.0](./overview.md)

---

## Overview

This document catalogs all technical and organizational measures implemented by Levqor to protect personal data and ensure UK GDPR compliance.

---

## 1. Encryption Controls

### 1.1 Encryption in Transit
- **TLS 1.2+** for all HTTPS connections
- **HSTS** (HTTP Strict Transport Security) headers enforced
- **Certificate pinning** on critical endpoints
- **Webhook signature verification** (HMAC-SHA256) for Stripe webhooks

### 1.2 Encryption at Rest
- **SQLite database:** File-level encryption via OS
- **PostgreSQL (Neon):** Encrypted storage via provider
- **API keys:** Encrypted before storage (AES-256)
- **DSAR exports:** Encrypted ZIP files (AES-256)
- **Environment secrets:** Encrypted via Replit Secrets

### 1.3 Key Management
- **JWT secrets:** Rotated every 90 days
- **API keys:** Zero-downtime rotation via dual-key system (API_KEYS + API_KEYS_NEXT)
- **DSAR tokens:** 32-byte secure random, single-use, 24-hour expiry
- **OTP codes:** PBKDF2-HMAC-SHA256 with 100k iterations

---

## 2. Access Controls

### 2.1 Authentication
- **Password-less magic links** (no password storage)
- **NextAuth v4** with session tokens
- **Session rotation** on every login
- **Session expiry:** 7 days inactivity

### 2.2 Authorization
- **Role-based access control (RBAC)** for admin endpoints
- **API key authentication** for programmatic access
- **Rate limiting** per endpoint and user
- **Admin token** for sensitive operations (ADMIN_TOKEN env var)

### 2.3 Account Security
- **Email verification** required for all accounts
- **Terms acceptance enforcement** via middleware
- **Account suspension** for payment failures (dunning system)
- **IP tracking** for audit purposes

---

## 3. Data Minimization & Retention

### 3.1 Collection Minimization
- **Optional fields:** Name, locale, currency marked as optional
- **No special category data** collected at system level
- **High-risk data firewall:** Automatic rejection of prohibited content
- **Anonymization:** User IDs anonymized in analytics

### 3.2 Automated Retention Policies

Implemented via `retention/config.py` and `retention/cleanup.py`:

| Data Type | Retention Period | Cleanup Method |
|-----------|------------------|----------------|
| API usage logs | 90 days | Automated daily job (3am UTC) |
| Status snapshots | 30 days | Automated daily job |
| DSAR export files | 30 days | Physical file deletion |
| Referral tracking | 2 years | Automated daily job |
| Billing records | 7 years | **Legal hold (UK tax law)** |
| Marketing consents | Until revoked + 2 years | Manual deletion only |

### 3.3 User-Initiated Deletion

- **POST /api/privacy/delete-my-data** endpoint (GDPR Art. 17)
- **One-click deletion** from /privacy-tools page
- **Deletion scope:**
  - ✅ Workflows, jobs, logs
  - ✅ API keys, referrals, partnerships
  - ✅ DSAR exports
  - ✅ User account (anonymized)
  - ❌ Billing records (7-year legal hold)

---

## 4. Rate Limiting & Anti-Abuse

### 4.1 Global Rate Limits
- **Per-IP:** 20 requests/minute
- **Global:** 200 requests/minute
- **Window:** 60 seconds (sliding window)

### 4.2 Protected Endpoints
- **Authentication endpoints:** Additional rate limiting (5 req/min)
- **DSAR requests:** 1 request per 24 hours per user
- **Data deletion:** No rate limit (user right)

### 4.3 Abuse Detection
- **IP blocking** for repeated violations
- **User-Agent tracking** in audit logs
- **Anomaly detection** via Sentry
- **Manual review** for high-volume accounts

---

## 5. High-Risk Data Prohibition

### 5.1 Automatic Keyword Scanning

All workflow submissions scanned for prohibited content:

**Prohibited Categories:**
1. **Medical/Healthcare:** diagnosis, treatment, prescription, patient, medical record
2. **Legal:** legal advice, contract, litigation, lawsuit, legal opinion
3. **Financial:** credit score, loan decision, investment advice, trading signal, tax return
4. **Safety-critical:** flight control, emergency dispatch, life support

**Enforcement:** Instant rejection with error code `high_risk_data`

**Audit Trail:** All blocked attempts logged in `risk_blocks` table with:
- User ID
- Blocked keywords
- Payload snippet
- IP address
- Timestamp

### 5.2 Legal References
- [Risk Disclosure Page](/risk-disclosure)
- [Acceptable Use Policy](/acceptable-use)
- [Terms of Service (Section 7A)](/terms)

---

## 6. Audit Logging

### 6.1 Comprehensive Audit Trail

All sensitive operations logged:

| Event Type | Logged Data | Retention |
|------------|-------------|-----------|
| User login/logout | Email, IP, timestamp | 90 days |
| Terms acceptance | Version, IP, timestamp | Permanent |
| Marketing consent | Status, IP, source, timestamp | 2 years post-revocation |
| API key creation/rotation | Key ID, user, timestamp | 90 days |
| DSAR requests | Email, token, timestamp | 90 days |
| Data deletion | User ID, scope, timestamp | 90 days |
| High-risk blocks | Terms, payload, IP, timestamp | 90 days |
| Billing events | Stripe event, customer, timestamp | 7 years |

### 6.2 Audit Log Access
- **Read-only** for compliance team
- **Exported** for annual audits
- **Retained** per retention schedule

---

## 7. Incident Response & Business Continuity

### 7.1 Incident Response Plan

See: **[Incident Response Procedure](/incident-response)** (customer-facing)

Internal procedures:
1. **Detection:** Sentry alerts, monitoring dashboards
2. **Containment:** Immediate isolation of affected systems
3. **Investigation:** Root cause analysis
4. **Notification:** ICO notification within 72 hours if required
5. **Remediation:** Patch deployment, post-mortem

### 7.2 Business Continuity

See: **[Business Continuity Plan](/business-continuity)** (customer-facing)

Internal measures:
- **Daily automated backups** (retention: 30 days)
- **Multi-region deployment** (Vercel Edge, Replit)
- **Failover procedures** for critical services
- **Disaster recovery testing** quarterly

### 7.3 Backup Strategy

See: **[Backup & Restore Procedure](/backups)** (customer-facing)

Technical implementation:
- **Database backups:** Daily automated (PostgreSQL WAL)
- **Code repositories:** Git version control (GitHub)
- **Configuration:** Environment variables backed up to secure vault
- **Recovery time objective (RTO):** 4 hours
- **Recovery point objective (RPO):** 24 hours

---

## 8. Third-Party & Subprocessor Management

### 8.1 Subprocessor Vetting

Before onboarding any subprocessor:
1. ✅ **Due diligence:** Security certifications (ISO 27001, SOC 2)
2. ✅ **Data Processing Agreement (DPA):** Signed contract
3. ✅ **SCCs:** Standard Contractual Clauses for international transfers
4. ✅ **Security questionnaire:** Completed and reviewed
5. ✅ **Annual review:** Re-certification every 12 months

### 8.2 Current Subprocessors

See [Compliance Pack Overview](./overview.md) for full list.

### 8.3 Customer Notification

- **Subprocessor list:** Published at [/subprocessors](/subprocessors)
- **Change notification:** 30 days advance notice
- **Objection right:** Customers may object to new subprocessors

---

## 9. Staff Training & Awareness

### 9.1 Data Protection Training

All staff with access to personal data complete:
- **Onboarding training:** GDPR basics, Levqor policies
- **Annual refresher:** Updates on regulations and practices
- **Incident response drills:** Quarterly simulations

### 9.2 Access Privileges

- **Least privilege principle:** Minimum access required
- **Regular access reviews:** Quarterly audit of permissions
- **Offboarding:** Immediate revocation on departure

---

## 10. Monitoring & Continuous Improvement

### 10.1 System Health Monitoring

- **24/7 uptime monitoring:** Sentry, Vercel Analytics
- **Performance tracking:** API latency, error rates
- **Security scanning:** Automated dependency vulnerability checks
- **Compliance dashboard:** Real-time GDPR metric tracking

### 10.2 Annual Compliance Review

Every 12 months:
1. ✅ Review ROPA, DPIA, LIA for accuracy
2. ✅ Audit subprocessor compliance
3. ✅ Test incident response procedures
4. ✅ Update retention policies if needed
5. ✅ Staff training completion verification
6. ✅ External audit (if required)

**Next Review:** November 2026

---

## 11. Privacy by Design & Default

### 11.1 Design Principles

Levqor embeds privacy into product development:
- **Data minimization** in all feature specifications
- **Encryption by default** for all data at rest and in transit
- **User control** over data (deletion, export, consent)
- **Transparency** via clear privacy policies and notices

### 11.2 Default Settings

- **Marketing consent:** Opt-in required (unchecked by default)
- **Analytics cookies:** Consent required
- **API access:** Restricted by default, requires explicit key generation
- **Data retention:** Shortest necessary period applied

---

## Related Documents

- [Compliance Pack Overview](./overview.md)
- [Compliance Register](./register.md)
- [ROPA](../ropa.md)
- [DPIA](../dpia-levqor-automation.md)
- [LIA](../lia-marketing-and-analytics.md)
- [Incident Response Procedure](/incident-response)
- [Business Continuity Plan](/business-continuity)
- [Backup & Restore Procedure](/backups)

---

**Technical & Organizational Controls** – Updated 14 November 2025
