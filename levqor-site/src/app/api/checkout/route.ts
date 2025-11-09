import { NextResponse } from "next/server";
import Stripe from "stripe";

// Use stable, recent API version
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY as string, { apiVersion: "2025-10-29.clover" });

// Helper: map plan/term to a price id using only static env references
function getPriceId(plan: string, term: string): string | undefined {
  // Newer 4-var scheme
  const S_SM = process.env.STRIPE_PRICE_STARTER;
  const S_SY = process.env.STRIPE_PRICE_STARTER_YEAR;
  const P_PM = process.env.STRIPE_PRICE_PRO;
  const P_PY = process.env.STRIPE_PRICE_PRO_YEAR;

  // Older 2-var scheme (monthly only), optional *_YEAR for yearly if present
  const S_ID_M = process.env.STRIPE_PRICE_ID_STARTER;
  const P_ID_M = process.env.STRIPE_PRICE_ID_PRO;
  const S_ID_Y = process.env.STRIPE_PRICE_ID_STARTER_YEAR;
  const P_ID_Y = process.env.STRIPE_PRICE_ID_PRO_YEAR;

  const key = `${plan}-${term}`; // starter-monthly, starter-yearly, pro-monthly, pro-yearly
  const table: Record<string, string | undefined> = {
    "starter-monthly": S_SM ?? S_ID_M,
    "starter-yearly":  S_SY ?? S_ID_Y,
    "pro-monthly":     P_PM ?? P_ID_M,
    "pro-yearly":      P_PY ?? P_ID_Y,
  };
  return table[key];
}

async function createSession(plan: string, term: string) {
  const price = getPriceId(plan, term);
  if (!price) {
    // Tell exactly what is missing without leaking values
    const msg = `Price ID not found for ${plan}-${term}. Check envs: STRIPE_PRICE_* or STRIPE_PRICE_ID_*`;
    return NextResponse.json({ error: msg }, { status: 400 });
  }
  const site = process.env.SITE_URL || "https://levqor.ai";
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price, quantity: 1 }],
    success_url: `${site}/success`,
    cancel_url: `${site}/pricing`,
  });
  return NextResponse.json({ url: session.url }, { status: 200 });
}

// POST accepts JSON { plan, term }
export async function POST(req: Request) {
  try {
    const { plan, term } = await req.json();
    if (!plan || !term) return NextResponse.json({ error: "Missing plan/term" }, { status: 400 });
    return await createSession(String(plan), String(term));
  } catch (e: any) {
    return NextResponse.json({ error: e?.message ?? "handler_failed" }, { status: 500 });
  }
}

// GET keeps backward compatibility: /api/checkout?plan=starter&term=monthly
export async function GET(req: Request) {
  const u = new URL(req.url);
  const plan = u.searchParams.get("plan");
  const term = u.searchParams.get("term");
  if (!plan || !term) return NextResponse.json({ error: "Missing plan/term" }, { status: 400 });
  return await createSession(plan, term);
}
