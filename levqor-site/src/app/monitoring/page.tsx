import Link from "next/link";

export default function MonitoringPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Automatic Workflow Monitoring</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">How Monitoring Works</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Uptime monitoring for all workflows</li>
            <li>Error tracking and logging</li>
            <li>Performance metrics collection</li>
            <li>Usage analytics</li>
            <li>Automated incident alerts</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Error Detection</h2>
          <p className="text-slate-300 leading-relaxed">
            Real-time error detection for all workflow executions.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Automatic alerts for critical failures.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Error logs retained for 30 days.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Auto-Retries</h2>
          <p className="text-slate-300 leading-relaxed">
            Failed workflows automatically retry up to 3 times.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Exponential backoff between retries (1min, 5min, 15min).
          </p>
          <p className="text-slate-300 leading-relaxed">
            Manual intervention available for persistent failures.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">What Users Can Expect</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Email notifications for workflow failures (Pro+ plans)</li>
            <li>Dashboard visibility into execution history</li>
            <li>Performance metrics and success rates</li>
            <li>Proactive issue detection and resolution</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
            <Link href="/incident-response" className="text-emerald-400 hover:underline">Incident Response</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
