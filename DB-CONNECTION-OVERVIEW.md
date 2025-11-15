# Database Connection Overview
**Generated:** 2025-11-15 21:35 UTC

## Configuration Summary

**Connection Method:** Flask-SQLAlchemy (ORM)  
**Environment Variable:** `DATABASE_URL`  
**Fallback:** SQLite (`levqor.db`) if DATABASE_URL not set

## Current Settings

**Database URL Pattern:**
```
postgresql://neondb_owner:npg_...@ep-pati...
```

**SQLAlchemy Configuration (`run.py` lines 54-56):**
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', f'sqlite:///{DB_PATH}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
```

## What's Missing

**No explicit configuration for:**
- SSL mode (defaults to Neon's requirement)
- Connection pool size
- Connection pool timeout
- Connection pool pre-ping
- Max overflow connections
- Pool recycle time

## Implication for Webhooks

**Current behavior:**
- Flask-SQLAlchemy creates default connection pool (size ~5)
- No pre-ping to detect stale connections
- No automatic retry on connection failure
- SSL connections required by Neon (implicit)

**Observed Issue:**
```
psycopg2.OperationalError: SSL connection has been closed unexpectedly
```

This suggests the connection pool may be serving stale connections or Neon is dropping idle connections.

## Recommended Improvements (After Stability Test)

If DB proves FLAKY:

1. **Enable connection pre-ping:**
```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # Test connections before using
    'pool_recycle': 3600,   # Recycle connections after 1 hour
}
```

2. **Add webhook-specific retry logic:**
```python
from sqlalchemy.exc import OperationalError
import time

def commit_with_retry(session, max_retries=3, delay=1):
    for attempt in range(max_retries):
        try:
            session.commit()
            return True
        except OperationalError:
            session.rollback()
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise
```

If DB proves STABLE:
- Keep current config
- Monitor webhook success rate in production
- Add retry logic only if production shows failures
