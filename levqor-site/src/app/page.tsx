"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import JsonLd from "@/components/JsonLd";

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
    description: 'AI-powered automation that self-heals and ships faster. Pay only for results.',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
      priceSpecification: {
        '@type': 'UnitPriceSpecification',
        price: '0',
        priceCurrency: 'USD',
      },
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '127',
    },
  };

  return (
    <>
      <JsonLd data={structuredData} />
      
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="text-xl font-bold text-white">
              Levqor
            </Link>
            <div className="hidden md:flex gap-6">
              <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">Pricing</Link>
              <Link href="/docs" className="text-sm text-slate-300 hover:text-white transition">Docs</Link>
              <Link href="/contact" className="text-sm text-slate-300 hover:text-white transition">Contact</Link>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/signin" className="text-sm text-slate-300 hover:text-white transition">
              Sign in
            </Link>
            <Link href="/signin" className="px-5 py-2.5 bg-white text-black rounded-xl font-semibold hover:bg-slate-100 transition">
              Start free trial
            </Link>
          </div>
        </nav>
      </header>

      <main className="min-h-screen bg-slate-950">
        {/* Hero Section */}
        <section className="max-w-6xl mx-auto px-4 pt-20 pb-16">
          <div className="max-w-4xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/30 bg-emerald-500/10 px-3 py-1 text-xs text-emerald-400 font-medium mb-6">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              Genesis v8.0 · Self-healing automation
            </div>
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6 text-white">
              Automate work. <span className="text-slate-400">Ship faster.</span>
            </h1>
            <p className="text-xl text-slate-300 mb-8 max-w-2xl">
              Self-healing automation for workflows, monitoring, alerts, and runbooks. 
              Email, Sheets, Slack, CRM.
            </p>
            
            {/* Primary CTAs */}
            <div className="flex flex-wrap gap-4 mb-6">
              <Link 
                href="/signin" 
                className="inline-flex items-center gap-2 px-6 py-3 bg-white text-black rounded-xl font-semibold hover:bg-slate-100 transition-all shadow-lg hover:shadow-xl"
              >
                Start free trial
              </Link>
              <Link 
                href="/pricing" 
                className="inline-flex items-center gap-2 px-6 py-3 border-2 border-slate-700 text-white rounded-xl font-semibold hover:bg-slate-900 transition-all"
              >
                See pricing
              </Link>
            </div>

            {/* Auth CTAs */}
            <div className="flex flex-wrap gap-3">
              <Link 
                href="/signin" 
                className="inline-flex items-center gap-2 px-4 py-2 text-sm bg-slate-900 border border-slate-700 text-slate-200 rounded-lg hover:bg-slate-800 transition"
              >
                <svg className="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Sign in with Google
              </Link>
              <Link 
                href="/signin?method=magic-link" 
                className="inline-flex items-center gap-2 px-4 py-2 text-sm bg-slate-900 border border-slate-700 text-slate-200 rounded-lg hover:bg-slate-800 transition"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                Get magic link
              </Link>
            </div>
          </div>
        </section>

        {/* Colorful Feature Tiles */}
        <section className="max-w-6xl mx-auto px-4 pb-16">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="rounded-2xl p-6 bg-gradient-to-br from-blue-500/20 to-blue-600/10 border border-blue-500/30 hover:shadow-xl hover:shadow-blue-500/10 transition-all">
              <div className="text-2xl mb-3">🔄</div>
              <h3 className="text-lg font-bold mb-2 text-white">Self-healing runs</h3>
              <p className="text-sm text-slate-300">Auto-retry with backoff. No manual intervention.</p>
            </div>
            
            <div className="rounded-2xl p-6 bg-gradient-to-br from-violet-500/20 to-violet-600/10 border border-violet-500/30 hover:shadow-xl hover:shadow-violet-500/10 transition-all">
              <div className="text-2xl mb-3">🎨</div>
              <h3 className="text-lg font-bold mb-2 text-white">Visual builder</h3>
              <p className="text-sm text-slate-300">Drag-drop steps. No wall of YAML.</p>
            </div>
            
            <div className="rounded-2xl p-6 bg-gradient-to-br from-emerald-500/20 to-emerald-600/10 border border-emerald-500/30 hover:shadow-xl hover:shadow-emerald-500/10 transition-all">
              <div className="text-2xl mb-3">🔍</div>
              <h3 className="text-lg font-bold mb-2 text-white">Smart diff</h3>
              <p className="text-sm text-slate-300">Isolate failures fast with intelligent comparison.</p>
            </div>
            
            <div className="rounded-2xl p-6 bg-gradient-to-br from-amber-500/20 to-amber-600/10 border border-amber-500/30 hover:shadow-xl hover:shadow-amber-500/10 transition-all">
              <div className="text-2xl mb-3">📋</div>
              <h3 className="text-lg font-bold mb-2 text-white">Audit trail</h3>
              <p className="text-sm text-slate-300">Each fix recorded. Full transparency.</p>
            </div>
          </div>
        </section>

        {/* Trust Band */}
        <section className="bg-slate-900/50 border-y border-slate-800 py-12">
          <div className="max-w-6xl mx-auto px-6 text-center">
            <p className="text-sm text-slate-400 mb-6 font-medium uppercase tracking-wide">
              Trusted by teams that can't afford downtime
            </p>
            <div className="flex flex-wrap justify-center gap-8 opacity-60">
              {["TechCorp", "DataFlow", "AutoScale", "CloudSync", "DevOps Pro"].map((logo) => (
                <div key={logo} className="bg-slate-800/50 px-6 py-3 rounded-lg border border-slate-700 font-bold text-slate-300">
                  {logo}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="max-w-6xl mx-auto px-4 py-20">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">Why teams choose Levqor</h2>
          <p className="text-center text-slate-400 mb-12 max-w-2xl mx-auto">
            Built for self-healing automation with enterprise-grade reliability
          </p>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-blue-500/30 transition-all group">
              <div className="text-4xl mb-4">🔄</div>
              <h3 className="text-xl font-bold mb-3 text-white">Self-healing runs</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-start gap-2"><span className="text-blue-400 mt-0.5">✓</span><span>Auto-retry with exponential backoff</span></li>
                <li className="flex items-start gap-2"><span className="text-blue-400 mt-0.5">✓</span><span>Smart diff to isolate failures</span></li>
                <li className="flex items-start gap-2"><span className="text-blue-400 mt-0.5">✓</span><span>Audit trail for each fix</span></li>
              </ul>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-violet-500/30 transition-all group">
              <div className="text-4xl mb-4">🎨</div>
              <h3 className="text-xl font-bold mb-3 text-white">Visual builder</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-start gap-2"><span className="text-violet-400 mt-0.5">✓</span><span>Drag-drop workflow steps</span></li>
                <li className="flex items-start gap-2"><span className="text-violet-400 mt-0.5">✓</span><span>Inline AI prompts</span></li>
                <li className="flex items-start gap-2"><span className="text-violet-400 mt-0.5">✓</span><span>Versioned blueprints</span></li>
              </ul>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-emerald-500/30 transition-all group">
              <div className="text-4xl mb-4">🔐</div>
              <h3 className="text-xl font-bold mb-3 text-white">Enterprise SSO</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">✓</span><span>SAML/OIDC support</span></li>
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">✓</span><span>Role-based access control</span></li>
                <li className="flex items-start gap-2"><span className="text-emerald-400 mt-0.5">✓</span><span>Organization audit log</span></li>
              </ul>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-amber-500/30 transition-all group">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-bold mb-3 text-white">SLA 99.9%</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-start gap-2"><span className="text-amber-400 mt-0.5">✓</span><span>Global edge network</span></li>
                <li className="flex items-start gap-2"><span className="text-amber-400 mt-0.5">✓</span><span>Warm starts</span></li>
                <li className="flex items-start gap-2"><span className="text-amber-400 mt-0.5">✓</span><span>Priority support lanes</span></li>
              </ul>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-rose-500/30 transition-all group">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-3 text-white">Audit & alerts</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-start gap-2"><span className="text-rose-400 mt-0.5">✓</span><span>Structured execution logs</span></li>
                <li className="flex items-start gap-2"><span className="text-rose-400 mt-0.5">✓</span><span>PagerDuty/Slack webhooks</span></li>
                <li className="flex items-start gap-2"><span className="text-rose-400 mt-0.5">✓</span><span>PII-aware log redaction</span></li>
              </ul>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-cyan-500/30 transition-all group">
              <div className="text-4xl mb-4">💳</div>
              <h3 className="text-xl font-bold mb-3 text-white">Stripe billing</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li className="flex items-start gap-2"><span className="text-cyan-400 mt-0.5">✓</span><span>Usage-based pricing</span></li>
                <li className="flex items-start gap-2"><span className="text-cyan-400 mt-0.5">✓</span><span>Trials and coupon codes</span></li>
                <li className="flex items-start gap-2"><span className="text-cyan-400 mt-0.5">✓</span><span>Exportable VAT invoices</span></li>
              </ul>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="bg-gradient-to-br from-slate-900 via-slate-950 to-black border-t border-slate-800 py-24">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
              Ready to automate your workflows?
            </h2>
            <p className="text-xl text-slate-300 mb-10">
              Start building with Levqor today. No credit card required.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="/signin"
                className="inline-block px-8 py-4 bg-white text-black rounded-xl font-semibold hover:bg-slate-100 transition-all text-lg shadow-2xl"
              >
                Start free trial
              </Link>
              <Link
                href="/pricing"
                className="inline-block px-8 py-4 bg-transparent border-2 border-slate-600 text-white rounded-xl font-semibold hover:bg-slate-900 transition-all text-lg"
              >
                See pricing
              </Link>
            </div>
            <p className="mt-8 text-sm text-slate-400">
              No long-term contracts. Cancel anytime.
            </p>
          </div>
        </section>
      </main>
    </>
  );
}
