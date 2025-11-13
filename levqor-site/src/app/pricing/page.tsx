"use client";
import Link from "next/link";

export default function Pricing() {
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

      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Page Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Done-for-you automation
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Fixed pricing. 48-hour delivery.
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            We build it. You use it. No hidden fees, no surprises. Choose your package and we'll deliver in 48 hours.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-16">
          {/* Starter Tier */}
          <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8 hover:border-emerald-400/50 transition-all">
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Starter</h3>
              <div className="flex items-baseline gap-1 mb-4">
                <span className="text-5xl font-bold text-white">£99</span>
              </div>
              <p className="text-slate-400">Perfect for your first automation.</p>
            </div>
            
            <div className="mb-8">
              <p className="text-sm text-slate-300 mb-4">One workflow, delivered in 48 hours.</p>
            </div>

            <ul className="space-y-3 mb-8 text-sm text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>1 workflow</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Up to 3 tools (e.g. Email + Sheets + CRM)</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Basic monitoring</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Email support for 7 days</span>
              </li>
            </ul>

            <Link 
              href="/signin" 
              className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold text-center transition"
            >
              Get started
            </Link>
          </div>

          {/* Professional Tier - Featured */}
          <div className="rounded-2xl bg-slate-900/50 border-2 border-emerald-500/50 p-8 relative transform scale-105">
            <div className="absolute -top-4 left-1/2 -translate-x-1/2">
              <span className="bg-emerald-500 text-slate-900 px-4 py-1 rounded-full text-xs font-bold uppercase">Most Popular</span>
            </div>
            
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Professional</h3>
              <div className="flex items-baseline gap-1 mb-4">
                <span className="text-5xl font-bold text-white">£249</span>
              </div>
              <p className="text-slate-400">For founders and teams who want reliability.</p>
            </div>
            
            <div className="mb-8">
              <p className="text-sm text-slate-300 mb-4">We design and ship your core automations in 2–4 days.</p>
            </div>

            <ul className="space-y-3 mb-8 text-sm text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Up to 3 workflows</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Up to 6 tools</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Self-healing on critical steps</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Priority support for 30 days</span>
              </li>
            </ul>

            <Link 
              href="/signin" 
              className="block w-full py-3 px-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-bold text-center transition shadow-lg"
            >
              Get started
            </Link>
          </div>

          {/* Enterprise Tier */}
          <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8 hover:border-emerald-400/50 transition-all">
            <div className="mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Enterprise</h3>
              <div className="flex items-baseline gap-1 mb-4">
                <span className="text-5xl font-bold text-white">£599</span>
              </div>
              <p className="text-slate-400">When automation is mission-critical.</p>
            </div>
            
            <div className="mb-8">
              <p className="text-sm text-slate-300 mb-4">Deep integration, monitoring, and a 7-day build window.</p>
            </div>

            <ul className="space-y-3 mb-8 text-sm text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Up to 7 workflows</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Advanced routing and fallbacks</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>Monitoring dashboard</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5 font-bold">✓</span>
                <span>30 days of hands-on support</span>
              </li>
            </ul>

            <Link 
              href="/signin" 
              className="block w-full py-3 px-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold text-center transition"
            >
              Get started
            </Link>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Frequently asked questions</h2>
          
          <div className="space-y-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">How does the 48-hour delivery work?</h3>
              <p className="text-slate-300 text-sm">
                Once you select a package and complete payment, we'll schedule a quick kickoff call to understand your workflow. 
                Within 48 hours, your automation will be built, tested, and ready to use.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">What if I need changes after delivery?</h3>
              <p className="text-slate-300 text-sm">
                All packages include support. Starter gets 7 days, Professional gets 30 days, and Enterprise gets 30 days of hands-on support. 
                We'll help you tweak and optimize your workflows.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">Do I need to pay monthly after this?</h3>
              <p className="text-slate-300 text-sm">
                No. These are one-time payments for us to build your automation. Your workflows run on your own accounts 
                (Gmail, Sheets, etc.) or our infrastructure depending on your needs.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-lg font-bold text-white mb-2">Can I upgrade later?</h3>
              <p className="text-slate-300 text-sm">
                Absolutely. If you start with Starter and need more workflows, we can upgrade you to Professional or Enterprise. 
                You'll only pay the difference.
              </p>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to automate your work?
          </h2>
          <p className="text-lg text-slate-400 mb-8">
            Choose your package and we'll have your automation running in 48 hours.
          </p>
          <Link
            href="/signin"
            className="inline-block px-10 py-5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all text-lg shadow-2xl"
          >
            Get started now
          </Link>
        </div>
      </div>
    </main>
  );
}
