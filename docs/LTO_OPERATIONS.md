# EchoPilot Long-Term Operations Guide (LTO)

**Version:** 2.0.0 "Quantum"  
**Date:** October 21, 2025  
**Status:** Production Ready

---

## 📋 Table of Contents

1. [Daily Operations](#daily-operations)
2. [Weekly Maintenance](#weekly-maintenance)
3. [Monthly Tasks](#monthly-tasks)
4. [Emergency Procedures](#emergency-procedures)
5. [Monitoring & Alerts](#monitoring--alerts)
6. [Backup & Recovery](#backup--recovery)
7. [Performance Optimization](#performance-optimization)
8. [Security Operations](#security-operations)

---

## Daily Operations

### 1. Health Check (08:00 UTC)
```bash
python3 scripts/daily_health_check.py
```

**Expected Output:**
- All endpoints return 200 OK
- Response times < 1000ms
- No critical errors in logs

**Failure Actions:**
- Telegram alert sent automatically
- Check `/tmp/logs/` for error details
- Review `logs/daily_health.json`

### 2. Log Review
```bash
# Check latest logs
tail -100 /tmp/logs/EchoPilot_Bot_*.log
tail -100 /tmp/logs/Scheduler_*.log
```

**Look for:**
- ERROR or CRITICAL level messages
- Failed API calls
- Database connection issues
- High latency warnings

### 3. Queue Monitoring
```bash
curl http://localhost:5000/api/queue/status \
  -H "X-Dash-Key: $DASHBOARD_KEY"
```

**Monitor:**
- Queue depth < 50 (normal)
- Processing rate > 10/min
- Failed jobs < 5%

---

## Weekly Maintenance

### Sunday 03:00 UTC - Automated Tasks

1. **Compliance Maintenance**
   - Audit chain verification
   - GDPR export cleanup (90-day retention)
   - Security scan execution

2. **Backup Verification**
   ```bash
   python3 scripts/dr_restore_check.py
   ```

3. **Performance Review**
   ```bash
   curl http://localhost:5000/api/slo/status \
     -H "X-Dash-Key: $DASHBOARD_KEY"
   ```

4. **Analytics Rollup**
   - Weekly DAU/WAU/MAU aggregation
   - Cost analysis
   - Revenue reporting

---

## Monthly Tasks

### First Monday of Month

1. **Security Updates**
   ```bash
   python3 scripts/security_scanner.py
   pip list --outdated
   ```

2. **Capacity Planning**
   - Review auto-scaler recommendations
   - Analyze growth trends
   - Update resource allocation

3. **Financial Review**
   ```bash
   curl http://localhost:5000/api/finops/summary?days=30 \
     -H "X-Dash-Key: $DASHBOARD_KEY"
   ```

4. **Partner Payouts**
   ```bash
   curl http://localhost:5000/api/growth/payouts/export \
     -H "X-Dash-Key: $DASHBOARD_KEY" > payouts_$(date +%Y%m).csv
   ```

---

## Emergency Procedures

### Service Down

1. **Check Status**
   ```bash
   curl http://localhost:5000/api/health
   ps aux | grep gunicorn
   ps aux | grep exec_scheduler
   ```

2. **Restart Services**
   ```bash
   # Via Replit UI: Stop and Start workflows
   # OR manual restart:
   pkill -f gunicorn
   pkill -f exec_scheduler.py
   # Workflows will auto-restart
   ```

3. **Check Logs**
   ```bash
   tail -200 /tmp/logs/EchoPilot_Bot_*.log
   grep ERROR /tmp/logs/Scheduler_*.log
   ```

### Database Issues

1. **Connection Test**
   ```bash
   python3 -c "import psycopg2; import os; conn = psycopg2.connect(os.getenv('DATABASE_URL')); print('✅ Connected')"
   ```

2. **Backup Restore**
   ```bash
   # List backups
   ls -lh backups/*.tar.gz
   
   # Restore from backup (CAREFUL!)
   python3 scripts/dr_restore_check.py --restore backups/latest.tar.gz
   ```

### High Load / Performance Degradation

1. **Check Metrics**
   ```bash
   curl http://localhost:5000/api/predict/load
   curl http://localhost:5000/api/healing/status
   ```

2. **Auto-Scaling**
   ```bash
   # Check autoscaler recommendations
   python3 scripts/autoscaler.py
   ```

3. **Manual Intervention**
   - Enable cost guardrails
   - Increase worker count
   - Clear stuck jobs from queue

---

## Monitoring & Alerts

### Telegram Alerts (Configured)

**Alert Triggers:**
- Health check failures
- SLO breaches
- Security scan issues
- DR verification failures
- Payment reconciliation errors

**Alert Channel:**
- Token: `TELEGRAM_BOT_TOKEN`
- Chat: `TELEGRAM_CHAT_ID`

### Prometheus Metrics

```bash
curl http://localhost:5000/metrics
```

**Key Metrics:**
- `http_requests_total` - Total requests
- `http_request_duration_seconds` - Latency quantiles
- `jobs_processed_total` - Job throughput
- `database_connections_active` - DB health

### SLO Monitoring

**Targets:**
- Availability: 99.9%
- P95 Latency: < 800ms
- P99 Latency: < 1200ms
- Webhook Success: 99%

**Check Status:**
```bash
curl http://localhost:5000/api/slo/status
```

---

## Backup & Recovery

### Automated Backups

**Schedule:**
- Daily: 00:30 UTC
- Location: `backups/` directory
- Retention: 30 days

**Verify Backup:**
```bash
python3 scripts/dr_restore_check.py
```

### Manual Backup

```bash
# Create backup
tar -czf backups/manual_$(date +%Y%m%d_%H%M%S).tar.gz \
  logs/ \
  bot/ \
  run.py \
  replit.md

# Verify backup
tar -tzf backups/manual_*.tar.gz | head -20
```

### Restore Procedure

1. **Stop Services**
2. **Extract Backup**
   ```bash
   tar -xzf backups/BACKUP_FILE.tar.gz
   ```
3. **Restart Services**
4. **Verify Health**

---

## Performance Optimization

### Database Optimization

```sql
-- Check table sizes
SELECT tablename, pg_size_pretty(pg_total_relation_size(tablename::regclass))
FROM pg_tables WHERE schemaname = 'public';

-- Vacuum analyze
VACUUM ANALYZE;
```

### Log Rotation

```bash
# Archive old logs
find logs/ -name '*.ndjson' -mtime +30 -exec gzip {} \;

# Delete ancient logs
find logs/ -name '*.gz' -mtime +90 -delete
```

### Cache Optimization

```bash
# Check cache hit rate
curl http://localhost:5000/api/regions/status
```

---

## Security Operations

### Weekly Security Scan

```bash
python3 scripts/security_scanner.py
```

**Review:**
- Vulnerability count
- Secret leaks
- SBOM changes

### Access Audit

```bash
# Check audit chain
curl http://localhost:5000/api/audit/chain \
  -H "X-Dash-Key: $DASHBOARD_KEY"

# Verify integrity
python3 -c "from bot.compliance_webhooks import verify_audit_chain; print(verify_audit_chain())"
```

### Token Rotation

**JWT Tokens:**
- Access: 15 min expiry (auto)
- Refresh: 24 hr expiry (auto)
- Blacklist: In-memory (restart clears)

**API Keys:**
- Rotate quarterly
- Update in `.env`
- Restart workflows

---

## Contact & Escalation

### Support Tiers

1. **L1 - Automated**
   - Health checks
   - Auto-healing
   - Self-diagnostics

2. **L2 - Manual**
   - Log review
   - Service restart
   - Configuration changes

3. **L3 - Expert**
   - Database recovery
   - Code changes
   - Architecture updates

### Emergency Contacts

- Telegram: Configured alerts
- Email: SMTP configured
- Status Page: `/api/platform/status`

---

## Appendix

### Useful Commands

```bash
# Platform status
curl http://localhost:5000/api/platform/status

# Phase report
curl http://localhost:5000/api/platform/phase-report -H "X-Dash-Key: $KEY"

# Analytics
curl http://localhost:5000/api/analytics/usage -H "X-Dash-Key: $KEY"

# FinOps summary
curl http://localhost:5000/api/finops/summary -H "X-Dash-Key: $KEY"

# Partner dashboard
curl http://localhost:5000/api/partners/dashboard?partner_id=PTR_XXX -H "X-Dash-Key: $KEY"
```

### Log Locations

- **Application Logs**: `/tmp/logs/EchoPilot_Bot_*.log`
- **Scheduler Logs**: `/tmp/logs/Scheduler_*.log`
- **Analytics**: `logs/analytics.ndjson`
- **Security**: `logs/security_report.json`
- **Audit**: `logs/compliance_hooks.ndjson`

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-21  
**Owner:** EchoPilot Operations Team
