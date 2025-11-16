import Link from "next/link";

export const metadata = {
  title: "Owner Handbook - Levqor Internal Documentation",
  description: "Internal documentation for Levqor system architecture, EchoPilot engine, and operational guides.",
  robots: "noindex, nofollow",
};

export default function OwnerHandbookPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-5xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-12">
          <div className="inline-flex items-center gap-2 rounded-full border border-amber-500/40 bg-amber-500/10 px-3 py-1 text-xs font-medium text-amber-200 mb-6">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Owner/Administrator Only
          </div>
          <h1 className="text-4xl font-bold mb-4 text-white">
            Levqor Owner Handbook
          </h1>
          <p className="text-xl text-slate-400">
            Internal system architecture, EchoPilot AI engine documentation, and operational guides for administrators.
          </p>
        </div>

        {/* Warning Notice */}
        <div className="bg-amber-900/20 border border-amber-500/30 rounded-lg p-6 mb-12">
          <div className="flex gap-3">
            <svg className="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div>
              <h3 className="font-bold text-white mb-2">Confidential - Internal Use Only</h3>
              <p className="text-sm text-amber-200">
                This page contains sensitive system architecture information. Do not share this URL with customers or external parties. This documentation is for owner/administrator reference only.
              </p>
            </div>
          </div>
        </div>

        {/* EchoPilot Engine Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white">EchoPilot AI Engine</h2>
          
          <div className="prose prose-invert max-w-none space-y-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-3">What is EchoPilot?</h3>
              <p className="text-slate-300 mb-4">
                <strong>EchoPilot AI engine</strong> is the internal automation and monitoring system that powers Levqor under the hood. It's NOT a separate product or public brand—it's the intelligence layer that keeps Levqor running smoothly 24/7.
              </p>
              <p className="text-slate-300">
                Think of it as Levqor's nervous system: constantly checking health, monitoring performance, detecting anomalies, and alerting you when something needs attention.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-4">What EchoPilot Does</h3>
              <ul className="space-y-3">
                <li className="flex gap-3">
                  <span className="text-emerald-400 flex-shrink-0 mt-1">✓</span>
                  <div>
                    <strong className="text-white">Health Monitoring</strong>
                    <p className="text-slate-400 text-sm">Checks backend, database, and API endpoints every 5 minutes to ensure everything is operational</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="text-emerald-400 flex-shrink-0 mt-1">✓</span>
                  <div>
                    <strong className="text-white">Stripe Integration Checks</strong>
                    <p className="text-slate-400 text-sm">Verifies Stripe API connectivity, webhook status, and payment processing health</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="text-emerald-400 flex-shrink-0 mt-1">✓</span>
                  <div>
                    <strong className="text-white">Database Stability Monitoring</strong>
                    <p className="text-slate-400 text-sm">Tracks connection pool health, query performance, and prevents stale connections</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="text-emerald-400 flex-shrink-0 mt-1">✓</span>
                  <div>
                    <strong className="text-white">Scheduler Monitoring</strong>
                    <p className="text-slate-400 text-sm">Ensures 15+ automated jobs (health checks, intelligence cycles, reporting) are running correctly</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="text-emerald-400 flex-shrink-0 mt-1">✓</span>
                  <div>
                    <strong className="text-white">Anomaly Detection</strong>
                    <p className="text-slate-400 text-sm">AI-powered detection of unusual patterns in system metrics and user behavior</p>
                  </div>
                </li>
                <li className="flex gap-3">
                  <span className="text-emerald-400 flex-shrink-0 mt-1">✓</span>
                  <div>
                    <strong className="text-white">Automated Audit Reports</strong>
                    <p className="text-slate-400 text-sm">Generates comprehensive health reports, cost analysis, and system status summaries</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* System Architecture Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white">System Architecture</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">Backend (Flask + Python)</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>• Production URL: <code className="text-emerald-400">https://api.levqor.ai</code></li>
                <li>• Direct URL: <code className="text-emerald-400">https://levqor-backend.replit.app</code></li>
                <li>• Framework: Flask + SQLAlchemy</li>
                <li>• Scheduler: APScheduler (19+ jobs)</li>
                <li>• Database: PostgreSQL (Neon) + SQLite (dev)</li>
              </ul>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">Frontend (Next.js 14)</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>• Production URL: <code className="text-emerald-400">https://www.levqor.ai</code></li>
                <li>• Platform: Vercel</li>
                <li>• Framework: Next.js 14 (App Router)</li>
                <li>• Auth: NextAuth v4</li>
                <li>• Pages: 114 routes</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Key Reports Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white">EchoPilot Reports & Documentation</h2>
          
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg overflow-hidden">
            <table className="w-full">
              <thead className="bg-slate-800/50">
                <tr className="border-b border-slate-700">
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Report Name</th>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Purpose</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">ECHOPILOT-FINAL-HEALTH-SUMMARY.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Executive summary of system health (backend, API, Stripe, DB, scheduler)</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">ECHOPILOT-FINAL-HEALTH-REPORT.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Detailed technical health report with all endpoint checks</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">ECHOPILOT-HEALTH-INVENTORY.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Complete inventory of all monitoring jobs and schedules</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">LEVQOR-LAUNCH-DECISION.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Production readiness assessment and launch decision report</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">BRUTAL-AUDIT-REPORT.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Comprehensive system audit identifying issues and risks</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">FRONTEND-TRANSFORMATION-COMPLETE.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Documentation of 26-page marketing website transformation</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 text-sm font-mono text-emerald-400">FRONTEND-AUTOMATION-REPORT.md</td>
                  <td className="px-6 py-4 text-sm text-slate-300">Frontend build verification and legal compliance check</td>
                </tr>
              </tbody>
            </table>
          </div>

          <p className="text-sm text-slate-400 mt-4">
            <strong>Location:</strong> All reports are stored in the root directory of the Replit project. They are markdown files generated by EchoPilot's monitoring and audit systems.
          </p>
        </section>

        {/* Monitoring & Error Tracking Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white">Monitoring & Error Tracking</h2>
          
          <div className="space-y-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">Sentry Error Tracking</h3>
              <p className="text-slate-300 mb-4">
                Error tracking is intended to be handled via Sentry for both frontend and backend.
              </p>
              <div className="bg-amber-900/20 border border-amber-500/30 rounded px-4 py-3">
                <p className="text-sm text-amber-200">
                  <strong>Current Status:</strong> Sentry DSN may be misconfigured. Errors will not appear in Sentry dashboard until the DSN is updated with a valid full URL (not just a token).
                </p>
              </div>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">EchoPilot Automated Monitoring</h3>
              <ul className="space-y-2 text-sm text-slate-300">
                <li>• <strong>Health checks:</strong> Every 5 minutes</li>
                <li>• <strong>Intelligence monitoring:</strong> Every 15 minutes</li>
                <li>• <strong>Synthetic endpoint checks:</strong> Every 15 minutes</li>
                <li>• <strong>Alert threshold checks:</strong> Every 5 minutes</li>
                <li>• <strong>Weekly governance reports:</strong> Sundays at midnight</li>
                <li>• <strong>Daily cost collection:</strong> Daily at 1:00 AM UTC</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Backend API Endpoints Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white">Key Backend Endpoints</h2>
          
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-lg font-bold text-white mb-4">Public Endpoints</h3>
            <ul className="space-y-2 text-sm font-mono">
              <li className="text-slate-300"><span className="text-emerald-400">GET</span> /health — System health check</li>
              <li className="text-slate-300"><span className="text-blue-400">POST</span> /api/support/public — Public support AI chat</li>
              <li className="text-slate-300"><span className="text-blue-400">POST</span> /api/support/private — Private support AI chat (authenticated)</li>
              <li className="text-slate-300"><span className="text-blue-400">POST</span> /api/support/escalate — Create support ticket</li>
              <li className="text-slate-300"><span className="text-emerald-400">GET</span> /api/support/tickets — List support tickets</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 mt-6">
            <h3 className="text-lg font-bold text-white mb-4">Stripe Webhooks</h3>
            <ul className="space-y-2 text-sm font-mono">
              <li className="text-slate-300"><span className="text-blue-400">POST</span> /api/webhooks/stripe/checkout-completed — Handle successful payments</li>
              <li className="text-slate-300"><span className="text-emerald-400">GET</span> /api/stripe/check — Verify Stripe connectivity</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 mt-6">
            <h3 className="text-lg font-bold text-white mb-4">Internal/Scheduler Endpoints</h3>
            <ul className="space-y-2 text-sm font-mono">
              <li className="text-slate-300"><span className="text-blue-400">POST</span> /internal/daily-email-tasks — Scheduled email tasks</li>
              <li className="text-slate-300"><span className="text-emerald-400">GET</span> /api/intelligence/status — Intelligence layer status</li>
              <li className="text-slate-300"><span className="text-emerald-400">GET</span> /api/insights/preview — Insights preview</li>
            </ul>
          </div>
        </section>

        {/* Quick Reference Section */}
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-6 text-white">Quick Reference</h2>
          
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">Support Contacts</h3>
              <ul className="space-y-2 text-sm">
                <li className="text-slate-300">General: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
                <li className="text-slate-300">Sales: <a href="mailto:sales@levqor.ai" className="text-emerald-400 hover:underline">sales@levqor.ai</a></li>
                <li className="text-slate-300">Privacy: <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a></li>
                <li className="text-slate-300">Legal: <a href="mailto:legal@levqor.ai" className="text-emerald-400 hover:underline">legal@levqor.ai</a></li>
              </ul>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-lg font-bold text-white mb-3">Critical URLs</h3>
              <ul className="space-y-2 text-sm">
                <li className="text-slate-300">Frontend: <a href="https://www.levqor.ai" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">www.levqor.ai</a></li>
                <li className="text-slate-300">API: <a href="https://api.levqor.ai" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">api.levqor.ai</a></li>
                <li className="text-slate-300">Backend Direct: <a href="https://levqor-backend.replit.app" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">levqor-backend.replit.app</a></li>
                <li className="text-slate-300">Stripe Dashboard: <a href="https://dashboard.stripe.com" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline">dashboard.stripe.com</a></li>
              </ul>
            </div>
          </div>
        </section>

        {/* Footer */}
        <div className="border-t border-slate-800 pt-8 mt-12">
          <div className="flex gap-6 text-sm">
            <Link href="/" className="text-emerald-400 hover:underline">← Back to Home</Link>
            <Link href="/dashboard" className="text-emerald-400 hover:underline">Dashboard</Link>
            <Link href="/admin/insights" className="text-emerald-400 hover:underline">Admin Insights</Link>
          </div>
          <p className="text-xs text-slate-500 mt-4">
            Last updated: November 16, 2025 • This page is not linked in public navigation and is for owner/administrator reference only.
          </p>
        </div>
      </div>
    </main>
  );
}
