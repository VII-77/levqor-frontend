"use client";
import Link from "next/link";
import { useState } from "react";
import { dfyPlans, subscriptionPlans } from "@/config/pricing";
import HighRiskWarning from "@/components/HighRiskWarning";

type Plan = "starter" | "professional" | "enterprise" | "growth" | "pro" | "business";
type Mode = "dfy" | "subscription";
type Term = "monthly" | "yearly";

export default function Pricing() {
  const [loading, setLoading] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [subscriptionTerm, setSubscriptionTerm] = useState<Term>("monthly");

  const handleCheckout = async (params: { mode: Mode; plan: Plan; term?: Term }) => {
    const { mode, plan, term } = params;
    const loadingKey = `${mode}-${plan}-${term || ""}`;
    setLoading(loadingKey);
    setError(null);

    try {
      const body = mode === "dfy" 
        ? { mode, plan }
        : { mode, plan, term };

      const response = await fetch("/api/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      const data = await response.json();

      if (data.ok && data.url) {
        window.location.href = data.url;
      } else {
        setError(data.error || "Checkout failed. Please try again or contact support.");
        setLoading(null);
      }
    } catch (err) {
      console.error("Checkout error:", err);
      setError("Failed to start checkout. Please try again or contact support@levqor.ai");
      setLoading(null);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">
            Levqor
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/" className="text-sm text-slate-300 hover:text-white transition">
              Home
            </Link>
            <Link href="/signin" className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
              Sign in
            </Link>
          </div>
        </nav>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-16">
        {/* Error Display */}
        {error && (
          <div className="max-w-3xl mx-auto mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
            {error}
          </div>
        )}

        {/* High-Risk Warning */}
        <div className="max-w-4xl mx-auto mb-8">
          <HighRiskWarning />
        </div>

        {/* Page Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Choose your path
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Pricing that works for you
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            One-time builds or ongoing automation? Monthly or yearly? Pick the plan that fits your workflow.
          </p>
        </div>

        {/* SECTION 1: Done-For-You (One-Time) */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-white">Done-for-you builds</h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              We build it. You use it. Fixed price, delivered in days.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {dfyPlans.map((plan, idx) => (
              <div
                key={plan.id}
                className={`rounded-2xl bg-slate-900/50 border p-8 hover:border-emerald-400/50 transition-all ${
                  idx === 1 ? "border-2 border-emerald-500/50 relative" : "border-slate-800"
                }`}
              >
                {idx === 1 && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                    <span className="bg-emerald-500 text-slate-900 px-4 py-1 rounded-full text-xs font-bold uppercase">
                      Most popular
                    </span>
                  </div>
                )}

                <div className="mb-6">
                  <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                  <div className="flex items-baseline gap-1 mb-4">
                    <span className="text-5xl font-bold text-white">£{plan.priceGBP}</span>
                    <span className="text-slate-400 text-sm">one-time</span>
                  </div>
                  <p className="text-slate-400 text-sm mb-2">
                    {plan.workflows} workflow{plan.workflows > 1 ? "s" : ""} • {plan.delivery}
                  </p>
                  <p className="text-slate-300 text-sm">{plan.support}</p>
                </div>

                <ul className="space-y-3 mb-8 text-sm text-slate-300">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  onClick={() => handleCheckout({ mode: "dfy", plan: plan.id })}
                  disabled={loading !== null}
                  className={`block w-full py-3 px-4 rounded-lg font-semibold text-center transition disabled:opacity-50 disabled:cursor-not-allowed ${
                    idx === 1
                      ? "bg-emerald-500 hover:bg-emerald-400 text-slate-900 shadow-lg"
                      : "bg-slate-800 hover:bg-slate-700 text-white"
                  }`}
                >
                  {loading === `dfy-${plan.id}-` ? "Loading..." : `Get ${plan.name} DFY`}
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* SECTION 2: Ongoing Subscriptions */}
        <section>
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-white">Ongoing automation plans</h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto mb-6">
              Continuous workflow creation, monitoring, and support. Cancel anytime.
            </p>

            {/* Monthly / Yearly Toggle */}
            <div className="inline-flex items-center gap-2 p-1 bg-slate-900 border border-slate-800 rounded-lg">
              <button
                onClick={() => setSubscriptionTerm("monthly")}
                className={`px-6 py-2 rounded-md font-semibold text-sm transition ${
                  subscriptionTerm === "monthly"
                    ? "bg-emerald-500 text-slate-900"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Monthly
              </button>
              <button
                onClick={() => setSubscriptionTerm("yearly")}
                className={`px-6 py-2 rounded-md font-semibold text-sm transition ${
                  subscriptionTerm === "yearly"
                    ? "bg-emerald-500 text-slate-900"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Yearly
                <span className="ml-2 text-xs opacity-80">(save ~20%)</span>
              </button>
            </div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
            {subscriptionPlans.map((plan, idx) => (
              <div
                key={plan.id}
                className={`rounded-2xl bg-slate-900/50 border p-6 hover:border-emerald-400/50 transition-all ${
                  idx === 2 ? "border-2 border-emerald-500/50 relative" : "border-slate-800"
                }`}
              >
                {idx === 2 && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                    <span className="bg-emerald-500 text-slate-900 px-3 py-1 rounded-full text-xs font-bold uppercase">
                      Best value
                    </span>
                  </div>
                )}

                <div className="mb-6">
                  <h3 className="text-xl font-bold text-white mb-2">{plan.name}</h3>
                  <div className="flex items-baseline gap-1 mb-4">
                    <span className="text-4xl font-bold text-white">
                      £{subscriptionTerm === "monthly" ? plan.monthlyGBP : plan.yearlyGBP}
                    </span>
                    <span className="text-slate-400 text-sm">/{subscriptionTerm === "monthly" ? "mo" : "yr"}</span>
                  </div>
                  <p className="text-slate-300 text-sm">
                    {typeof plan.workflowsPerMonth === "number" 
                      ? `${plan.workflowsPerMonth} workflow${plan.workflowsPerMonth > 1 ? "s" : ""}/mo`
                      : plan.workflowsPerMonth}
                  </p>
                </div>

                <ul className="space-y-2 mb-8 text-xs text-slate-300">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  onClick={() => handleCheckout({ mode: "subscription", plan: plan.id, term: subscriptionTerm })}
                  disabled={loading !== null}
                  className={`block w-full py-3 px-4 rounded-lg font-semibold text-center text-sm transition disabled:opacity-50 disabled:cursor-not-allowed ${
                    idx === 2
                      ? "bg-emerald-500 hover:bg-emerald-400 text-slate-900 shadow-lg"
                      : "bg-slate-800 hover:bg-slate-700 text-white"
                  }`}
                >
                  {loading === `subscription-${plan.id}-${subscriptionTerm}` 
                    ? "Loading..." 
                    : `Get ${plan.name}`}
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* FAQ Section */}
        <section className="mt-20 max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Frequently asked questions</h2>

          <div className="space-y-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">What's the difference between DFY and subscriptions?</h3>
              <p className="text-slate-300 text-sm">
                <strong>Done-for-you (DFY)</strong> is a one-time payment where we build your workflows and deliver them in 48 hours to 7 days.
                You get the workflows plus support for 7-30 days depending on your tier.
                <br /><br />
                <strong>Subscriptions</strong> give you ongoing workflow creation, monitoring, self-healing, and continuous support.
                Perfect if you need regular automation work or want us to manage everything long-term.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">Can I upgrade or switch plans?</h3>
              <p className="text-slate-300 text-sm">
                Yes. You can upgrade from DFY to a subscription, or switch between subscription tiers anytime.
                Contact us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> for plan changes.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">Do you offer refunds?</h3>
              <p className="text-slate-300 text-sm">
                Yes, we offer a 14-day money-back guarantee for both DFY and subscription plans.
                See our <Link href="/refunds" className="text-emerald-400 hover:underline">refund policy</Link> for details.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">What happens after I pay?</h3>
              <p className="text-slate-300 text-sm">
                <strong>For DFY:</strong> We'll email you within 24 hours to schedule a kickoff call, then build and deliver your workflows within the stated timeframe.
                <br /><br />
                <strong>For subscriptions:</strong> You'll get access to our dashboard and we'll onboard you within 24 hours to start creating your workflows.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Still have questions?
          </h2>
          <p className="text-lg text-slate-400 mb-8">
            Email us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> or check our <Link href="/docs" className="text-emerald-400 hover:underline">documentation</Link>.
          </p>
          <button
            onClick={() => {
              window.scrollTo({ top: 0, behavior: "smooth" });
            }}
            className="inline-block px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all text-lg shadow-2xl"
          >
            Back to top
          </button>
        </div>
      </div>
    </main>
  );
}
