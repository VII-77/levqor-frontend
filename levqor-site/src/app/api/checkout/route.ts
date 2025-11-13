import { NextResponse } from "next/server";
import Stripe from "stripe";
import { STRIPE_DFY_PRICE_IDS, STRIPE_SUB_PRICE_IDS } from "@/config/pricing";

export const dynamic = "force-dynamic";

function readEnv() {
  return {
    SECRET: process.env.STRIPE_SECRET_KEY,
    SITE_URL: process.env.SITE_URL || process.env.NEXT_PUBLIC_SITE_URL || "https://www.levqor.ai",
    
    STARTER_M: process.env.STRIPE_PRICE_STARTER,
    STARTER_Y: process.env.STRIPE_PRICE_STARTER_YEAR,
    GROWTH_M: process.env.STRIPE_PRICE_GROWTH,
    GROWTH_Y: process.env.STRIPE_PRICE_GROWTH_YEAR,
    PRO_M: process.env.STRIPE_PRICE_PRO,
    PRO_Y: process.env.STRIPE_PRICE_PRO_YEAR,
    BIZ_M: process.env.STRIPE_PRICE_BUSINESS,
    BIZ_Y: process.env.STRIPE_PRICE_BUSINESS_YEAR,
    
    DFY_STARTER: process.env.STRIPE_PRICE_DFY_STARTER,
    DFY_PROFESSIONAL: process.env.STRIPE_PRICE_DFY_PROFESSIONAL,
    DFY_ENTERPRISE: process.env.STRIPE_PRICE_DFY_ENTERPRISE,
    
    ADDON_SUPPORT: process.env.STRIPE_PRICE_ADDON_PRIORITY_SUPPORT,
    ADDON_SLA: process.env.STRIPE_PRICE_ADDON_SLA_99_9,
    ADDON_WL: process.env.STRIPE_PRICE_ADDON_WHITE_LABEL,
  };
}

function missingEnv(e: ReturnType<typeof readEnv>) {
  return Object.entries(e).filter(([_k, v]) => !v || String(v).trim() === "").map(([k]) => k);
}

function stripeClient(secret?: string) {
  if (!secret) throw new Error("missing STRIPE_SECRET_KEY");
  return new Stripe(secret, { apiVersion: "2024-06-20" as any });
}

export async function GET() {
  const env = readEnv();
  const missing = missingEnv(env);
  return NextResponse.json({ 
    ok: missing.length === 0, 
    missing,
    dfyConfigured: !!(env.DFY_STARTER && env.DFY_PROFESSIONAL && env.DFY_ENTERPRISE),
    subscriptionConfigured: !!(env.STARTER_M && env.PRO_M && env.BIZ_M)
  });
}

type SubscriptionBody = {
  mode: "subscription";
  plan: "starter" | "growth" | "pro" | "business";
  term: "monthly" | "yearly";
  addons?: ("PRIORITY_SUPPORT" | "SLA_99_9" | "WHITE_LABEL")[];
};

type DFYBody = {
  mode: "dfy";
  plan: "starter" | "professional" | "enterprise";
};

type CheckoutBody = SubscriptionBody | DFYBody;

