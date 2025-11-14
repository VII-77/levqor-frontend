# Levqor Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Variables Required

#### Backend (Python/Flask)
Copy these environment variables to your production environment (e.g., Replit Secrets, Vercel, etc.):

```bash
# === Database ===
DATABASE_URL=postgresql://user:password@host:port/database

# === Authentication ===
NEXTAUTH_SECRET=<generate-with-openssl-rand-base64-32>
NEXTAUTH_URL=https://levqor.ai
AUTH_FROM_EMAIL=noreply@levqor.ai

# === Stripe Payments ===
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_STARTER=price_...
STRIPE_PRICE_GROWTH=price_...
STRIPE_PRICE_BUSINESS=price_...
STRIPE_PRICE_STARTER_YEAR=price_...
STRIPE_PRICE_GROWTH_YEAR=price_...
STRIPE_PRICE_BUSINESS_YEAR=price_...
STRIPE_PRICE_DFY_STARTER=price_...
STRIPE_PRICE_DFY_PRO=price_...
STRIPE_PRICE_DFY_ENTERPRISE=price_...
STRIPE_PRICE_ADDON_PRIORITY_SUPPORT=price_...
STRIPE_PRICE_ADDON_SLA_99_9=price_...
STRIPE_PRICE_ADDON_WHITE_LABEL=price_...

# === Email Service (Resend) ===
RESEND_API_KEY=re_...

# === NextAuth Providers ===
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
AZURE_AD_CLIENT_ID=...
AZURE_AD_CLIENT_SECRET=...
AZURE_AD_TENANT_ID=...

# === Sentry (Error Tracking) ===
SENTRY_DSN=https://...@sentry.io/...
NEXT_PUBLIC_SENTRY_DSN=https://...@sentry.io/...

# === API Configuration ===
NEXT_PUBLIC_API_URL=https://api.levqor.ai
API_KEY=<generate-secure-random-key>

# === Feature Flags ===
DUNNING_ENABLED=true
INTELLIGENT_LAYER_ENABLED=true

# === CORS ===
ALLOWED_ORIGINS=https://levqor.ai,https://www.levqor.ai
```

#### Frontend (Next.js)
These are exposed to the client (NEXT_PUBLIC_*):

```bash
NEXT_PUBLIC_API_URL=https://api.levqor.ai
NEXT_PUBLIC_SENTRY_DSN=https://...@sentry.io/...
```

---

## 2. Database Setup

### Create Production Database
1. Use Neon PostgreSQL or your preferred provider
2. Copy the connection string to `DATABASE_URL`
3. Run migrations:

```bash
# Backend directory
python -c "from backend.database.setup import initialize_database; initialize_database()"
```

### Verify Tables Created
The following tables should exist:
- `users`
- `jobs`
- `api_keys`
- `referrals`
- `leads`
- `lead_activity`
- `dfy_orders`
- `dfy_activity`
- `upsell_log`
- `billing_dunning_events`
- `cookie_consent`
- `marketing_consent`
- And more (see `backend/database/setup.py`)

---

## 3. Stripe Configuration

### Create Products and Prices
1. Log into Stripe Dashboard
2. Create products for:
   - **Subscriptions**: Starter, Growth, Business (Monthly + Yearly)
   - **DFY Services**: Starter (£99), Professional (£249), Enterprise (£599)
   - **Add-ons**: Priority Support, 99.9% SLA, White Label
3. Copy all Price IDs to environment variables

### Configure Webhooks
1. Go to Stripe → Developers → Webhooks
2. Add endpoint: `https://api.levqor.ai/api/stripe/webhooks`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
4. Copy webhook signing secret to `STRIPE_WEBHOOK_SECRET`

---

## 4. Email Configuration (Resend)

