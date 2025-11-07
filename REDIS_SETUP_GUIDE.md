# Redis Setup Guide for Levqor Phase-4

## Quick Start: Get Free Redis in 2 Minutes

### Option 1: Upstash (Recommended)

**Why Upstash?**
- Generous free tier (10,000 commands/day)
- Global edge locations (low latency)
- Serverless pricing (pay per use)
- No credit card required

**Steps:**

1. **Sign Up**
   - Go to: https://console.upstash.com
   - Sign up with GitHub or Google

2. **Create Database**
   - Click "Create Database"
   - Select "Global" for worldwide coverage
   - Name it: `levqor-prod` (or any name)
   - Click "Create"

3. **Get Connection URL**
   - Click on your new database
   - Scroll to "REST API" section
   - Find "UPSTASH_REDIS_REST_URL"
   - **OR** look for connection string in format:
     ```
     rediss://default:YOUR_PASSWORD@region.upstash.io:6379
     ```

4. **Copy to Replit**
   - Copy the FULL URL (including `rediss://` prefix)
   - Go to Replit Secrets (lock icon in sidebar)
   - Find `REDIS_URL`
   - Paste the full connection URL
   - Click "Save"

### Option 2: Redis Cloud

**Steps:**

1. **Sign Up**
   - Go to: https://redis.com/try-free
   - Create free account

2. **Create Database**
   - Click "New Subscription"
   - Choose "Free" plan (30MB)
   - Select cloud provider & region
   - Create new database

3. **Get Credentials**
   - Click on your database
   - Go to "Configuration" tab
   - Find "Public endpoint"
   - Note: `redis-12345.c123.us-east-1-1.ec2.cloud.redislabs.com:12345`
   - Find "Default user password"
   - Note the password

4. **Build Connection URL**
   Format: `redis://default:PASSWORD@ENDPOINT`
   
   Example:
   ```
   redis://default:abc123xyz@redis-12345.c123.us-east-1-1.ec2.cloud.redislabs.com:12345
   ```

5. **Add to Replit**
   - Copy the full URL
   - Update `REDIS_URL` in Replit Secrets

## What to Copy

### ✅ Correct Format:
```
redis://default:MyPassword123@redis-12345.upstash.io:6379
```
or with TLS:
```
rediss://default:MyPassword123@redis-12345.upstash.io:6379
```

### ❌ Wrong Format:
```
MyPassword123
```
(Just the password - this won't work!)

## Verification

After updating the secret:

1. **Delete the SENTRY_DSN secret** (you can't access it)
2. **Update REDIS_URL** with full connection URL
3. **Restart backend** (automatic)
4. **Verify it works:**
   ```bash
   python3 scripts/verify_phase4_secrets.py
   curl http://localhost:5000/ops/queue_health
   ```

Expected output:
```json
{"status": "ok", "depth": 0, "fail_rate": 0, ...}
```

## Need Help?

If you're stuck, just share:
1. Which provider you chose (Upstash or Redis Cloud)
2. What the connection string looks like (first 20 chars only)

I'll help you format it correctly!
