import Link from "next/link";

export default function DeliveryPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Service Delivery</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">DFY Delivery Times</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>DFY Starter: 48 hours</li>
            <li>DFY Professional: 3–4 days</li>
            <li>DFY Enterprise: 7 days</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Subscriptions</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Workflow creation = based on tier</li>
            <li>Fixes = included</li>
            <li>Optimisations = included (Pro+)</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA</Link>
            <Link href="/revisions" className="text-emerald-400 hover:underline">Revisions</Link>
            <Link href="/support-policy" className="text-emerald-400 hover:underline">Support</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
