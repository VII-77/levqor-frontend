"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import JsonLd from "@/components/JsonLd";
import Logo from "@/components/Logo";
import Footer from "@/components/Footer";
import HighRiskWarning from "@/components/HighRiskWarning";

function StatusPill() {
  const [status, setStatus] = useState<{ ok: boolean; message: string } | null>(null);

  useEffect(() => {
    fetch("https://api.levqor.ai/health")
      .then((res) => res.json())
      .then((data) => setStatus({ ok: data.status === "healthy" || data.ok === true, message: "All systems operational" }))
      .catch(() => setStatus({ ok: false, message: "Checking status..." }));
  }, []);

  if (!status) return null;

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium ${status.ok ? "bg-green-500/20 text-green-400 border border-green-500/30" : "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30"}`}>
      <span className={`w-2 h-2 rounded-full ${status.ok ? "bg-green-400 animate-pulse" : "bg-yellow-400"}`}></span>
      {status.message}
    </div>
  );
}

export default function Home() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Levqor',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web',
    url: 'https://levqor.ai',
    description: 'Genesis v8.0 - Self-healing automation that fixes itself. Built for operators, founders, and teams who can\'t afford downtime.',
    offers: {
      '@type': 'AggregateOffer',
      lowPrice: '99',
      highPrice: '599',
      priceCurrency: 'GBP',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.9',
      ratingCount: '247',
    },
  };

  return (
    <>
      <JsonLd data={structuredData} />
      
      {/* Header Navigation */}
      <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/60">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Logo />
            <div className="hidden md:flex gap-6">
              <Link href="/" className="text-sm text-slate-300 hover:text-white transition">Home</Link>
              <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">Pricing</Link>
              <Link href="/docs" className="text-sm text-slate-300 hover:text-white transition">Docs</Link>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/signin" className="hidden sm:block text-sm text-slate-300 hover:text-white transition">
              Sign in
            </Link>
            <Link href="/pricing" className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
              Start free trial
            </Link>
          </div>
        </nav>
      </header>

      <main className="min-h-screen bg-slate-950">
        {/* Hero Section */}
        <section className="max-w-6xl mx-auto px-4 pt-20 pb-16">
          <div className="max-w-4xl mx-auto text-center">
            {/* Genesis v8.0 Badge */}
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Genesis v8.0
            </div>
            
            {/* Main Headline */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight mb-6 text-slate-50">
              Automate work. Ship faster.
            </h1>
            
            {/* Subheadline */}
            <p className="text-lg sm:text-xl text-slate-300 mb-10 max-w-2xl mx-auto leading-relaxed">
              Levqor runs your workflows, detects failures, and self-heals in minutes so you don't have to babysit your ops.
            </p>
            
            {/* Hero CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link 
                href="/pricing" 
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl text-lg"
              >
                Start free trial
              </Link>
              <Link 
                href="/contact"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all text-lg"
              >
                View demo
              </Link>
            </div>

            <div className="inline-flex items-center gap-2">
              <StatusPill />
            </div>
          </div>

          {/* High-Risk Warning */}
          <div className="max-w-3xl mx-auto mt-12">
            <HighRiskWarning />
          </div>
        </section>

        {/* Genesis Feature Tiles - 4 Tiles */}
        <section className="max-w-6xl mx-auto px-4 py-12">
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {/* Tile 1: Self-healing */}
            <div className="rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30 p-6 hover:from-emerald-500/40 hover:to-blue-500/40 transition-all duration-300">
              <div className="text-4xl mb-4">🔁</div>
              <h3 className="text-lg font-bold text-white mb-2">Self-healing workflows</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Detects failures automatically and retries, rolls back, or routes to backups.
              </p>
            </div>

            {/* Tile 2: Visual Builder */}
            <div className="rounded-2xl bg-gradient-to-br from-violet-500/20 to-purple-500/20 border border-violet-500/30 p-6 hover:from-violet-500/40 hover:to-purple-500/40 transition-all duration-300">
              <div className="text-4xl mb-4">🎨</div>
              <h3 className="text-lg font-bold text-white mb-2">Visual builder</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Design automations with a clean, visual canvas instead of 50 browser tabs.
              </p>
            </div>

            {/* Tile 3: Intelligence Engine */}
            <div className="rounded-2xl bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30 p-6 hover:from-amber-500/40 hover:to-orange-500/40 transition-all duration-300">
              <div className="text-4xl mb-4">🧠</div>
              <h3 className="text-lg font-bold text-white mb-2">Intelligence engine</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Understands context, picks the safest path, and recommends improvements.
              </p>
            </div>

            {/* Tile 4: Connect Everything */}
            <div className="rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 p-6 hover:from-cyan-500/40 hover:to-blue-500/40 transition-all duration-300">
              <div className="text-4xl mb-4">🔗</div>
              <h3 className="text-lg font-bold text-white mb-2">Connect everything</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Email, Sheets, Drive, CRM, Stripe, webhooks, and your own APIs.
              </p>
            </div>
          </div>
        </section>

        {/* Trust / Social Proof Section */}
        <section className="max-w-6xl mx-auto px-4 py-16 text-center">
          <p className="text-lg text-slate-400 mb-8">
            Built for operators, founders, and teams who can't afford downtime.
          </p>
          <div className="flex flex-wrap justify-center gap-8 text-slate-600 text-sm font-medium">
            <span>Trusted by innovative teams</span>
          </div>
        </section>

        {/* Pricing Preview Section */}
        <section id="pricing" className="max-w-6xl mx-auto px-4 py-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-white">Done-for-you pricing</h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              We build it. You use it. Fixed pricing. 48-hour delivery.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {/* Starter Tier */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8 hover:border-emerald-400/50 transition-all">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-2">Starter</h3>
                <div className="flex items-baseline gap-1 mb-4">
                  <span className="text-4xl font-bold text-white">£99</span>
                </div>
                <p className="text-sm text-slate-400">Perfect for your first automation.</p>
              </div>
              <ul className="space-y-3 mb-8 text-sm text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>1 workflow</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Up to 3 tools (e.g. Email + Sheets + CRM)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Basic monitoring</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Email support for 7 days</span>
                </li>
              </ul>
              <Link href="/pricing" className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold text-center transition">
                Get started
              </Link>
            </div>

            {/* Professional Tier - Featured */}
            <div className="rounded-2xl bg-slate-900/50 border-2 border-emerald-500/50 p-8 relative">
              <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                <span className="bg-emerald-500 text-slate-900 px-4 py-1 rounded-full text-xs font-bold">POPULAR</span>
              </div>
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-2">Professional</h3>
                <div className="flex items-baseline gap-1 mb-4">
                  <span className="text-4xl font-bold text-white">£249</span>
                </div>
                <p className="text-sm text-slate-400">For founders and teams who want reliability.</p>
              </div>
              <ul className="space-y-3 mb-8 text-sm text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Up to 3 workflows</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Up to 6 tools</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Self-healing on critical steps</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Priority support for 30 days</span>
                </li>
              </ul>
              <Link href="/pricing" className="block w-full py-3 px-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold text-center transition">
                Get started
              </Link>
            </div>

            {/* Enterprise Tier */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8 hover:border-emerald-400/50 transition-all">
              <div className="mb-6">
                <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
                <div className="flex items-baseline gap-1 mb-4">
                  <span className="text-4xl font-bold text-white">£599</span>
                </div>
                <p className="text-sm text-slate-400">When automation is mission-critical.</p>
              </div>
              <ul className="space-y-3 mb-8 text-sm text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Up to 7 workflows</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Advanced routing and fallbacks</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>Monitoring dashboard</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-0.5">✓</span>
                  <span>30 days of hands-on support</span>
                </li>
              </ul>
              <Link href="/pricing" className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold text-center transition">
                Get started
              </Link>
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section className="bg-gradient-to-br from-emerald-500/10 via-slate-950 to-blue-500/10 border-t border-slate-800 py-24">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
              Ready in 48 hours.
            </h2>
            <p className="text-xl text-slate-300 mb-10">
              See our done-for-you pricing and get started today.
            </p>
            <Link
              href="/pricing"
              className="inline-block px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all text-lg shadow-2xl"
            >
              See done-for-you pricing
            </Link>
            <p className="mt-8 text-sm text-slate-400">
              48-hour delivery • Fixed pricing • Money-back guarantee
            </p>
          </div>
        </section>
      </main>
      
      <Footer />
    </>
  );
}
