import Link from "next/link";

export default function OnboardingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Customer Onboarding</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <div className="space-y-3">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-1">Step 1</h3>
              <p className="text-slate-300 text-sm">Payment received</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-1">Step 2</h3>
              <p className="text-slate-300 text-sm">Automatic email confirmation</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-1">Step 3</h3>
              <p className="text-slate-300 text-sm">Kickoff form (requirements + access)</p>
            </div>
          </div>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">What You Need to Provide</h2>
          <p className="text-slate-300 leading-relaxed">
            For DFY builds, customers must provide:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Credentials for required services</li>
            <li>Access to relevant platforms</li>
            <li>Domain names (if applicable)</li>
            <li>Clear workflow requirements</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Process Steps</h2>
          <div className="space-y-3">

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-1">Step 4</h3>
              <p className="text-slate-300 text-sm">Workflow build begins</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-1">Step 5</h3>
              <p className="text-slate-300 text-sm">Delivery + revision cycle</p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-emerald-400 mb-1">Step 6</h3>
              <p className="text-slate-300 text-sm">Handover + support window</p>
            </div>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/delivery" className="text-emerald-400 hover:underline">Delivery</Link>
            <Link href="/support-policy" className="text-emerald-400 hover:underline">Support</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
