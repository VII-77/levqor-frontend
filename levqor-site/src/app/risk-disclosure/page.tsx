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
          <h2 className="text-2xl font-bold text-white">⚠️ High-Risk Data Prohibited</h2>
          <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-6 space-y-4">
            <p className="text-slate-300 leading-relaxed font-semibold">
              Levqor does NOT automate:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li><strong className="text-white">Medical or health decisions</strong> - No diagnosis, treatment, prescriptions, or health data processing</li>
              <li><strong className="text-white">Legal workflows or document creation</strong> - No legal advice, contracts, or legal reasoning</li>
              <li><strong className="text-white">Financial advice or investment decisions</strong> - No tax advice, credit scoring, trading signals, or loan decisions</li>
              <li><strong className="text-white">Anything involving personal health, taxes, credit, or regulated decisions</strong></li>
            </ul>
            <p className="text-slate-300 leading-relaxed mt-4">
              Your workflow must not contain high-risk or regulated data.
            </p>
          </div>
        </section>

        <section className="mt-8 space-y-4">
          <h2 className="text-2xl font-bold text-white">What Levqor Will NOT Process or Automate</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 space-y-4">
            <div>
              <h3 className="text-lg font-semibold text-red-300 mb-2">🏥 Medical & Healthcare</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4">
                <li>Medical decisions, health data, or diagnosis assistance</li>
                <li>Treatment recommendations or prescription management</li>
                <li>Patient records or clinical workflows</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-red-300 mb-2">⚖️ Legal Services</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4">
                <li>Legal reasoning, legal workflows, or legal document generation</li>
                <li>Contract drafting or legal consultation</li>
                <li>Litigation support or case management</li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-red-300 mb-2">💰 Financial & Investment</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4">
                <li>Financial recommendations, credit scoring, lending, or investment decisions</li>
                <li>Tax advice, tax return preparation, or tax filing</li>
                <li>Trading signals or portfolio management</li>
              </ul>
            </div>
            
            <p className="text-slate-300 leading-relaxed font-semibold mt-6">
              Any workflow that could materially impact health, legal standing, or financial status is automatically rejected at the system level.
            </p>
          </div>
        </section>

        <section className="mt-8 space-y-4">
          <h2 className="text-2xl font-bold text-white">Enforcement & Error Response</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 space-y-4">
            <p className="text-slate-300 leading-relaxed">
              All workflow submissions are automatically scanned for prohibited content. If high-risk keywords are detected, you'll receive an immediate error response:
            </p>
            
            <div className="bg-slate-950 border border-slate-700 rounded-lg p-4 font-mono text-sm">
              <pre className="text-red-400">{`{
  "ok": false,
  "category": "high_risk_data",
  "error": "This workflow cannot be created because it 
           contains restricted medical, legal, or financial 
           content."
}`}</pre>
            </div>
            
            <p className="text-slate-300 leading-relaxed">
              All blocked attempts are logged for compliance monitoring and security purposes.
            </p>
          </div>
        </section>

        <section className="mt-8 space-y-4">
          <h2 className="text-2xl font-bold text-white">Why This Policy Exists</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 space-y-4">
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Required for GDPR, UK GDPR, ICO guidance on automated decision making.</strong> The Information Commissioner's Office provides strict guidance on processing regulated data and automated decisions that could significantly affect individuals.
            </p>
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Prevents illegal processing of regulated data.</strong> Medical, legal, and financial services require specific licenses and regulatory compliance that Levqor does not possess.
            </p>
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Protects Levqor from medical/legal/financial liability.</strong> Automated decisions in these domains carry significant legal and financial risk for both the service provider and users.
            </p>
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Required before public launch.</strong> This policy is a mandatory safeguard for operating a compliant SaaS automation platform.
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
