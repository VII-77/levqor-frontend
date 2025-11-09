import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, { apiVersion: '2025-10-29.clover' });

const ENV_CHECK = {
  STARTER: !!process.env.STRIPE_PRICE_STARTER,
  STARTER_YEAR: !!process.env.STRIPE_PRICE_STARTER_YEAR,
  PRO: !!process.env.STRIPE_PRICE_PRO,
  PRO_YEAR: !!process.env.STRIPE_PRICE_PRO_YEAR,
  ID_STARTER: !!process.env.STRIPE_PRICE_ID_STARTER,
  ID_PRO: !!process.env.STRIPE_PRICE_ID_PRO,
};

let schemeLogged = false;

function getPriceId(plan: string, term: string): string | null {
  if (!schemeLogged) {
    console.log('[Checkout] Environment variables:', ENV_CHECK);
    schemeLogged = true;
  }

  if (ENV_CHECK.STARTER && ENV_CHECK.PRO) {
    console.log('[Checkout] Using 4-var scheme');
    if (plan === 'starter' && term === 'monthly') return process.env.STRIPE_PRICE_STARTER!;
    if (plan === 'starter' && term === 'yearly') return process.env.STRIPE_PRICE_STARTER_YEAR!;
    if (plan === 'pro' && term === 'monthly') return process.env.STRIPE_PRICE_PRO!;
    if (plan === 'pro' && term === 'yearly') return process.env.STRIPE_PRICE_PRO_YEAR!;
  } else if (ENV_CHECK.ID_STARTER && ENV_CHECK.ID_PRO) {
    console.log('[Checkout] Using 2-var scheme');
    if (plan === 'starter' && term === 'monthly') return process.env.STRIPE_PRICE_ID_STARTER!;
    if (plan === 'pro' && term === 'monthly') return process.env.STRIPE_PRICE_ID_PRO!;
    if (term === 'yearly') {
      return null;
    }
  }

  return null;
}

async function handleCheckout(plan: string, term: string) {
  if (!['starter', 'pro'].includes(plan) || !['monthly', 'yearly'].includes(term)) {
    return NextResponse.json({ error: 'Unknown plan/term' }, { status: 400 });
  }

  const priceId = getPriceId(plan, term);

  if (!priceId) {
    if (term === 'yearly' && !ENV_CHECK.STARTER_YEAR && !ENV_CHECK.PRO_YEAR) {
      return NextResponse.json({ error: 'Yearly plan not configured' }, { status: 400 });
    }
    return NextResponse.json({ error: `Price ID not found for ${plan}/${term}` }, { status: 400 });
  }

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      line_items: [{ price: priceId, quantity: 1 }],
      success_url: `${process.env.SITE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.SITE_URL}/pricing`,
      allow_promotion_codes: true,
      billing_address_collection: 'auto',
      automatic_tax: { enabled: true },
    });

    return NextResponse.json({ url: session.url });
  } catch (e: any) {
    console.error('[Checkout] Stripe error:', e);
    return NextResponse.json({ error: e.message ?? 'checkout_error' }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const plan = (body.plan || '').toLowerCase();
    const term = (body.term || '').toLowerCase();
    return handleCheckout(plan, term);
  } catch (e: any) {
    return NextResponse.json({ error: 'Invalid JSON body' }, { status: 400 });
  }
}

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const plan = (searchParams.get('plan') || '').toLowerCase();
  const term = (searchParams.get('term') || '').toLowerCase();
  return handleCheckout(plan, term);
}
