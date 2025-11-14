import Link from "next/link";

export default function DFYAgreementPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-4xl mx-auto px-4 py-12 space-y-8">
        <div className="mb-8">
          <Link href="/pricing" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to Pricing
          </Link>
        </div>

        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">Done-For-You Automation Services Agreement</h1>
          <p className="text-slate-400 text-lg">
            Master Services Agreement for one-time automation builds
          </p>
          <p className="text-sm text-slate-500 mt-2">
            Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
          </p>
        </div>

        <div className="bg-emerald-950/20 border-2 border-emerald-900/50 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-emerald-300 mb-3">📋 Service Packages</h2>
          <div className="space-y-3 text-slate-300">
            <div className="flex justify-between items-center bg-slate-900/50 p-3 rounded">
              <span className="font-semibold">Starter Build</span>
              <span className="text-emerald-400">£99 • 1 workflow</span>
            </div>
            <div className="flex justify-between items-center bg-slate-900/50 p-3 rounded">
              <span className="font-semibold">Growth Build</span>
              <span className="text-emerald-400">£249 • 3 workflows</span>
            </div>
            <div className="flex justify-between items-center bg-slate-900/50 p-3 rounded">
              <span className="font-semibold">Pro Build</span>
              <span className="text-emerald-400">£599 • 7 workflows</span>
            </div>
          </div>
        </div>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">1. Scope of Services</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              Levqor ("Provider") agrees to design, build, test, and deploy custom automation workflows ("Deliverables") 
              for the Client based on the selected Done-For-You package.
            </p>
            <p>
              Each workflow includes:
            </p>
            <ul className="list-disc list-inside ml-4 space-y-2">
              <li>Initial requirements gathering and planning session</li>
              <li>Workflow architecture design and approval</li>
              <li>Implementation with API integrations as specified</li>
              <li>Testing and quality assurance</li>
              <li>Deployment to production environment</li>
              <li>30-day post-launch support for bug fixes</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">2. Deliverables Timeline</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <ul className="space-y-2">
                <li><strong className="text-white">Starter (1 workflow):</strong> 5-7 business days</li>
                <li><strong className="text-white">Growth (3 workflows):</strong> 10-14 business days</li>
                <li><strong className="text-white">Pro (7 workflows):</strong> 21-28 business days</li>
              </ul>
            </div>
            <p className="text-sm text-slate-400">
              Timelines begin after receipt of full payment and completion of requirements gathering. 
              Complex integrations or third-party API delays may extend delivery.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">3. Revisions & Changes</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>Each package includes:</p>
            <ul className="list-disc list-inside ml-4 space-y-2">
              <li><strong>Starter:</strong> 1 round of revisions per workflow</li>
              <li><strong>Growth:</strong> 2 rounds of revisions per workflow</li>
              <li><strong>Pro:</strong> 3 rounds of revisions per workflow</li>
            </ul>
            <p>
              Revisions must be requested within 14 days of delivery. Scope changes beyond the original 
              specification may incur additional charges at £75/hour.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">4. Client Responsibilities</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>Client agrees to:</p>
            <ul className="list-disc list-inside ml-4 space-y-2">
              <li>Provide accurate requirements and timely feedback</li>
              <li>Supply necessary API keys, credentials, and access to third-party systems</li>
              <li>Respond to requests for information within 48 hours</li>
              <li>Designate a single point of contact for the project</li>
              <li>Test and accept deliverables within 7 days of delivery</li>
            </ul>
            <p className="text-sm text-slate-400">
              Delays caused by Client non-responsiveness may extend delivery timelines.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">5. Acceptance & Sign-Off</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              Upon delivery, Client has 7 calendar days to test and provide feedback. Acceptance is deemed 
              automatic if no issues are raised within this period.
            </p>
            <p>
              Critical bugs affecting core functionality will be fixed at no charge. Feature additions or 
              scope changes require separate agreement.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">6. Service Exclusions</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>The following are NOT included in DFY packages:</p>
            <ul className="list-disc list-inside ml-4 space-y-2">
              <li>Medical, legal, financial, or tax automation workflows (prohibited by policy)</li>
              <li>Third-party subscription costs (e.g., API fees, software licenses)</li>
              <li>Ongoing maintenance beyond 30-day support period</li>
              <li>Custom integrations requiring Provider to obtain paid API access</li>
              <li>Data migration from legacy systems</li>
              <li>Training beyond initial handoff documentation</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">7. Limitation of Liability</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              Provider's liability is limited to the amount paid for the specific DFY package. Provider is 
              not liable for:
            </p>
            <ul className="list-disc list-inside ml-4 space-y-2">
              <li>Third-party API failures or service interruptions</li>
              <li>Data loss due to Client actions or third-party failures</li>
              <li>Consequential, indirect, or special damages</li>
              <li>Issues arising from Client-provided credentials or access</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">8. Payment Terms</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              Full payment is required before work commences. Payments are processed via Stripe and are 
              non-refundable once work has begun.
            </p>
            <p>
              If Client requests cancellation before delivery, refunds are provided on a pro-rata basis 
              for work not yet completed, minus a 20% administrative fee.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">9. Intellectual Property</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              Upon full payment and acceptance, Client receives full ownership of the delivered workflows 
              and associated documentation. Provider retains the right to reuse general techniques, 
              methodologies, and non-Client-specific components.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">10. Termination</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              Either party may terminate this agreement with 7 days' written notice. Upon termination:
            </p>
            <ul className="list-disc list-inside ml-4 space-y-2">
              <li>Client receives work completed to date</li>
              <li>Provider invoices for work completed based on hourly rate (£75/hour)</li>
              <li>Unused prepaid funds are refunded minus administrative fee</li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-3xl font-bold text-white border-b border-slate-800 pb-3">11. Governing Law</h2>
          <div className="text-slate-300 space-y-3 leading-relaxed">
            <p>
              This agreement is governed by the laws of England and Wales. Disputes shall be resolved 
              through good-faith negotiation, mediation, or arbitration before litigation.
            </p>
          </div>
        </section>

        <div className="bg-blue-950/20 border-2 border-blue-900/50 rounded-lg p-6 mt-12">
          <h2 className="text-xl font-bold text-blue-300 mb-3">📞 Questions or Concerns?</h2>
          <p className="text-slate-300 mb-4">
            If you have questions about this agreement or need clarification on any terms, please contact us before purchasing.
          </p>
          <div className="flex gap-4">
            <a href="mailto:dfy@levqor.ai" className="text-blue-400 hover:underline">dfy@levqor.ai</a>
            <Link href="/disputes" className="text-blue-400 hover:underline">Raise a concern</Link>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/pricing" className="text-emerald-400 hover:underline font-semibold">View Pricing</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
            <Link href="/delivery" className="text-emerald-400 hover:underline">Delivery Process</Link>
            <Link href="/revisions" className="text-emerald-400 hover:underline">Revision Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
