# 🎯 EchoPilot Secure Operations Dashboard

## ✅ What's Been Built

A production-ready, secure operations dashboard has been created with the following features:

### 🔒 Security Features
- **Dashboard Key Authentication**: All API routes require `DASHBOARD_KEY` via `X-Dash-Key` header
- **CSRF Protection**: POST requests validate Origin/Referer headers
- **Security Headers**: Cache-Control, X-Frame-Options, X-Content-Type-Options
- **Server-Side Token Handling**: No secrets exposed to frontend
- **Uniform JSON Response**: All responses follow `{"ok": true/false, "data": {...}, "error": null/string}` pattern

### 🌐 Dashboard Routes

| Route | Method | Description | Auth |
|-------|--------|-------------|------|
| `/dashboard` | GET | Serve dashboard UI | None |
| `/api/supervisor-status` | GET | System health check | DASHBOARD_KEY |
| `/api/pulse` | POST | Create governance pulse | DASHBOARD_KEY + CSRF |
| `/api/create-test-job` | POST | Create test job in queue | DASHBOARD_KEY + CSRF |
| `/api/job-log-latest` | GET | Get latest job with finance data | DASHBOARD_KEY |
| `/api/flip-paid` | POST | Update Payment Status→Paid | DASHBOARD_KEY + CSRF |

### 📁 Files Created/Modified

- **dashboard.html** (8.1K) - Clean, responsive UI with gradient design
- **run.py** (25K+) - Added security middleware and 6 secure API routes

---

## 🚀 Setup Instructions

### Step 1: Create DASHBOARD_KEY Secret

1. Go to **Replit Secrets** (🔒 icon in left sidebar)
2. Click **+ New Secret**
3. Name: `DASHBOARD_KEY`
4. Value: Create a strong random key (e.g., use this command):
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
5. Click **Add secret**

**Example value:**
```
XyZ123aBc456DeF789GhI012JkL345MnO678PqR901StU234
```

### Step 2: Configure Automation Queue (Optional)

If you want to use the "Create Test Job" feature, ensure your **Automation Queue** database in Notion has these properties:

| Property Name | Type | Required |
|---------------|------|----------|
| Task Name | Title | ✅ |
| Description | Text (Rich Text) | ✅ |
| Trigger | Checkbox | ✅ |
| Status | Select | Optional |

**To add these:**
1. Open your Automation Queue database in Notion
2. Click **+ Add Property** for each
3. Match the name and type exactly

---

## 🎯 How to Use the Dashboard

### 1. Open the Dashboard
```
https://echopilotai.replit.app/dashboard
```

### 2. Enter Your Dashboard Key
- Paste your `DASHBOARD_KEY` value into the password field at the top
- The key is stored in your browser session only (never sent insecurely)

### 3. Test the Buttons (In Order)

1. **✅ Check Health**
   - Verifies system is running
   - Response: `{"ok": true, "data": {"status": "ok"}, "error": null}`

2. **📊 Supervisor Status**
   - Shows worker state (Notion, Drive, OpenAI)
   - Response includes timestamp and service status

3. **💓 Send Pulse**
   - Creates a System Pulse entry in Governance database
   - Returns created pulse ID

4. **🎯 Create Test Job** *(requires Automation Queue setup)*
   - Adds a test job with sample1.mp3 payload
   - Job will be processed in ~60 seconds

5. **Wait 60-90 seconds** (for Notion sync + bot processing)

6. **📋 Refresh Jobs**
   - Shows latest job with QA score, duration, finance fields
   - Automatically saves `page_id` for next step

7. **💰 Flip to Paid**
   - Updates the last job's Payment Status to "Paid"
   - Uses saved `page_id` from previous step

---

## 🔍 Response Format

All API responses follow this structure:

### Success Response
```json
{
  "ok": true,
  "data": {
    "message": "Operation successful",
    "id": "abc123...",
    ...
  },
  "error": null
}
```

### Error Response
```json
{
  "ok": false,
  "data": null,
  "error": "Detailed error message"
}
```

---

## 🛡️ Security Details

### Authentication Flow
```
User Browser → Enter DASHBOARD_KEY → Click Button →
  Fetch with X-Dash-Key Header → Flask Middleware →
    Validate Key → Execute Route → Return JSON
```

### CSRF Protection
- Validates Origin/Referer contains `echopilotai.replit.app` or `localhost`
- Only applies to POST requests
- Prevents cross-site request forgery attacks

### Headers Applied
```
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Pragma: no-cache
```

---

## 🧪 Testing Checklist

- [ ] Created `DASHBOARD_KEY` secret in Replit
- [ ] Opened `/dashboard` successfully
- [ ] Entered dashboard key in password field
- [ ] ✅ Check Health returns `"ok": true`
- [ ] 📊 Supervisor Status shows all services "ok"
- [ ] 💓 Send Pulse creates governance entry
- [ ] 📋 Refresh Jobs shows recent job data
- [ ] 💰 Flip to Paid updates payment status

---

## 📊 Dashboard Features

### UI Features
- **Clean gradient design** (purple/blue theme)
- **Real-time activity log** with color-coded messages
- **Button state management** (disables during requests)
- **Automatic error handling** with clear messages
- **Mobile-responsive** layout
- **Secure key input** (password field, not stored)

### Backend Features
- **Middleware-based auth** (DRY, reusable)
- **CSRF protection** (POST request validation)
- **Security headers** (applied to all responses)
- **Uniform error handling** (consistent JSON structure)
- **Notion sync retry logic** (handles API lag gracefully)

---

## 🎉 Ready to Use!

Your secure operations dashboard is production-ready. Once you add the `DASHBOARD_KEY` secret, you can:

1. Monitor system health in real-time
2. Create test jobs on-demand
3. Review finance metrics (QA, Duration, Revenue, Margin)
4. Update payment statuses
5. Track governance pulses

**Dashboard URL:**
```
https://echopilotai.replit.app/dashboard
```

**Next Steps:**
1. Add `DASHBOARD_KEY` secret
2. Test all buttons
3. Bookmark the dashboard for daily ops
4. Share the dashboard URL with your team (they'll need the key)

---

**Built with ❤️ for EchoPilot AI**
