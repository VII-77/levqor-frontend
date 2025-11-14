import Link from "next/link";

export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Privacy Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed">
          Levqor ("we", "us") is committed to protecting your privacy and complying with UK GDPR.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Personal Data We Collect</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Account information (name, email)</li>
            <li>Payment information (processed by Stripe; we never store card data)</li>
            <li>Usage analytics</li>
            <li>Workflow input/output data (for debugging or service delivery)</li>
            <li>Support communications</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. How We Use Personal Data</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>To provide our automation services</li>
            <li>To process payments</li>
            <li>To prevent abuse, fraud, and ensure security</li>
            <li>To improve performance</li>
            <li>To communicate with you</li>
            <li>To comply with legal obligations</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Lawful Basis</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Contract</li>
            <li>Legitimate interests</li>
            <li>Consent (cookies, marketing)</li>
            <li>Legal obligation</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Sharing Data</h2>
          <p className="text-slate-300 leading-relaxed">
            We use trusted subprocessors:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Stripe (payments)</li>
            <li>Vercel (hosting)</li>
            <li>Replit (backend operations)</li>
            <li>OpenAI (AI processing)</li>
            <li>Google (authentication)</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. International Transfers</h2>
          <p className="text-slate-300 leading-relaxed">
            We use approved mechanisms such as SCCs for transfers outside the UK.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Data Retention</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Account: until deletion</li>
            <li>Workflow logs: 30–180 days</li>
            <li>Payment records: 6 years</li>
            <li>Support messages: 12 months</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Cookies</h2>
          <p className="text-slate-300 leading-relaxed">
            We use functional, analytical, and preference cookies.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Your Rights</h2>
          <p className="text-slate-300 leading-relaxed">
            You may request access, deletion, correction, restriction, data portability.
          </p>
          <p className="text-slate-300 leading-relaxed mt-4">
            Data removed within 30 days except where law requires retention.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Security</h2>
          <p className="text-slate-300 leading-relaxed">
            We use encryption, access controls, audit logs, rate-limits, and continuous monitoring.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Contact</h2>
          <p className="text-slate-300 leading-relaxed">
            Email: <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/cookies" className="text-emerald-400 hover:underline">Cookie Policy</Link>
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
