"use client";
import Link from "next/link";
import { dfyPlans } from "@/config/pricing";

export default function DFYUpgradePage() {
  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">Levqor</Link>
        </nav>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Upgrade Your DFY Package
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Get more workflows, extended support, and advanced features
          </p>
        </div>

        <section className="grid md:grid-cols-3 gap-8 mb-16">
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
                    Recommended
                  </span>
                </div>
              )}

              <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
              <div className="flex items-baseline gap-1 mb-4">
                <span className="text-5xl font-bold text-white">£{plan.priceGBP}</span>
                <span className="text-slate-400 text-sm">one-time</span>
              </div>

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
                Upgrade to {plan.name}
              </Link>
            </div>
          ))}
        </section>

        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Comparison</h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-b border-slate-800">
                  <th className="text-left py-4 px-4 text-sm font-semibold text-slate-400">Feature</th>
                  <th className="text-center py-4 px-4 text-sm font-semibold text-white">Starter</th>
                  <th className="text-center py-4 px-4 text-sm font-semibold text-white">Professional</th>
                  <th className="text-center py-4 px-4 text-sm font-semibold text-white">Enterprise</th>
                </tr>
              </thead>
              <tbody className="text-sm">
                <tr className="border-b border-slate-800/50">
                  <td className="py-4 px-4 text-slate-300">Workflows</td>
                  <td className="text-center py-4 px-4 text-slate-400">1</td>
                  <td className="text-center py-4 px-4 text-slate-400">3</td>
                  <td className="text-center py-4 px-4 text-slate-400">7</td>
                </tr>
                <tr className="border-b border-slate-800/50">
                  <td className="py-4 px-4 text-slate-300">Delivery Time</td>
                  <td className="text-center py-4 px-4 text-slate-400">48 hours</td>
                  <td className="text-center py-4 px-4 text-slate-400">3-4 days</td>
                  <td className="text-center py-4 px-4 text-slate-400">7 days</td>
                </tr>
                <tr className="border-b border-slate-800/50">
                  <td className="py-4 px-4 text-slate-300">Support</td>
                  <td className="text-center py-4 px-4 text-slate-400">7 days</td>
                  <td className="text-center py-4 px-4 text-slate-400">30 days</td>
                  <td className="text-center py-4 px-4 text-slate-400">30 days</td>
                </tr>
                <tr className="border-b border-slate-800/50">
                  <td className="py-4 px-4 text-slate-300">Revisions</td>
                  <td className="text-center py-4 px-4 text-slate-400">1 round</td>
                  <td className="text-center py-4 px-4 text-slate-400">2 rounds</td>
                  <td className="text-center py-4 px-4 text-slate-400">2 rounds</td>
                </tr>
                <tr className="border-b border-slate-800/50">
                  <td className="py-4 px-4 text-slate-300">Self-Healing</td>
                  <td className="text-center py-4 px-4 text-slate-600">—</td>
                  <td className="text-center py-4 px-4 text-emerald-400">✓</td>
                  <td className="text-center py-4 px-4 text-emerald-400">✓</td>
                </tr>
                <tr>
                  <td className="py-4 px-4 text-slate-300">Custom Integrations</td>
                  <td className="text-center py-4 px-4 text-slate-600">—</td>
                  <td className="text-center py-4 px-4 text-slate-600">—</td>
                  <td className="text-center py-4 px-4 text-emerald-400">✓</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Real Examples</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-3">Lead Capture</h3>
              <p className="text-slate-400 text-sm mb-4">
                Website form → Google Sheets → CRM → Email notification
              </p>
              <p className="text-emerald-400 text-sm font-semibold">Starter: 1 workflow</p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-3">Full Sales Flow</h3>
              <p className="text-slate-400 text-sm mb-4">
                Lead capture + Email sequence + CRM sync
              </p>
              <p className="text-emerald-400 text-sm font-semibold">Professional: 3 workflows</p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-3">Complete Operations</h3>
              <p className="text-slate-400 text-sm mb-4">
                Sales + Onboarding + Support + Reporting + Analytics
              </p>
              <p className="text-emerald-400 text-sm font-semibold">Enterprise: 7 workflows</p>
            </div>
          </div>
        </section>

        <div className="text-center py-16 px-6 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to upgrade?
          </h2>
          <p className="text-lg text-slate-400 mb-8">
            Get more workflows and extended support. We'll credit your original purchase.
          </p>
          <Link
            href="/pricing#dfy"
            className="inline-block px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold text-lg transition shadow-2xl"
          >
            View Plans
          </Link>
        </div>
      </div>
    </main>
  );
}
