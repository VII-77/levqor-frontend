import Link from "next/link";

export default function BusinessContinuityPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Business Continuity & Disaster Recovery</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Backup Datacenters</h2>
          <p className="text-slate-300 leading-relaxed">
            Daily backups stored across multiple EU-based data centers.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Redundant infrastructure across multiple availability zones.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Geographic distribution ensures resilience.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Recovery Objectives</h2>
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-2">RTO (Recovery Time Objective)</h3>
              <p className="text-slate-300 text-sm">Target: &lt;12 hours</p>
              <p className="text-slate-400 text-xs mt-2">Time to restore full service after disaster</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-400 mb-2">RPO (Recovery Point Objective)</h3>
              <p className="text-slate-300 text-sm">Target: &lt;6 hours</p>
              <p className="text-slate-400 text-xs mt-2">Maximum acceptable data loss window</p>
            </div>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Failover Process</h2>
          <ol className="list-decimal list-inside space-y-2 text-slate-300 ml-4">
            <li>Automatic detection of primary system failure</li>
            <li>Traffic rerouted to standby infrastructure within minutes</li>
            <li>Database restored from latest backup</li>
            <li>Service verification and testing</li>
            <li>Customer notification of restoration</li>
          </ol>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Worst-Case Continuity Plan</h2>
          <div className="bg-amber-900/20 border border-amber-800 rounded-lg p-4">
            <p className="text-slate-300 leading-relaxed mb-3">
              In the event of catastrophic failure affecting all systems:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>Customer notification within 1 hour via email and status page</li>
              <li>Emergency operations center activated</li>
              <li>Restoration from offsite backups initiated</li>
              <li>Regular status updates every 2 hours</li>
              <li>Post-incident report within 48 hours of resolution</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">DR Testing</h2>
          <p className="text-slate-300 leading-relaxed">
            Disaster recovery plan tested quarterly.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Full failover exercises conducted annually.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Results documented and plan updated accordingly.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/backups" className="text-emerald-400 hover:underline">Backup Policy</Link>
            <Link href="/incident-response" className="text-emerald-400 hover:underline">Incident Response</Link>
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
