import Link from "next/link";

export default function RiskDisclosurePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Risk Disclosure</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <p className="text-slate-300 leading-relaxed">
            Automation can fail due to API outages, human error, external system changes, or rate-limits.
          </p>
          <p className="text-slate-300 leading-relaxed">
            We provide monitoring and fixes but cannot fully eliminate third-party risks.
          </p>
        </section>

        <section className="mt-12 space-y-4">
          <h2 className="text-2xl font-bold text-white">High-Risk Automation Restrictions</h2>
          <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-6 space-y-4">
            <p className="text-slate-300 leading-relaxed font-semibold">
              To protect users and comply with UK GDPR, PECR, ICO guidance, and general risk management requirements, Levqor does not permit automation of the following:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>Medical advice, diagnosis, treatment, or health-related decision-making</li>
              <li>Legal advice, contract generation, or legal document preparation</li>
              <li>Tax advice, financial planning, investment recommendations, or trading signals</li>
              <li>Processing of data involving minors (under 18 years old)</li>
              <li>Special category data including race, ethnicity, religion, biometrics, or health data</li>
              <li>Regulated professional services requiring licensed practitioners</li>
            </ul>
            <p className="text-slate-300 leading-relaxed">
              These restrictions are mandatory and enforced at the technical level. Any workflows containing prohibited content will be automatically rejected.
            </p>
            <p className="text-slate-300 leading-relaxed">
              This policy protects both users and Levqor from liability associated with high-risk automated decision-making in sensitive domains.
            </p>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
