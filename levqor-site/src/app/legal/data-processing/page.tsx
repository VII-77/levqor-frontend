import Link from "next/link";

export default function DataProcessingPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Data Processing Addendum (DPA)</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-sm text-amber-400 bg-amber-500/10 border border-amber-500/30 rounded-lg p-4 mb-8">
          <strong>Note:</strong> This is a short-form Data Processing Addendum template. For enterprise customers requiring 
          a formal DPA or custom terms, please contact us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Introduction</h2>
          <p className="text-slate-300 leading-relaxed">
            This Data Processing Addendum ("DPA") supplements our <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link> and 
            <Link href="/privacy" className="text-emerald-400 hover:underline"> Privacy Policy</Link>. It outlines how Levqor processes personal data on your behalf when 
            you use our automation platform.
          </p>
          <p className="text-slate-300 leading-relaxed">
            This DPA applies where you (the "Controller") use Levqor to process personal data and Levqor acts as your 
            "Processor" under UK GDPR.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Roles and Responsibilities</h2>
          
          <div className="space-y-4">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">You (Controller)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                You determine the purposes and means of processing personal data when:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>Designing workflows that collect or use personal data (e.g., customer emails, contact lists).</li>
                <li>Configuring integrations that access personal data (e.g., Gmail, CRM systems).</li>
                <li>Deciding what data to store, how long to retain it, and who can access it.</li>
              </ul>
              <p className="text-slate-300 text-sm mt-2">
                <strong>Your obligations:</strong> Ensure you have a lawful basis for processing, inform data subjects, 
                and comply with UK GDPR.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Levqor (Processor)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                Levqor processes personal data on your behalf when:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>Executing workflows that handle personal data.</li>
                <li>Storing workflow logs, execution records, and error reports.</li>
                <li>Providing monitoring, alerts, and debugging services.</li>
              </ul>
              <p className="text-slate-300 text-sm mt-2">
                <strong>Our obligations:</strong> Process data only as instructed, implement appropriate security, and 
                assist with data subject requests.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Levqor (Controller)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                Levqor also acts as a Controller for:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>Your account information (email, name, authentication tokens).</li>
                <li>Platform usage analytics and error telemetry.</li>
                <li>Billing and payment records (via Stripe).</li>
              </ul>
              <p className="text-slate-300 text-sm mt-2">
                This data is processed under our <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>, not this DPA.
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Scope of Processing</h2>
          <p className="text-slate-300 leading-relaxed">
            When acting as your Processor, Levqor may process:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Subject matter:</strong> Execution of automated workflows on your behalf.</li>
            <li><strong>Duration:</strong> For the duration of your service engagement plus retention period (typically 12 months for logs).</li>
            <li><strong>Nature and purpose:</strong> Workflow automation, monitoring, error detection, and alerting.</li>
            <li><strong>Types of personal data:</strong> Any data you choose to include in your workflows (e.g., names, emails, phone numbers, 
            addresses, transaction data, etc.).</li>
            <li><strong>Categories of data subjects:</strong> Your customers, contacts, employees, or other individuals as determined by you.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Processing Instructions</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor will process personal data only in accordance with your documented instructions, which include:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Workflow configurations you design and approve.</li>
            <li>Integration settings (which third-party services to connect to).</li>
            <li>Retention and deletion settings you specify.</li>
            <li>This DPA and our <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            If we believe an instruction violates UK GDPR or other laws, we will notify you immediately.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Sub-Processors</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor uses trusted third-party sub-processors to operate the platform:
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-slate-300 border border-slate-800 rounded-lg">
              <thead className="bg-slate-900">
                <tr>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Sub-Processor</th>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Service</th>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Location</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">Neon (PostgreSQL)</td>
                  <td className="px-4 py-2">Database hosting</td>
                  <td className="px-4 py-2">EU/US</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">Vercel</td>
                  <td className="px-4 py-2">Application hosting</td>
                  <td className="px-4 py-2">Global (CDN)</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">Stripe</td>
                  <td className="px-4 py-2">Payment processing</td>
                  <td className="px-4 py-2">US (PCI-DSS certified)</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">Sentry</td>
                  <td className="px-4 py-2">Error tracking</td>
                  <td className="px-4 py-2">US</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">Resend</td>
                  <td className="px-4 py-2">Email delivery</td>
                  <td className="px-4 py-2">US</td>
                </tr>
                <tr>
                  <td className="px-4 py-2">Cloudflare</td>
                  <td className="px-4 py-2">CDN & security</td>
                  <td className="px-4 py-2">Global</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="text-slate-300 leading-relaxed mt-4">
            By using Levqor, you authorize the use of these sub-processors. We have data processing agreements in place 
            with all sub-processors and ensure they meet GDPR requirements.
          </p>
          <p className="text-slate-300 leading-relaxed">
            If we add new sub-processors, we will update this list and notify you via email. You may object to a new 
            sub-processor within 30 days.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. International Data Transfers</h2>
          <p className="text-slate-300 leading-relaxed">
            Some sub-processors operate in the United States and other countries outside the UK/EU. We ensure adequate 
            safeguards are in place:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Standard Contractual Clauses (SCCs):</strong> Used where required for UK-to-US transfers.</li>
            <li><strong>Adequacy decisions:</strong> We rely on UK/EU adequacy decisions where applicable.</li>
            <li><strong>Processor commitments:</strong> All sub-processors commit to GDPR-equivalent protections.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Security Measures</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor implements technical and organisational measures to protect personal data, including:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Encryption in transit (TLS 1.2+) and at rest (AES-256).</li>
            <li>Access controls and authentication (OAuth 2.0, API key rotation).</li>
            <li>Regular security audits and vulnerability scanning.</li>
            <li>Automated monitoring and alerting (Sentry, health checks).</li>
            <li>Incident response procedures (24-hour containment, 72-hour notification).</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            For full details, see our <Link href="/security" className="text-emerald-400 hover:underline">Security & Data Protection</Link> page.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Data Subject Rights</h2>
          <p className="text-slate-300 leading-relaxed">
            As a Processor, Levqor will assist you in responding to data subject requests (DSRs):
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Access:</strong> We will provide workflow logs and execution records upon your request.</li>
            <li><strong>Deletion:</strong> We will delete personal data from our systems within 30 days of your instruction.</li>
            <li><strong>Rectification:</strong> We will correct inaccurate data as instructed.</li>
            <li><strong>Portability:</strong> We will export data in JSON or CSV format.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            If a data subject contacts us directly, we will redirect them to you as the Controller.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Data Breach Notification</h2>
          <p className="text-slate-300 leading-relaxed">
            In the event of a personal data breach, Levqor will:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Notify you within <strong>24 hours</strong> of becoming aware of the breach.</li>
            <li>Provide details of the breach, affected data, and remediation steps.</li>
            <li>Assist you in assessing whether you need to notify the ICO or data subjects.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            You are responsible for determining whether notification to the ICO or data subjects is required under UK GDPR.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Audits and Compliance</h2>
          <p className="text-slate-300 leading-relaxed">
            You have the right to audit our data processing activities. We will:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Provide audit reports and compliance documentation upon reasonable request.</li>
            <li>Allow you (or a third-party auditor) to inspect our security measures, subject to confidentiality and 
            reasonable notice (30 days).</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            For Enterprise customers, we can arrange formal audit procedures. Contact <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">11. Data Retention and Deletion</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor retains personal data as follows:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Workflow logs:</strong> 12 months (configurable upon request).</li>
            <li><strong>Error reports:</strong> 6 months.</li>
            <li><strong>Account data:</strong> 90 days after account closure.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            You may request early deletion by contacting <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>. 
            We will delete data within 30 days unless legally required to retain it (e.g., UK tax records for 7 years).
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">12. Termination</h2>
          <p className="text-slate-300 leading-relaxed">
            Upon termination of your service:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>We will return or delete all personal data processed on your behalf within 90 days.</li>
            <li>You may request an export of your data before termination.</li>
            <li>We may retain limited data for legal or operational purposes (e.g., billing records, audit logs).</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">13. Limitation of Liability</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor's liability for data processing is subject to the limitations in our <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>. 
            We are not liable for:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Breaches caused by your instructions or misconfigurations.</li>
            <li>Breaches caused by third-party sub-processors (subject to our selection and oversight).</li>
            <li>Indirect or consequential damages.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">14. Governing Law</h2>
          <p className="text-slate-300 leading-relaxed">
            This DPA is governed by the laws of England and Wales and is supplementary to our <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">15. Contact Us</h2>
          <p className="text-slate-300 leading-relaxed">
            For questions about this DPA or to request a formal, signed DPA for enterprise use, contact us at:
          </p>
          <ul className="list-none space-y-1 text-slate-300 ml-4">
            <li>Email: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
            <li>Privacy: <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a></li>
          </ul>
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
