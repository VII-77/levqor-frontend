import Link from "next/link";

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Terms of Service</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed">
          Welcome to Levqor ("we", "us", "our"). By accessing or using our services, you agree to these Terms of Service ("Terms"). If you do not agree, do not use Levqor.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Services</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor provides automation systems, workflow development, consulting, and software tools delivered as:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Done-For-You one-time builds (DFY)</li>
            <li>Subscription plans</li>
            <li>Platform access (where applicable)</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Eligibility</h2>
          <p className="text-slate-300 leading-relaxed">
            You must be at least 18 and legally allowed to enter contracts in your region.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Accounts</h2>
          <p className="text-slate-300 leading-relaxed">
            You are responsible for maintaining account security and ensuring all information is accurate.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Payments</h2>
          <p className="text-slate-300 leading-relaxed">
            Payments are processed via Stripe.
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>DFY = one-time payment.</li>
            <li>Subscriptions = recurring billing until cancelled.</li>
            <li>Prices, tiers, and billing intervals are shown at checkout.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Refunds</h2>
          <p className="text-slate-300 leading-relaxed">
            Refunds follow our Refund Policy. DFY work begins immediately; refunds may be limited depending on progress.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Fair Use</h2>
          <p className="text-slate-300 leading-relaxed">
            All subscriptions include a Fair Use Policy. Abuse, infinite tasks, or unacceptable behaviour may result in suspension.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Acceptable Use</h2>
          <p className="text-slate-300 leading-relaxed">
            You agree not to misuse our services, attack our systems, engage in fraud, scrape excessively, or violate laws.
          </p>
        </section>

        <section className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-6 space-y-4">
          <h2 className="text-2xl font-bold text-white">7A. High-Risk Data Prohibition</h2>
          <p className="text-slate-300 leading-relaxed font-semibold">
            Levqor is NOT designed for, and MUST NOT be used for:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong className="text-white">Medical or healthcare decisions</strong> - Including diagnosis, treatment, prescriptions, or health data processing</li>
            <li><strong className="text-white">Legal advice or decision-making</strong> - Including legal reasoning, contract generation, or legal document creation</li>
            <li><strong className="text-white">Financial advice, lending, credit scoring, or trading decisions</strong> - Including tax advice, investment recommendations, or automated financial workflows</li>
            <li><strong className="text-white">Safety-critical systems</strong> - Including transport, emergency services, critical infrastructure, or life-safety automation</li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-4">
            <strong className="text-white">Any such use is strictly prohibited</strong> and constitutes a material breach of these Terms.
          </p>
          <p className="text-slate-300 leading-relaxed">
            All workflow submissions are automatically scanned for prohibited content. Workflows containing high-risk or regulated data will be immediately rejected.
          </p>
          <p className="text-slate-300 leading-relaxed">
            You use Levqor for such purposes entirely at your own risk. We disclaim all liability for any harm, loss, or regulatory action resulting from prohibited use.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Intellectual Property</h2>
          <p className="text-slate-300 leading-relaxed">
            All branding, code, workflows, UI, and documentation belong to Levqor.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Limitation of Liability</h2>
          <p className="text-slate-300 leading-relaxed">
            Service provided as-is.
          </p>
          <p className="text-slate-300 leading-relaxed">
            We do not guarantee specific outcomes or financial results.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Levqor is not liable for indirect, incidental, or consequential damages.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Termination</h2>
          <p className="text-slate-300 leading-relaxed">
            We may suspend or terminate accounts for violations of these Terms, abuse, non-payment, or harmful actions.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">11. Governing Law</h2>
          <p className="text-slate-300 leading-relaxed">
            United Kingdom law applies. Disputes handled via UK jurisdiction.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">12. DMCA</h2>
          <p className="text-slate-300 leading-relaxed">
            DMCA Agent: <a href="mailto:legal@levqor.ai" className="text-emerald-400 hover:underline">legal@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Claims must include signature, URLs, evidence.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">13. Appendix: Managed Automation Services (DFY)</h2>
          
          <h3 className="text-xl font-semibold text-emerald-400 mt-6">DFY Coverage</h3>
          <p className="text-slate-300 leading-relaxed">
            Done-For-You builds include workflow design, implementation, and testing.
          </p>

          <h3 className="text-xl font-semibold text-emerald-400 mt-6">Scope Boundaries</h3>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Workflow automation within agreed specifications</li>
            <li>Integration with accessible third-party APIs</li>
            <li>Basic error handling and monitoring</li>
          </ul>

          <h3 className="text-xl font-semibold text-emerald-400 mt-6">Out-of-Scope Items</h3>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Infrastructure hosting beyond initial setup</li>
            <li>Third-party API costs</li>
            <li>Custom enterprise integrations (requires separate agreement)</li>
            <li>Ongoing maintenance (requires subscription plan)</li>
          </ul>

          <h3 className="text-xl font-semibold text-emerald-400 mt-6">Customer Responsibilities</h3>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Provide required API keys and credentials</li>
            <li>Grant access to platforms/tools</li>
            <li>Respond to clarification requests within 48 hours</li>
            <li>Review and test delivered workflows</li>
            <li>Report issues within acceptance window (5 days)</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">14. Compliance Footnotes</h2>
          <div className="bg-amber-900/20 border border-amber-800 rounded-lg p-4">
            <p className="text-slate-300 leading-relaxed font-semibold">
              Important: Levqor is not liable for misuse of automated workflows.
            </p>
            <p className="text-slate-300 leading-relaxed mt-3">
              Customers are solely responsible for ensuring their automations comply with all applicable laws, regulations, and third-party terms of service.
            </p>
            <p className="text-slate-300 leading-relaxed mt-3">
              This includes but is not limited to: CAN-SPAM, GDPR, PECR, data protection laws, anti-fraud regulations, and platform-specific acceptable use policies.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">15. Contact</h2>
          <p className="text-slate-300 leading-relaxed">
            Email: <a href="mailto:legal@levqor.ai" className="text-emerald-400 hover:underline">legal@levqor.ai</a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
