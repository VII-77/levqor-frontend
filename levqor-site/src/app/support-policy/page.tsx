import Link from "next/link";

export default function SupportPolicyPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Support Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Response Times</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: 24–48h</li>
            <li>Growth: 12–24h</li>
            <li>Pro: &lt;12h</li>
            <li>Business: priority queue, same-day</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Support Channels</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Email (primary)</li>
            <li>Dashboard chat (when activated)</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Contact</h2>
          <p className="text-slate-300 leading-relaxed">
            Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
            <Link href="/delivery" className="text-emerald-400 hover:underline">Delivery</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
