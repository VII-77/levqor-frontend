import Link from "next/link";

export default function SecurityPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Security & Data Protection</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-sm text-blue-400 bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 mb-8">
          <strong>Our commitment:</strong> Security and data protection are foundational to Levqor. We implement industry 
          best practices to keep your workflows and data safe.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. Overview</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor handles sensitive workflow data, integrations with third-party services, and automated operations on 
            your behalf. We take security seriously and continuously invest in protecting your data.
          </p>
          <p className="text-slate-300 leading-relaxed">
            However, <strong>no system is 100% secure</strong>. This page outlines our security measures and your 
            responsibilities.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Encryption</h2>
          
          <div className="space-y-4">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Encryption in Transit (HTTPS/TLS)</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                All data transmitted between your browser and Levqor is encrypted using <strong>TLS 1.2+</strong>. 
                This includes:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>Login credentials and session tokens.</li>
                <li>Workflow configurations and API keys.</li>
                <li>API requests and responses.</li>
              </ul>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Encryption at Rest</h3>
              <p className="text-slate-300 text-sm leading-relaxed">
                Data stored in our databases (PostgreSQL via Neon) is encrypted at rest using <strong>AES-256 encryption</strong>. 
                This includes:
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-300 text-sm ml-4 mt-2">
                <li>User account information.</li>
                <li>Workflow execution logs.</li>
                <li>API keys and secrets (hashed where appropriate).</li>
              </ul>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Authentication & Access Control</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor uses <strong>OAuth 2.0</strong> for authentication via Google and Microsoft. We do not store your 
            passwords—authentication is handled by these trusted identity providers.
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Session tokens:</strong> Short-lived and rotated regularly.</li>
            <li><strong>CSRF protection:</strong> All state-changing requests are protected against cross-site request forgery.</li>
            <li><strong>Rate limiting:</strong> API endpoints are rate-limited to prevent abuse (20 requests/minute per IP, 
            200 requests/minute globally).</li>
            <li><strong>API key rotation:</strong> API keys can be rotated with zero downtime.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Infrastructure Security</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor is hosted on trusted, enterprise-grade infrastructure:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Vercel:</strong> Serverless deployment with automatic HTTPS and DDoS protection.</li>
            <li><strong>Neon (PostgreSQL):</strong> Managed database with daily backups and point-in-time recovery.</li>
            <li><strong>Cloudflare:</strong> CDN and firewall protecting against DDoS, bot attacks, and malicious traffic.</li>
            <li><strong>Replit:</strong> Secure development environment with automated security updates.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            All infrastructure providers are SOC 2 Type II certified and comply with GDPR.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Application Security</h2>
          <p className="text-slate-300 leading-relaxed">
            We implement secure coding practices and continuously monitor for vulnerabilities:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Input validation:</strong> All user inputs are validated and sanitized to prevent injection attacks.</li>
            <li><strong>JSON schema validation:</strong> API requests are validated against strict schemas.</li>
            <li><strong>Request size limits:</strong> 512KB max body size to prevent resource exhaustion.</li>
            <li><strong>Security headers:</strong> HSTS, CSP, COOP, COEP, and X-Frame-Options to mitigate common attacks.</li>
            <li><strong>Dependency scanning:</strong> Automated checks for vulnerable npm packages.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Monitoring & Incident Response</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor includes comprehensive monitoring and alerting:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Error tracking:</strong> Sentry monitors all errors and anomalies in real-time.</li>
            <li><strong>Health checks:</strong> Automated synthetic checks every 5-15 minutes.</li>
            <li><strong>Anomaly detection:</strong> AI-powered monitoring flags unusual latency or failure patterns.</li>
            <li><strong>Audit logs:</strong> All critical actions (API key changes, workflow modifications) are logged.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            In the event of a security incident, we will:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Investigate and contain the incident within 24 hours.</li>
            <li>Notify affected users within 72 hours (or sooner if required by law).</li>
            <li>Provide a public incident report with lessons learned.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Data Backups</h2>
          <p className="text-slate-300 leading-relaxed">
            Our database provider (Neon) performs:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Daily backups:</strong> Full database snapshots retained for 7 days.</li>
            <li><strong>Point-in-time recovery:</strong> Restore to any moment within the last 7 days.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            Backups are encrypted and stored in geographically separate regions.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Third-Party Integrations</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor integrates with third-party services (Google, Stripe, Notion, etc.). Security responsibilities:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>OAuth tokens:</strong> Stored encrypted and scoped to minimum necessary permissions.</li>
            <li><strong>API keys:</strong> Hashed and never logged in plain text.</li>
            <li><strong>Webhook verification:</strong> HMAC signatures validate incoming webhooks.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            You are responsible for securing your own third-party accounts (e.g., enabling 2FA on Google).
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">9. Your Responsibilities</h2>
          <p className="text-slate-300 leading-relaxed">
            To keep your account secure, you should:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Use strong authentication:</strong> Enable 2FA on your Google or Microsoft account.</li>
            <li><strong>Protect your credentials:</strong> Do not share your login details or API keys.</li>
            <li><strong>Monitor activity:</strong> Review workflow execution logs regularly for unexpected behavior.</li>
            <li><strong>Report suspicious activity:</strong> Contact <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a> immediately 
            if you notice anything unusual.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">10. Compliance</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor complies with:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>UK GDPR:</strong> Data protection and user rights (see our <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>).</li>
            <li><strong>PCI-DSS (via Stripe):</strong> Payment data is handled by Stripe, a PCI Level 1 certified provider.</li>
            <li><strong>UK tax regulations:</strong> Secure retention of payment records for 7 years.</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">11. Reporting Security Issues</h2>
          <p className="text-slate-300 leading-relaxed">
            If you discover a security vulnerability in Levqor, please report it responsibly:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Email: <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a></li>
            <li>Include: Description, steps to reproduce, and potential impact.</li>
            <li>We will acknowledge receipt within 24 hours and provide updates as we investigate.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            We appreciate responsible disclosure and will credit researchers (with their permission) in our security advisories.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">12. Limitations</h2>
          <p className="text-slate-300 leading-relaxed">
            While we implement strong security measures, <strong>no system is impenetrable</strong>. We cannot guarantee:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>100% uptime or zero risk of data breaches.</li>
            <li>Security of third-party services you integrate with (Google, Stripe, etc.).</li>
            <li>Protection against sophisticated state-sponsored attacks.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            You use Levqor at your own risk. See our <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link> for liability disclaimers.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">13. Contact Us</h2>
          <p className="text-slate-300 leading-relaxed">
            For security questions or to report an issue, contact us at:
          </p>
          <ul className="list-none space-y-1 text-slate-300 ml-4">
            <li>Email: <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a></li>
            <li>General support: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a></li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
