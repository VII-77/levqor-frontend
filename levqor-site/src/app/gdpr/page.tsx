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
