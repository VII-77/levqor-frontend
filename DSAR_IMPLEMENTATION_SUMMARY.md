# DSAR (Data Subject Access Request) System - Implementation Summary

## ✅ Implementation Complete

The DSAR export system has been fully implemented to comply with UK GDPR and EU GDPR Article 15 (Right of Access).

## 🏗️ Architecture

### Backend Components

1. **dsar/models.py** - Database schema
   - `dsar_requests` table: Tracks all export requests
   - `dsar_exports` table: Stores export metadata and security tokens
   - `dsar_audit_log` table: Comprehensive compliance audit trail

2. **dsar/exporter.py** - Data collection engine
   - Collects user account data
   - Collects referrals, API keys, partnerships, marketplace orders
   - Generates ZIP exports with metadata.json, data.json, README.txt
   - Excludes sensitive data (password hashes, full API keys, tokens)

3. **dsar/security.py** - Security layer
   - 32-byte random download tokens (24h expiry)
   - 6-digit OTP with PBKDF2-HMAC-SHA256 hashing (15min expiry)
   - Constant-time comparison to prevent timing attacks
   - One-time use enforcement

4. **dsar/email.py** - Email notifications
   - Resend API integration
   - HTML/text email templates
   - Secure download link + OTP delivery
   - Professional GDPR-compliant messaging

5. **dsar/audit.py** - Compliance logging
   - Logs all DSAR events (request, generation, email, download)
   - Includes IP, user agent, timestamps
   - Console + database dual logging

### Backend Endpoints

- **POST /api/data-export/request**
  - Requires authentication (X-User-Email header)
  - Rate limited: 1 request per 24 hours per user
  - Generates export, creates tokens, sends email
  - Returns 202 Accepted

- **POST /api/data-export/download**
  - Validates token + OTP
  - Checks expiry (24h for token, 15min for OTP)
  - Streams ZIP file
  - Logs download event
  - Returns 200 with application/zip

### Frontend Components

1. **levqor-site/src/app/privacy-tools/page.tsx**
   - Main DSAR request interface
   - User authentication check
   - Request export button
   - Information about what's included
   - Error/success messaging

2. **levqor-site/src/app/data-export/download/page.tsx**
   - OTP verification page
   - 6-digit code input with validation
   - Token from URL query parameter
   - File download trigger
   - Success/error states

3. **levqor-site/src/app/data-requests/page.tsx** (updated)
   - Added prominent link to /privacy-tools
   - Encourages self-service data export

## 🔒 Security Features

- **32-byte cryptographically secure tokens** (256-bit entropy)
- **6-digit OTP with salted PBKDF2-HMAC-SHA256** (100k iterations)
- **Time-based expiry**: 24h for downloads, 15min for OTP
- **One-time use enforcement** via downloaded_at timestamp
- **Rate limiting**: 1 export request per 24 hours per user
- **Constant-time OTP comparison** (prevents timing attacks)
- **Email-only delivery** (no direct web downloads)
- **Full audit trail** for regulatory compliance

## 📊 Data Included in Export

- User account information (email, name, preferences)
- Referral data (source, campaign, medium)
- Developer API keys (prefixes only, not full keys)
- Partnership registrations
- Marketplace orders
- Terms acceptance records
- Marketing consent history

## 🚫 Data Excluded (Security)

- Password hashes
- Full API keys and secrets
- OAuth tokens and refresh tokens
- Session identifiers
- Internal system identifiers

## 📁 File Structure

```
dsar/
├── __init__.py
├── models.py       # Database schema
├── exporter.py     # Data collection & ZIP generation
├── security.py     # Token & OTP management
├── email.py        # Resend email integration
└── audit.py        # Compliance logging

exports/            # ZIP storage (gitignored)
└── levqor_export_<user_id>_<timestamp>.zip

levqor-site/src/app/
├── privacy-tools/page.tsx          # Request UI
├── data-export/download/page.tsx   # Download UI
└── data-requests/page.tsx          # Updated info page
```

## 🔄 User Flow

1. User visits /privacy-tools
2. Clicks "Request Data Export"
3. Backend generates ZIP with all user data
4. Backend creates secure token + OTP
5. User receives email with:
   - Download link (valid 24h)
   - 6-digit OTP (valid 15min)
6. User clicks link → /data-export/download?token=XXX
7. User enters OTP from email
8. Backend verifies token + OTP
9. ZIP file downloads automatically
10. Download event logged to audit trail

## 📧 Email Template Features

- Branded HTML email with dark theme
- Clear OTP display (formatted: 123 456)
- Security warnings about expiry times
- Alternative text-only version
- GDPR compliance references
- Contact information for privacy team

## 📝 Compliance

✅ **UK GDPR Article 15** - Right of Access
✅ **EU GDPR Article 15** - Right of Access
✅ **Data minimization** - Only necessary data collected
✅ **Security by design** - OTP + token dual security
✅ **Audit trail** - Complete logging for regulatory review
✅ **Transparency** - Clear communication about data included/excluded
✅ **Time-bound** - Automatic expiry prevents stale access

## 🧪 Testing Checklist

- [x] Database tables created successfully
- [x] Backend starts without errors
- [x] Frontend pages accessible
- [x] Email integration configured (requires RESEND_API_KEY)
- [ ] End-to-end test: Request → Email → Download
- [ ] Rate limiting verification
- [ ] Token expiry verification
- [ ] OTP expiry verification
- [ ] Audit log verification

## 🚀 Deployment Requirements

1. Set `RESEND_API_KEY` environment variable
2. Set `AUTH_FROM_EMAIL` (e.g., no-reply@levqor.ai)
3. Set `BASE_URL` (e.g., https://www.levqor.ai)
4. Ensure `exports/` directory is writable
5. Verify SMTP/email delivery
6. Test end-to-end flow before go-live

## 📊 Metrics & Monitoring

The system logs all events to:
- `dsar_audit_log` table (persistent)
- Console logs (APScheduler monitoring)
- Backend logs (Gunicorn workers)

Monitor for:
- Request frequency (rate limiting effectiveness)
- Email delivery failures
- Download success rate
- Expired token/OTP attempts
- File generation errors

## 🔧 Maintenance

- Periodic cleanup of expired exports (>24h old)
- Monitor audit log size growth
- Review email delivery success rate
- Update export schema as new data tables added
- Ensure compliance with evolving GDPR regulations

## 📚 Documentation References

- Internal: docs/compliance/ropa.md (DSAR listed as processing activity)
- Internal: docs/compliance/dpia-levqor-automation.md
- Internal: docs/compliance/lia-marketing-and-analytics.md
- Public: /privacy (Privacy Policy)
- Public: /gdpr (GDPR Compliance Page)
- Public: /data-requests (DSAR Information)
- Public: /privacy-tools (Self-Service Portal)

---

Implementation Date: November 14, 2025
Status: ✅ Complete - Ready for Testing
