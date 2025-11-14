import Link from "next/link";

export default function IncidentResponsePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Incident Response Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Detection</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Automated monitoring and alerting 24/7</li>
            <li>Manual reporting via support channels</li>
            <li>Security vulnerability disclosures</li>
            <li>Customer-reported issues</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Containment</h2>
          <ol className="list-decimal list-inside space-y-2 text-slate-300 ml-4">
            <li>Immediate isolation of affected systems</li>
            <li>Root cause analysis initiated</li>
            <li>Temporary workarounds deployed</li>
            <li>Evidence preservation for security incidents</li>
          </ol>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Notification Procedures</h2>
          <p className="text-slate-300 leading-relaxed">
            1-hour acknowledgement for all incidents.
          </p>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4 mt-3">
            <p className="text-slate-300 text-sm mb-2">
              <span className="font-semibold">Severity 1-2:</span> Immediate email notification + status page update
            </p>
            <p className="text-slate-300 text-sm mb-2">
              <span className="font-semibold">Severity 3:</span> Status page update within 2 hours
            </p>
            <p className="text-slate-300 text-sm">
              <span className="font-semibold">Severity 4:</span> Resolution notification only
            </p>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">72-Hour GDPR Breach Requirement</h2>
          <div className="bg-red-900/20 border border-red-800 rounded-lg p-4">
            <p className="text-slate-300 leading-relaxed mb-2">
              For personal data breaches, we will:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4 text-sm">
              <li>Notify affected users within 72 hours</li>
              <li>Report to ICO (Information Commissioner's Office) if applicable</li>
              <li>Provide details of breach type, scope, and impact</li>
              <li>Outline mitigation steps and remediation plan</li>
              <li>Offer support to affected customers</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Severity Levels</h2>
          
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-red-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-red-400 mb-2">Severity 1: Critical</h3>
              <p className="text-slate-300 text-sm">Complete service outage, data breach, security incident</p>
              <p className="text-slate-400 text-xs mt-2">Response: Immediate, 24/7</p>
            </div>

            <div className="bg-slate-900/50 border border-orange-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-orange-400 mb-2">Severity 2: High</h3>
              <p className="text-slate-300 text-sm">Major feature failure, significant performance degradation</p>
              <p className="text-slate-400 text-xs mt-2">Response: Within 2 hours</p>
            </div>

            <div className="bg-slate-900/50 border border-yellow-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-yellow-400 mb-2">Severity 3: Medium</h3>
              <p className="text-slate-300 text-sm">Partial feature issues, workflow errors</p>
              <p className="text-slate-400 text-xs mt-2">Response: Within 4 hours</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-slate-400 mb-2">Severity 4: Low</h3>
              <p className="text-slate-300 text-sm">Minor bugs, cosmetic issues</p>
              <p className="text-slate-400 text-xs mt-2">Response: Within 24 hours</p>
            </div>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Customer Communication Rules</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Status page updates every 30 minutes during incidents</li>
            <li>Email notifications for Severity 1-2 incidents</li>
            <li>Hourly updates during prolonged outages</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Post-Incident Reporting</h2>
          <p className="text-slate-300 leading-relaxed">
            Detailed post-incident reports within 48 hours of resolution.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Reports include:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Timeline of events</li>
            <li>Root cause analysis</li>
            <li>Impact assessment</li>
            <li>Remediation actions taken</li>
            <li>Preventive measures implemented</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
            <Link href="/support-policy" className="text-emerald-400 hover:underline">Support Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
