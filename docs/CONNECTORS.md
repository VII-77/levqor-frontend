# Levqor Connectors Documentation

## Overview
Levqor Connectors enable seamless integration with external services through standardized, production-ready API endpoints.

## Authentication Model

### API Authentication
All connector endpoints support:
- **Bearer Token**: `Authorization: Bearer <token>` (future implementation)
- **IP-based**: Fallback to IP address for quota tracking

### Quota System
- **Free Plan**: 1 successful call per day per connector
- **Pro Plan**: Unlimited calls
- **Response**: `402 Payment Required` when free limit exceeded with upgrade link

## Environment Variables

Required secrets (configure via Replit Secrets):

| Service | Environment Variables | Required |
|---------|----------------------|----------|
| Slack | `SLACK_WEBHOOK_URL` | Yes |
| Notion | `NOTION_API_KEY` | Yes |
| Google Sheets | `GOOGLE_SERVICE_ACCOUNT_JSON`, `GOOGLE_SHEETS_SPREADSHEET_ID` | Both Yes |
| Telegram | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID_DEFAULT` (optional) | Token Yes |
| Email (Resend) | `RESEND_API_KEY` | Yes |

## Endpoints

### 1. Slack - Send Message
**Endpoint**: `POST /actions/slack.send`

**Request Body**:
```json
{
  "text": "Hello from Levqor!",
  "channel": "#general"  // optional
}
```

**Success Response** (200):
```json
{
  "status": "sent"
}
```

**Error Responses**:
- `400`: Validation error
- `402`: Rate limit exceeded (free plan)
- `503`: Connector not configured

**Example**:
```bash
curl -X POST https://levqor.ai/actions/slack.send \
  -H "Content-Type: application/json" \
  -d '{"text": "Deployment complete!"}'
```

---

### 2. Notion - Create Page
**Endpoint**: `POST /actions/notion.create`

**Request Body**:
```json
{
  "database_id": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "props": {
    "Name": {
      "title": [{"text": {"content": "New Task"}}]
    },
    "Status": {
      "select": {"name": "To Do"}
    }
  }
}
```

**Success Response** (200):
```json
{
  "status": "created",
  "id": "a1b2****p6"
}
```

**Notes**:
- `database_id`: 32-36 character Notion database ID
- `props`: Notion API properties object
- ID is masked in response for privacy

**Example**:
```bash
curl -X POST https://levqor.ai/actions/notion.create \
  -H "Content-Type: application/json" \
  -d '{
    "database_id": "abc123...",
    "props": {
      "Name": {"title": [{"text": {"content": "Meeting Notes"}}]}
    }
  }'
```

---

### 3. Google Sheets - Append Row
**Endpoint**: `POST /actions/sheets.append`

**Request Body**:
```json
{
  "range": "Sheet1!A1:C1",
  "values": [
    ["2025-01-07", "New Lead", "contact@example.com"]
  ]
}
```

**Success Response** (200):
```json
{
  "status": "appended",
  "updated": 1
}
```

**Notes**:
- `range`: A1 notation (e.g., `Sheet1!A1:Z1`)
- `values`: 2D array of strings
- Uses Google Service Account for authentication

**Example**:
```bash
curl -X POST https://levqor.ai/actions/sheets.append \
  -H "Content-Type: application/json" \
  -d '{
    "range": "Leads!A1:C1",
    "values": [["2025-01-07", "John Doe", "john@example.com"]]
  }'
```

---

### 4. Telegram - Send Message
**Endpoint**: `POST /actions/telegram.send`

**Request Body**:
```json
{
  "text": "Alert: Server CPU > 90%",
  "chat_id": "123456789"  // optional if TELEGRAM_CHAT_ID_DEFAULT set
}
```

**Success Response** (200):
```json
{
  "status": "sent"
}
```

**Notes**:
- `chat_id`: Optional if `TELEGRAM_CHAT_ID_DEFAULT` env var is set
- Text supports Markdown formatting
- Max length: 4096 characters

**Example**:
```bash
curl -X POST https://levqor.ai/actions/telegram.send \
  -H "Content-Type: application/json" \
  -d '{"text": "🚨 Critical alert!", "chat_id": "123456789"}'
```

---

### 5. Email - Send via Resend
**Endpoint**: `POST /actions/email.send`

**Request Body**:
```json
{
  "to": "customer@example.com",
  "subject": "Welcome to Levqor",
  "text": "Thank you for signing up!"
}
```

**Success Response** (200):
```json
{
  "status": "sent"
}
```

**Notes**:
- Email validation enforced on `to` field
- Subject max length: 200 characters
- Plain text only (HTML support planned)

**Example**:
```bash
curl -X POST https://levqor.ai/actions/email.send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Test Email",
    "text": "This is a test message."
  }'
```

---

## Health Check
**Endpoint**: `GET /actions/health`

**Response** (200):
```json
{
  "status": "ok",
  "connectors": {
    "slack": true,
    "notion": false,
    "sheets": true,
    "telegram": false,
    "email": true
  },
  "configured": 3,
  "total": 5
}
```

Shows which connectors are properly configured.

---

## Error Handling

### Standard Error Response
```json
{
  "error": "error_code",
  "message": "Human-readable description",
  "details": {}  // optional validation details
}
```

### Error Codes
| Code | HTTP Status | Description |
|------|-------------|-------------|
| `validation_error` | 400 | Invalid request schema |
| `not_configured` | 503 | Connector env vars missing |
| `rate_limited` | 402 | Free plan quota exceeded |
| `upstream_error` | 500 | Third-party service error |

---

## Rate Limiting

Free plan users are limited to **1 successful call per day per connector**.

**Rate Limit Response**:
```json
{
  "error": "rate_limited",
  "message": "Free plan: 1 slack call/day. Upgrade for unlimited.",
  "upgrade": "/pricing"
}
```

Quota resets daily at 00:00 UTC.

---

## Security & Privacy

### Logging
- All connector calls are logged to `logs/connectors.log`
- **Never logs**: Secrets, API keys, payload content
- **Logs**: Timestamp, IP (hashed), connector, status, response time

### Masking
External IDs (Notion pages, etc.) are masked in responses:
- Example: `a1b2c3d4e5f6g7h8` → `a1b2****h8`

### Timeouts
- All HTTP requests: 10 second timeout
- Retry logic: 1 retry on 5xx errors with backoff

---

## Best Practices

1. **Test with `/actions/health`** before attempting connector calls
2. **Handle 503 errors** gracefully (connector not configured)
3. **Implement exponential backoff** for 429/503 responses
4. **Validate input** on client-side before API calls
5. **Monitor quota usage** to avoid hitting free plan limits

---

## Support

- **Issues**: Create ticket at support@levqor.ai
- **Feature Requests**: Vote on roadmap at levqor.ai/roadmap
- **Custom Connectors**: Enterprise plan offers custom integrations

---

*Last Updated: 2025-01-07*
