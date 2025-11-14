import Link from "next/link";

export default function DataRequestsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Data Subject Requests</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Your Rights</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Right to access</li>
            <li>Right to rectification</li>
            <li>Right to erasure</li>
            <li>Right to restrict processing</li>
            <li>Right to data portability</li>
            <li>Right to object</li>
            <li>Right to withdraw consent</li>
          </ul>
        </section>

        <section className="bg-emerald-950/30 border-2 border-emerald-900/50 rounded-lg p-6 mt-8">
          <h2 className="text-2xl font-bold text-white mb-4">🔐 Self-Service Data Export</h2>
          <p className="text-slate-300 leading-relaxed mb-4">
            You can now request and download your personal data instantly using our Privacy Tools page. 
            This is the fastest way to exercise your right of access under GDPR Article 15.
          </p>
          <Link 
            href="/privacy-tools"
            className="inline-flex items-center gap-2 px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Go to Privacy Tools
          </Link>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Other Data Subject Requests</h2>
          <p className="text-slate-300 leading-relaxed">
            For other rights (rectification, erasure, restriction, portability, objection), please contact:
          </p>
          <p className="text-slate-300 leading-relaxed">
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline font-semibold">privacy@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Identity verification required for all requests. Response within 30 days (extendable to 60 days in complex cases).
          </p>
        </section>

        <section className="bg-red-950/20 border-2 border-red-900/50 rounded-lg p-6 mt-8">
          <h2 className="text-2xl font-bold text-white mb-4">🗑️ Automated Data Deletion</h2>
          <p className="text-slate-300 leading-relaxed mb-4">
            You can now delete your personal data instantly using the "Delete My Data (GDPR)" button in Privacy Tools. 
            This exercises your right to erasure under GDPR Article 17.
          </p>
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 mb-4">
            <h3 className="text-sm font-semibold text-amber-400 mb-2">What gets deleted:</h3>
            <ul className="space-y-1 text-sm text-slate-300 ml-4">
              <li>• Workflows, jobs, and automation logs</li>
              <li>• API keys and developer tools</li>
              <li>• Referral and partnership data</li>
              <li>• Account information (anonymized)</li>
            </ul>
          </div>
          <div className="bg-blue-950/30 border border-blue-900/50 rounded-lg p-4 mb-4">
            <h3 className="text-sm font-semibold text-blue-300 mb-2">What's preserved (legal requirement):</h3>
            <ul className="space-y-1 text-sm text-slate-300 ml-4">
              <li>• Billing records and invoices (7 years)</li>
              <li>• Stripe payment history (financial audit requirements)</li>
            </ul>
          </div>
          <Link 
            href="/privacy-tools"
            className="inline-flex items-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Go to Privacy Tools
          </Link>
          <p className="text-xs text-slate-400 mt-3">
            Automated cleanup also runs daily, deleting expired records based on our retention policy.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/privacy-tools" className="text-emerald-400 hover:underline font-semibold">Privacy Tools</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/gdpr" className="text-emerald-400 hover:underline">GDPR Compliance</Link>
            <Link href="/dpa" className="text-emerald-400 hover:underline">Data Processing Agreement</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
