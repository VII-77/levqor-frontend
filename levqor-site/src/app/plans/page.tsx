import Link from "next/link";

export default function PlansPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Service Descriptions</h1>
        <p className="text-slate-400 mb-12">
          Detailed breakdown of each plan
        </p>

        <section className="space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-emerald-400 mb-4">DFY Starter (£99)</h2>
            <p className="text-slate-300 mb-4">One-time payment for a single workflow automation</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>1 workflow automation</li>
              <li>48-hour delivery</li>
              <li>1 revision</li>
              <li>Basic error handling</li>
            </ul>

            <h3 className="text-lg font-semibold text-white mb-2 mt-4">Boundaries:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>Single automation only</li>
              <li>No ongoing maintenance</li>
              <li>Limited to 2 third-party integrations</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-blue-400 mb-4">DFY Professional (£249)</h2>
            <p className="text-slate-300 mb-4">One-time payment for three workflow automations</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>3 workflow automations</li>
              <li>3-4 day delivery</li>
              <li>2 revisions</li>
              <li>Advanced error handling</li>
              <li>Basic monitoring setup</li>
            </ul>

            <h3 className="text-lg font-semibold text-white mb-2 mt-4">Boundaries:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>Up to 3 workflows</li>
              <li>No ongoing maintenance</li>
              <li>Up to 5 third-party integrations total</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-purple-400 mb-4">DFY Enterprise (£599)</h2>
            <p className="text-slate-300 mb-4">One-time payment for seven workflow automations</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>7 workflow automations</li>
              <li>7-day delivery</li>
              <li>3 revisions</li>
              <li>Advanced error handling & monitoring</li>
              <li>Documentation included</li>
            </ul>

            <h3 className="text-lg font-semibold text-white mb-2 mt-4">Boundaries:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>Up to 7 workflows</li>
              <li>No ongoing maintenance</li>
              <li>Unlimited third-party integrations</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-emerald-400 mb-4">Starter (£29/month)</h2>
            <p className="text-slate-300 mb-4">Monthly subscription for ongoing workflow support</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>1 workflow/month</li>
              <li>Email support (24-48h response)</li>
              <li>Basic monitoring</li>
              <li>Bug fixes included</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-blue-400 mb-4">Growth (£79/month)</h2>
            <p className="text-slate-300 mb-4">Monthly subscription for growing teams</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>3 workflows/month</li>
              <li>Priority email support (12-24h response)</li>
              <li>Advanced monitoring</li>
              <li>Bug fixes & minor updates included</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-purple-400 mb-4">Pro (£149/month)</h2>
            <p className="text-slate-300 mb-4">Monthly subscription for professional automation</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>7 workflows/month</li>
              <li>Priority support (&lt;12h response)</li>
              <li>Advanced monitoring & alerts</li>
              <li>Bug fixes & optimizations included</li>
              <li>Monthly strategy call</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h2 className="text-2xl font-bold text-amber-400 mb-4">Business (£299/month)</h2>
            <p className="text-slate-300 mb-4">Monthly subscription for enterprise automation</p>
            
            <h3 className="text-lg font-semibold text-white mb-2">Included:</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li>Unlimited workflows (fair use: 20/month)</li>
              <li>Dedicated support (same-day response)</li>
              <li>Enterprise monitoring & SLA</li>
              <li>All fixes, updates, & optimizations</li>
              <li>Weekly strategy calls</li>
              <li>Custom integrations available</li>
            </ul>

            <h3 className="text-lg font-semibold text-white mb-2 mt-4">Fair Use:</h3>
            <p className="text-slate-300">Reasonable business use capped at ~20 workflows/month or 200 runs/day.</p>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/pricing" className="text-emerald-400 hover:underline">Pricing</Link>
            <Link href="/fair-use" className="text-emerald-400 hover:underline">Fair Use Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
