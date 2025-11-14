import { NextRequest, NextResponse } from 'next/server';
import Stripe from 'stripe';

export const runtime = 'edge';
export const dynamic = 'force-dynamic';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY as string, {
  apiVersion: '2025-10-29.clover',
});

export async function POST(req: NextRequest) {
  try {
    const raw = await req.text();
    const sig = req.headers.get('stripe-signature') || '';
    const secret = process.env.STRIPE_WEBHOOK_SECRET!;
    let event: Stripe.Event;

    try {
      event = stripe.webhooks.constructEvent(raw, sig, secret);
    } catch (e: any) {
      return new NextResponse(JSON.stringify({ error: 'Invalid signature', detail: e?.message }), { status: 400 });
    }

    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    switch (event.type) {
      case 'invoice.payment_failed':
        await fetch(`${backendUrl}/api/internal/billing/payment-failed`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Internal-Secret': process.env.INTERNAL_API_SECRET || 'dev_secret' },
          body: JSON.stringify({ event: event.data.object })
        });
        break;
        
      case 'invoice.paid':
        await fetch(`${backendUrl}/api/internal/billing/payment-succeeded`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-Internal-Secret': process.env.INTERNAL_API_SECRET || 'dev_secret' },
          body: JSON.stringify({ event: event.data.object })
        });
        break;
        
      case 'checkout.session.completed':
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
      case 'customer.subscription.deleted':
        // TODO: persist to DB or log
        break;
    }
    return NextResponse.json({ ok: true });
  } catch (e: any) {
    console.error('[Stripe Webhook Error]', e);
    return new NextResponse(JSON.stringify({ error: 'handler_failed', detail: e?.message }), { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({ ok: true, route: '/api/stripe/webhook' });
}
