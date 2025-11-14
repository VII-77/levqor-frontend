import Link from "next/link";

export default function AccountSuspensionPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Account Suspension & Reactivation</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Suspension Reasons</h2>
          <p className="text-slate-300 leading-relaxed">
            Accounts may be suspended for:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Failed billing</li>
            <li>Abuse of service</li>
            <li>Fraud detection</li>
            <li>Chargebacks</li>
            <li>Violation of policies</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Failed Payment Process</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>1st attempt: immediate retry</li>
            <li>2nd attempt: 3 days</li>
            <li>3rd attempt: 7 days</li>
            <li>Account restricted after 14 days</li>
            <li>Cancellation after 30 days</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Reactivation</h2>
          <p className="text-slate-300 leading-relaxed">
            Contact <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> to resolve suspension.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Payment must be updated for billing-related suspensions.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
            <Link href="/acceptable-use" className="text-emerald-400 hover:underline">Acceptable Use</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
