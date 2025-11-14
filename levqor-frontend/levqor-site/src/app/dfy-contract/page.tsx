"use client";
import Link from "next/link";

export default function DFYContractPage() {
  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">
            Levqor
          </Link>
          <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">
            Pricing
          </Link>
        </nav>
      </header>

      <div className="max-w-4xl mx-auto px-4 py-16">
        <h1 className="text-3xl font-bold text-white mb-4">Done-For-You Service Agreement</h1>
        <p className="text-slate-400 mb-8">Last updated: November 14, 2025</p>

        <div className="prose prose-invert prose-slate max-w-none space-y-8">
          {/* Introduction */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">1. Introduction</h2>
            <p className="text-slate-300">
              This Done-For-You (DFY) Service Agreement ("Agreement") governs the provision of custom automation workflow development services ("Services") by Levqor ("we", "us", "our") to the customer ("you", "your", "Client").
            </p>
            <p className="text-slate-300 mt-4">
              By purchasing a DFY service package, you agree to be bound by this Agreement and our general Terms of Service.
            </p>
          </section>

          {/* Service Scope */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">2. Service Scope</h2>
            
            <h3 className="text-xl font-semibold text-white mt-6 mb-3">2.1 DFY Starter (£99)</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>1 custom automation workflow</li>
              <li>Up to 2 tool integrations</li>
              <li>Basic error handling</li>
              <li>48-hour delivery from kickoff call</li>
              <li>1 round of revisions</li>
              <li>7 days email support</li>
              <li>Documentation and setup instructions</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-6 mb-3">2.2 DFY Professional (£249)</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>3 custom automation workflows</li>
              <li>Up to 6 tool integrations</li>
              <li>Advanced error handling and notifications</li>
              <li>3-4 day delivery from kickoff call</li>
              <li>2 rounds of revisions</li>
              <li>30 days email support</li>
              <li>Performance monitoring and optimization</li>
              <li>Comprehensive documentation</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-6 mb-3">2.3 DFY Enterprise (£599)</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>7 custom automation workflows</li>
              <li>Unlimited tool integrations</li>
              <li>Enterprise-grade error handling and self-healing</li>
              <li>7-day delivery from kickoff call</li>
              <li>2 rounds of revisions</li>
              <li>30 days priority email support</li>
              <li>Custom integrations and API configurations</li>
              <li>Performance dashboard and reporting</li>
              <li>Complete technical documentation</li>
            </ul>
          </section>

          {/* Delivery Timeline */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">3. Delivery Timeline</h2>
            <ol className="list-decimal list-inside space-y-3 text-slate-300">
              <li><strong className="text-white">Order Confirmation:</strong> Within 24 hours of payment</li>
              <li><strong className="text-white">Kickoff Call:</strong> Scheduled within 24-48 hours of order</li>
              <li><strong className="text-white">Build Phase:</strong> Starts immediately after kickoff call and credential submission</li>
              <li><strong className="text-white">Delivery:</strong> According to tier (48 hours / 3-4 days / 7 days)</li>
              <li><strong className="text-white">Support Period:</strong> Begins upon delivery (7 or 30 days depending on tier)</li>
            </ol>
            <p className="text-slate-300 mt-4">
              <strong className="text-white">Note:</strong> Timelines are based on business days and assume timely client response to requests for information and credentials.
            </p>
          </section>

          {/* Client Responsibilities */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">4. Client Responsibilities</h2>
            <p className="text-slate-300 mb-4">To ensure successful delivery, you must provide:</p>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>Clear workflow requirements and desired outcomes</li>
              <li>Access credentials for all relevant tools and platforms</li>
              <li>API keys, webhooks, or integration tokens as needed</li>
              <li>Sample data for testing purposes</li>
              <li>Availability for 30-60 minute kickoff call</li>
              <li>Timely responses to questions (within 48 hours)</li>
              <li>Review and feedback on deliverables within support period</li>
            </ul>
          </section>

          {/* Revisions */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">5. Revisions & Changes</h2>
            
            <h3 className="text-xl font-semibold text-white mt-4 mb-3">5.1 Included Revisions</h3>
            <p className="text-slate-300">
              Each tier includes a specified number of revision rounds to address issues or adjustments to the original scope:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Starter: 1 round</li>
              <li>Professional: 2 rounds</li>
              <li>Enterprise: 2 rounds</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-4 mb-3">5.2 Scope Changes</h3>
            <p className="text-slate-300">
              Changes beyond the original scope require additional payment:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Minor changes: £25-50</li>
              <li>Major changes: Re-quote required</li>
              <li>Additional workflows: Purchase additional tier or upgrade</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-4 mb-3">5.3 Post-Support Changes</h3>
            <p className="text-slate-300">
              After your support period expires, you can:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Purchase individual changes (£25-50 per change)</li>
              <li>Upgrade to a subscription plan for ongoing support</li>
              <li>Purchase a new DFY package</li>
            </ul>
          </section>

          {/* Deliverables */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">6. Deliverables</h2>
            <p className="text-slate-300 mb-4">Upon completion, you will receive:</p>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>Fully functional automation workflows</li>
              <li>Access credentials to your workflows</li>
              <li>Step-by-step documentation</li>
              <li>Setup and usage instructions</li>
              <li>Video walkthrough (Professional and Enterprise tiers)</li>
              <li>Performance monitoring dashboard (Professional and Enterprise tiers)</li>
              <li>Export of workflow configurations</li>
            </ul>
          </section>

          {/* Exclusions */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">7. Service Exclusions</h2>
            <p className="text-slate-300 mb-4">DFY services do NOT include:</p>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>Ongoing maintenance after support period</li>
              <li>Third-party tool subscription costs</li>
              <li>Custom software development or coding</li>
              <li>Data migration or data cleanup services</li>
              <li>Training or workshops (available separately)</li>
              <li>Phone support (Business plan only)</li>
              <li>White-label or reseller arrangements</li>
              <li>High-risk automation (medical, legal, financial decision-making)</li>
            </ul>
          </section>

          {/* Data Security */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">8. Data Security & Privacy</h2>
            
            <h3 className="text-xl font-semibold text-white mt-4 mb-3">8.1 Credential Handling</h3>
            <p className="text-slate-300">
              All access credentials provided are:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Transmitted via secure encrypted channels</li>
              <li>Stored using industry-standard encryption</li>
              <li>Accessed only by authorized team members</li>
              <li>Deleted permanently after project completion</li>
              <li>Never shared with third parties</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-4 mb-3">8.2 GDPR Compliance</h3>
            <p className="text-slate-300">
              We are GDPR and UK-GDPR compliant. See our{" "}
              <Link href="/privacy" className="text-emerald-400 hover:underline">
                Privacy Policy
              </Link>{" "}
              and{" "}
              <Link href="/data-processing" className="text-emerald-400 hover:underline">
                Data Processing Agreement
              </Link>{" "}
              for full details.
            </p>
          </section>

          {/* Payment Terms */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">9. Payment Terms</h2>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>Full payment required before work begins</li>
              <li>Payment processed securely via Stripe</li>
              <li>Prices listed in GBP (£)</li>
              <li>No refunds after delivery unless defective (see section 11)</li>
              <li>Subscription upgrades available anytime</li>
            </ul>
          </section>

          {/* Support Period */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">10. Support Period</h2>
            
            <h3 className="text-xl font-semibold text-white mt-4 mb-3">10.1 Coverage</h3>
            <p className="text-slate-300">
              During your support period, we provide:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Bug fixes and error resolution</li>
              <li>Performance optimization</li>
              <li>Questions and guidance via email</li>
              <li>Workflow troubleshooting</li>
              <li>Integration updates if APIs change</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-4 mb-3">10.2 Response Times</h3>
            <ul className="list-disc list-inside space-y-2 text-slate-300">
              <li>Starter: 48-hour response time</li>
              <li>Professional: 24-hour response time</li>
              <li>Enterprise: 12-hour response time</li>
            </ul>
          </section>

          {/* Guarantee */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">11. 14-Day Money-Back Guarantee</h2>
            <p className="text-slate-300">
              We offer a 14-day money-back guarantee from the date of delivery. If you're not satisfied with your workflow:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-4">
              <li>Request a refund within 14 days of delivery</li>
              <li>No questions asked</li>
              <li>Full refund processed within 5-7 business days</li>
              <li>You keep the workflows even after refund</li>
            </ul>
            <p className="text-slate-300 mt-4">
              <strong className="text-white">Note:</strong> Guarantee only applies if workflows are materially defective or do not match agreed specifications.
            </p>
          </section>

          {/* Liability */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">12. Limitation of Liability</h2>
            <p className="text-slate-300">
              Our total liability for any DFY service is limited to the amount you paid for that service. We are not liable for:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-4">
              <li>Indirect, consequential, or special damages</li>
              <li>Loss of profits, revenue, or data</li>
              <li>Third-party tool failures or API changes</li>
              <li>Misuse of delivered workflows</li>
              <li>Compliance issues arising from your use</li>
            </ul>
          </section>

          {/* Disclaimers */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">13. Disclaimers</h2>
            
            <h3 className="text-xl font-semibold text-white mt-4 mb-3">13.1 High-Risk Prohibition</h3>
            <p className="text-slate-300">
              Levqor CANNOT and WILL NOT automate:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Medical diagnosis or treatment decisions</li>
              <li>Legal advice or case management</li>
              <li>Financial investment decisions</li>
              <li>Healthcare record decisions</li>
              <li>Life-critical systems</li>
            </ul>

            <h3 className="text-xl font-semibold text-white mt-4 mb-3">13.2 Your Responsibility</h3>
            <p className="text-slate-300">
              You are responsible for:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-2">
              <li>Compliance with all applicable laws and regulations</li>
              <li>Proper use of delivered workflows</li>
              <li>Data accuracy and validation</li>
              <li>Third-party tool Terms of Service compliance</li>
              <li>Backup and disaster recovery</li>
            </ul>
          </section>

          {/* Termination */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">14. Termination</h2>
            <p className="text-slate-300">
              Either party may terminate this Agreement:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 mt-4">
              <li>Client: By requesting refund within guarantee period</li>
              <li>Levqor: If client breaches Terms of Service</li>
              <li>Levqor: If client provides false or misleading information</li>
              <li>Levqor: If project involves prohibited use cases</li>
            </ul>
            <p className="text-slate-300 mt-4">
              Upon termination outside guarantee period, no refund is provided but client retains delivered workflows.
            </p>
          </section>

          {/* Governing Law */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">15. Governing Law</h2>
            <p className="text-slate-300">
              This Agreement is governed by the laws of England and Wales. Any disputes shall be subject to the exclusive jurisdiction of the courts of England and Wales.
            </p>
          </section>

          {/* Contact */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h2 className="text-2xl font-bold text-white mb-4">16. Contact Information</h2>
            <p className="text-slate-300">
              For questions about this Agreement or your DFY service:
            </p>
            <ul className="list-none space-y-2 text-slate-300 mt-4">
              <li>Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
              <li>Website: <Link href="/" className="text-emerald-400 hover:underline">levqor.ai</Link></li>
              <li>Legal: <a href="mailto:legal@levqor.ai" className="text-emerald-400 hover:underline">legal@levqor.ai</a></li>
            </ul>
          </section>
        </div>

        <div className="mt-12 p-6 bg-emerald-950/20 border border-emerald-900/30 rounded-xl text-center">
          <p className="text-white font-semibold mb-2">Ready to get started?</p>
          <p className="text-slate-300 text-sm mb-4">Choose your DFY package and automate your business</p>
          <Link
            href="/pricing#dfy"
            className="inline-block px-8 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-bold transition"
          >
            View DFY Plans
          </Link>
        </div>
      </div>
    </main>
  );
}