export async function POST(req: Request) {
  try {
    const env = readEnv();
    const body = await req.json() as CheckoutBody;

    console.log("[checkout] Request:", { mode: body.mode, plan: body.plan, term: "term" in body ? body.term : "n/a" });

    if (!body || !body.mode || !body.plan) {
      return NextResponse.json(
        { ok: false, error: "Missing required fields: mode and plan" },
        { status: 400 }
      );
    }

    const stripe = stripeClient(env.SECRET);
    let sessionConfig: Stripe.Checkout.SessionCreateParams;

    if (body.mode === "dfy") {
      const dfyMap: Record<string, string | undefined> = {
        "starter": env.DFY_STARTER,
        "professional": env.DFY_PROFESSIONAL,
        "enterprise": env.DFY_ENTERPRISE,
      };

      const priceId = dfyMap[body.plan];
      if (!priceId) {
        console.error("[checkout] DFY price not configured for plan:", body.plan);
        return NextResponse.json(
          { 
            ok: false, 
            error: `DFY pricing not yet configured for ${body.plan}. Please contact support@levqor.ai` 
          },
          { status: 500 }
        );
      }

      console.log("[checkout] DFY checkout:", { plan: body.plan, priceId: priceId.substring(0, 15) + "..." });

      sessionConfig = {
        mode: "payment",
        line_items: [{ price: priceId, quantity: 1 }],
        allow_promotion_codes: true,
        success_url: `${env.SITE_URL}/success?session_id={CHECKOUT_SESSION_ID}&type=dfy&plan=${body.plan}`,
        cancel_url: `${env.SITE_URL}/cancel?type=dfy&plan=${body.plan}`,
      };

    } else if (body.mode === "subscription") {
      if (!("term" in body) || !body.term) {
        return NextResponse.json(
          { ok: false, error: "Missing required field: term (monthly or yearly)" },
          { status: 400 }
        );
      }

      const subMap: Record<string, string | undefined> = {
        "starter:monthly": env.STARTER_M,
        "starter:yearly": env.STARTER_Y,
        "growth:monthly": env.GROWTH_M,
        "growth:yearly": env.GROWTH_Y,
        "pro:monthly": env.PRO_M,
        "pro:yearly": env.PRO_Y,
        "business:monthly": env.BIZ_M,
        "business:yearly": env.BIZ_Y,
      };

      const core = subMap[`${body.plan}:${body.term}`];
      if (!core) {
        console.error("[checkout] Subscription price not configured:", { plan: body.plan, term: body.term });
        return NextResponse.json(
          { ok: false, error: `Subscription pricing not configured for ${body.plan} ${body.term}` },
          { status: 500 }
        );
      }

      console.log("[checkout] Subscription checkout:", { 
        plan: body.plan, 
        term: body.term, 
        priceId: core.substring(0, 15) + "..." 
      });

      const addonMap: Record<string, string> = {
        "PRIORITY_SUPPORT": String(env.ADDON_SUPPORT || ""),
        "SLA_99_9": String(env.ADDON_SLA || ""),
        "WHITE_LABEL": String(env.ADDON_WL || ""),
      };

      const line_items = [{ price: core, quantity: 1 }];
      
      if (body.addons && body.addons.length > 0) {
        for (const addon of body.addons) {
          const id = addonMap[addon];
          if (!id) {
            console.warn("[checkout] Addon not configured:", addon);
            continue;
          }
          line_items.push({ price: id, quantity: 1 });
        }
      }

      sessionConfig = {
        mode: "subscription",
        line_items,
        allow_promotion_codes: true,
        success_url: `${env.SITE_URL}/success?session_id={CHECKOUT_SESSION_ID}&type=subscription&plan=${body.plan}&term=${body.term}`,
        cancel_url: `${env.SITE_URL}/cancel?type=subscription&plan=${body.plan}&term=${body.term}`,
      };

    } else {
      return NextResponse.json(
        { ok: false, error: "Invalid mode. Must be 'dfy' or 'subscription'" },
        { status: 400 }
      );
    }

    const session = await stripe.checkout.sessions.create(sessionConfig);

    if (!session.url) {
      console.error("[checkout] No session URL returned from Stripe");
      return NextResponse.json(
        { ok: false, error: "Failed to create checkout session" },
        { status: 500 }
      );
    }

    console.log("[checkout] Success! Session created:", session.id);
    return NextResponse.json({ ok: true, url: session.url });

  } catch (err: any) {
    console.error("[checkout] Error:", {
      message: err?.message,
      type: err?.type,
      code: err?.code,
      param: err?.param,
      statusCode: err?.statusCode,
      stack: err?.stack?.substring(0, 500)
    });

    const errorDetails = `${err?.type || "unknown"}: ${err?.message || err}`;
    return NextResponse.json(
      { 
        ok: false, 
        error: errorDetails, 
        debug: { code: err?.code, param: err?.param } 
      },
      { status: 500 }
    );
  }
}
