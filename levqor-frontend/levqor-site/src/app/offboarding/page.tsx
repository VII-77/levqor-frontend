import Link from "next/link";

export default function OffboardingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Customer Offboarding</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Access Removal</h2>
          <p className="text-slate-300 leading-relaxed">
            Upon cancellation, access to workflows and dashboard is removed at the end of the billing period.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Data Export</h2>
          <p className="text-slate-300 leading-relaxed">
            Request data export before cancellation: <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Data deleted 30 days after account closure.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">End-of-Support</h2>
          <p className="text-slate-300 leading-relaxed">
            Support ends when subscription expires.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Workflows are deactivated immediately after account closure.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/cancellation" className="text-emerald-400 hover:underline">Cancellation Policy</Link>
            <Link href="/data-requests" className="text-emerald-400 hover:underline">Data Requests</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
