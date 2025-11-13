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

        <p className="text-sm text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-lg p-4 mb-8">
          <strong>Disclaimer:</strong> This document is a standard template and does not constitute legal advice. 
          For compliance questions specific to your situation, please consult a qualified solicitor.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Who We Are</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor is an automation platform designed for operators, founders, and teams. We are based in London, UK, 
            and process data in accordance with UK GDPR and applicable data protection laws.
          </p>
          <p className="text-slate-300 leading-relaxed">
            You can contact us at: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> or <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a>.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Data We Collect</h2>
          <p className="text-slate-300 leading-relaxed">
            When you use Levqor, we may collect:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Account details:</strong> Email address, name, authentication tokens (via Google or Microsoft OAuth).</li>
            <li><strong>Usage logs:</strong> Workflow execution records, API calls, error reports, and system performance metrics.</li>
            <li><strong>Payment information:</strong> Billing details processed and stored by Stripe (we do not store full card numbers).</li>
            <li><strong>Technical data:</strong> IP address, browser type, device information, and timestamps.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. How We Use Your Data</h2>
          <p className="text-slate-300 leading-relaxed">
            We use your data to:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Provide and improve our automation platform.</li>
            <li>Execute workflows and monitor system health.</li>
            <li>Send alerts, notifications, and operational updates.</li>
            <li>Process payments and manage subscriptions.</li>
            <li>Comply with legal obligations and prevent abuse.</li>
            <li>Analyze platform usage and generate insights (anonymized where appropriate).</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Legal Basis for Processing</h2>
          <p className="text-slate-300 leading-relaxed">
            Under UK GDPR, we process your data based on:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Contract:</strong> To fulfill our service agreement with you.</li>
            <li><strong>Legitimate interests:</strong> To improve our platform, prevent fraud, and maintain security.</li>
            <li><strong>Legal obligation:</strong> To comply with UK tax, financial, and regulatory requirements.</li>
            <li><strong>Consent:</strong> For optional analytics and marketing (where applicable).</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Third-Party Processors</h2>
          <p className="text-slate-300 leading-relaxed">
            We work with trusted third-party services to operate Levqor:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Stripe:</strong> Payment processing (PCI-DSS compliant).</li>
            <li><strong>Vercel:</strong> Application hosting and CDN.</li>
            <li><strong>Neon (PostgreSQL):</strong> Database hosting.</li>
            <li><strong>Replit:</strong> Development and deployment infrastructure.</li>
            <li><strong>Cloudflare:</strong> CDN, DNS, and DDoS protection.</li>
            <li><strong>Resend:</strong> Transactional email delivery.</li>
            <li><strong>Google / Microsoft:</strong> OAuth authentication providers.</li>
            <li><strong>Sentry:</strong> Error tracking and monitoring.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            These processors are selected for their strong data protection standards. We have appropriate agreements in place 
            to ensure they handle your data securely and in compliance with UK GDPR.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Data Retention</h2>
          <p className="text-slate-300 leading-relaxed">
            We retain your data as follows:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Account data:</strong> Retained while your account is active, plus 90 days after deletion.</li>
            <li><strong>Workflow logs:</strong> Retained for 12 months for operational and debugging purposes.</li>
            <li><strong>Payment records:</strong> Retained for 7 years to comply with UK tax regulations.</li>
            <li><strong>Error reports:</strong> Retained for 6 months to improve system stability.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            After these periods, data is securely deleted or anonymized.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Your Rights</h2>
          <p className="text-slate-300 leading-relaxed">
            Under UK GDPR, you have the right to:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Access:</strong> Request a copy of your personal data.</li>
            <li><strong>Correction:</strong> Request corrections to inaccurate data.</li>
            <li><strong>Deletion:</strong> Request deletion of your data (subject to legal retention requirements).</li>
            <li><strong>Portability:</strong> Request your data in a machine-readable format.</li>
            <li><strong>Restriction:</strong> Request limited processing in certain circumstances.</li>
            <li><strong>Object:</strong> Object to processing based on legitimate interests.</li>
            <li><strong>Withdraw consent:</strong> Where consent is the legal basis.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            To exercise these rights, contact us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>. 
            We will respond within 30 days.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Security</h2>
          <p className="text-slate-300 leading-relaxed">
            We implement industry-standard security measures including:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Encryption in transit (HTTPS/TLS) and at rest.</li>
            <li>Regular security audits and vulnerability scans.</li>
            <li>Access controls and authentication.</li>
            <li>Automated monitoring and alerting.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            However, no system is 100% secure. You are responsible for securing your account credentials and enabling 
            two-factor authentication where available.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Automated Decision-Making</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor performs automated monitoring, anomaly detection, and workflow execution. These automated systems 
            are designed to self-heal failures and optimize performance. You retain full control over your workflows 
            and can override automated decisions at any time.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. International Transfers</h2>
          <p className="text-slate-300 leading-relaxed">
            Some of our processors operate servers in the United States and other regions. We ensure adequate safeguards 
            are in place, such as Standard Contractual Clauses (SCCs) and compliance with UK-approved transfer mechanisms.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">11. Cookies</h2>
          <p className="text-slate-300 leading-relaxed">
            We use essential cookies for authentication and session management, and optional analytics cookies to improve 
            our platform. See our <Link href="/cookies" className="text-emerald-400 hover:underline">Cookie Policy</Link> for details.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">12. Changes to This Policy</h2>
          <p className="text-slate-300 leading-relaxed">
            We may update this Privacy Policy from time to time. Significant changes will be communicated via email or 
            a notice on our platform. Continued use of Levqor after changes constitutes acceptance.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">13. Contact Us</h2>
          <p className="text-slate-300 leading-relaxed">
            For privacy questions or to exercise your rights, contact us at:
          </p>
          <ul className="list-none space-y-1 text-slate-300 ml-4">
            <li>Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
            <li>Security: <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a></li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-4">
            You also have the right to lodge a complaint with the UK Information Commissioner's Office (ICO) at 
            <a href="https://ico.org.uk" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline"> ico.org.uk</a>.
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
