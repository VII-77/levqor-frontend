import Link from "next/link";

export default function FairUsePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Fair Use Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed">
          This policy ensures fair, reliable service for all Levqor customers.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Definition</h2>
          <p className="text-slate-300 leading-relaxed">
            "Fair use" = volume of workflows, revisions, tasks, and support requests typical for the tier purchased.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Examples of Fair Use</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: 1 workflow/month</li>
            <li>Growth: 3 workflows/month</li>
            <li>Pro: 7 workflows/month</li>
            <li>Business: Unlimited within "reasonable business use"</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Unacceptable Use</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Unlimited revisions to avoid paying for higher tiers</li>
            <li>Abusing support channels</li>
            <li>Generating extreme workloads</li>
            <li>Using Levqor to create harmful or illegal automations</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Enforcement</h2>
          <p className="text-slate-300 leading-relaxed">
            We may limit usage, warn, suspend, or upgrade your plan.
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
