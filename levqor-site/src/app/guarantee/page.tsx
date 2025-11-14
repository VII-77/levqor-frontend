"use client";
import Link from "next/link";

export default function GuaranteePage() {
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

      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Hero */}
        <section className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <svg className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            14-Day Money-Back Guarantee
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Try it risk-free for 14 days
          </h1>
          <p className="text-xl text-slate-400 max-w-2xl mx-auto">
            We're confident you'll love your automations. If not, we'll refund you — no questions asked.
          </p>
        </section>

        {/* Guarantee Details */}
        <section className="mb-16">
          <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8 mb-8">
            <h2 className="text-2xl font-bold text-white mb-6">Our guarantee to you</h2>
            
            <div className="space-y-6">
              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center">
                    <svg className="w-5 h-5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white mb-2">14-day refund window</h3>
                  <p className="text-slate-400">
                    For both DFY builds and subscriptions, you have 14 days from purchase to request a full refund. No lengthy forms or justifications required.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center">
                    <svg className="w-5 h-5 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white mb-2">No questions asked</h3>
                  <p className="text-slate-400">
                    If you're not satisfied for any reason, just email <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> and we'll process your refund within 3-5 business days.
                  </p>
                </div>
              </div>

              <div className="flex gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-full bg-violet-500/20 flex items-center justify-center">
                    <svg className="w-5 h-5 text-violet-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white mb-2">Keep the work</h3>
                  <p className="text-slate-400">
                    For DFY builds: If you request a refund within 14 days, you can keep the workflows we've already built. They're yours, even if you get your money back.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* How to Request */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">How to request a refund</h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-emerald-400">1</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Email us</h3>
              <p className="text-sm text-slate-400">
                Send an email to <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> with "Refund Request" in the subject line
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-blue-500/20 border border-blue-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-blue-400">2</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">We confirm</h3>
              <p className="text-sm text-slate-400">
                We'll respond within 24 hours to confirm your refund and cancel any active subscriptions
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-violet-500/20 border border-violet-500/30 flex items-center justify-center">
                <span className="text-2xl font-bold text-violet-400">3</span>
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Get refunded</h3>
              <p className="text-sm text-slate-400">
                Your refund will be processed to your original payment method within 3-5 business days
              </p>
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="mb-16">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">Guarantee FAQ</h2>
          
          <div className="space-y-4">
            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-white mb-2">Does this apply to both DFY and subscriptions?</h3>
              <p className="text-slate-400 text-sm">
                Yes. Both one-time DFY builds and monthly/yearly subscriptions are covered by our 14-day money-back guarantee.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-white mb-2">What if I'm past the 14-day window?</h3>
              <p className="text-slate-400 text-sm">
                We still want to help. Email us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> and we'll work with you to find a solution — whether that's fixing issues, upgrading/downgrading, or providing partial credit.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-white mb-2">Can I really keep the workflows if I get a refund?</h3>
              <p className="text-slate-400 text-sm">
                Yes, for DFY builds. If you request a refund within 14 days, any workflows we've already delivered are yours to keep. We believe in delivering value even if things don't work out.
              </p>
            </div>

            <div className="rounded-xl bg-slate-900/50 border border-slate-800 p-6">
              <h3 className="text-lg font-bold text-white mb-2">How long does the refund take?</h3>
              <p className="text-slate-400 text-sm">
                We process refunds within 24 hours of your request. Depending on your bank or payment provider, it may take 3-5 business days for the funds to appear in your account.
              </p>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="text-center py-12 px-6 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30">
          <h2 className="text-2xl font-bold text-white mb-4">
            Ready to try Levqor risk-free?
          </h2>
          <p className="text-slate-400 mb-6 max-w-xl mx-auto">
            Join teams automating with confidence, backed by our 14-day money-back guarantee.
          </p>
          <Link
            href="/pricing"
            className="inline-block px-10 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all shadow-2xl"
          >
            View Pricing
          </Link>
        </section>
      </div>
    </main>
  );
}
