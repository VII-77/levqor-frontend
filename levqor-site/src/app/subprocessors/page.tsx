import Link from "next/link";

export default function SubprocessorsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Subprocessor List</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed mb-8">
          Levqor uses the following trusted third-party subprocessors to deliver our services:
        </p>

        <section className="space-y-4">
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-1">Stripe</h3>
              <p className="text-slate-400 text-sm">Payments</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-1">Vercel</h3>
              <p className="text-slate-400 text-sm">Hosting</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-1">Replit</h3>
              <p className="text-slate-400 text-sm">Backend</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-1">OpenAI</h3>
              <p className="text-slate-400 text-sm">Model inference</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-1">Google</h3>
              <p className="text-slate-400 text-sm">OAuth</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-1">Cloudflare</h3>
              <p className="text-slate-400 text-sm">DNS</p>
            </div>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <p className="text-slate-300 text-sm leading-relaxed">
            All subprocessors are selected for their strong data protection standards and compliance with UK GDPR. 
            We have appropriate data processing agreements in place with each provider.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/dpa" className="text-emerald-400 hover:underline">Data Processing Agreement</Link>
            <Link href="/gdpr" className="text-emerald-400 hover:underline">GDPR Compliance</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
