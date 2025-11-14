"use client";
import Link from "next/link";

export default function CallPage() {
  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">Levqor</Link>
        </nav>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Book a Call
          </h1>
          <p className="text-lg text-slate-400 max-w-2xl mx-auto">
            Schedule a 15-minute call to discuss your automation needs
          </p>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-12 text-center">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-blue-500/20 flex items-center justify-center">
            <svg className="w-10 h-10 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>

          <h2 className="text-2xl font-bold text-white mb-4">
            Calendly Integration Coming Soon
          </h2>
          <p className="text-slate-400 mb-8">
            For now, email us directly to schedule your call
          </p>

          <a
            href="mailto:sales@levqor.ai?subject=Book%20a%20Call&body=Hi,%0A%0AI'd%20like%20to%20schedule%20a%20call%20to%20discuss:%0A%0A[Your%20message%20here]"
            className="inline-block px-10 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition shadow-2xl"
          >
            Email sales@levqor.ai
          </a>

          <div className="mt-12 pt-8 border-t border-slate-800">
            <h3 className="text-lg font-bold text-white mb-4">What we'll discuss:</h3>
            <ul className="text-left max-w-md mx-auto space-y-2 text-slate-400">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Your current workflows and pain points</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Which automations would save you the most time</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Best DFY package for your needs</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Timeline and next steps</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}
