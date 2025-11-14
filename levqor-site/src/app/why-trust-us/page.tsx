"use client";
import Link from "next/link";

export default function WhyTrustUsPage() {
  return (
    <main className="min-h-screen bg-slate-950">
      {/* Header */}
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">
            Levqor
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/" className="text-sm text-slate-300 hover:text-white transition">
              Home
            </Link>
            <Link href="/pricing" className="text-sm text-slate-300 hover:text-white transition">
              Pricing
            </Link>
            <Link href="/signin" className="px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
              Sign in
            </Link>
          </div>
        </nav>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Hero */}
        <section className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <svg className="w-4 h-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
            Built on trust & transparency
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Why trust Levqor with your automations?
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            We're not just another automation tool. We're your automation partner, committed to security, compliance, and your success.
          </p>
        </section>

        {/* Trust Pillars */}
        <section className="mb-20">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Pillar 1 */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8">
              <div className="w-12 h-12 mb-4 rounded-lg bg-emerald-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Security-first approach</h3>
              <ul className="space-y-2 text-slate-400">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>API keys encrypted at rest with AES-256</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>TLS 1.3 encryption for all data in transit</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Zero-downtime API key rotation</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Rate limiting and account lockout protection</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Security event logging with audit trail</span>
                </li>
              </ul>
            </div>

            {/* Pillar 2 */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8">
              <div className="w-12 h-12 mb-4 rounded-lg bg-blue-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">GDPR & PECR compliant</h3>
              <ul className="space-y-2 text-slate-400">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Granular cookie consent with opt-in/opt-out</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Right to access, export, and delete your data (DSAR)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Marketing consent with double opt-in</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Automated data retention and deletion</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Full audit trail for compliance</span>
                </li>
              </ul>
            </div>

            {/* Pillar 3 */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8">
              <div className="w-12 h-12 mb-4 rounded-lg bg-violet-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-violet-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Transparent operations</h3>
              <ul className="space-y-2 text-slate-400">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Public status page with uptime metrics</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>14-day money-back guarantee, no questions asked</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Clear terms of service and privacy policy</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Detailed documentation and FAQs</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Responsive support team (24-48h email response)</span>
                </li>
              </ul>
            </div>

            {/* Pillar 4 */}
            <div className="rounded-2xl bg-slate-900/50 border border-slate-800 p-8">
              <div className="w-12 h-12 mb-4 rounded-lg bg-amber-500/20 flex items-center justify-center">
                <svg className="w-6 h-6 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-white mb-3">Proven reliability</h3>
              <ul className="space-y-2 text-slate-400">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Self-healing workflows that recover from errors</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>24/7 automated health monitoring</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Sentry integration for error tracking</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>Automated weekly reports on workflow health</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span>SLA guarantees available (Business plan)</span>
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Compliance Docs */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              Our compliance commitment
            </h2>
            <p className="text-lg text-slate-400 max-w-2xl mx-auto">
              We maintain comprehensive documentation and processes to protect your data
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <Link href="/docs/ropa" className="rounded-xl bg-slate-900/50 border border-slate-800 p-6 hover:border-emerald-500/50 transition">
              <h3 className="text-lg font-bold text-white mb-2">ROPA</h3>
              <p className="text-sm text-slate-400">
                Record of Processing Activities — how we handle and protect your data
              </p>
            </Link>

            <Link href="/docs/dpia" className="rounded-xl bg-slate-900/50 border border-slate-800 p-6 hover:border-emerald-500/50 transition">
              <h3 className="text-lg font-bold text-white mb-2">DPIA</h3>
              <p className="text-sm text-slate-400">
                Data Protection Impact Assessment — our risk evaluation and mitigation
              </p>
            </Link>

            <Link href="/docs/lia" className="rounded-xl bg-slate-900/50 border border-slate-800 p-6 hover:border-emerald-500/50 transition">
              <h3 className="text-lg font-bold text-white mb-2">LIA</h3>
              <p className="text-sm text-slate-400">
                Legitimate Interest Assessment — legal basis for data processing
              </p>
            </Link>
          </div>
        </section>

        {/* Transparency Actions */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">
              What we do to earn your trust
            </h2>
          </div>

          <div className="space-y-4 max-w-3xl mx-auto">
            <div className="flex gap-4 items-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <span className="text-emerald-400 font-bold">✓</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-white mb-1">We never sell your data</h3>
                <p className="text-slate-400 text-sm">
                  Your workflows, data, and API keys are yours. We don't share, sell, or monetize your information.
                </p>
              </div>
            </div>

            <div className="flex gap-4 items-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <span className="text-emerald-400 font-bold">✓</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-white mb-1">Open communication</h3>
                <p className="text-slate-400 text-sm">
                  Need help? Email <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> and get a human response within 24-48 hours.
                </p>
              </div>
            </div>

            <div className="flex gap-4 items-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <span className="text-emerald-400 font-bold">✓</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-white mb-1">Continuous improvement</h3>
                <p className="text-slate-400 text-sm">
                  We actively monitor, test, and improve our platform. Security patches are deployed within 24 hours of discovery.
                </p>
              </div>
            </div>

            <div className="flex gap-4 items-start">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
                <span className="text-emerald-400 font-bold">✓</span>
              </div>
              <div>
                <h3 className="text-lg font-bold text-white mb-1">UK-based company</h3>
                <p className="text-slate-400 text-sm">
                  Operating under UK law with GDPR/PECR compliance. Your data rights are protected by UK regulations.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="text-center py-12 px-6 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-blue-500/20 border border-emerald-500/30">
          <h2 className="text-2xl font-bold text-white mb-4">
            Ready to build with a partner you can trust?
          </h2>
          <p className="text-slate-400 mb-6 max-w-xl mx-auto">
            Join teams automating with confidence, backed by our security-first approach and 14-day guarantee.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/pricing"
              className="inline-block px-10 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-xl font-bold transition-all shadow-2xl"
            >
              View Pricing
            </Link>
            <Link
              href="/guarantee"
              className="inline-block px-10 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-xl font-bold transition-all border border-slate-700"
            >
              Read Our Guarantee
            </Link>
          </div>
        </section>
      </div>
    </main>
  );
}
