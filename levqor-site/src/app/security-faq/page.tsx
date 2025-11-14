import Link from "next/link";

export default function SecurityFAQPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Security FAQ</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-lg font-bold text-white mb-3">Q: Is my data encrypted?</h3>
            <p className="text-slate-300 text-sm">A: Yes, in transit (TLS) and at rest.</p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-lg font-bold text-white mb-3">Q: Who has access to my workflows?</h3>
            <p className="text-slate-300 text-sm">A: Only authorised engineers, and only when necessary.</p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-lg font-bold text-white mb-3">Q: What about OpenAI?</h3>
            <p className="text-slate-300 text-sm">A: Your data is processed securely and not used to train public models.</p>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/subprocessors" className="text-emerald-400 hover:underline">Subprocessors</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
