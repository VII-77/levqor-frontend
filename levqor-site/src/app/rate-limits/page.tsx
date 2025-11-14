import Link from "next/link";

export default function RateLimitsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Rate Limiting & Abuse Protection</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">API Call Limits</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: 1,000 API calls/day</li>
            <li>Growth: 10,000 API calls/day</li>
            <li>Pro: 50,000 API calls/day</li>
            <li>Business: 200,000 API calls/day</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Workflow Trigger Frequency</h2>
          <p className="text-slate-300 leading-relaxed">
            Maximum trigger frequency: 100 runs/hour per workflow.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Daily soft cap: 200 workflow runs/day (unlimited plans).
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Consequences for Abuse</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Automatic throttling after threshold breach</li>
            <li>Warning email notification</li>
            <li>Temporary suspension for repeated violations</li>
            <li>Account termination for severe abuse</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Requesting Higher Limits</h2>
          <p className="text-slate-300 leading-relaxed">
            Contact <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> for custom enterprise limits.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/fair-use" className="text-emerald-400 hover:underline">Fair Use Policy</Link>
            <Link href="/acceptable-use" className="text-emerald-400 hover:underline">Acceptable Use</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
