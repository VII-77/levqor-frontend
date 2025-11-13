# Levqor Site - Production Frontend

## Overview
Production-grade Next.js frontend for Levqor workflow automation platform. Deployed to **www.levqor.ai** via Vercel with Cloudflare DDoS protection.

## Production Status
- **Domain**: www.levqor.ai
- **Vercel Project**: levqor-site (prj_0uD8XkWsrf6z7F9DHlUvyfDinas5)
- **Team**: team_brpiJYLXLxoOUdPwhMJ2TJ6e
- **Latest Deployment**: READY and LIVE

## Recent Changes (Nov 12, 2025)
1. Fixed Vercel project confusion - switched from levqor-frontend to levqor-site
2. Promoted latest deployment to production (www.levqor.ai)
3. Deleted 20 old deployments to free Vercel limits (45 remaining, down from 50+)
4. Verified vercel.json ignoreCommand prevents preview deployment spam
5. Confirmed Cloudflare DDoS protection active (blocks curl, protects production)

## Architecture
- **Framework**: Next.js 15.0.3 with App Router
- **Auth**: Auth.js v5 (NextAuth) with GitHub OAuth
- **Payment**: Stripe integration for subscriptions
- **Deployment**: Vercel with automatic GitHub deploys (main branch only)
- **Protection**: Cloudflare proxy for DDoS/rate limiting

## Critical Files
- `src/app/page.tsx` - Homepage with Genesis v8 polish (189 lines)
- `src/app/signin/page.tsx` - Polished OAuth signin
- `src/app/workflow/page.tsx` - Protected workflow dashboard
- `src/middleware.ts` - Auth protection for /workflow routes
- `vercel.json` - Prevents preview deployments except main/tags

## Known Issues

### Git Index Corruption (CRITICAL)
**Status**: BLOCKING Genesis v8 deployment
**Problem**: Git index corrupted - local file has 189 lines (Genesis v8) but git HEAD shows 26 lines (old version). Git diff reports 0 lines changed despite different MD5 checksums.

**Failed Attempts**:
- `git rm --cached` + `git add` - no effect
- `git checkout HEAD` + copy + `git add` - no effect
- Force index rebuild - still shows "Everything up to date"

**Impact**: Cannot commit Genesis v8 homepage improvements to git, therefore cannot deploy to production.

**Workaround Options**:
1. Create new file with different name, delete old, rename back
2. Use git filter-branch or git replace (requires local git, not available in Replit Agent)
3. Clone fresh repo in new directory and copy files
4. Wait for Replit to fix git corruption issue

## Deployment Configuration

### vercel.json
```json
{
  "ignoreCommand": "node -e \"const b=process.env.VERCEL_GIT_COMMIT_REF; const t=process.env.VERCEL_GIT_COMMIT_TAG; process.exit( (b==='main' || t) ? 0 : 1 )\""
}
```
This prevents preview deployments on every commit, only deploys main branch or tagged releases.

### Environment Variables
- `VERCEL_TOKEN` - Deployment API access
- `VERCEL_TEAM_ID` - Team ID for API calls
- Auth.js secrets (managed via Replit Secrets)
- Stripe keys (managed via Replit Secrets)

## Performance Optimizations
- HTML: `cache-control: no-cache` (always fresh)
- Static assets: Long cache-control for JS/CSS bundles
- Cloudflare edge caching for global performance
- Vercel edge functions for auth middleware

## Next Steps
1. **URGENT**: Resolve git index corruption to deploy Genesis v8
2. Continue cleanup: Delete more old deployments if hitting Vercel limits
3. Monitor production for auth redirect issues (middleware may need review)
4. Add more SEO metadata once Genesis v8 deploys
5. Performance monitoring and Core Web Vitals optimization

## User Preferences
- Focus on production stability over flashy features
- Minimize deployment spam to stay within Vercel limits
- Clean, polished UI following Genesis v8 design system
- SEO optimization for organic growth
