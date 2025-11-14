import Link from "next/link";

export default function GDPRPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">GDPR Compliance</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed mb-8">
          We comply with UK GDPR:
        </p>

        <section className="space-y-4">
          <ul className="list-disc list-inside space-y-3 text-slate-300 ml-4">
            <li>Lawful basis documented</li>
            <li>Data minimised</li>
            <li>Retention schedule applied</li>
            <li>Subprocessors audited</li>
            <li>Cookie consent applied</li>
            <li>Rights requests supported</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Lawful Basis for Processing</h2>
          <p className="text-slate-300 leading-relaxed mb-4">
            We process data under:
          </p>
          
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-2">Contractual Necessity</h3>
              <p className="text-slate-300 text-sm">Account data, workflows</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-400 mb-2">Legitimate Interests</h3>
              <p className="text-slate-300 text-sm">Monitoring, security</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-purple-400 mb-2">Explicit Consent</h3>
              <p className="text-slate-300 text-sm">Marketing, cookies</p>
            </div>
          </div>
        </section>

        <section className="space-y-4 mt-12">
          <h2 className="text-2xl font-bold text-white">Compliance Documentation</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <p className="text-slate-300 leading-relaxed mb-4">
              We maintain comprehensive internal documentation to demonstrate GDPR compliance, including:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li><strong>Record of Processing Activities (ROPA)</strong> - Documenting all data processing operations</li>
              <li><strong>Data Protection Impact Assessment (DPIA)</strong> - Evaluating risks for automation workflows</li>
              <li><strong>Legitimate Interest Assessment (LIA)</strong> - Justifying analytics and operational processing</li>
            </ul>
            <p className="text-slate-400 text-sm mt-4">
              These documents are available to enterprise customers, regulatory authorities, and data subjects upon request. 
              Contact <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a> for access.
            </p>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/dpa" className="text-emerald-400 hover:underline">Data Processing Agreement</Link>
            <Link href="/cookies" className="text-emerald-400 hover:underline">Cookie Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
