import Link from "next/link";

export default function HighRiskDataPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-6 mb-8">
          <h1 className="text-4xl font-bold text-red-400 mb-2">High-Risk Data Prohibition</h1>
          <p className="text-slate-300">
            Non-negotiable restrictions on prohibited workflow categories
          </p>
        </div>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">❌ Levqor Does NOT Automate</h2>
          <p className="text-slate-300 leading-relaxed">
            The following categories are <strong className="text-white">strictly prohibited</strong> and cannot be processed under any circumstances:
          </p>
          
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <ul className="space-y-3 text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold text-xl mt-0.5">•</span>
                <div>
                  <strong className="text-white">Medical data or healthcare decisions</strong>
                  <p className="text-slate-400 text-sm mt-1">
                    No diagnosis, treatment recommendations, prescription management, patient records, or health data processing
                  </p>
                </div>
              </li>
              
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold text-xl mt-0.5">•</span>
                <div>
                  <strong className="text-white">Financial advice or creditworthiness decisions</strong>
                  <p className="text-slate-400 text-sm mt-1">
                    No investment advice, credit scoring, lending decisions, tax advice, or trading signals
                  </p>
                </div>
              </li>
              
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold text-xl mt-0.5">•</span>
                <div>
                  <strong className="text-white">Legal advice or legal case workflows</strong>
                  <p className="text-slate-400 text-sm mt-1">
                    No legal reasoning, contract drafting, legal consultation, or litigation support
                  </p>
                </div>
              </li>
              
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold text-xl mt-0.5">•</span>
                <div>
                  <strong className="text-white">Criminal data or policing workflows</strong>
                  <p className="text-slate-400 text-sm mt-1">
                    No law enforcement data, criminal records, investigative workflows, or policing decisions
                  </p>
                </div>
              </li>
              
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold text-xl mt-0.5">•</span>
                <div>
                  <strong className="text-white">Biometric or genetic data</strong>
                  <p className="text-slate-400 text-sm mt-1">
                    No fingerprints, facial recognition, DNA data, or biometric identification
                  </p>
                </div>
              </li>
              
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold text-xl mt-0.5">•</span>
                <div>
                  <strong className="text-white">Anything regulated as high-risk under GDPR Article 9</strong>
                  <p className="text-slate-400 text-sm mt-1">
                    Includes special category data: racial/ethnic origin, political opinions, religious beliefs, trade union membership, sex life/sexual orientation
                  </p>
                </div>
              </li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">⚖️ Legal Consequences</h2>
          <div className="bg-yellow-950/20 border border-yellow-900/30 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              Attempting to automate these categories <strong className="text-white">violates our Terms of Service</strong> and will result in:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>Immediate workflow rejection with error message</li>
              <li>Account suspension without refund</li>
              <li>Termination of service for repeated violations</li>
              <li>Compliance logging and potential reporting to authorities</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Why This Policy Exists</h2>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">GDPR Compliance:</strong> GDPR Article 9 prohibits processing special category data without explicit legal basis and appropriate safeguards.
            </p>
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Regulatory Requirements:</strong> Medical, legal, and financial services require specific licenses and regulatory compliance that Levqor does not possess.
            </p>
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Liability Protection:</strong> Automated decisions in these domains carry significant legal and financial risk for both service providers and users.
            </p>
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Public Safety:</strong> High-risk data processing requires human oversight and cannot be delegated to automation alone.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Enforcement</h2>
          <p className="text-slate-300 leading-relaxed">
            All workflow submissions are automatically scanned for prohibited keywords and patterns. Violations are:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Detected in real-time during submission</li>
            <li>Logged for compliance monitoring</li>
            <li>Blocked immediately with error response</li>
            <li>Reviewed by compliance team for account action</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex flex-wrap gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/risk-disclosure" className="text-emerald-400 hover:underline">Risk Disclosure</Link>
            <Link href="/acceptable-use" className="text-emerald-400 hover:underline">Acceptable Use</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
