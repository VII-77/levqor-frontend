import Link from "next/link";

export default function DPAPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Data Processing Agreement</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed">
          Between Customer ("Controller") and Levqor ("Processor").
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Purpose</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor processes data solely to provide automation services.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Subprocessors</h2>
          <p className="text-slate-300 leading-relaxed">
            Listed in our Subprocessor List.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Obligations</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor will:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Maintain security</li>
            <li>Process only on instruction</li>
            <li>Notify of breaches</li>
            <li>Assist with rights requests</li>
            <li>Use SCCs for international transfers</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Retention</h2>
          <p className="text-slate-300 leading-relaxed">
            Data deleted upon contract end or customer request.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Contact</h2>
          <p className="text-slate-300 leading-relaxed">
            Email: <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
