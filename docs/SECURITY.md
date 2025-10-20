# Security Documentation

## Overview

EchoPilot implements enterprise-grade security controls designed for production deployment. This document outlines our security architecture, controls, and best practices.

## Security Architecture

### Defense in Depth

1. **Application Layer**
   - CSRF protection on state-changing operations
   - Rate limiting with exponential backoff
   - Input validation and sanitization
   - PII redaction in logs

2. **Transport Layer**
   - HTTPS only (Strict-Transport-Security)
   - Secure headers (CSP, X-Frame-Options, etc.)
   - No mixed content

3. **Authentication & Authorization**
   - Role-Based Access Control (RBAC)
   - Admin and analyst roles
   - Dashboard key authentication
   - JWT tokens for API access

## Security Controls

### 1. Content Security Policy (CSP)

```
Content-Security-Policy: 
  default-src 'self'; 
  script-src 'self' 'unsafe-inline'; 
  style-src 'self' 'unsafe-inline'; 
  img-src 'self' data: https:; 
  font-src 'self' data:;
```

**Purpose:** Prevents XSS attacks by restricting resource loading.

### 2. Rate Limiting

- **10 requests per 60 seconds** (default)
- **Exponential backoff** on violations
- **Lockout mechanism** for persistent abuse
- **Per-IP + User-Agent** fingerprinting

**Endpoints protected:**
- `/api/status/summary`: 30 req/60s
- All POST endpoints: 10 req/60s
- Payment endpoints: 5 req/60s

### 3. CSRF Protection

All state-changing operations require CSRF tokens:

```javascript
// Get CSRF token
const { csrf_token, session_id } = await fetch('/api/csrf-token').then(r => r.json());

// Use in requests
fetch('/api/create-job', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': csrf_token,
    'X-Session-ID': session_id
  }
});
```

### 4. Audit Logging

All sensitive operations are logged to `logs/ndjson/audit.ndjson`:

```json
{
  "ts": "2025-10-20T22:50:00Z",
  "action": "payment_refund",
  "user": "admin",
  "ok": true,
  "ip": "1.2.3.4",
  "endpoint": "/api/refund",
  "method": "POST",
  "details": {"amount": 50.00, "email": "[REDACTED]"}
}
```

**Logged actions:**
- Authentication attempts
- Authorization failures
- Payment operations
- Data access/modifications
- Rate limit violations
- CSRF violations

### 5. PII Redaction

Automatically redacts in logs:
- Email addresses → `[EMAIL]`
- Credit cards → `[CARD]`
- Fields: `password`, `token`, `secret`, `api_key`, `ssn`

### 6. Secure Headers

```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

## Role-Based Access Control (RBAC)

### Roles

1. **Admin**
   - Full system access
   - Payment refunds
   - User management
   - System configuration

2. **Analyst**
   - Read-only metrics
   - View logs and audits
   - Generate reports
   - No payment access

3. **Viewer** (future)
   - Dashboard access only
   - Limited API calls

### Implementation

Set roles via `ROLES_JSON` environment variable:

```json
{
  "CHMDlYY5TNE0NIB7qul7KYRa9a4BSbID-4WqpoE_DaE": "admin",
  "another-key-here": "analyst"
}
```

Protected endpoints use `@require_role` decorator:

```python
@app.route('/api/refund', methods=['POST'])
@require_role('admin')
def refund_payment():
    # Only admins can access
    pass
```

## Compliance

### WCAG 2.2 AA

- Keyboard navigation support
- ARIA labels on interactive elements
- Sufficient color contrast ratios
- Visible focus indicators
- Reduced motion support

### GDPR/CCPA Ready

- PII redaction in logs
- Data export capabilities
- Audit trail for data access
- Clear privacy controls
- Cookie consent (if cookies used)

### SOC 2 Preparation

- Comprehensive audit logging
- Access controls (RBAC)
- Security monitoring
- Incident response procedures
- Backup and recovery

## Threat Model

### Threats Mitigated

✅ **Cross-Site Scripting (XSS)**
- CSP headers
- Input sanitization
- Content-Type enforcement

✅ **Cross-Site Request Forgery (CSRF)**
- Token-based protection
- Origin/Referer validation

✅ **Brute Force Attacks**
- Rate limiting
- Exponential backoff
- Account lockouts

✅ **SQL Injection**
- Parameterized queries
- ORM usage
- Input validation

✅ **Sensitive Data Exposure**
- PII redaction
- Audit logs
- HTTPS only

✅ **Broken Authentication**
- Secure key management
- Session timeout
- RBAC enforcement

### Known Limitations

⚠️ **Session Management**
- Currently using in-memory storage
- Production should use Redis

⚠️ **API Key Rotation**
- Manual process
- Should automate rotation

⚠️ **2FA**
- Not yet implemented
- Planned for future release

## Best Practices

### For Administrators

1. **Rotate Dashboard Keys Quarterly**
   ```bash
   # Generate new key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Monitor Audit Logs Daily**
   ```bash
   tail -f logs/ndjson/audit.ndjson
   ```

3. **Review Rate Limit Violations**
   ```bash
   grep "rate_limit_exceeded" logs/ndjson/audit.ndjson
   ```

4. **Check Failed Auth Attempts**
   ```bash
   grep '"ok":false' logs/ndjson/audit.ndjson | grep auth
   ```

### For Developers

1. **Always Use CSRF Protection**
   ```python
   @app.route('/api/action', methods=['POST'])
   @require_csrf
   def action():
       pass
   ```

2. **Rate Limit New Endpoints**
   ```python
   @app.route('/api/new')
   @rate_limit(max_requests=10, window_seconds=60)
   def new_endpoint():
       pass
   ```

3. **Audit Sensitive Operations**
   ```python
   audit_log("payment_created", {"amount": amount}, user=user_id)
   ```

4. **Never Log Secrets**
   ```python
   # Bad
   logger.info(f"API key: {api_key}")
   
   # Good
   audit_log("api_key_used", {"key_id": key_id})
   ```

## Incident Response

### If Breach Suspected

1. **Isolate:**
   - Rotate all dashboard keys immediately
   - Disable affected accounts
   - Check audit logs for scope

2. **Investigate:**
   ```bash
   # Review recent activity
   tail -1000 logs/ndjson/audit.ndjson
   
   # Check rate limit violations
   grep "rate_limit" logs/ndjson/audit.ndjson
   
   # Review auth failures
   grep "unauthorized" logs/ndjson/audit.ndjson
   ```

3. **Remediate:**
   - Patch vulnerabilities
   - Update security controls
   - Document lessons learned

4. **Notify:**
   - Inform affected users
   - Report to compliance if required

## Security Updates

This document is updated with each security-related change. Last updated: **October 20, 2025** (Boss Mode UI v2 deployment).

### Recent Changes

- Added CSP headers
- Implemented rate limiting
- Added CSRF protection
- PII redaction in logs
- Audit logging system
- RBAC enforcement

---

**Questions or Security Concerns?**  
Review audit logs or contact the security team.
