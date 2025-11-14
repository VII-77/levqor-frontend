import Link from "next/link";

export default function PricingChangesPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Pricing Change Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Notice Period</h2>
          <p className="text-slate-300 leading-relaxed">
            30 days advance notice for all pricing changes.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Email notification sent to all affected customers.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Grandfathering Rules</h2>
          <p className="text-slate-300 leading-relaxed">
            Existing customers maintain current pricing for their active subscription term.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Annual subscribers locked in for the full year.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Monthly subscribers receive current pricing until next renewal after notice period.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Billing Cycle Effects</h2>
          <p className="text-slate-300 leading-relaxed">
            Price changes apply at next billing cycle after notice period.
          </p>
          <p className="text-slate-300 leading-relaxed">
            No mid-cycle price adjustments.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Customers may cancel before new pricing takes effect without penalty.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Your Options</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Continue at new pricing</li>
            <li>Downgrade to lower tier</li>
            <li>Switch to annual billing (locks in rate for 12 months)</li>
            <li>Cancel subscription before new pricing takes effect</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/pricing" className="text-emerald-400 hover:underline">Current Pricing</Link>
            <Link href="/billing" className="text-emerald-400 hover:underline">Billing Policy</Link>
            <Link href="/cancellation" className="text-emerald-400 hover:underline">Cancellation</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
