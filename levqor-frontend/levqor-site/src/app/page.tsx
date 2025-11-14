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
              Automate your business in 24 hours.<br />No tech skills needed.
            </h1>
            
            {/* Subheadline */}
            <p className="text-lg sm:text-xl text-slate-300 mb-10 max-w-2xl mx-auto leading-relaxed">
              DFY setups, subscription automation, workflows, integrations. We build it. You use it.
            </p>
            
            {/* Hero CTAs */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <a
                href="#pricing"
                onClick={(e) => {
                  e.preventDefault();
                  document.getElementById('pricing')?.scrollIntoView({ behavior: 'smooth' });
                }}
                className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl text-lg cursor-pointer"
              >
                Get Started
              </a>
              <Link 
                href="/dfy"
                className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all text-lg"
              >
                Book DFY
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

        {/* Value Proposition Section - 3 Key Benefits */}
        <section className="max-w-6xl mx-auto px-4 py-16">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Benefit 1 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
                <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Save 20+ hours/week</h3>
              <p className="text-slate-400">
                Eliminate repetitive tasks and focus on what matters. Automate data entry, reporting, and workflows.
              </p>
            </div>

            {/* Benefit 2 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center">
                <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">24-hour setup available</h3>
              <p className="text-slate-400">
                Our Done-For-You service delivers fully built automations in 24-48 hours. No learning curve required.
              </p>
            </div>

            {/* Benefit 3 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-violet-500/20 border border-violet-500/30 flex items-center justify-center">
                <svg className="w-8 h-8 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">No-code & AI-powered</h3>
              <p className="text-slate-400">
                Visual builder + smart AI assistant. Build complex workflows without writing a single line of code.
              </p>
            </div>
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
        <section className="max-w-6xl mx-auto px-4 py-16">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-white mb-4">Trusted by operators and founders</h2>
            <p className="text-slate-400 max-w-2xl mx-auto">
              Join teams already saving 20+ hours/week with automated workflows
            </p>
          </div>

          {/* Testimonials Placeholder */}
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="flex items-center gap-2 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-slate-300 text-sm mb-4">
                "Cut our reporting time from 4 hours to 15 minutes. Game changer for our team."
              </p>
              <p className="text-slate-500 text-xs">— Founder, SaaS startup</p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="flex items-center gap-2 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-slate-300 text-sm mb-4">
                "24-hour delivery was legit. Had our CRM automation running the next day."
              </p>
              <p className="text-slate-500 text-xs">— Operations Manager, Agency</p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="flex items-center gap-2 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-slate-300 text-sm mb-4">
                "Finally, automation that actually works. Self-healing saved us multiple times already."
              </p>
              <p className="text-slate-500 text-xs">— CEO, E-commerce</p>
            </div>
          </div>

          {/* Trust Logos Row */}
          <div className="flex flex-wrap justify-center items-center gap-8 text-slate-600 text-sm font-medium">
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-slate-400">GDPR Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
              </svg>
              <span className="text-slate-400">Secure Payments</span>
            </div>
            <div className="flex items-center gap-2">
              <svg className="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-slate-400">24/7 Monitoring</span>
            </div>
          </div>
        </section>

        {/* DFY vs Subscription Breakdown */}
        <section className="max-w-6xl mx-auto px-4 py-16">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Two ways to automate</h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              Choose Done-For-You builds or flexible subscriptions. Both get you automated fast.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
            {/* DFY Column */}
            <div className="rounded-2xl bg-slate-900/50 border-2 border-emerald-500/50 p-8">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">Done-For-You</h3>
                <p className="text-slate-400 text-sm">We build it. You use it.</p>
              </div>

              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-white font-medium">24-48 hour delivery</p>
                    <p className="text-slate-400 text-sm">Get your automation running fast</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-white font-medium">Fixed pricing</p>
                    <p className="text-slate-400 text-sm">£99, £249, or £599 one-time</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-white font-medium">Perfect for projects</p>
                    <p className="text-slate-400 text-sm">One-off builds, no commitment</p>
                  </div>
                </li>
              </ul>

              <Link href="/pricing#dfy" className="block w-full py-3 px-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold text-center transition">
                View DFY Pricing
              </Link>
            </div>

            {/* Subscription Column */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-white mb-2">Subscriptions</h3>
                <p className="text-slate-400 text-sm">Ongoing automation at scale</p>
              </div>

              <ul className="space-y-3 mb-8">
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-white font-medium">Unlimited workflow runs</p>
                    <p className="text-slate-400 text-sm">No per-execution fees</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-white font-medium">Monthly or yearly</p>
                    <p className="text-slate-400 text-sm">Starting at £29/month</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <div>
                    <p className="text-white font-medium">For ongoing operations</p>
                    <p className="text-slate-400 text-sm">Scale with your business</p>
                  </div>
                </li>
              </ul>

              <Link href="/pricing#subscriptions" className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold text-center transition">
                View Subscriptions
              </Link>
            </div>
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
