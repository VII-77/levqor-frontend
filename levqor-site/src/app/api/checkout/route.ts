import { NextResponse } from "next/server";
import Stripe from "stripe";

const ENV = {
  SECRET: process.env.STRIPE_SECRET_KEY,
  STARTER_M: process.env.STRIPE_PRICE_STARTER,
  STARTER_Y: process.env.STRIPE_PRICE_STARTER_YEAR,
  PRO_M:     process.env.STRIPE_PRICE_PRO,
  PRO_Y:     process.env.STRIPE_PRICE_PRO_YEAR,
  BIZ_M:     process.env.STRIPE_PRICE_BUSINESS,
  BIZ_Y:     process.env.STRIPE_PRICE_BUSINESS_YEAR,
  ADDON_SUPPORT: process.env.STRIPE_PRICE_ADDON_PRIORITY_SUPPORT,
  ADDON_SLA:     process.env.STRIPE_PRICE_ADDON_SLA_99_9,
  ADDON_WL:      process.env.STRIPE_PRICE_ADDON_WHITE_LABEL
};

const stripe = new Stripe(String(ENV.SECRET || ""), { apiVersion: "2025-10-29.clover" });

function missingEnv(): string[] {
  return Object.entries(ENV)
    .filter(([_, v]) => !v || String(v).trim() === "")
    .map(([k]) => k);
}

export async function GET() {
  const missing = missingEnv();
  const ok = missing.length === 0;
  return NextResponse.json({ ok, missing });
}

type Body = {
  plan: "starter" | "pro" | "business",
  term: "monthly" | "yearly",
  addons?: ("PRIORITY_SUPPORT"|"SLA_99_9"|"WHITE_LABEL")[]
};

export async function POST(req: Request) {
  try {
    const missing = missingEnv();
    if (missing.length) return NextResponse.json({ ok:false, error:`missing_env:${missing.join(",")}` }, { status:500 });

    const { plan, term, addons=[] } = await req.json() as Body;
    const map: Record<string, string> = {
      "starter:monthly": String(ENV.STARTER_M),
      "starter:yearly":  String(ENV.STARTER_Y),
      "pro:monthly":     String(ENV.PRO_M),
      "pro:yearly":      String(ENV.PRO_Y),
      "business:monthly":String(ENV.BIZ_M),
      "business:yearly": String(ENV.BIZ_Y)
    };
    const core = map[`${plan}:${term}`];
    if (!core) return NextResponse.json({ ok:false, error:"invalid_plan_term" }, { status:400 });

    const addonMap: Record<string,string> = {
      "PRIORITY_SUPPORT": String(ENV.ADDON_SUPPORT),
      "SLA_99_9":         String(ENV.ADDON_SLA),
      "WHITE_LABEL":      String(ENV.ADDON_WL)
    };
    const line_items = [{ price: core, quantity: 1 } as {price:string;quantity:number}]
      .concat(addons.map(a => {
        const id = addonMap[a];
        if (!id) throw new Error(`missing_addon_price:${a}`);
        return { price:id, quantity:1 };
      }));

    const session = await stripe.checkout.sessions.create({
      mode: "subscription",
      line_items,
      allow_promotion_codes: true,
      success_url: `${process.env.SITE_URL ?? ""}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.SITE_URL ?? ""}/pricing?canceled=1`
    });

    if (!session.url) return NextResponse.json({ ok:false, error:"no_session_url" }, { status:500 });
    return NextResponse.json({ ok:true, url:session.url });
  } catch (e:any) {
    return NextResponse.json({ ok:false, error:String(e?.message ?? e) }, { status:500 });
  }
}
