import Link from "next/link";

export default function SLAPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Service Level Agreement (SLA)</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Uptime Guarantee</h2>
          <p className="text-slate-300 leading-relaxed">
            Target uptime: 99.5% (excludes scheduled maintenance)
          </p>
          <p className="text-slate-300 leading-relaxed">
            Measured monthly across all core services.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Maintenance windows announced 24h in advance.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Emergency maintenance may occur when required.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Response Times by Support Tier</h2>
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-slate-400 mb-2">Starter</h3>
              <p className="text-slate-300 text-sm">No SLA - Best effort support</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-2">Growth</h3>
              <p className="text-slate-300 text-sm">Response: 48 hours | Resolution: 5 business days</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-400 mb-2">Pro</h3>
              <p className="text-slate-300 text-sm">Response: 24 hours | Resolution: 3 business days</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-purple-400 mb-2">Business</h3>
              <p className="text-slate-300 text-sm">Response: 12 hours | Resolution: 2 business days | Dedicated support</p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. DFY Delivery</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>1 workflow → 48 hours</li>
            <li>3 workflows → 3–4 days</li>
            <li>7 workflows → 7 days</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Exclusions</h2>
          <p className="text-slate-300 leading-relaxed">
            SLA does not cover:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Force majeure events</li>
            <li>Third-party API outages</li>
            <li>DDoS attacks</li>
            <li>Customer-caused issues</li>
            <li>Scheduled maintenance windows</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Service Credits for Downtime</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
            <p className="text-slate-300 text-sm mb-2">
              <span className="font-semibold">99.0% - 99.5%:</span> 10% credit
            </p>
            <p className="text-slate-300 text-sm mb-2">
              <span className="font-semibold">95.0% - 99.0%:</span> 25% credit
            </p>
            <p className="text-slate-300 text-sm">
              <span className="font-semibold">&lt;95.0%:</span> 50% credit
            </p>
          </div>
          <p className="text-slate-300 text-sm mt-3">
            Credits applied to next billing cycle. Request within 30 days of incident.
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
