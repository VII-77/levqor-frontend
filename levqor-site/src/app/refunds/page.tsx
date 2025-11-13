import Link from "next/link";

export default function RefundsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Refund & Cancellation Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-sm text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-lg p-4 mb-8">
          <strong>Important:</strong> Levqor operates on a done-for-you service model. Refunds are limited because our work 
          involves engineering time, configuration, and custom development for your specific workflows.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Our Done-For-You Model</h2>
          <p className="text-slate-300 leading-relaxed">
            Unlike subscription software, Levqor provides custom automation development. When you purchase a package:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>We schedule a kickoff call to understand your requirements.</li>
            <li>Our engineers design and build your workflows.</li>
            <li>We test and deploy the automation within the agreed timeframe.</li>
            <li>You receive ongoing support (7–30 days depending on your package).</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            This is a service engagement, not a SaaS subscription. Once work begins, significant engineering effort has been invested.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Refund Eligibility</h2>
          
          <div className="space-y-4">
            <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-4">
              <h3 className="text-lg font-bold text-emerald-400 mb-2">✓ Full Refund (Before Work Starts)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                If you cancel <strong>before the kickoff call</strong> or <strong>before we begin development</strong>, 
                you are eligible for a full refund (minus any payment processing fees charged by Stripe).
              </p>
              <p className="text-slate-400 text-sm mt-2">
                To request a refund at this stage, email <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> within 
                24 hours of purchase.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-slate-300 mb-2">⚠️ Partial Refund (During Development)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                If you cancel <strong>after the kickoff call but before delivery</strong>, we will assess the work completed 
                and issue a partial refund based on:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>Time spent on design and configuration.</li>
                <li>Third-party API setup costs (if applicable).</li>
                <li>Percentage of workflow development completed.</li>
              </ul>
              <p className="text-slate-400 text-sm mt-2">
                Typical partial refunds range from 25% to 75% depending on progress.
              </p>
            </div>

            <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4">
              <h3 className="text-lg font-bold text-red-400 mb-2">✗ No Refund (After Delivery)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                Once your workflows are <strong>delivered and operational</strong>, refunds are <strong>not available</strong>. 
                At this stage:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>We have completed the engineering work.</li>
                <li>Your workflows are live and functional.</li>
                <li>You have access to the agreed support period for tweaks and adjustments.</li>
              </ul>
              <p className="text-slate-400 text-sm mt-2">
                If you're unhappy with the delivered automation, we will work with you during the support window to make 
                improvements. This is included in your package.
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. What Counts as "Delivery"?</h2>
          <p className="text-slate-300 leading-relaxed">
            A workflow is considered delivered when:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>It is tested and functional in your environment.</li>
            <li>We provide access credentials or a monitoring dashboard (if applicable).</li>
            <li>You are notified via email that the workflow is live.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            Your support period begins immediately after delivery.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Requesting a Refund</h2>
          <p className="text-slate-300 leading-relaxed">
            To request a refund, email <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> with:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Your account email address.</li>
            <li>Order/payment reference (from Stripe receipt).</li>
            <li>Reason for the refund request.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            We will respond within 2 business days. Approved refunds are processed within 5–10 business days to your 
            original payment method.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Cancellation Before Payment</h2>
          <p className="text-slate-300 leading-relaxed">
            You may cancel at any time before completing payment. No charges will be made.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Support Period (Not a Refund Window)</h2>
          <p className="text-slate-300 leading-relaxed">
            Your package includes post-delivery support:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Starter:</strong> 7 days of email support.</li>
            <li><strong>Professional:</strong> 30 days of priority support.</li>
            <li><strong>Enterprise:</strong> 30 days of hands-on support.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            During this period, we will help you with:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Tweaking workflows to better match your needs.</li>
            <li>Fixing bugs or errors.</li>
            <li>Adjusting triggers, filters, or notification settings.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            This is <strong>not a trial period</strong>. Once delivered, the work is complete and refunds are not available. 
            However, we are committed to making sure the automation works for you.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Upgrades and Additional Work</h2>
          <p className="text-slate-300 leading-relaxed">
            If you start with Starter and later want to upgrade to Professional or Enterprise, you can pay the difference. 
            Refunds for upgrades follow the same policy as original purchases.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Additional workflows requested outside your original package are priced separately and are non-refundable once delivered.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Exceptional Circumstances</h2>
          <p className="text-slate-300 leading-relaxed">
            In rare cases (e.g., technical impossibility, significant service failure on our part), we may issue a refund 
            even after delivery. This is assessed on a case-by-case basis.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Contact <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> to discuss.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Legal Rights</h2>
          <p className="text-slate-300 leading-relaxed">
            This policy does not affect your statutory rights under UK consumer protection law. If you believe we have 
            failed to deliver the agreed service, you may have additional rights.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Contact Us</h2>
          <p className="text-slate-300 leading-relaxed">
            For refund requests or questions, contact us at:
          </p>
          <ul className="list-none space-y-1 text-slate-300 ml-4">
            <li>Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
