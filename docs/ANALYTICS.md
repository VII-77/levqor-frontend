# EchoPilot Analytics & Product Insights

## Overview
Phase 111 provides deep usage analytics with DAU/WAU/MAU metrics, feature usage tracking, and funnel analysis. The system captures client-side events with local retry and processes them through daily rollup jobs.

## Architecture

### Client-Side Telemetry
- **File**: `static/js/telemetry.js`
- **Features**:
  - Lightweight event tracking with debounce (1s)
  - Local retry queue (max 100 events)
  - Automatic page view tracking
  - Click tracking via `data-track` attributes
  - Batched event submission
  - Offline support with IndexedDB fallback

### Server-Side Processing
- **Module**: `bot/analytics.py`
- **Storage**: `logs/analytics_events.ndjson`
- **Rollup**: `logs/analytics.ndjson`

### Daily Rollup Job
- **Schedule**: Daily at 03:15 UTC
- **Function**: Aggregates raw events into daily summaries
- **Metrics**: DAU, WAU, MAU, feature usage, funnel steps

## API Endpoints

### GET /api/analytics/usage
Get analytics summary with DAU/WAU/MAU metrics.

**Authentication**: Requires `X-Dash-Key`

**Query Parameters**:
- `days` (integer, optional): Analysis window in days (1-365, default: 30)

**Response**:
```json
{
  "ok": true,
  "ts": "2025-10-21T10:00:00Z",
  "period_days": 30,
  "dau": 42.5,
  "wau": 156.3,
  "mau": 487,
  "feature_usage": {
    "dashboard": 1250,
    "workflow_builder": 892,
    "boss_mode": 456
  },
  "funnel_steps": {
    "page_view": 5234,
    "action": 2156,
    "conversion": 487
  },
  "total_events": 7877,
  "unique_days": 30,
  "unique_weeks": 5
}
```

**Performance**:
- P95 Latency: < 250ms
- P99 Latency: < 500ms

### POST /api/analytics/event
Client telemetry endpoint for event ingestion.

**Authentication**: None (public endpoint)

**Request Body**:
```json
{
  "events": [
    {
      "event_type": "page_view",
      "user_id": "user123",
      "feature": "dashboard",
      "metadata": {
        "referrer": "https://example.com"
      },
      "ts": "2025-10-21T10:00:00Z",
      "url": "/dashboard"
    }
  ]
}
```

**Response**:
```json
{
  "ok": true,
  "logged": 1
}
```

**Limits**:
- Max 100 events per batch
- Events older than 365 days are ignored

## Client Integration

### Basic Usage
```html
<!-- Include telemetry script -->
<script src="/static/js/telemetry.js"></script>

<!-- Track custom events -->
<script>
  EchoPilot.track('action', 'button_click', {
    button_id: 'submit-btn',
    form_name: 'contact'
  });
</script>
```

### Automatic Tracking
```html
<!-- Track clicks automatically -->
<button data-track="submit_form" data-action="click">
  Submit
</button>

<!-- Track navigation -->
<a href="/pricing" data-track="pricing_page" data-action="navigate">
  View Pricing
</a>
```

### User Identification
```javascript
// Set user ID after login
EchoPilot.setUserId('user_12345');

// Anonymous by default
```

## Metrics Definitions

### DAU (Daily Active Users)
Average unique users per day over the analysis period.

**Calculation**:
```
DAU = (Sum of unique users per day) / (Number of days with data)
```

### WAU (Weekly Active Users)
Average unique users per week over the analysis period.

**Calculation**:
```
WAU = (Sum of unique users per week) / (Number of weeks with data)
```

### MAU (Monthly Active Users)
Total unique users over the analysis period (typically 30 days).

### Feature Usage
Count of events per feature, sorted by popularity.

### Funnel Steps
Event counts by type:
- `page_view`: Page impressions
- `action`: User interactions (clicks, form submissions, etc.)
- `conversion`: Goal completions

## Event Types

### page_view
Automatically tracked on page load.

**Fields**:
- `event_type`: "page_view"
- `feature`: Page path (e.g., "dashboard", "workflow")
- `url`: Full URL path

### action
User interactions with tracked elements.

**Fields**:
- `event_type`: "action"
- `feature`: Element identifier from `data-track`
- `metadata.action`: Action type (click, submit, etc.)

### conversion
Goal completions or important user actions.

**Fields**:
- `event_type`: "conversion"
- `feature`: Conversion goal name
- `metadata`: Additional context

## Storage Format

### Events Log (logs/analytics_events.ndjson)
Raw events in NDJSON format:
```json
{
  "ts": "2025-10-21T10:00:00Z",
  "event_type": "page_view",
  "user_id": "user123",
  "feature": "dashboard",
  "metadata": {}
}
```

### Rollup Log (logs/analytics.ndjson)
Daily aggregated summaries:
```json
{
  "ts": "2025-10-21T03:15:00Z",
  "period_days": 30,
  "dau": 42.5,
  "wau": 156.3,
  "mau": 487,
  "feature_usage": {...},
  "funnel_steps": {...},
  "total_events": 7877
}
```

## Privacy & Compliance

### PII Handling
- User IDs are opaque identifiers (no emails, names, etc.)
- IP addresses are NOT logged
- Metadata is developer-controlled (avoid PII)

### Data Retention
- Raw events: 90 days
- Rollup summaries: 365 days
- Configurable via environment variables

### GDPR Compliance
- Right to erasure: Delete events by user_id
- Right to access: Export events by user_id
- Data minimization: Only essential fields tracked

## Performance

### Event Ingestion
- Throughput: 10,000 events/minute
- Latency: P95 < 50ms, P99 < 100ms
- Batch size: Up to 100 events

### Analytics Queries
- DAU/WAU/MAU calculation: < 250ms for 30-day window
- Feature usage aggregation: < 150ms
- Memory usage: O(unique_users + unique_features)

## Monitoring

### Metrics to Watch
- Event ingestion rate (events/minute)
- Failed event batches (%)
- Rollup job duration (seconds)
- Analytics query latency (ms)

### Alerts
- Event ingestion failures > 1%
- Rollup job duration > 60 seconds
- Analytics query P95 > 500ms

## Troubleshooting

### Events not appearing
1. Check client-side console for errors
2. Verify `/api/analytics/event` is accessible
3. Check `logs/analytics_events.ndjson` for new entries
4. Ensure events have valid `event_type`

### Zero DAU/WAU/MAU
1. Verify events exist in last 30 days
2. Check user_id is set (not null)
3. Run manual rollup: `python3 bot/analytics.py`
4. Check for NDJSON parsing errors

### High latency
1. Reduce analysis window (days parameter)
2. Archive old events (> 90 days)
3. Optimize NDJSON parsing
4. Consider database migration for high volume

## Future Enhancements
- Real-time analytics dashboard
- Cohort analysis
- Retention curves
- A/B test integration
- Custom event validation
- BigQuery/Snowflake export

---

**Version**: Phase 111  
**Last Updated**: October 2025  
**Owner**: EchoPilot Analytics Team
