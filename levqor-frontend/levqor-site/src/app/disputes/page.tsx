import Link from "next/link";

export default function DisputesPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Dispute Resolution & Complaints</h1>
        <p className="text-slate-400 mb-8">
          We're committed to resolving concerns fairly and transparently. Please follow these steps.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Step 1: Contact Support First</h2>
          <p className="text-slate-300 leading-relaxed">
            Most issues can be resolved quickly through our standard support channels. We're here to help.
          </p>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
            <div>
              <h3 className="text-lg font-medium text-white mb-2">Primary Contact</h3>
              <p className="text-slate-300">
                Email:{" "}
                <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                  support@levqor.ai
                </a>
              </p>
            </div>
            <div>
              <h3 className="text-lg font-medium text-white mb-2">Response Time</h3>
              <p className="text-slate-300">
                Standard: 1–3 business days for initial response
              </p>
              <p className="text-slate-300">
                Business plan holders: Priority support with faster response times
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Step 2: Request Escalation</h2>
          <p className="text-slate-300 leading-relaxed">
            If your issue isn't resolved to your satisfaction through standard support, you can request escalation.
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Reply to your support ticket with "REQUEST ESCALATION" in the subject line</li>
            <li>Clearly state why you believe escalation is necessary</li>
            <li>Include all relevant ticket numbers and correspondence</li>
            <li>A senior team member will review your case within 2–3 business days</li>
          </ul>
          <p className="text-slate-400 text-sm mt-4">
            For more information on our escalation process, see our{" "}
            <Link href="/support-escalation" className="text-emerald-400 hover:underline">
              support escalation policy
            </Link>
            .
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Step 3: Formal Complaint</h2>
          <p className="text-slate-300 leading-relaxed">
            For unresolved matters after escalation, you may file a formal complaint.
          </p>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <div>
              <h3 className="text-lg font-medium text-white mb-2">How to File</h3>
              <p className="text-slate-300">
                Email:{" "}
                <a href="mailto:complaints@levqor.ai" className="text-emerald-400 hover:underline">
                  complaints@levqor.ai
                </a>
              </p>
            </div>
            <div>
              <h3 className="text-lg font-medium text-white mb-2">What to Include</h3>
              <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4 text-sm">
                <li>Your account details (name, email, company)</li>
                <li>Complete timeline of events</li>
                <li>All previous ticket numbers and correspondence</li>
                <li>Screenshots or evidence supporting your complaint</li>
                <li>Specific resolution you're seeking</li>
              </ul>
            </div>
            <div>
              <h3 className="text-lg font-medium text-white mb-2">Response Timeline</h3>
              <p className="text-slate-300">
                Formal complaints are reviewed by senior management within 5–7 business days. You'll receive:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4 text-sm mt-2">
                <li>Acknowledgment within 24 hours</li>
                <li>Full investigation results within 7 business days</li>
                <li>Clear explanation of our findings and proposed resolution</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Step 4: External Dispute Resolution</h2>
          <p className="text-slate-300 leading-relaxed">
            If we're unable to reach a mutually acceptable resolution, you have the right to pursue external avenues.
          </p>
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-6 space-y-3">
            <h3 className="text-lg font-medium text-yellow-400">For UK/EU Customers</h3>
            <p className="text-slate-300 text-sm">
              You may have the right to refer unresolved disputes to relevant regulatory bodies or alternative dispute resolution services in your jurisdiction. We'll provide necessary documentation to support any such referral.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">About Chargebacks</h2>
          <p className="text-slate-300 leading-relaxed">
            We understand payment disputes happen. However, chargebacks should be a last resort.
          </p>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 text-sm">
              <strong className="text-white">Before initiating a chargeback:</strong> Please contact us directly. Chargebacks:
            </p>
            <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4 text-sm">
              <li>May result in immediate service suspension</li>
              <li>Can take 60–90 days to resolve (vs. 5–7 days through our process)</li>
              <li>May include additional fees from your bank</li>
              <li>Could affect your ability to use our services in future</li>
            </ul>
            <p className="text-slate-300 text-sm mt-4">
              We're happy to work with you on a fair resolution first. Email{" "}
              <a href="mailto:billing@levqor.ai" className="text-emerald-400 hover:underline">
                billing@levqor.ai
              </a>{" "}
              for billing disputes.
            </p>
          </div>
        </section>

        <section className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
          <h3 className="text-lg font-bold text-white">Our Commitment</h3>
          <p className="text-slate-300 text-sm">
            We take all complaints seriously and investigate thoroughly. Our goal is always to find a fair resolution that respects both parties. We appreciate customers who give us the opportunity to make things right.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Related Resources</h2>
          <ul className="space-y-2">
            <li>
              <Link href="/terms" className="text-emerald-400 hover:underline">
                Terms of Service
              </Link>
            </li>
            <li>
              <Link href="/refunds" className="text-emerald-400 hover:underline">
                Refund Policy
              </Link>
            </li>
            <li>
              <Link href="/sla" className="text-emerald-400 hover:underline">
                Service Level Agreement
              </Link>
            </li>
            <li>
              <Link href="/fair-use" className="text-emerald-400 hover:underline">
                Fair Use Policy
              </Link>
            </li>
          </ul>
        </section>
      </div>
    </main>
  );
}