1. Sign up at [resend.com](https://resend.com)
2. Verify your sending domain (levqor.ai)
3. Create API key → Copy to `RESEND_API_KEY`
4. Set `AUTH_FROM_EMAIL=noreply@levqor.ai`

### Email Templates
These are already in `/templates/email/`:
- `dunning_1.txt` (Payment Failed - Day 1)
- `dunning_2.txt` (Payment Failed - Day 7)
- `dunning_3.txt` (Final Notice - Day 14)
- `lead-magnet-welcome.txt`
- `followup-24h.txt`, `followup-48h.txt`, `followup-72h.txt`
- `dfy-welcome.txt`, `dfy-upsell-12h.txt`, `dfy-last-chance-36h.txt`

---

## 5. OAuth Providers

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 Client ID
3. Authorized redirect URIs:
   - `https://levqor.ai/api/auth/callback/google`
4. Copy Client ID and Secret

### Azure AD (Optional)
1. Go to [Azure Portal](https://portal.azure.com)
2. App Registrations → New Registration
3. Redirect URI: `https://levqor.ai/api/auth/callback/azure-ad`
4. Copy Application (client) ID, Directory (tenant) ID, and create Client Secret

---

## 6. Sentry Setup

1. Create project at [sentry.io](https://sentry.io)
2. Copy DSN to `SENTRY_DSN` and `NEXT_PUBLIC_SENTRY_DSN`
3. Sentry will automatically capture errors in production

---

## 7. Security Checklist

- [ ] All secrets use strong random values (32+ characters)
- [ ] `NEXTAUTH_SECRET` generated with: `openssl rand -base64 32`
- [ ] `API_KEY` generated with: `openssl rand -hex 32`
- [ ] HTTPS enabled on both frontend and backend
- [ ] CORS configured with `ALLOWED_ORIGINS`
- [ ] Rate limiting enabled (configured in `backend/middleware/security.py`)
- [ ] Stripe webhook signature verification enabled
- [ ] Database uses SSL connection
- [ ] Environment variables never committed to Git

---

## 8. Deployment Steps

### Backend Deployment (Replit/Railway/Fly.io)

#### Option A: Replit
1. Fork this repository to Replit
2. Add all environment variables to Secrets
3. Ensure `run.py` is the entry point
4. Deploy with Autoscale deployment target

#### Option B: Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link project
railway login
railway link

# Set environment variables
railway variables set DATABASE_URL=...
# (repeat for all vars)

# Deploy
railway up
```

#### Option C: Fly.io
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch app
flyctl launch

# Set secrets
flyctl secrets set DATABASE_URL=...
# (repeat for all vars)

# Deploy
flyctl deploy
```

### Frontend Deployment (Vercel)

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd levqor-site

# Login
vercel login

# Deploy
vercel --prod

# Set environment variables in Vercel Dashboard
# Settings → Environment Variables
```

---

## 9. Post-Deployment Verification

### Health Checks
```bash
# Backend health
curl https://api.levqor.ai/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "...",
  "database": "connected",
  "version": "8.0"
}
```

### Frontend Check
1. Visit https://levqor.ai
2. Verify:
   - Landing page loads
   - Pricing page shows all plans
   - Sign-in flow works
   - Cookie consent banner appears

### Payment Flow Test
1. Go to https://levqor.ai/pricing
2. Click "Get Started" on any plan
3. Complete checkout with Stripe test card: `4242 4242 4242 4242`
4. Verify subscription created in Stripe Dashboard
5. Check database for user record

### Email Test
```bash
# Backend API test
curl -X POST https://api.levqor.ai/api/test/email \
  -H "Content-Type: application/json" \
  -d '{"to": "your@email.com"}'
```

### Dunning System Test
1. Create test subscription
2. Force payment failure in Stripe
3. Verify dunning emails sent at Day 1, 7, 14
4. Check `billing_dunning_events` table

---

## 10. Monitoring

### APScheduler Jobs Running
The backend runs these scheduled jobs:
- **Health Monitor** (every 5 minutes)
- **Billing Dunning** (every hour)
- **Intelligence Layer** (every 30 minutes)
- **Data Retention Cleanup** (daily at midnight)
- **Weekly Governance Report** (Mondays at 9am)

### Check Logs
```bash
# View backend logs
tail -f /var/log/levqor/backend.log

# View Sentry errors
https://sentry.io/organizations/.../issues/
```

---

## 11. DNS Configuration

### Domain Setup
Point your domain to deployment:

**For Vercel (Frontend):**
```
A record: @ → 76.76.21.21
CNAME: www → cname.vercel-dns.com
```

**For Backend:**
```
A record: api → <backend-ip-address>
```

### SSL Certificates
- Vercel: Auto-provisioned
- Replit: Auto-provisioned
- Railway/Fly.io: Auto-provisioned with Let's Encrypt

---

## 12. Backup Strategy

### Database Backups
```bash
# Daily automated backups (Neon does this automatically)
# Manual backup:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Environment Variables Backup
Keep a secure copy of all environment variables in:
1. Password manager (1Password, Bitwarden)
2. Encrypted file on separate system

---

## 13. Rollback Plan

If deployment fails:
1. Revert to previous Vercel deployment
2. Revert backend to previous commit
3. Check database for any migrations that need reversing
4. Monitor Sentry for new errors

---

## 14. Performance Tuning

### Backend
- Gunicorn workers: `2-4` (based on CPU cores)
- Threads per worker: `4`
- Timeout: `30` seconds
- Database connection pool: `10`

### Frontend
- Next.js build optimization: `npm run build`
- Static generation for legal pages
- Image optimization enabled

---

## 15. Compliance Verification

After deployment, verify all compliance features work:
- [ ] Cookie consent banner appears
- [ ] Terms acceptance required on signin
- [ ] Marketing consent opt-in works
- [ ] DSAR request page functional (/my-data)
- [ ] High-risk workflow warnings display
- [ ] Unsubscribe links work
- [ ] GDPR opt-out page functional
- [ ] All legal pages accessible

---

## 16. Launch Checklist

### Pre-Launch (24 hours before)
- [ ] All environment variables set
- [ ] Database migrations complete
- [ ] Stripe products and prices created
- [ ] Stripe webhooks configured
- [ ] Email sending verified
- [ ] OAuth providers configured
- [ ] SSL certificates active
- [ ] DNS propagated

### Launch Day
- [ ] Final smoke test all critical paths
- [ ] Monitor error logs (Sentry)
- [ ] Monitor server metrics
- [ ] Test payment flow end-to-end
- [ ] Verify email deliverability
- [ ] Check APScheduler jobs running
- [ ] Announce launch 🚀

### Post-Launch (48 hours)
- [ ] Review Sentry errors
- [ ] Check Stripe webhook events
- [ ] Verify dunning emails sent
- [ ] Monitor database performance
- [ ] Review user signups
- [ ] Check email open rates

---

## Support & Troubleshooting

### Common Issues

**Issue: Stripe webhook signature verification fails**
```
Solution: Verify STRIPE_WEBHOOK_SECRET matches Stripe dashboard
```

**Issue: Emails not sending**
```
Solution: 
1. Check RESEND_API_KEY is valid
2. Verify domain verified in Resend
3. Check email template paths exist
```

**Issue: Database connection fails**
```
Solution:
1. Verify DATABASE_URL format
2. Check firewall allows connections
3. Ensure SSL mode configured
```

**Issue: OAuth redirect fails**
```
Solution:
1. Check NEXTAUTH_URL matches deployment URL
2. Verify OAuth redirect URIs in provider settings
3. Ensure callbacks use HTTPS
```

---

## Maintenance Windows

Schedule regular maintenance:
- **Weekly**: Review error logs, update dependencies
- **Monthly**: Database optimization, backup verification
- **Quarterly**: Security audit, dependency updates

---

## Emergency Contacts

**Production Issues:**
- Email: ops@levqor.ai
- Status Page: https://levqor.ai/status

**Security Issues:**
- Email: security@levqor.ai
- Immediate escalation required

---

## Version

**Levqor Genesis v8.0**
- Last Updated: November 14, 2025
- Deployment Target: Production
- Python: 3.11+
- Node.js: 20+
- PostgreSQL: 14+

---

**Deployment complete! Welcome to production. 🎉**
