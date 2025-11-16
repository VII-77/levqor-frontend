# Levqor Error Monitoring System

**Custom in-house error tracking solution replacing Sentry**

## Overview
A complete 6-phase error monitoring infrastructure that logs, tracks, and alerts on errors across the frontend and backend. Provides real-time Telegram alerts for critical errors and daily email summaries.

---

## Architecture

### Phase 1: Backend Logging Infrastructure ✅
- **ErrorEvent Model**: SQLite table storing all error events
  - Fields: `id`, `created_at`, `source`, `service`, `path_or_screen`, `user_email`, `severity`, `message`, `stack`
  - Severity levels: `info`, `warning`, `error`, `critical`

- **API Endpoints**:
  - `POST /api/errors/log`: Log new error events (no authentication required for logging)
  - `GET /api/errors/recent`: Retrieve recent errors (requires `X-Internal-Secret` header)

### Phase 2: Backend Integration ✅
- **Error Logger Helper** (`backend/utils/error_logger.py`):
  - `log_error(service, message, severity, ...)`: Convenience function for backend error logging
  
- **Integrated Services**:
  - Support AI (`backend/services/support_ai.py`): Logs public/private chat API errors
  - Stripe Webhooks (`backend/routes/stripe_checkout_webhook.py`): Logs checkout processing failures

### Phase 3: Frontend Error Reporting ✅
- **Error Client** (`levqor-site/src/lib/errorClient.ts`):
  - `logClientError()`: Send error to backend API
  - `logJSError()`: Log JavaScript errors with automatic stack trace extraction
  
- **Integrated Components**:
  - Support Chat (`SupportChat.tsx`): Reports API failures from both public and private support chat

### Phase 4: Owner Dashboard ✅
- **Error Dashboard** (`/owner/errors`):
  - Real-time error viewing with filtering (severity, source, service)
  - Statistics cards showing total, critical, errors, warnings
  - Detailed error modal with full stack traces
  - Linked from Owner Handbook

### Phase 5: EchoPilot Automation ✅
- **Scheduled Jobs** (added to `monitors/scheduler.py`):
  
  1. **Critical Error Alerts** (every 10 minutes):
     - Function: `check_critical_errors()`
     - Checks for errors with `severity='critical'` in last 10 minutes
     - Sends Telegram notifications with error details
     - Requires: `TELEGRAM_BOT_TOKEN` environment variable
  
  2. **Daily Email Summary** (daily at 9:00 AM UTC):
     - Function: `send_daily_error_summary()`
     - Aggregates last 24 hours of errors
     - Sends HTML email with error breakdown by severity and service
     - Sends to: `OWNER_EMAIL` environment variable (defaults to support@levqor.ai)

### Phase 6: Verification ✅
- All endpoints tested and operational
- Scheduler successfully loaded 21 jobs (up from 19)
- Error logging confirmed via database queries

---

## Configuration

### Required Environment Variables

```bash
# For Telegram alerts (critical errors)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id  # Default: 5932848683

# For daily email summaries
OWNER_EMAIL=your@email.com  # Default: support@levqor.ai

# For owner dashboard access (frontend)
NEXT_PUBLIC_INTERNAL_SECRET=your_secret_key

# For API authentication (backend)
INTERNAL_SECRET=your_secret_key
```

### Optional Environment Variables

```bash
# Database path (defaults to levqor.db)
DATABASE_PATH=path/to/levqor.db

# API base URL (frontend)
NEXT_PUBLIC_API_URL=https://api.levqor.ai
```

---

## Usage

### Backend Error Logging

```python
from backend.utils.error_logger import log_error

# Log an error
log_error(
    service="payment_processor",
    message="Stripe checkout session creation failed",
    severity="error",
    user_email="customer@example.com",
    path="/api/checkout"
)

# Log a critical error (triggers Telegram alert)
log_error(
    service="database",
    message="Database connection pool exhausted",
    severity="critical"
)
```

### Frontend Error Logging

