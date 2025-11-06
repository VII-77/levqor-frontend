# Levqor Marketing Frontend

Next.js marketing website for Levqor that consumes the Flask backend API.

## Backend Integration

This frontend connects to the Levqor Flask backend at:
- **Production**: https://api.levqor.ai
- **Endpoints**:
  - Marketing data: `/api/v1/marketing/summary`
  - Marketing assets: `/marketing/*.json`
  - Checkout: `/billing/create-checkout-session`

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Run development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
npm run start
```

## Environment Variables

Create `.env.local` with:

```
NEXT_PUBLIC_BACKEND_BASE=https://api.levqor.ai
NEXT_PUBLIC_BACKEND_CHECKOUT=https://api.levqor.ai/billing/create-checkout-session
NEXT_PUBLIC_BACKEND_SUMMARY=https://api.levqor.ai/api/v1/marketing/summary
NEXT_PUBLIC_ASSETS_BASE=https://api.levqor.ai
NEXT_PUBLIC_APP_NAME=Levqor
NEXT_PUBLIC_PLAUSIBLE_DOMAIN=
NEXT_PUBLIC_HEAP_ID=
```

## Deployment

### Vercel (Recommended)

```bash
vercel deploy --prod
```

### Other Platforms

This is a standard Next.js app and can be deployed to any platform that supports Next.js:
- Vercel
- Netlify
- AWS Amplify
- Google Cloud Run
- Docker

## Pages

- `/` - Landing page with hero, USPs, testimonials, and newsletter signup
- `/pricing` - Pricing plans with CTA buttons

## Components

- `CTAButton` - Checkout button that redirects to Stripe
- `USPGrid` - Value propositions grid
- `Testimonials` - Customer testimonials
- `LiveStats` - Real-time platform statistics
- `SubscribeForm` - Newsletter signup form
- `RefCapture` - UTM parameter tracking

## Analytics

Supports optional analytics via environment variables:
- Plausible Analytics (set `NEXT_PUBLIC_PLAUSIBLE_DOMAIN`)
- Heap Analytics (set `NEXT_PUBLIC_HEAP_ID`)
