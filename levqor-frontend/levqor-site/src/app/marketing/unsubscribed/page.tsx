import Link from "next/link";

export default function MarketingUnsubscribedPage() {
  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl text-center">
          <div className="w-16 h-16 bg-slate-700/50 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          
          <h1 className="text-3xl font-bold text-white mb-4">You've been unsubscribed</h1>
          <p className="text-slate-300 mb-6">
            You will no longer receive marketing emails or product updates from Levqor.
          </p>

          <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-6 mb-6">
            <p className="text-slate-400 text-sm">
              <strong className="text-white">Note:</strong> You'll still receive important account-related emails, 
              such as security alerts, password resets, billing receipts, and service notifications.
            </p>
          </div>

          <p className="text-sm text-slate-400 mb-6">
            Changed your mind? You can resubscribe anytime from your account settings.
          </p>

          <div className="flex gap-4 justify-center">
            <Link
              href="/"
              className="inline-block px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition"
            >
              Back to home
            </Link>
            <a
              href="mailto:support@levqor.ai"
              className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
            >
              Contact support
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}