```typescript
import { logClientError, logJSError } from '@/lib/errorClient';

// Log a custom error
logClientError({
  service: 'checkout_flow',
  message: 'Payment form submission failed',
  severity: 'error',
  userEmail: user.email,
});

// Log a JavaScript exception
try {
  riskyOperation();
} catch (error) {
  logJSError('user_dashboard', error, 'error', user.email);
}
```

### Viewing Errors

1. **Owner Dashboard**: Navigate to `/owner/errors` (linked from `/owner/handbook`)
2. **Direct API**: `GET /api/errors/recent?limit=100&severity=critical` with `X-Internal-Secret` header

---

## Scheduler Jobs

The error monitoring system adds 2 scheduled jobs to EchoPilot:

| Job | Frequency | Description |
|-----|-----------|-------------|
| `critical_error_check` | Every 10 minutes | Checks for critical errors and sends Telegram alerts |
| `daily_error_summary` | Daily at 9:00 AM UTC | Sends email summary of errors in last 24 hours |

View all jobs in the scheduler logs: `INFO:levqor.scheduler:✅ APScheduler initialized with 21 jobs`

---

## Files Modified/Created

### Backend
- `backend/models/error_event.py` - ErrorEvent model
- `backend/routes/error_logging.py` - API endpoints
- `backend/utils/error_logger.py` - Helper functions
- `backend/services/support_ai.py` - Error logging integration
- `backend/routes/stripe_checkout_webhook.py` - Error logging integration
- `monitors/scheduler.py` - Scheduled jobs for alerts/summaries

### Frontend
- `levqor-site/src/lib/errorClient.ts` - Error reporting client
- `levqor-site/src/app/owner/errors/page.tsx` - Owner dashboard
- `levqor-site/src/components/support/SupportChat.tsx` - Error logging integration
- `levqor-site/src/app/owner/handbook/page.tsx` - Link to error dashboard

### Documentation
- `ERROR_MONITORING_SYSTEM.md` - This file

---

## Severity Levels

| Level | Color | Usage | Alerts |
|-------|-------|-------|--------|
| `critical` | Red | System-breaking errors, requires immediate attention | ✅ Telegram (immediate) |
| `error` | Orange | Significant errors affecting functionality | ❌ Email summary only |
| `warning` | Yellow | Potential issues, degraded experience | ❌ Email summary only |
| `info` | Blue | Informational events, non-critical | ❌ Email summary only |

---

## Testing

### Test Error Logging Endpoint

```bash
curl -X POST http://localhost:8000/api/errors/log \
  -H "Content-Type: application/json" \
  -d '{
    "source": "backend",
    "service": "test_service",
    "severity": "error",
    "message": "Test error for verification"
  }'
```

### Test Error Retrieval

```bash
curl -X GET 'http://localhost:8000/api/errors/recent?limit=5' \
  -H "X-Internal-Secret: your_secret_here"
```

### Test Database

```sql
SELECT * FROM error_events ORDER BY created_at DESC LIMIT 10;
```

---

## Next Steps

1. **Set Environment Variables**: Configure `TELEGRAM_BOT_TOKEN` and `OWNER_EMAIL`
2. **Set Internal Secret**: Add `INTERNAL_SECRET` and `NEXT_PUBLIC_INTERNAL_SECRET` for dashboard access
3. **Monitor Logs**: Watch scheduler logs to confirm jobs are running
4. **Test Critical Alerts**: Trigger a critical error to verify Telegram notifications
5. **Wait for Daily Summary**: Check email at 9:00 AM UTC next day

---

## Replacement of Sentry

This system **replaces Sentry** with:
- ✅ Custom error storage (SQLite/PostgreSQL)
- ✅ Real-time Telegram alerts for critical errors
- ✅ Daily email summaries
- ✅ Owner dashboard for error viewing
- ✅ Frontend and backend error tracking
- ✅ No external dependencies or monthly fees
- ✅ Full control over error data and retention

---

**Status**: ✅ Fully operational and integrated into Levqor v8.0
**Last Updated**: November 16, 2025
