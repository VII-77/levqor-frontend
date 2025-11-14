import Link from "next/link";

export default function DataRequestsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Data Subject Requests</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Your Rights</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Right to access</li>
            <li>Right to rectification</li>
            <li>Right to erasure</li>
            <li>Right to restrict processing</li>
            <li>Right to data portability</li>
            <li>Right to object</li>
            <li>Right to withdraw consent</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Request Procedure</h2>
          <p className="text-slate-300 leading-relaxed">
            Submit via <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Identity verification required.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Response within 30 days (extendable to 60)
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/gdpr" className="text-emerald-400 hover:underline">GDPR Compliance</Link>
            <Link href="/dpa" className="text-emerald-400 hover:underline">Data Processing Agreement</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
