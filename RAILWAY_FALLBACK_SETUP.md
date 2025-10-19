# Railway Fallback Setup Guide

## Overview

EchoPilot now supports **Railway fallback routing** to work around Replit's GCP Load Balancer proxy limitations that cause certain endpoints to return 404 errors.

### Why Railway Fallback?

Some endpoints (`/supervisor`, `/forecast`, `/metrics`, `/pulse`) return **404 on Replit's public URL** due to infrastructure routing issues, even though they work perfectly when accessed internally. Railway provides stable routing without these proxy issues.

## Features

✅ **Transparent Proxy** - Automatically routes affected endpoints to Railway  
✅ **Zero Code Changes** - Works via environment variables only  
✅ **Dual Deployment** - Keep Replit for automation, Railway for API access  
✅ **Cost Efficient** - Railway's free tier handles low-volume API requests  

## Architecture

```
User → https://echopilotai.replit.app/metrics
         ↓
     (Replit proxy returns 404)
         ↓
     (Edge routing enabled?)
         ↓ YES
     Proxy to → https://your-app.railway.app/metrics
         ↓
     Return result to user
```

## Setup Instructions

### Step 1: Deploy to Railway

1. **Create Railway Account**  
   - Visit: https://railway.app
   - Sign up with GitHub

2. **Create New Project**  
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your EchoPilot repository

3. **Configure Railway**  
   Railway will auto-detect Flask and deploy with Gunicorn.
   
   Ensure these settings:
   ```bash
   Build Command:  (leave empty - Railway auto-detects)
   Start Command:  gunicorn -w 2 -k gthread -t 120 --bind 0.0.0.0:$PORT run:app
   ```

4. **Copy Environment Variables**  
   Add all your Replit secrets to Railway:
   - `AI_INTEGRATIONS_OPENAI_API_KEY`
   - `AI_INTEGRATIONS_OPENAI_BASE_URL`
   - `NOTION_*` database IDs
   - `TELEGRAM_BOT_TOKEN`
   - `STRIPE_SECRET_KEY`
   - All other secrets from Replit

5. **Get Railway URL**  
   After deployment completes:
   - Go to Settings → Domains
   - Copy the generated URL: `https://your-app.railway.app`

### Step 2: Enable Railway Fallback in Replit

Add these two secrets in Replit:

```bash
EDGE_ENABLE=true
EDGE_BASE_URL=https://your-app.railway.app
```

**How to Add Secrets in Replit:**
1. Open Replit project
2. Go to "Tools" → "Secrets" 
3. Add `EDGE_ENABLE` with value `true`
4. Add `EDGE_BASE_URL` with your Railway URL
5. Click "Add secret" for each

### Step 3: Restart Workflow

After adding secrets:
1. Restart the EchoPilot Bot workflow
2. Run test: `bash scripts/test_edge.sh`

You should now see:
```
✓ /supervisor  (HTTP 200)  ← Proxied to Railway
✓ /forecast    (HTTP 200)  ← Proxied to Railway
✓ /metrics     (HTTP 200)  ← Proxied to Railway
✓ /pulse       (HTTP 200)  ← Proxied to Railway
```

## Testing

### Without Railway Fallback (Current State)
```bash
bash scripts/test_edge.sh

# Output:
✓ /health      (HTTP 200)  ← Works on Replit
✗ /supervisor  (HTTP 404)  ← Blocked by Replit proxy
✗ /metrics     (HTTP 404)  ← Blocked by Replit proxy
```

### With Railway Fallback Enabled
```bash
# After adding EDGE_ENABLE and EDGE_BASE_URL:
bash scripts/test_edge.sh

# Output:
✓ /health      (HTTP 200)  ← Replit
✓ /supervisor  (HTTP 200)  ← Railway (proxied)
✓ /metrics     (HTTP 200)  ← Railway (proxied)
```

## Cost Estimates

### Railway Pricing
- **Free Tier**: $5 credit/month (~550 hours)
- **Hobby Plan**: $5/month (500 hours)
- **Low Volume**: Free tier is usually sufficient for API-only access

### Total Monthly Cost
```
Replit Reserved VM:  $10/month (automation + bot)
Railway Free Tier:   $0/month (API access only)
AI (gpt-4o-mini):    $5-15/month (task processing)
─────────────────────────────────
Total:               ~$15-25/month
```

## Affected Endpoints

### ✅ Always Work (No Fallback Needed)
- `GET  /` - Health check
- `GET  /health` - Health status
- `POST /jobs/*` - Job management
- `GET  /api/*` - Alternative API paths (some)

### ⚠️  Require Railway Fallback
- `GET  /supervisor` - System supervisor
- `GET  /forecast` - 30-day forecasts
- `GET  /metrics` - Cross-database metrics
- `POST /pulse` - System pulse reports

## How It Works

### Code Flow

1. **Request arrives** at affected endpoint
2. **Check EDGE_ENABLE** environment variable
3. **If enabled**: Proxy request to Railway URL
4. **If disabled**: Execute locally (may return 404 on Replit)

### Proxy Logic (`run.py`)
```python
def proxy_to_edge(endpoint, method="GET"):
    if not EDGE_ENABLE or not EDGE_BASE_URL:
        return None  # Local execution
    
    # Forward to Railway
    url = f"{EDGE_BASE_URL}/{endpoint}"
    resp = requests.get(url, timeout=10)
    return jsonify(resp.json()), resp.status_code

@app.get("/metrics")
def metrics_route():
    # Try Railway first
    edge_response = proxy_to_edge("metrics", "GET")
    if edge_response:
        return edge_response
    
    # Fallback to local
    return local_metrics()
```

## Troubleshooting

### Railway deployment fails
- Check environment variables are set correctly
- Verify start command uses port `$PORT` (Railway auto-assigns)
- Check Railway logs: Settings → Deployments → View Logs

### Endpoints still return 404
- Verify `EDGE_ENABLE=true` (case-sensitive)
- Verify `EDGE_BASE_URL` has no trailing slash
- Restart Replit workflow after adding secrets
- Test Railway URL directly: `curl https://your-app.railway.app/health`

### Slow response times
- Railway free tier has cold starts (~5-10 seconds)
- Upgrade to Hobby plan for persistent containers
- Consider caching layer (Redis) for production

## Alternative Platforms

If Railway doesn't work for you, these alternatives also have stable routing:

- **Fly.io** - Similar to Railway, generous free tier
- **Render** - Free tier available, great for Flask apps
- **Heroku** - Classic PaaS, paid plans only now
- **DigitalOcean App Platform** - $5/month minimum

All support the same environment variable approach.

## Disable Railway Fallback

To disable and go back to Replit-only:

1. Remove `EDGE_ENABLE` secret (or set to `false`)
2. Remove `EDGE_BASE_URL` secret
3. Restart workflow

Endpoints will return 404 again, but internal automation continues working.

## Production Recommendations

For production use with external API access:

1. ✅ **Use Railway fallback** for reliable API access
2. ✅ **Keep Replit deployment** for automation (works perfectly)
3. ✅ **Monitor both platforms** (Railway for API, Replit for tasks)
4. ✅ **Set up Railway alerts** (webhook monitoring)
5. ✅ **Implement rate limiting** (protect against abuse)

---

**Questions?** Test with `bash scripts/test_edge.sh` to verify your setup!
