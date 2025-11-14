import Link from "next/link";

export default function SupportEscalationPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Support Escalation Matrix</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-2">Tier 1: Support Review</h3>
              <p className="text-slate-300 text-sm">Initial ticket triage and common issues</p>
              <p className="text-slate-400 text-xs mt-2">Channel: Email</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-400 mb-2">Tier 2: Engineer Response</h3>
              <p className="text-slate-300 text-sm">Technical issues and workflow debugging</p>
              <p className="text-slate-400 text-xs mt-2">Channel: Priority Email</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-purple-400 mb-2">Tier 3: Founder/CTO Escalation</h3>
              <p className="text-slate-300 text-sm">Critical system issues or major incidents</p>
              <p className="text-slate-400 text-xs mt-2">Channel: Emergency</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-amber-400 mb-2">Tier 4: Legal + Regulatory</h3>
              <p className="text-slate-300 text-sm">Compliance, data breaches, legal matters</p>
              <p className="text-slate-400 text-xs mt-2">Channel: Emergency escalation</p>
            </div>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/support-policy" className="text-emerald-400 hover:underline">Support Policy</Link>
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
