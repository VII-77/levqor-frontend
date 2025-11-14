'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function DfyProPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCheckout = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          mode: 'dfy',
          plan: 'professional'
        })
      });

      const data = await response.json();

      if (data.ok && data.url) {
        window.location.href = data.url;
      } else {
        setError(data.error || 'Something went wrong starting checkout. Please try again or contact support@levqor.ai');
        setLoading(false);
      }
    } catch (err) {
      setError('Something went wrong starting checkout. Please try again or contact support@levqor.ai');
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      {/* Header */}
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">
            Levqor
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">
              Pricing
            </Link>
            <Link href="/" className="text-sm text-slate-300 hover:text-white transition">
              Home
            </Link>
            <Link href="/signin" className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
              Sign in
            </Link>
          </div>
        </nav>
      </header>

      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* SECTION 1 - HERO */}
        <section className="py-16 sm:py-24 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-4 py-1.5 text-sm font-medium text-emerald-200 mb-8">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            £249 one-time · DFY Pro
          </div>

          <h1 className="text-5xl sm:text-6xl font-bold mb-6 bg-gradient-to-r from-emerald-400 via-cyan-400 to-violet-400 bg-clip-text text-transparent">
            Done-For-You Automation Pro
          </h1>
          
          <p className="text-2xl sm:text-3xl text-slate-300 mb-12 max-w-3xl mx-auto">
            We build your automation for you in 48–72 hours.
          </p>

          <div className="space-y-3 mb-12 max-w-2xl mx-auto text-left">
            <div className="flex items-start gap-3">
              <span className="text-emerald-400 mt-1 text-xl">✓</span>
              <p className="text-lg text-slate-300">You explain the workflow. We build it.</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-emerald-400 mt-1 text-xl">✓</span>
              <p className="text-lg text-slate-300">48–72 hour delivery.</p>
            </div>
            <div className="flex items-start gap-3">
              <span className="text-emerald-400 mt-1 text-xl">✓</span>
              <p className="text-lg text-slate-300">7 days of support + one revision.</p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button
              onClick={handleCheckout}
              disabled={loading}
              className="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-bold text-lg shadow-lg hover:shadow-emerald-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Redirecting…' : 'Book DFY Pro – £249 one-time'}
            </button>
            
            <a
              href="mailto:support@levqor.ai"
              className="px-8 py-4 border-2 border-slate-700 hover:border-emerald-500 text-slate-300 hover:text-white rounded-lg font-semibold text-lg transition-all"
            >
              Talk first – get a 2-minute plan
            </a>
          </div>

          {error && (
            <div className="mt-6 p-4 bg-red-950/50 border border-red-900/50 rounded-lg max-w-md mx-auto">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}
        </section>

        {/* SECTION 2 - WHAT YOU GET */}
        <section className="py-16 border-t border-slate-800">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-4">
            What you get with DFY Pro (£249)
          </h2>
          
          <div className="max-w-3xl mx-auto">
            <ul className="space-y-4 mb-8">
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">1 fully-built end-to-end automation</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">Up to 2 custom triggers (email, webhook, API, or schedule)</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">Optimised for reliability and speed</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">One round of revisions</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">7 days of post-launch support</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">Full documentation in plain English</span>
              </li>
            </ul>

            <p className="text-lg text-slate-400 leading-relaxed">
              DFY Pro is for founders and teams who don't want to fight with tools. You tell us what you need automated. We design, build, and hand over a working system.
            </p>
          </div>
        </section>

        {/* SECTION 3 - WHO IT'S FOR */}
        <section className="py-16 border-t border-slate-800">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-12">
            Who DFY Pro is perfect for
          </h2>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-emerald-500/50 transition-all">
              <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center mb-4">
                <span className="text-2xl">👤</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Solo founders</h3>
              <p className="text-slate-400">
                You're doing everything yourself and need one big manual process removed.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-cyan-500/50 transition-all">
              <div className="w-12 h-12 rounded-full bg-cyan-500/10 flex items-center justify-center mb-4">
                <span className="text-2xl">👥</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Small teams</h3>
              <p className="text-slate-400">
                You have stable processes but no time to wire tools together.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-violet-500/50 transition-all">
              <div className="w-12 h-12 rounded-full bg-violet-500/10 flex items-center justify-center mb-4">
                <span className="text-2xl">✨</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Creators & consultants</h3>
              <p className="text-slate-400">
                You want leads, payments, or delivery automated without learning automation tools.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6 hover:border-amber-500/50 transition-all">
              <div className="w-12 h-12 rounded-full bg-amber-500/10 flex items-center justify-center mb-4">
                <span className="text-2xl">⚙️</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Busy ops people</h3>
              <p className="text-slate-400">
                You need less chaos and fewer manual steps, not more dashboards.
              </p>
            </div>
          </div>
        </section>

        {/* SECTION 4 - HOW IT WORKS */}
        <section className="py-16 border-t border-slate-800">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-12">
            How DFY Pro works
          </h2>

          <div className="max-w-3xl mx-auto space-y-8">
            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-emerald-500 flex items-center justify-center font-bold text-slate-950">
                  1
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Step 1 – You book DFY Pro (£249)</h3>
                <p className="text-slate-400">
                  You answer a short intake form about your current workflow and tools.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-cyan-500 flex items-center justify-center font-bold text-slate-950">
                  2
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Step 2 – We design your automation</h3>
                <p className="text-slate-400">
                  We map the triggers, steps, and outputs in a simple diagram.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-violet-500 flex items-center justify-center font-bold text-slate-950">
                  3
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Step 3 – We build & test</h3>
                <p className="text-slate-400">
                  We implement the workflow, test edge cases, and fix issues.
                </p>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-amber-500 flex items-center justify-center font-bold text-slate-950">
                  4
                </div>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-2">Step 4 – Handover & support</h3>
                <p className="text-slate-400">
                  You get a walkthrough video, documentation, and 7 days of support.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 5 - PRICING & GUARANTEE */}
        <section className="py-16 border-t border-slate-800">
          <div className="max-w-2xl mx-auto text-center">
            <div className="inline-flex items-center gap-2 rounded-full border border-violet-500/40 bg-violet-500/10 px-4 py-1.5 text-sm font-medium text-violet-200 mb-6">
              Simple pricing – no subscriptions
            </div>

            <h2 className="text-3xl sm:text-4xl font-bold mb-6">
              £249 one-time · DFY Automation Pro
            </h2>

            <ul className="space-y-3 mb-8 text-left max-w-md mx-auto">
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">No monthly subscription</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">No hourly surprises</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1 font-bold">✓</span>
                <span className="text-lg text-slate-300">Clear scope and deliverables</span>
              </li>
            </ul>

            <div className="bg-emerald-950/30 border border-emerald-900/50 rounded-xl p-6 mb-8">
              <p className="text-lg text-slate-300 leading-relaxed">
                If we cannot deliver the agreed automation, you get a full refund. No small print. We only take on projects we are confident we can complete.
              </p>
            </div>

            <button
              onClick={handleCheckout}
              disabled={loading}
              className="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-bold text-lg shadow-lg hover:shadow-emerald-500/50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Redirecting…' : 'Book DFY Pro – £249 one-time'}
            </button>

            {error && (
              <div className="mt-6 p-4 bg-red-950/50 border border-red-900/50 rounded-lg">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}
          </div>
        </section>

        {/* SECTION 6 - MINI FAQ */}
        <section className="py-16 border-t border-slate-800 mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-center mb-12">
            DFY Pro – common questions
          </h2>

          <div className="max-w-3xl mx-auto space-y-8">
            <div>
              <h3 className="text-xl font-bold text-white mb-3">
                What tools can you work with?
              </h3>
              <p className="text-slate-400 leading-relaxed">
                We work with tools like Make, Zapier (if needed), Notion, Google Workspace, Stripe, email providers, and standard APIs. If your tool has an API or Zapier/Make connector, we can likely use it.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold text-white mb-3">
                What if my workflow is too big?
              </h3>
              <p className="text-slate-400 leading-relaxed">
                If your scope is larger than DFY Pro, we'll tell you before payment or suggest breaking it into phases. We do not take on work we know we can't complete under this package.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold text-white mb-3">
                What if I'm not happy with the first version?
              </h3>
              <p className="text-slate-400 leading-relaxed">
                DFY Pro includes one revision round. If after that we still can't reach a working solution that matches the agreed scope, we refund you.
              </p>
            </div>

            <div>
              <h3 className="text-xl font-bold text-white mb-3">
                Will I be locked into Levqor forever?
              </h3>
              <p className="text-slate-400 leading-relaxed">
                No. You own the automation we build. We document everything so you're not dependent on us.
              </p>
            </div>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-800 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-semibold text-white mb-4">Product</h3>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><Link href="/pricing" className="hover:text-white transition">Pricing</Link></li>
                <li><Link href="/dfy-pro" className="hover:text-white transition">DFY Pro</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-4">Legal</h3>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><Link href="/terms" className="hover:text-white transition">Terms</Link></li>
                <li><Link href="/privacy" className="hover:text-white transition">Privacy</Link></li>
                <li><Link href="/refunds" className="hover:text-white transition">Refunds</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-4">Support</h3>
              <ul className="space-y-2 text-sm text-slate-400">
                <li><a href="mailto:support@levqor.ai" className="hover:text-white transition">Contact</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-slate-800 text-center text-sm text-slate-400">
            © {new Date().getFullYear()} Levqor. All rights reserved.
          </div>
        </div>
      </footer>
    </main>
  );
}
