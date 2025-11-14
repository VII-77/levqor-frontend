"use client";
import Link from "next/link";

export default function DFYPage() {
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
            <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">
              Pricing
            </Link>
            <Link href="/signin" className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
              Sign in
            </Link>
          </div>
        </nav>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Hero Section */}
        <section className="text-center mb-20">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Done-For-You Automation
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 text-white">
            We build it. You use it.<br />
            <span className="text-emerald-400">No learning curve.</span>
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto mb-8">
            Skip the tutorials. Get fully-built, production-ready automations delivered in 24-48 hours.
            Just describe what you need — we handle the rest.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/pricing#dfy"
              className="px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all text-lg shadow-2xl"
            >
              View DFY Pricing
            </Link>
            <a
              href="mailto:sales@levqor.ai?subject=DFY%20Consultation"
              className="px-10 py-5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all text-lg border border-slate-700"
            >
              Schedule a Call
            </a>
          </div>
        </section>

        {/* How It Works - 4 Steps */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              How Done-For-You works
            </h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              From idea to automation in 4 simple steps. No tech skills required.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {/* Step 1 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-emerald-400">1</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Choose your plan</h3>
              <p className="text-sm text-slate-400">
                Pick Starter (1 workflow), Professional (3 workflows), or Enterprise (7 workflows)
              </p>
            </div>

            {/* Step 2 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-400">2</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Kickoff call</h3>
              <p className="text-sm text-slate-400">
                We schedule a 30-minute call to understand your workflow, tools, and goals
              </p>
            </div>

            {/* Step 3 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-violet-500/20 border border-violet-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-violet-400">3</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">We build it</h3>
              <p className="text-sm text-slate-400">
                Our team builds, tests, and monitors your automation with your tools and data
              </p>
            </div>

            {/* Step 4 */}
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-amber-500/20 border border-amber-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-amber-400">4</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">You use it</h3>
              <p className="text-sm text-slate-400">
                Get your workflows, documentation, and support for 7-30 days depending on your tier
              </p>
            </div>
          </div>
        </section>

        {/* What You Get */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              What you get
            </h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              Every DFY build includes these deliverables — no hidden extras.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Fully-built workflows
              </h3>
              <p className="text-slate-400 text-sm">
                Production-ready automations connecting your tools (CRM, Sheets, Email, Slack, etc) with error handling and monitoring.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Testing & validation
              </h3>
              <p className="text-slate-400 text-sm">
                We test every workflow with real data to ensure it works before handoff. Includes end-to-end testing and edge case validation.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Documentation
              </h3>
              <p className="text-slate-400 text-sm">
                Clear docs on how your workflows work, what each step does, and how to maintain or modify them if needed.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-xl font-bold text-white mb-3 flex items-center gap-2">
                <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Support & revisions
              </h3>
              <p className="text-slate-400 text-sm">
                7-30 days of email support (depending on tier) with 1-2 rounds of revisions to get it exactly right.
              </p>
            </div>
          </div>
        </section>

        {/* Use Cases */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              Common DFY use cases
            </h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              Real automations we've built for teams like yours
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="w-12 h-12 mb-4 rounded-lg bg-emerald-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Lead capture to CRM</h3>
              <p className="text-sm text-slate-400">
                Website form → Google Sheets → CRM → Email notification. Automatic enrichment and lead scoring included.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="w-12 h-12 mb-4 rounded-lg bg-blue-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Weekly reports</h3>
              <p className="text-sm text-slate-400">
                Pull data from analytics, CRM, and billing → Generate PDF report → Email to stakeholders every Monday at 9am.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="w-12 h-12 mb-4 rounded-lg bg-violet-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Onboarding automation</h3>
              <p className="text-sm text-slate-400">
                New customer → Create accounts → Send welcome email → Schedule kickoff call → Add to Slack channel.
              </p>
            </div>
          </div>
        </section>

        {/* Testimonials */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              What customers say
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="flex items-center gap-2 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-slate-300 mb-4">
                "I spent weeks trying to learn Zapier and still couldn't get it working. Levqor's DFY team built exactly what I needed in 2 days. Worth every penny."
              </p>
              <p className="text-slate-500 text-sm">— Founder, Marketing Agency</p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <div className="flex items-center gap-2 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-slate-300 mb-4">
                "The Professional plan was perfect. Got 3 workflows built and they all work flawlessly. Saved me easily 15 hours/week."
              </p>
              <p className="text-slate-500 text-sm">— Operations Manager, SaaS Company</p>
            </div>
          </div>
        </section>

        {/* Pricing Preview */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
              DFY pricing
            </h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              Fixed pricing. No surprises. Delivered in 48 hours to 7 days.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6 text-center">
              <h3 className="text-xl font-bold text-white mb-2">Starter</h3>
              <div className="text-4xl font-bold text-white mb-4">£99</div>
              <p className="text-slate-400 text-sm mb-4">1 workflow • 48-hour delivery</p>
              <Link href="/pricing#dfy" className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition">
                Get Started
              </Link>
            </div>

            <div className="rounded-xl bg-slate-900/50 border-2 border-emerald-500/50 p-6 text-center relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <span className="bg-emerald-500 text-slate-900 px-3 py-1 rounded-full text-xs font-bold uppercase">
                  Most Popular
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Professional</h3>
              <div className="text-4xl font-bold text-white mb-4">£249</div>
              <p className="text-slate-400 text-sm mb-4">3 workflows • 3-4 days</p>
              <Link href="/pricing#dfy" className="block w-full py-3 px-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
                Get Professional
              </Link>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6 text-center">
              <h3 className="text-xl font-bold text-white mb-2">Enterprise</h3>
              <div className="text-4xl font-bold text-white mb-4">£599</div>
              <p className="text-slate-400 text-sm mb-4">7 workflows • 7 days</p>
              <Link href="/pricing#dfy" className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition">
                Get Enterprise
              </Link>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="text-center py-16 px-6 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to automate in 24 hours?
          </h2>
          <p className="text-lg text-slate-400 mb-8 max-w-2xl mx-auto">
            Skip the learning curve. Get fully-built workflows delivered by our expert team.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/pricing#dfy"
              className="px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all text-lg shadow-2xl"
            >
              View DFY Pricing
            </Link>
            <a
              href="mailto:sales@levqor.ai?subject=DFY%20Questions"
              className="px-10 py-5 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all text-lg border border-slate-700"
            >
              Ask a Question
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}
