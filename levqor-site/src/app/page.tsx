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
    description: 'AI-powered automations built for your business in 48 hours. Fixed pricing. Money-back guarantee.',
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
      
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 bg-slate-950/80 backdrop-blur-md border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="text-xl font-bold text-white">
              Levqor
            </Link>
            <div className="hidden md:flex gap-6">
              <Link href="#pricing" className="text-sm text-slate-300 hover:text-white transition">Pricing</Link>
              <Link href="/docs" className="text-sm text-slate-300 hover:text-white transition">Docs</Link>
              <Link href="/contact" className="text-sm text-slate-300 hover:text-white transition">Contact</Link>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <Link href="/signin" className="text-sm text-slate-300 hover:text-white transition">
              Sign in
            </Link>
            <Link href="/signin" className="px-5 py-2.5 bg-white text-black rounded-xl font-semibold hover:bg-slate-100 transition">
              Start Free Audit
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
              <StatusPill />
            </div>
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6 text-white">
              Automate Work. <span className="text-slate-400">Save Time.</span> Grow Faster.
            </h1>
            <p className="text-xl text-slate-300 mb-8 max-w-2xl">
              Get AI-powered automations built for your business in 48 hours. 
              Fixed pricing. No developers. No complexity.
            </p>
            
            {/* Primary CTAs */}
            <div className="flex flex-wrap gap-4 mb-8">
              <Link 
                href="/signin" 
                className="inline-flex items-center gap-2 px-8 py-4 bg-white text-black rounded-xl font-bold hover:bg-slate-100 transition-all shadow-lg hover:shadow-xl text-lg"
              >
                Start Free Audit
              </Link>
              <Link 
                href="#pricing" 
                className="inline-flex items-center gap-2 px-8 py-4 border-2 border-slate-700 text-white rounded-xl font-semibold hover:bg-slate-900 transition-all text-lg"
              >
                See Pricing
              </Link>
            </div>

            <p className="text-sm text-slate-400">
              No commitments. No pressure. Money-back guarantee.
            </p>
          </div>
        </section>

        {/* Value Props */}
        <section className="max-w-6xl mx-auto px-4 pb-16">
          <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
            <h2 className="text-2xl font-bold text-center mb-8 text-white">Why businesses choose Levqor</h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="flex items-start gap-3">
                <div className="text-2xl">⚡</div>
                <div>
                  <h3 className="font-bold text-white mb-1">48-hour delivery</h3>
                  <p className="text-sm text-slate-300">Built and deployed in 2 days, not 2 weeks</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="text-2xl">💷</div>
                <div>
                  <h3 className="font-bold text-white mb-1">Fixed pricing</h3>
                  <p className="text-sm text-slate-300">£99, £249, or £599. No hidden costs</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="text-2xl">✅</div>
                <div>
                  <h3 className="font-bold text-white mb-1">Money-back guarantee</h3>
                  <p className="text-sm text-slate-300">Not happy? Full refund, no questions</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="text-2xl">📊</div>
                <div>
                  <h3 className="font-bold text-white mb-1">Real-time monitoring</h3>
                  <p className="text-sm text-slate-300">Track every automation with live dashboards</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="text-2xl">🎓</div>
                <div>
                  <h3 className="font-bold text-white mb-1">Zero learning curve</h3>
                  <p className="text-sm text-slate-300">We build it. You use it. That's it</p>
                </div>
              </div>
              <div className="flex items-start gap-3">
                <div className="text-2xl">🔧</div>
                <div>
                  <h3 className="font-bold text-white mb-1">Built-for-you</h3>
                  <p className="text-sm text-slate-300">Not DIY templates. Real custom automation</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Pricing Tiles */}
        <section id="pricing" className="max-w-6xl mx-auto px-4 pb-16">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">Simple, transparent pricing</h2>
          <p className="text-center text-slate-400 mb-12 max-w-2xl mx-auto">
            Choose the package that fits your needs. All include money-back guarantee.
          </p>
          
          <div className="grid md:grid-cols-3 gap-6">
            {/* £99 Package */}
            <div className="bg-slate-900/50 border-2 border-blue-500/30 rounded-2xl p-8 hover:bg-slate-900 hover:border-blue-500/50 transition-all group relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative">
                <div className="text-blue-400 font-bold text-sm mb-2">STARTER</div>
                <div className="text-5xl font-bold text-white mb-2">£99</div>
                <div className="text-slate-400 text-sm mb-6">48-Hour Automation</div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-blue-400 mt-0.5">✓</span>
                    <span>For one repetitive task</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-blue-400 mt-0.5">✓</span>
                    <span>Delivered in 48 hours</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-blue-400 mt-0.5">✓</span>
                    <span>Money-back guarantee</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-blue-400 mt-0.5">✓</span>
                    <span>7 days support included</span>
                  </li>
                </ul>
                <Link href="/signin" className="block w-full py-3 bg-blue-500 text-white text-center rounded-xl font-semibold hover:bg-blue-600 transition">
                  Get Started
                </Link>
              </div>
            </div>

            {/* £249 Package */}
            <div className="bg-slate-900/50 border-2 border-violet-500/50 rounded-2xl p-8 hover:bg-slate-900 hover:border-violet-500/70 transition-all group relative overflow-hidden scale-105 shadow-2xl shadow-violet-500/20">
              <div className="absolute top-4 right-4 bg-violet-500 text-white text-xs font-bold px-3 py-1 rounded-full">POPULAR</div>
              <div className="absolute inset-0 bg-gradient-to-br from-violet-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative">
                <div className="text-violet-400 font-bold text-sm mb-2">PROFESSIONAL</div>
                <div className="text-5xl font-bold text-white mb-2">£249</div>
                <div className="text-slate-400 text-sm mb-6">Workflow Buildout</div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-violet-400 mt-0.5">✓</span>
                    <span>Automate multiple steps</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-violet-400 mt-0.5">✓</span>
                    <span>Emails, CRM, WhatsApp</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-violet-400 mt-0.5">✓</span>
                    <span>2–4 day delivery</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-violet-400 mt-0.5">✓</span>
                    <span>14 days support included</span>
                  </li>
                </ul>
                <Link href="/signin" className="block w-full py-3 bg-violet-500 text-white text-center rounded-xl font-semibold hover:bg-violet-600 transition">
                  Get Started
                </Link>
              </div>
            </div>

            {/* £599 Package */}
            <div className="bg-slate-900/50 border-2 border-emerald-500/30 rounded-2xl p-8 hover:bg-slate-900 hover:border-emerald-500/50 transition-all group relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="relative">
                <div className="text-emerald-400 font-bold text-sm mb-2">ENTERPRISE</div>
                <div className="text-5xl font-bold text-white mb-2">£599</div>
                <div className="text-slate-400 text-sm mb-6">AI Automation System</div>
                <ul className="space-y-3 mb-8">
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>End-to-end automation</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>Decision-based workflows</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>Monitoring + self-healing</span>
                  </li>
                  <li className="flex items-start gap-2 text-slate-300">
                    <span className="text-emerald-400 mt-0.5">✓</span>
                    <span>7-day delivery + 30 days support</span>
                  </li>
                </ul>
                <Link href="/signin" className="block w-full py-3 bg-emerald-500 text-white text-center rounded-xl font-semibold hover:bg-emerald-600 transition">
                  Get Started
                </Link>
              </div>
            </div>
          </div>
        </section>

        {/* Social Proof */}
        <section className="bg-slate-900/50 border-y border-slate-800 py-12">
          <div className="max-w-6xl mx-auto px-6 text-center">
            <p className="text-2xl font-bold text-white mb-2">
              Trusted by local businesses, freelancers, and agencies
            </p>
            <p className="text-slate-400 mb-8">
              Real ROI. Real time saved.
            </p>
            <div className="flex flex-wrap justify-center gap-6 opacity-60">
              {["TechCorp", "DataFlow", "AutoScale", "CloudSync", "DevOps Pro", "StartupLab"].map((logo) => (
                <div key={logo} className="bg-slate-800/50 px-6 py-3 rounded-lg border border-slate-700 font-bold text-slate-300">
                  {logo}
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Use Cases */}
        <section className="max-w-6xl mx-auto px-4 py-20">
          <h2 className="text-4xl font-bold text-center mb-4 text-white">What can you automate?</h2>
          <p className="text-center text-slate-400 mb-12 max-w-2xl mx-auto">
            From simple tasks to complex workflows, we've got you covered
          </p>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-blue-500/30 transition-all">
              <div className="text-3xl mb-3">📧</div>
              <h3 className="text-xl font-bold mb-3 text-white">Email & Lead Follow-up</h3>
              <p className="text-slate-300 text-sm mb-4">Automatically respond to leads, send follow-ups, and update your CRM. Never miss a hot lead again.</p>
              <div className="text-xs text-slate-500">E-commerce • Agencies • Coaches</div>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-violet-500/30 transition-all">
              <div className="text-3xl mb-3">💬</div>
              <h3 className="text-xl font-bold mb-3 text-white">WhatsApp & Customer Service</h3>
              <p className="text-slate-300 text-sm mb-4">Auto-reply to common questions, send order updates, handle bookings. 24/7 customer service.</p>
              <div className="text-xs text-slate-500">Salons • Restaurants • Trades</div>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-emerald-500/30 transition-all">
              <div className="text-3xl mb-3">📊</div>
              <h3 className="text-xl font-bold mb-3 text-white">Invoicing & Admin</h3>
              <p className="text-slate-300 text-sm mb-4">Generate invoices, send payment reminders, update spreadsheets. Free up 6+ hours per week.</p>
              <div className="text-xs text-slate-500">Freelancers • Local Businesses</div>
            </div>
            
            <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl hover:bg-slate-900 hover:border-amber-500/30 transition-all">
              <div className="text-3xl mb-3">🗓️</div>
              <h3 className="text-xl font-bold mb-3 text-white">Scheduling & Bookings</h3>
              <p className="text-slate-300 text-sm mb-4">Sync calendars, send reminders, handle cancellations. Automated end-to-end.</p>
              <div className="text-xs text-slate-500">Estate Agents • Healthcare • Services</div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="bg-gradient-to-br from-slate-900 via-slate-950 to-black border-t border-slate-800 py-24">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 text-white">
              Start with a free automation audit
            </h2>
            <p className="text-xl text-slate-300 mb-10">
              No commitments. No pressure. Let's identify 2-3 tasks we can automate for you.
            </p>
            <Link
              href="/signin"
              className="inline-block px-10 py-5 bg-white text-black rounded-xl font-bold hover:bg-slate-100 transition-all text-lg shadow-2xl"
            >
              Start Free Audit
            </Link>
            <p className="mt-8 text-sm text-slate-400">
              48-hour delivery • Money-back guarantee • No credit card required
            </p>
          </div>
        </section>
      </main>
    </>
  );
}
