"use client";
import Link from "next/link";
import { dfyPlans } from "@/config/pricing";

const FAQ_ITEMS = [
  { q: "How quickly can you deliver?", a: "DFY Starter: 48 hours. Professional: 3-4 days. Enterprise: 7 days. We start immediately after your kickoff call." },
  { q: "What if I need revisions?", a: "All DFY plans include revisions. Starter: 1 round, Professional: 2 rounds, Enterprise: 2 rounds + ongoing support for 30 days." },
  { q: "Can you integrate with my existing tools?", a: "Yes! We work with 100+ tools including Google Sheets, Airtable, Salesforce, HubSpot, Slack, email platforms, and more." },
  { q: "Do I need technical skills?", a: "No. We build everything for you. You'll get fully functional workflows plus documentation on how to use them." },
  { q: "What if it doesn't work?", a: "We test everything before delivery. If something breaks, we fix it during your support period (7-30 days depending on tier)." },
  { q: "Can I upgrade later?", a: "Absolutely. You can upgrade from Starter to Professional or Enterprise anytime. We'll credit your original purchase." },
  { q: "Do you offer refunds?", a: "Yes, 14-day money-back guarantee. No questions asked." },
  { q: "What happens after purchase?", a: "1) We email you within 24h to schedule kickoff. 2) 30-min call to understand requirements. 3) We build + test. 4) Deliver with docs + support." },
  { q: "How many workflows can I get?", a: "Starter: 1, Professional: 3, Enterprise: 7. Each workflow can have multiple steps and integrations." },
  { q: "What tools do you use?", a: "We use industry-standard automation platforms like Make, Zapier, n8n, or custom code depending on your needs." },
  { q: "Is my data secure?", a: "Yes. We're GDPR compliant, use encrypted connections, and never store your credentials. You maintain full control." },
  { q: "Can I cancel support?", a: "DFY is one-time. Once delivered, the workflows are yours forever. Support is included for the specified period (7-30 days)." }
];

export default function SalesPage() {
  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">Levqor</Link>
          <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">View All Plans</Link>
        </nav>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="bg-amber-500/10 border border-amber-500/30 rounded-xl p-4 mb-12 text-center">
          <p className="text-amber-200 font-semibold">
            ⚡ 48h delivery included this week only — Limited spots available
          </p>
        </div>

        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold text-white mb-6">
            Get Your Workflows Built in 48 Hours
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Stop wasting time on manual tasks. We build production-ready automations while you focus on growing your business.
          </p>
        </div>

        <section className="grid md:grid-cols-3 gap-8 mb-20">
          {dfyPlans.map((plan, idx) => (
            <div
              key={plan.id}
              className={`rounded-2xl bg-slate-900/50 border p-8 ${
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

              <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
              <div className="flex items-baseline gap-1 mb-4">
                <span className="text-5xl font-bold text-white">£{plan.priceGBP}</span>
                <span className="text-slate-400 text-sm">one-time</span>
              </div>
              <p className="text-slate-400 text-sm mb-6">
                {plan.workflows} workflow{plan.workflows > 1 ? "s" : ""} • {plan.delivery}
              </p>

              <ul className="space-y-3 mb-8 text-sm text-slate-300">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>

              <Link
                href={`/pricing#dfy`}
                className={`block w-full py-3 px-4 rounded-lg font-semibold text-center transition ${
                  idx === 1
                    ? "bg-emerald-500 hover:bg-emerald-400 text-slate-900 shadow-lg"
                    : "bg-slate-800 hover:bg-slate-700 text-white"
                }`}
              >
                Get {plan.name}
              </Link>
            </div>
          ))}
        </section>

        <section className="mb-20">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">What You Get</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">Fully Built Workflows</h3>
              <p className="text-slate-400 text-sm">
                Production-ready automations tested and verified before delivery.
              </p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">Documentation</h3>
              <p className="text-slate-400 text-sm">
                Clear guides on how everything works and how to maintain it.
              </p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">Testing & QA</h3>
              <p className="text-slate-400 text-sm">
                Every workflow tested with real data to ensure it works perfectly.
              </p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">Support Period</h3>
              <p className="text-slate-400 text-sm">
                7-30 days of email support depending on your tier.
              </p>
            </div>
          </div>
        </section>

        <section className="mb-20">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Testimonials</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {[
              { text: "Cut our reporting time from 4 hours to 15 minutes.", author: "Founder, SaaS" },
              { text: "24-hour delivery was legit. Automation running next day.", author: "Operations Manager" },
              { text: "Finally, automation that actually works reliably.", author: "CEO, E-commerce" }
            ].map((t, i) => (
              <div key={i} className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
                <p className="text-slate-300 mb-4">"{t.text}"</p>
                <p className="text-slate-500 text-sm">— {t.author}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="mb-20">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Frequently Asked Questions</h2>
          <div className="space-y-4 max-w-3xl mx-auto">
            {FAQ_ITEMS.map((faq, i) => (
              <div key={i} className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
                <h3 className="text-lg font-bold text-white mb-2">{faq.q}</h3>
                <p className="text-slate-400 text-sm">{faq.a}</p>
              </div>
            ))}
          </div>
        </section>

        <div className="text-center py-16 px-6 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to automate your business?
          </h2>
          <p className="text-lg text-slate-400 mb-8">
            Get started with DFY automation today. 14-day money-back guarantee.
          </p>
          <Link
            href="/pricing#dfy"
            className="inline-block px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold text-lg transition shadow-2xl"
          >
            View DFY Plans
          </Link>
        </div>
      </div>
    </main>
  );
}
