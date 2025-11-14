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
          <h2 className="text-2xl font-bold text-white">2. Workflow Limits</h2>
          <p className="text-slate-300 leading-relaxed">
            Workflows per plan must match advertised limits.
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: 1 workflow/month</li>
            <li>Growth: 3 workflows/month</li>
            <li>Pro: 7 workflows/month</li>
            <li>Business: Unlimited within "reasonable business use"</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. API Usage Limits</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: 1,000 API calls/day</li>
            <li>Growth: 10,000 API calls/day</li>
            <li>Pro: 50,000 API calls/day</li>
            <li>Business: 200,000 API calls/day</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Automation Triggers Per Month</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Starter: ~1,000 triggers/month</li>
            <li>Growth: ~10,000 triggers/month</li>
            <li>Pro: ~50,000 triggers/month</li>
            <li>Business: Unlimited (soft cap 200 runs/day = ~6,000/month)</li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-3">
            Daily soft cap for unlimited plans: 200 workflow runs/day
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Unlimited Plans Fair Use Thresholds</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>No more than reasonable daily usage</li>
            <li>No abuse of external APIs</li>
            <li>No mass automated scraping</li>
            <li>No recurring high-volume tasks without review</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Abuse/Misuse Definitions</h2>
          <div className="bg-amber-900/20 border border-amber-800 rounded-lg p-4">
            <p className="text-slate-300 font-semibold mb-2">Abuse includes:</p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4 text-sm">
              <li>Exceeding tier limits by 3x consistently</li>
              <li>Generating artificial load to test limits</li>
              <li>Reselling access without authorization</li>
              <li>Unlimited revisions to avoid paying for higher tiers</li>
              <li>Abusing support channels</li>
              <li>Creating harmful or illegal automations</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Suspension Rules</h2>
          <ol className="list-decimal list-inside space-y-2 text-slate-300 ml-4">
            <li>First violation: Warning email + 48-hour review period</li>
            <li>Second violation: Temporary throttling + upgrade recommendation</li>
            <li>Third violation: Account suspension pending review</li>
            <li>Severe abuse: Immediate suspension without warning</li>
          </ol>
          <p className="text-slate-300 leading-relaxed mt-3">
            We reserve the right to throttle or review usage at any time.
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
