import Link from "next/link";

export default function EmailUnsubscribePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Email Unsubscribe Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">One-Click Unsubscribe</h2>
          <p className="text-slate-300 leading-relaxed">
            Every marketing email from Levqor includes an unsubscribe link in the footer. Clicking this link will:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Instantly remove you from our marketing list</li>
            <li>Take you to a confirmation page</li>
            <li>No login or password required</li>
            <li>No questions asked</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Processing Time</h2>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Standard processing:</strong> Unsubscribe requests are processed within <strong className="text-white">48 hours</strong>.
            </p>
            <p className="text-slate-400 text-sm">
              You may receive one final marketing email if it was already scheduled before your unsubscribe request was processed. After 48 hours, you will no longer receive marketing communications.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Alternative Unsubscribe Methods</h2>
          <div className="space-y-4">
            <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Account Settings</h3>
              <p className="text-slate-300 text-sm">
                If you have a Levqor account, visit{" "}
                <Link href="/settings/marketing" className="text-emerald-400 hover:underline">
                  Marketing Preferences
                </Link>{" "}
                to manage your email subscriptions and update your preferences.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Email Support</h3>
              <p className="text-slate-300 text-sm">
                Send an email to{" "}
                <a href="mailto:unsubscribe@levqor.ai" className="text-emerald-400 hover:underline">
                  unsubscribe@levqor.ai
                </a>{" "}
                with "UNSUBSCRIBE" in the subject line. Include the email address you wish to unsubscribe.
              </p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">General Support</h3>
              <p className="text-slate-300 text-sm">
                Contact{" "}
                <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                  support@levqor.ai
                </a>{" "}
                with your unsubscribe request. We'll process it manually if needed.
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Transactional Emails (Cannot Unsubscribe)</h2>
          <div className="bg-yellow-950/20 border border-yellow-900/30 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Important:</strong> You cannot unsubscribe from transactional emails. These are essential service communications required to operate your account:
            </p>
            <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
              <li><strong className="text-white">Order & Payment:</strong> Purchase confirmations, receipts, invoices, payment failures</li>
              <li><strong className="text-white">Account Security:</strong> Password resets, login alerts, suspicious activity warnings</li>
              <li><strong className="text-white">Service Updates:</strong> Maintenance windows, outage notifications, service changes</li>
              <li><strong className="text-white">Support:</strong> Ticket responses, support case updates</li>
              <li><strong className="text-white">Legal & Compliance:</strong> Policy updates, terms changes, GDPR notices, data breach notifications</li>
              <li><strong className="text-white">Billing:</strong> Payment reminders, subscription renewals, cancellation confirmations</li>
            </ul>
            <p className="text-slate-400 text-sm mt-4">
              These emails are legally required or necessary to fulfill our contract with you. They are <strong className="text-white">not marketing</strong> and are exempt from GDPR marketing consent requirements.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Re-Subscribing</h2>
          <p className="text-slate-300 leading-relaxed">
            Changed your mind? You can re-subscribe to marketing emails at any time:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Visit{" "}
              <Link href="/settings/marketing" className="text-emerald-400 hover:underline">
                Marketing Preferences
              </Link>{" "}
              and opt back in
            </li>
            <li>Email{" "}
              <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                support@levqor.ai
              </a>{" "}
              requesting re-subscription
            </li>
            <li>Fill out a newsletter signup form on our website</li>
          </ul>
          <p className="text-slate-400 text-sm mt-4">
            You'll need to complete double opt-in verification again to ensure your consent is current.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">GDPR Compliance</h2>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              Our unsubscribe process complies with:
            </p>
            <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4 text-sm">
              <li><strong className="text-white">GDPR Article 21:</strong> Right to object to processing</li>
              <li><strong className="text-white">GDPR Article 7(3):</strong> Easy withdrawal of consent</li>
              <li><strong className="text-white">PECR Regulation 22:</strong> Marketing communications opt-out</li>
              <li><strong className="text-white">ICO Guidance:</strong> Clear, simple unsubscribe mechanisms</li>
            </ul>
            <p className="text-slate-300 text-sm mt-3">
              We log all unsubscribe requests for compliance and audit purposes. Your data is retained in compliance with our{" "}
              <Link href="/privacy" className="text-emerald-400 hover:underline">
                Privacy Policy
              </Link>.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Questions or Issues?</h2>
          <p className="text-slate-300 leading-relaxed">
            If you continue to receive marketing emails after unsubscribing, or have any questions:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Email{" "}
              <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">
                privacy@levqor.ai
              </a>{" "}
              (Data Protection Officer)
            </li>
            <li>Email{" "}
              <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                support@levqor.ai
              </a>{" "}
              (General Support)
            </li>
            <li>Contact the ICO (UK supervisory authority) if unresolved</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex flex-wrap gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/marketing-consent" className="text-emerald-400 hover:underline">Marketing Consent</Link>
            <Link href="/privacy-tools/opt-out" className="text-emerald-400 hover:underline">GDPR Opt-Out Controls</Link>
            <Link href="/settings/marketing" className="text-emerald-400 hover:underline">Manage Preferences</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
