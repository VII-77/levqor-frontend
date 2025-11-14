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
          <h2 className="text-2xl font-bold text-white">3.2 Security Measures</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>TLS 1.2+ in transit</li>
            <li>AES-256 at rest</li>
            <li>API keys stored encrypted</li>
            <li>Access logs monitored</li>
            <li>Regular security audits</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Retention</h2>
          <p className="text-slate-300 leading-relaxed">
            Data retention schedule:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Account data: retained while active</li>
            <li>Backups: 14–30 days</li>
            <li>Logs: 7–14 days</li>
            <li>Billing records: 6 years (legal requirement)</li>
            <li>AI output: not stored unless necessary for service</li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-3">
            Data deleted upon contract end or customer request.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Breach Notifications</h2>
          <p className="text-slate-300 leading-relaxed">
            Notify affected users within 72 hours.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Explain type, scope, and impact.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Provide mitigation steps.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Notify ICO if applicable.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">11. Contact</h2>
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
