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
    monthlyGBP: 149,
    yearlyGBP: 1490,
    workflowsPerMonth: 7,
    monitoring: "Pro monitoring dashboard",
    support: "Priority + tuning",
    features: [
      "Up to 7 workflows per month",
      "Pro monitoring dashboard",
      "Priority support + optimization calls",
      "Advanced self-healing",
      "Performance tuning included"
    ]
  },
  {
    id: "business",
    name: "Business",
    monthlyGBP: 299,
    yearlyGBP: 2990,
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
