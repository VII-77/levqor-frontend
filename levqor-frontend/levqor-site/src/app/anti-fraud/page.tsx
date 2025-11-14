import Link from "next/link";

export default function AntiFraudPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Anti-Spam & Anti-Fraud Notice</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Compliance Requirements</h2>
          <p className="text-slate-300 leading-relaxed">
            All automated workflows must comply with:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>CAN-SPAM Act</li>
            <li>UK GDPR</li>
            <li>UK PECR (Privacy and Electronic Communications Regulations)</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Prohibited Activities</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Sending unsolicited bulk emails</li>
            <li>Fraudulent transactions or chargebacks</li>
            <li>Automated account creation for abuse</li>
            <li>Mass scraping without permission</li>
            <li>Circumventing rate limits or security measures</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Fraud Detection</h2>
          <p className="text-slate-300 leading-relaxed">
            Stripe Radar enabled for all transactions.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Suspicious transactions reviewed manually.
          </p>
          <p className="text-slate-300 leading-relaxed">
            High-risk orders require verification.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Protection Statement</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor is not liable for customer misuse of automated workflows.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Customers are responsible for ensuring their automations comply with all applicable laws.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/acceptable-use" className="text-emerald-400 hover:underline">Acceptable Use</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
