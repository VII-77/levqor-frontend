import Link from "next/link";

export default function BillingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Billing Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Billing Cycles</h2>
          <p className="text-slate-300 leading-relaxed">
            Subscriptions are billed monthly or annually based on your selected plan.
          </p>
          <p className="text-slate-300 leading-relaxed">
            DFY builds are one-time payments.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Pro-Rata Rules</h2>
          <p className="text-slate-300 leading-relaxed">
            Upgrades are pro-rated for the remainder of your billing period.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Downgrades take effect at the next billing cycle.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Failed Payment Retries</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>1st attempt: immediate retry</li>
            <li>2nd attempt: 3 days</li>
            <li>3rd attempt: 7 days</li>
            <li>Account restricted after 14 days</li>
            <li>Cancellation after 30 days</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Invoice Timing</h2>
          <p className="text-slate-300 leading-relaxed">
            Invoices are sent immediately upon successful payment.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Recurring invoices are sent at the start of each billing period.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Chargeback Handling</h2>
          <p className="text-slate-300 leading-relaxed">
            Chargebacks result in immediate account suspension.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Contact support to resolve disputes before initiating chargebacks.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
            <Link href="/account-suspension" className="text-emerald-400 hover:underline">Account Suspension</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
