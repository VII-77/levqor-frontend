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
          <h2 className="text-2xl font-bold text-white">Payment Failure Policy</h2>
          <p className="text-slate-300 leading-relaxed">
            If a payment fails, we'll automatically retry and notify you via email. Here's our dunning process:
          </p>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <div>
              <h3 className="font-semibold text-emerald-400">Day 1: Initial Notice</h3>
              <p className="text-slate-400 text-sm mt-1">
                You'll receive an email notification. Service remains active. Update your payment method to avoid interruption.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-amber-400">Day 7: Warning Notice</h3>
              <p className="text-slate-400 text-sm mt-1">
                Second email sent. Service is at risk. Update payment within 7 days to prevent service pause.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-red-400">Day 14: Final Notice</h3>
              <p className="text-slate-400 text-sm mt-1">
                Final email sent. Service will be paused within 3 days if payment is not received.
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-red-500">Day 17+: Suspension</h3>
              <p className="text-slate-400 text-sm mt-1">
                Account suspended. All workflows paused. API access disabled. Update payment to restore service immediately.
              </p>
            </div>
          </div>
          <p className="text-slate-300 leading-relaxed mt-4">
            <strong className="text-white">Important:</strong> You can update your payment method at any time to prevent service interruption. 
            Once payment is received, your account is automatically restored.
          </p>
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
