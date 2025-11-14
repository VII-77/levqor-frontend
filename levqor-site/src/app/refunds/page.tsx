import Link from "next/link";

export default function RefundsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Refund Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">14-Day Refund Policy</h2>
          <p className="text-slate-300 leading-relaxed">
            Refunds available within 14 days if:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>No deliverables were created</li>
            <li>No workflow was delivered</li>
            <li>No automation was executed</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">DFY One-Time Builds</h2>
          <p className="text-slate-300 leading-relaxed">
            DFY builds are non-refundable once work begins.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Subscriptions</h2>
          <p className="text-slate-300 leading-relaxed">
            Refunds are not provided for periods already billed.
          </p>
          <p className="text-slate-300 leading-relaxed">
            You may cancel anytime; service continues until period ends.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Failed Payments</h2>
          <p className="text-slate-300 leading-relaxed">
            We may pause service until payment is resolved.
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
          </div>
        </div>
      </div>
    </main>
  );
}
