import Link from "next/link";

export default function AIDisclosurePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">AI Disclosure</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">AI Usage</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor uses AI to provide workflow generation, optimisation, debugging and monitoring.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Outputs may occasionally be inaccurate.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Human review recommended for critical processes.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">AI Limitations</h2>
          <p className="text-slate-300 leading-relaxed">
            AI predictions are probabilistic.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Not suitable for life-critical or financial-trading decisions.
          </p>
          <p className="text-slate-300 leading-relaxed">
            We do not guarantee accuracy or correctness of AI output.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/risk-disclosure" className="text-emerald-400 hover:underline">Risk Disclosure</Link>
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
