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

        <p className="text-sm text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-lg p-4 mb-8">
          <strong>Disclaimer:</strong> This document is a standard template and does not constitute legal advice. 
          You are responsible for your own use of the platform.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Agreement to Terms</h2>
          <p className="text-slate-300 leading-relaxed">
            By accessing or using Levqor (the "Service"), you agree to be bound by these Terms of Service. 
            If you do not agree, do not use the Service.
          </p>
          <p className="text-slate-300 leading-relaxed">
            These Terms constitute a legally binding agreement between you and Levqor. We reserve the right to update 
            these Terms at any time. Your continued use after changes constitutes acceptance.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Description of Service</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor is a done-for-you automation platform. We build, configure, and monitor workflows that integrate 
            with your existing tools (email, spreadsheets, CRMs, APIs, etc.). Our platform includes:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Workflow design and implementation.</li>
            <li>Self-healing automation with failure detection and recovery.</li>
            <li>Monitoring dashboards and alerts.</li>
            <li>Integration with third-party services (Google, Microsoft, Stripe, etc.).</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Account Responsibilities</h2>
          <p className="text-slate-300 leading-relaxed">
            You are responsible for:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Maintaining the confidentiality of your account credentials.</li>
            <li>All activities that occur under your account.</li>
            <li>Ensuring your workflows comply with applicable laws and regulations.</li>
            <li>Notifying us immediately of any unauthorized access or security breach.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            We recommend enabling two-factor authentication (2FA) on your Google or Microsoft account used for sign-in.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Acceptable Use</h2>
          <p className="text-slate-300 leading-relaxed">
            You agree not to:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Use the Service for illegal activities, spam, or malicious purposes.</li>
            <li>Abuse, exploit, or attempt to gain unauthorized access to our systems.</li>
            <li>Violate intellectual property rights or third-party terms of service.</li>
            <li>Exceed rate limits or deliberately overload our infrastructure.</li>
            <li>Create workflows that automate harassment, discrimination, or harmful activities.</li>
            <li>Reverse-engineer, decompile, or attempt to extract source code.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            We reserve the right to suspend or terminate accounts that violate these terms.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Payment and Billing</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor operates on a done-for-you, one-time payment model:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Pricing:</strong> £99 (Starter), £249 (Professional), £599 (Enterprise).</li>
            <li><strong>Payment:</strong> One-time payment for workflow development and initial support period.</li>
            <li><strong>Delivery:</strong> We deliver your automation within the specified timeframe (typically 48 hours to 7 days).</li>
            <li><strong>Additional work:</strong> Upgrades or additional workflows are priced separately.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            All payments are processed securely via Stripe. We do not store your full card details.
          </p>
          <p className="text-slate-300 leading-relaxed">
            For refund and cancellation terms, see our <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Service Availability and Support</h2>
          <p className="text-slate-300 leading-relaxed">
            We aim to provide a reliable service but cannot guarantee 100% uptime. Scheduled maintenance and 
            unexpected outages may occur.
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Starter:</strong> 7 days of email support after delivery.</li>
            <li><strong>Professional:</strong> 30 days of priority email support.</li>
            <li><strong>Enterprise:</strong> 30 days of hands-on support and monitoring.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Intellectual Property</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor retains all rights to the platform's code, design, and proprietary technology. You retain ownership 
            of your data and workflow configurations.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Upon payment, you receive a non-exclusive, non-transferable license to use the workflows we build for you. 
            You may not resell, redistribute, or sublicense our work without written permission.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Disclaimers and Limitations of Liability</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor is provided "as is" without warranties of any kind, express or implied. We do not guarantee:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>That the Service will be error-free or uninterrupted.</li>
            <li>That workflows will meet all your specific business requirements.</li>
            <li>That third-party integrations (Google, Stripe, etc.) will always function correctly.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            To the fullest extent permitted by law, Levqor shall not be liable for:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Indirect, incidental, or consequential damages.</li>
            <li>Loss of profits, data, or business opportunities.</li>
            <li>Damages arising from third-party service failures.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            Our total liability to you shall not exceed the amount you paid for the Service.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Indemnification</h2>
          <p className="text-slate-300 leading-relaxed">
            You agree to indemnify and hold Levqor harmless from any claims, damages, or expenses arising from:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Your use of the Service.</li>
            <li>Your violation of these Terms.</li>
            <li>Your workflows or data.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Termination</h2>
          <p className="text-slate-300 leading-relaxed">
            We reserve the right to suspend or terminate your account if:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>You violate these Terms.</li>
            <li>Your workflows pose a security risk or violate third-party terms.</li>
            <li>We discontinue the Service (with reasonable notice).</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            Upon termination, you will lose access to your workflows and data. We may retain logs and records as 
            required by law or for operational purposes.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">11. Governing Law and Disputes</h2>
          <p className="text-slate-300 leading-relaxed">
            These Terms are governed by the laws of England and Wales. Any disputes shall be resolved in the courts 
            of England and Wales.
          </p>
          <p className="text-slate-300 leading-relaxed">
            For informal resolution, please contact us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> before 
            pursuing legal action.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">12. Changes to These Terms</h2>
          <p className="text-slate-300 leading-relaxed">
            We may update these Terms from time to time. Material changes will be communicated via email or a notice 
            on our platform. Continued use after changes constitutes acceptance.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">13. Contact Us</h2>
          <p className="text-slate-300 leading-relaxed">
            For questions about these Terms, contact us at:
          </p>
          <ul className="list-none space-y-1 text-slate-300 ml-4">
            <li>Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
          </ul>
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
