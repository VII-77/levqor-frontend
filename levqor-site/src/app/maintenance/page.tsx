import Link from "next/link";

export default function MaintenancePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Maintenance & Downtime Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Scheduled Maintenance Windows</h2>
          <p className="text-slate-300 leading-relaxed">
            Minor updates: Weekly (typically Sundays, 02:00-04:00 UTC)
          </p>
          <p className="text-slate-300 leading-relaxed">
            Major updates: Monthly (first Saturday, 02:00-06:00 UTC)
          </p>
          <p className="text-slate-300 leading-relaxed">
            Security updates: Immediately as required
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Expected Downtime</h2>
          <p className="text-slate-300 leading-relaxed">
            Typical maintenance window: 15-30 minutes
          </p>
          <p className="text-slate-300 leading-relaxed">
            Maximum scheduled downtime: 2 hours
          </p>
          <p className="text-slate-300 leading-relaxed">
            Emergency maintenance may occur when required with minimal notice.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Customer Notifications</h2>
          <p className="text-slate-300 leading-relaxed">
            Maintenance announced 24 hours in advance via email.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Status page updated during all maintenance windows.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Emergency maintenance communicated immediately.
          </p>
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
