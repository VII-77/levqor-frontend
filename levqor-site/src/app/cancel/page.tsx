import Link from "next/link";

export default function CancelPage() {
  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
      <div className="max-w-2xl mx-auto text-center">
        {/* Cancel Icon */}
        <div className="mb-8 inline-flex items-center justify-center w-20 h-20 rounded-full bg-slate-800 border-2 border-slate-700">
          <svg className="w-10 h-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>

        {/* Cancel Message */}
        <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
          Payment cancelled
        </h1>
        
        <p className="text-xl text-slate-300 mb-8 leading-relaxed">
          No worries! Your payment was not processed. You can return to pricing whenever you're ready.
        </p>

        {/* Reassurance Box */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 mb-8 text-left">
          <h2 className="text-xl font-bold text-white mb-4">Still have questions?</h2>
          
          <div className="space-y-3 text-slate-300 text-sm">
            <p>
              If you cancelled because you had questions about our service, we're here to help:
            </p>
            <ul className="space-y-2 ml-4">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5">→</span>
                <span>Check our <Link href="/docs" className="text-emerald-400 hover:underline">documentation</Link> for technical details</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5">→</span>
                <span>Email us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-0.5">→</span>
                <span>Review our <Link href="/refunds" className="text-emerald-400 hover:underline">refund policy</Link> (14-day money-back guarantee)</span>
              </li>
            </ul>
          </div>
        </div>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link 
            href="/"
            className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition"
          >
            Back to homepage
          </Link>
          <Link 
            href="/pricing"
            className="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition shadow-lg"
          >
            View pricing again
          </Link>
        </div>
      </div>
    </main>
  );
}
