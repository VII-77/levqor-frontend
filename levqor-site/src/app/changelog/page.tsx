import Link from "next/link";

export default function ChangelogPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Changelog</h1>
        <p className="text-slate-400 mb-12">
          Product updates, fixes, and improvements
        </p>

        <section className="space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <div className="flex items-start justify-between mb-3">
              <h3 className="text-xl font-bold text-white">v1.0.0 - Genesis Launch</h3>
              <span className="text-sm text-slate-500">{new Date().toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" })}</span>
            </div>
            <ul className="space-y-2 text-slate-300 text-sm">
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">+</span>
                <span>Dual pricing model (DFY + Subscriptions)</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">+</span>
                <span>Stripe checkout integration</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">+</span>
                <span>Comprehensive legal framework (20 pages)</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">+</span>
                <span>UK/GDPR compliance</span>
              </li>
            </ul>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/" className="text-emerald-400 hover:underline">Home</Link>
            <Link href="/pricing" className="text-emerald-400 hover:underline">Pricing</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
