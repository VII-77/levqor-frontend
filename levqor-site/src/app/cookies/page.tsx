import Link from "next/link";

export default function CookiesPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Cookie Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">1. What Are Cookies?</h2>
          <p className="text-slate-300 leading-relaxed">
            Cookies are small text files stored on your device when you visit a website. They help websites remember your 
            preferences and provide essential functionality.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Levqor uses cookies to ensure secure authentication, maintain session state, and improve your experience.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">2. Types of Cookies We Use</h2>
          
          <div className="space-y-4">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Essential Cookies</h3>
              <p className="text-slate-300 text-sm leading-relaxed mb-2">
                These cookies are necessary for the platform to function. They enable core features like authentication, 
                session management, and security.
              </p>
              <p className="text-slate-300 text-sm">
                <strong>Examples:</strong> Login session tokens, CSRF protection, cookie consent preferences.
              </p>
              <p className="text-emerald-400 text-sm mt-2">
                ✓ These cookies cannot be disabled as they are required for the Service to work.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Analytics Cookies</h3>
              <p className="text-slate-300 text-sm leading-relaxed mb-2">
                These cookies help us understand how users interact with Levqor, which features are most used, and where 
                improvements can be made.
              </p>
              <p className="text-slate-300 text-sm">
                <strong>Examples:</strong> Page views, workflow execution counts, error tracking (via Sentry).
              </p>
              <p className="text-slate-400 text-sm mt-2">
                ℹ️ Analytics data is anonymized where possible.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-bold text-white mb-2">Third-Party Cookies</h3>
              <p className="text-slate-300 text-sm leading-relaxed mb-2">
                When you sign in with Google or Microsoft, those providers may set their own cookies to manage authentication.
              </p>
              <p className="text-slate-300 text-sm">
                <strong>Providers:</strong> Google OAuth, Microsoft Azure AD, Stripe (for payment processing).
              </p>
              <p className="text-slate-400 text-sm mt-2">
                ℹ️ These cookies are subject to the privacy policies of Google, Microsoft, and Stripe respectively.
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">3. Cookies We Set</h2>
          <p className="text-slate-300 leading-relaxed">
            Below is a summary of the main cookies used by Levqor:
          </p>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-slate-300 border border-slate-800 rounded-lg">
              <thead className="bg-slate-900">
                <tr>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Cookie Name</th>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Purpose</th>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Type</th>
                  <th className="px-4 py-2 text-left border-b border-slate-800">Duration</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">next-auth.session-token</td>
                  <td className="px-4 py-2">Maintains your login session</td>
                  <td className="px-4 py-2">Essential</td>
                  <td className="px-4 py-2">30 days</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">next-auth.csrf-token</td>
                  <td className="px-4 py-2">Security (CSRF protection)</td>
                  <td className="px-4 py-2">Essential</td>
                  <td className="px-4 py-2">Session</td>
                </tr>
                <tr className="border-b border-slate-800">
                  <td className="px-4 py-2">levqor_cookie_consent</td>
                  <td className="px-4 py-2">Stores your cookie preferences</td>
                  <td className="px-4 py-2">Essential</td>
                  <td className="px-4 py-2">1 year</td>
                </tr>
                <tr>
                  <td className="px-4 py-2">_sentry_*</td>
                  <td className="px-4 py-2">Error tracking and debugging</td>
                  <td className="px-4 py-2">Analytics</td>
                  <td className="px-4 py-2">Session</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">4. Managing Your Cookie Preferences</h2>
          <p className="text-slate-300 leading-relaxed">
            You can control cookies through:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li><strong>Browser settings:</strong> Most browsers allow you to block or delete cookies. Consult your browser's 
            help documentation for instructions.</li>
            <li><strong>Cookie banner:</strong> When you first visit Levqor, you can accept or decline non-essential cookies 
            via the cookie banner.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-4">
            <strong>Note:</strong> Blocking essential cookies will prevent you from signing in and using the platform.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">5. Local Storage and Session Storage</h2>
          <p className="text-slate-300 leading-relaxed">
            In addition to cookies, Levqor may use browser local storage and session storage to:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Cache workflow data for faster load times.</li>
            <li>Store temporary UI state (e.g., expanded sections, filters).</li>
            <li>Remember your cookie consent choice.</li>
          </ul>
          <p className="text-slate-300 leading-relaxed">
            This data is stored locally on your device and is not sent to our servers unless required for functionality.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">6. Data Protection and Privacy</h2>
          <p className="text-slate-300 leading-relaxed">
            Cookie data is processed in accordance with our <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link> and 
            UK GDPR. We do not use cookies to track you across third-party websites.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">7. Changes to This Policy</h2>
          <p className="text-slate-300 leading-relaxed">
            We may update this Cookie Policy from time to time. Changes will be reflected here with an updated "Last updated" date.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">8. Contact Us</h2>
          <p className="text-slate-300 leading-relaxed">
            For questions about cookies, contact us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>.
          </p>
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
