import Link from "next/link";

export default function CancellationPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Cancellation Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <p className="text-slate-300 leading-relaxed">
            Subscriptions cancel anytime.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Access remains until the billing cycle ends.
          </p>
          <p className="text-slate-300 leading-relaxed">
            We do not offer refunds for used periods.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Account Deletion</h2>
          <p className="text-slate-300 leading-relaxed">
            Send request to: <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Identity verification required.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Data deleted within 30 days except legal records.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
