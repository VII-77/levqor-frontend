import Link from "next/link";

export default function SLAPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Service Level Agreement (SLA)</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Uptime</h2>
          <p className="text-slate-300 leading-relaxed">
            Target uptime: 99.5%
          </p>
          <p className="text-slate-300 leading-relaxed">
            Maintenance windows announced 24h in advance.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Emergency maintenance may occur when required.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Subscription Plan Response Times</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: No SLA</li>
            <li>Growth: 48h response</li>
            <li>Pro: 24h response</li>
            <li>Business: 12h response + dedicated support</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. DFY Delivery</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>1 workflow → 48 hours</li>
            <li>3 workflows → 3–4 days</li>
            <li>7 workflows → 7 days</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Exclusions</h2>
          <p className="text-slate-300 leading-relaxed">
            Force majeure, upstream outages, DDoS, rate-limits.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Credits</h2>
          <p className="text-slate-300 leading-relaxed">
            Service credits may be granted for prolonged outages.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Contact</h2>
          <p className="text-slate-300 leading-relaxed">
            Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
