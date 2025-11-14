import Link from "next/link";

export default function SecurityPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Security</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed mb-8">
          Security and data protection are foundational to Levqor. We implement industry best practices:
        </p>

        <section className="space-y-4">
          <ul className="list-disc list-inside space-y-3 text-slate-300 ml-4">
            <li>HTTPS everywhere</li>
            <li>Role-based access</li>
            <li>Audit logging</li>
            <li>Monitoring</li>
            <li>Rate-limits</li>
            <li>Encryption at rest and in transit</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <p className="text-slate-300 text-sm leading-relaxed">
            For security concerns or to report a vulnerability, contact{" "}
            <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">
              security@levqor.ai
            </a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/gdpr" className="text-emerald-400 hover:underline">GDPR Compliance</Link>
            <Link href="/subprocessors" className="text-emerald-400 hover:underline">Subprocessors</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
