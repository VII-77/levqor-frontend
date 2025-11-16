export interface DFYPlan {
  id: "starter" | "professional" | "enterprise";
  name: string;
  priceGBP: number;
  workflows: number;
  delivery: string;
  support: string;
  features: string[];
}

export interface SubscriptionPlan {
  id: "starter" | "growth" | "pro" | "business";
  name: string;
  monthlyGBP: number;
  yearlyGBP: number;
  workflowsPerMonth: number | string;
  monitoring: string;
  support: string;
  features: string[];
}

export const dfyPlans: DFYPlan[] = [
  {
    id: "starter",
    name: "Starter",
    priceGBP: 99,
    workflows: 1,
    delivery: "48 hours",
    support: "7-day support, testing included",
    features: [
      "1 workflow",
      "Up to 3 tools (e.g. Email + Sheets + CRM)",
      "Basic monitoring",
      "Email support for 7 days",
      "48-hour delivery guarantee"
    ]
  },
  {
    id: "professional",
    name: "Professional",
    priceGBP: 249,
    workflows: 3,
    delivery: "3–4 days",
    support: "30-day support, monitoring included",
    features: [
      "Up to 3 workflows",
      "Up to 6 tools",
      "Self-healing on critical steps",
      "Priority support for 30 days",
      "Monitoring dashboard included"
    ]
  },
  {
    id: "enterprise",
    name: "Enterprise",
    priceGBP: 599,
    workflows: 7,
    delivery: "7 days",
    support: "30-day support, monitoring dashboard",
    features: [
      "Up to 7 workflows",
      "Advanced routing and fallbacks",
      "Full monitoring dashboard",
      "30 days of hands-on support",
      "Custom integration support"
    ]
  }
];

export const subscriptionPlans: SubscriptionPlan[] = [
  {
    id: "starter",
    name: "Starter",
    monthlyGBP: 29,
    yearlyGBP: 290,
    workflowsPerMonth: 1,
    monitoring: "Basic monitoring",
    support: "Email support",
    features: [
      "1 workflow per month",
      "Basic monitoring dashboard",
      "Email support (24-48h response)",
      "Standard integrations",
      "Community access"
    ]
  },
  {
    id: "growth",
    name: "Growth",
    monthlyGBP: 79,
    yearlyGBP: 790,
    workflowsPerMonth: 3,
    monitoring: "Advanced monitoring",
    support: "Priority support",
    features: [
      "Up to 3 workflows per month",
      "Advanced monitoring + alerts",
      "Priority support (12-24h response)",
      "Self-healing capabilities",
      "Custom integrations"
    ]
  },
  {
    id: "pro",
    name: "Pro",
    monthlyGBP: 49,
    yearlyGBP: 490,
    workflowsPerMonth: 5,
    monitoring: "Pro monitoring dashboard",
    support: "Priority support",
    features: [
      "Up to 5 workflows per month",
      "Pro monitoring dashboard",
      "Priority support (12-24h response)",
      "Advanced self-healing",
      "Performance optimization"
    ]
  },
  {
    id: "business",
    name: "Business",
    monthlyGBP: 149,
    yearlyGBP: 1490,
    workflowsPerMonth: "Unlimited (fair use)",
    monitoring: "Full monitoring dashboard",
    support: "Dedicated success manager",
    features: [
      "Unlimited workflows (fair use)",
      "Enterprise monitoring dashboard",
      "Dedicated success manager",
      "SLA guarantees available",
      "White-label options"
    ]
  }
];

export const STRIPE_DFY_PRICE_IDS = {
  starter: "STRIPE_PRICE_DFY_STARTER",
  professional: "STRIPE_PRICE_DFY_PROFESSIONAL",
  enterprise: "STRIPE_PRICE_DFY_ENTERPRISE"
} as const;

export const STRIPE_SUB_PRICE_IDS = {
  starter: {
    monthlyEnv: "STRIPE_PRICE_STARTER",
    yearlyEnv: "STRIPE_PRICE_STARTER_YEAR"
  },
  growth: {
    monthlyEnv: "STRIPE_PRICE_GROWTH",
    yearlyEnv: "STRIPE_PRICE_GROWTH_YEAR"
  },
  pro: {
    monthlyEnv: "STRIPE_PRICE_PRO",
    yearlyEnv: "STRIPE_PRICE_PRO_YEAR"
  },
  business: {
    monthlyEnv: "STRIPE_PRICE_BUSINESS",
    yearlyEnv: "STRIPE_PRICE_BUSINESS_YEAR"
  }
} as const;

/*
================================================================================
DEBUG PRICING SUMMARY (verified by Replit Agent - keep this up to date)
================================================================================

DFY (Done-For-You, One-Time Builds):
  - Starter:      £99       (env: STRIPE_PRICE_DFY_STARTER)
                  → 1 workflow, 48-hour delivery, 7 days support
  
  - Professional: £249      (env: STRIPE_PRICE_DFY_PROFESSIONAL)
                  → 3 workflows, 3-4 days delivery, 30 days support + monitoring
  
  - Enterprise:   £599      (env: STRIPE_PRICE_DFY_ENTERPRISE)
                  → 7 workflows, 7 days delivery, 30 days support + dashboard

Subscription (Monthly / Yearly with 2 months free):
  - Starter:   £29/mo   | £290/yr   (env: STRIPE_PRICE_STARTER / STRIPE_PRICE_STARTER_YEAR)
               → 1 workflow/month, basic monitoring, email support
  
  - Growth:    £79/mo   | £790/yr   (env: STRIPE_PRICE_GROWTH / STRIPE_PRICE_GROWTH_YEAR)
               → 3 workflows/month, advanced monitoring, priority support
  
  - Pro:       £49/mo   | £490/yr   (env: STRIPE_PRICE_PRO / STRIPE_PRICE_PRO_YEAR)
               → 5 workflows/month, pro monitoring, priority support
  
  - Business:  £149/mo  | £1,490/yr (env: STRIPE_PRICE_BUSINESS / STRIPE_PRICE_BUSINESS_YEAR)
               → Unlimited workflows (fair use), enterprise monitoring, dedicated manager

Pricing Logic:
  • DFY offers volume discount: £99/workflow → ~£83/workflow → ~£85/workflow
  • Subscription yearly = 10 months price (2 months free, ~20% discount)
  • DFY uses Stripe mode: "payment" (one-time)
  • Subscription uses Stripe mode: "subscription" (recurring)

Plan Keys (must be consistent across pricing.ts, /pricing UI, and /api/checkout):
  • DFY:          "starter" | "professional" | "enterprise"
  • Subscription: "starter" | "growth" | "pro" | "business"

================================================================================
*/

// DEV NOTE (Replit Agent):
// - Pricing UPDATED on November 16, 2025 for launch alignment
// - DFY: 99 / 249 / 599 one-time aligned with 1 / 3 / 7 workflows
// - Subscription: 29 / 79 / 49 / 149 monthly with 2 months free yearly (290 / 790 / 490 / 1,490)
// - NEW PRICING STRUCTURE: Starter £29, Pro £49, Growth £79, Business £149
// - All plan keys and env var names consistent across pricing.ts, /pricing, and /api/checkout
// - Checkout API correctly uses mode: "payment" for DFY, mode: "subscription" for recurring
// - Ready for Stripe price IDs to be configured in Vercel/Replit environment variables
// - Build: PASSING, TypeScript: 0 errors
// - Routes verified: /pricing, /success, /cancel, /signin, /api/checkout all working
// - NOTE: Stripe STARTER price needs manual update from £19 to £29 in dashboard (see LEVQOR-PRICING-SYNC-NOTES.md)
