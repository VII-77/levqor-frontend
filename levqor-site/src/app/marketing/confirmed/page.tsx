import Link from "next/link";

export default function MarketingConfirmedPage() {
  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl text-center">
          <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          
          <h1 className="text-3xl font-bold text-white mb-4">Subscription Confirmed!</h1>
          <p className="text-slate-300 mb-6">
            Thank you for confirming your subscription to Levqor updates. You'll now receive:
          </p>

          <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-6 mb-6 text-left">
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">•</span>
                <span>Product updates and new features</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">•</span>
                <span>Tips and best practices for workflow automation</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">•</span>
                <span>Exclusive offers and early access opportunities</span>
              </li>
            </ul>
          </div>

          <p className="text-sm text-slate-400 mb-6">
            You can unsubscribe at any time using the link in any email we send you.
          </p>

          <Link
            href="/"
            className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
          >
            Back to home →
          </Link>
        </div>
      </div>
    </main>
  );
}
