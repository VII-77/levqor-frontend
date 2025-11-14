# Record of Processing Activities (ROPA) – Levqor

**Controller:** Levqor  
**Date Created:** November 14, 2025  
**Last Updated:** November 14, 2025  
**Review Cycle:** Annually or upon major feature changes  

---

## Purpose

This document records all data processing activities conducted by Levqor in compliance with UK GDPR Article 30 (Records of Processing Activities).

---

## Processing Activities

### 1. Account Management & Authentication

**Purpose:**  
User registration, authentication, and account management

**Data Categories:**
- Email address (identifier)
- Name (optional, user-provided)
- Authentication tokens (NextAuth session tokens)
- Account creation timestamp
- Terms acceptance records (version, timestamp, IP address)
- Cookie consent preferences

**Data Subjects:**  
Customers, platform users

**Legal Basis:**  
- Contract (service provision)
- Consent (cookie preferences, marketing)

**Retention Period:**  
- Active accounts: Duration of service + 30 days after deletion request
- Deleted accounts: Anonymized within 30 days
- Billing records: 7 years (legal requirement)

**Recipients / Subprocessors:**
- Vercel (hosting, Next.js deployment)
- Resend (email delivery for magic links)
- Replit (backend infrastructure)

**Security Measures:**
- HTTPS/TLS encryption in transit
- Password-less magic link authentication
- Session token rotation
- Access logs with IP tracking
- Rate limiting (20 req/min per IP, 200 req/min global)

---

### 2. Workflow Automation & Job Processing

**Purpose:**  
Execute customer-defined automation workflows, process jobs, track status

**Data Categories:**
- Workflow definitions (customer-provided automation rules)
- Job metadata (ID, status, timestamps)
- Input/output data (customer workflow data)
- Execution logs (API calls, errors, timing data)
- API keys for third-party integrations (encrypted)

**Data Subjects:**  
Customers, end-users of customer workflows (indirect)

**Legal Basis:**  
Contract (service delivery)

**Retention Period:**
- Workflow data: Duration of active subscription
- Execution logs: 90 days (automated cleanup)
- Status snapshots: 30 days (automated cleanup)

**Recipients / Subprocessors:**
- Replit (execution environment)
- Customer-specified third-party APIs (as directed by customer)
- Sentry (error monitoring - anonymized data only)

**Security Measures:**
- Encrypted API key storage
- Execution isolation
- Automated high-risk data scanning (medical/legal/financial rejection)
- Comprehensive audit logging
- Request payload size limits (512KB max)

---

### 3. Billing & Payment Processing

**Purpose:**  
Process payments, manage subscriptions, handle billing disputes

**Data Categories:**
- Stripe customer ID (pseudonymized)
- Stripe subscription ID
- Payment method details (held by Stripe, not Levqor)
- Invoice history
- Payment failure events
- Dunning state (payment retry status)

**Data Subjects:**  
Paying customers

**Legal Basis:**  
- Contract (payment processing)
- Legal obligation (tax/accounting records)

**Retention Period:**
- Billing events: 7 years (UK tax law requirement)
- Invoice records: 7 years (legal requirement)
- Stripe payment metadata: 7 years

**Recipients / Subprocessors:**
- Stripe (payment processor)
- Notion (invoice logging for internal operations)

**Security Measures:**
- PCI DSS compliance via Stripe
- No direct storage of card data
- Encrypted Stripe API keys
- Webhook signature verification (HMAC)
- Dunning email system with PECR compliance

---

### 4. Marketing Communications

**Purpose:**  
Send product updates, marketing emails, newsletters (with explicit consent)

**Data Categories:**
- Email address
- Marketing consent status (pending/granted/revoked)
- Consent timestamp
- Consent IP address
- Consent source (signup form, settings page)
- Double opt-in confirmation status
- Unsubscribe timestamp

**Data Subjects:**  
Customers who opted in to marketing

**Legal Basis:**  
Consent (explicit, double opt-in per PECR/GDPR)

**Retention Period:**
- Active consent records: Until revoked
- Revoked consent: 2 years (proof of consent withdrawal)

**Recipients / Subprocessors:**
- Resend (email delivery)

**Security Measures:**
- Double opt-in verification (token-based)
- One-click unsubscribe in all marketing emails
- Separate consent for marketing vs. transactional emails
- Audit trail for all consent changes

---

## Data Transfers

**International Transfers:**  
Some subprocessors may process data outside the UK/EEA. Where this occurs, we rely on:
- Stripe: Standard Contractual Clauses (SCCs)
- Vercel: SCCs
- Replit: SCCs
- Resend: SCCs (EU/US transfers)

All transfers comply with GDPR Chapter V requirements.

---

## Updates & Review

This ROPA must be updated when:
- New processing activities are introduced
- Subprocessors change
- Retention periods are modified
- Legal basis changes
- Major feature launches occur

**Next Review:** November 14, 2026 (or earlier if major changes)

---

**Internal Use Only** - This document is for internal compliance purposes.
