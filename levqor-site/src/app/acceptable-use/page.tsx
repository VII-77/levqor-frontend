import Link from "next/link";

export default function AcceptableUsePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Acceptable Use Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed">
          You agree NOT to use Levqor to:
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Prohibited Use</h2>
          <ul className="list-disc list-inside space-y-3 text-slate-300 ml-4">
            <li>Spam</li>
            <li>Fraud</li>
            <li>Harassment</li>
            <li>Scraping protected content</li>
            <li>Bypassing security</li>
            <li>Illegal data processing</li>
            <li>Automating harmful behaviour</li>
            <li>Deepfakes of real individuals</li>
          </ul>
        </section>

        <section className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-6 mt-8 space-y-4">
          <h2 className="text-2xl font-bold text-white">🚫 High-Risk Data Prohibited</h2>
          <p className="text-slate-300 leading-relaxed">
            You must NOT use Levqor to automate workflows involving:
          </p>
          <ul className="list-disc list-inside space-y-3 text-slate-300 ml-4">
            <li><strong className="text-white">Medical or clinical workflows</strong> - No diagnosis, treatment recommendations, prescriptions, or health data processing</li>
            <li><strong className="text-white">Legal advice automation</strong> - No legal reasoning, contract generation, or legal document creation</li>
            <li><strong className="text-white">Financial advice or investment decisions</strong> - No automated trading, credit scoring, lending decisions, or tax advice</li>
            <li><strong className="text-white">Safety-critical control systems</strong> - No transport, emergency services, or critical infrastructure automation</li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-4">
            All workflow submissions are automatically scanned. Workflows containing prohibited content will be immediately rejected.
          </p>
          <p className="text-slate-300 leading-relaxed">
            For more details, see our <Link href="/risk-disclosure" className="text-emerald-400 hover:underline">Risk Disclosure</Link> page.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <p className="text-slate-300 leading-relaxed">
            Violations may result in suspension.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/fair-use" className="text-emerald-400 hover:underline">Fair Use Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
