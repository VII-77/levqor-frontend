import Link from "next/link";

export default function MarketingConsentPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Marketing Consent Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">When We Collect Consent</h2>
          <p className="text-slate-300 leading-relaxed">
            Levqor collects marketing consent at the following touchpoints:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>During account sign-up (optional checkbox)</li>
            <li>When subscribing to newsletters or product updates</li>
            <li>At checkout when purchasing DFY builds or subscriptions</li>
            <li>Through lead generation forms or gated content</li>
          </ul>
          <p className="text-slate-300 leading-relaxed mt-4">
            Marketing consent is <strong className="text-white">always optional</strong> and separate from service-related communications.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Double Opt-In Required</h2>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              To comply with GDPR and PECR (Privacy and Electronic Communications Regulations), we use <strong className="text-white">double opt-in</strong> for all marketing communications:
            </p>
            <ol className="list-decimal list-inside space-y-2 text-slate-300 ml-4">
              <li><strong className="text-white">Initial Consent:</strong> You check the marketing consent box during sign-up or subscription</li>
              <li><strong className="text-white">Confirmation Email:</strong> We send a confirmation email to verify your email address</li>
              <li><strong className="text-white">Verification Required:</strong> You must click the confirmation link to activate your subscription</li>
              <li><strong className="text-white">Active Subscription:</strong> Only after confirmation will you receive marketing emails</li>
            </ol>
            <p className="text-slate-400 text-sm mt-4">
              This process ensures your consent is genuine, verified, and documented.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">What You'll Receive</h2>
          <p className="text-slate-300 leading-relaxed">
            With your consent, we may send:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Product updates and new feature announcements</li>
            <li>Automation tips, best practices, and case studies</li>
            <li>Exclusive offers, discounts, and early access to new products</li>
            <li>Educational content (webinars, guides, tutorials)</li>
            <li>Industry news and insights relevant to automation</li>
          </ul>
          <p className="text-slate-400 text-sm mt-4">
            Frequency: Typically 2–4 emails per month. We respect your inbox.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">How to Withdraw Consent</h2>
          <div className="bg-emerald-950/20 border border-emerald-900/30 rounded-lg p-6 space-y-3">
            <p className="text-slate-300 leading-relaxed">
              You can withdraw marketing consent at any time through multiple methods:
            </p>
            <div className="space-y-4">
              <div>
                <h3 className="text-white font-semibold mb-1">1. Unsubscribe Link</h3>
                <p className="text-slate-400 text-sm">
                  Every marketing email includes an unsubscribe link in the footer. One click, instant opt-out.
                </p>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">2. Account Settings</h3>
                <p className="text-slate-400 text-sm">
                  Visit{" "}
                  <Link href="/settings/marketing" className="text-emerald-400 hover:underline">
                    /settings/marketing
                  </Link>{" "}
                  to manage your email preferences and subscriptions.
                </p>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">3. Email Support</h3>
                <p className="text-slate-400 text-sm">
                  Email{" "}
                  <a href="mailto:unsubscribe@levqor.ai" className="text-emerald-400 hover:underline">
                    unsubscribe@levqor.ai
                  </a>{" "}
                  with "UNSUBSCRIBE" in the subject line.
                </p>
              </div>
            </div>
            <p className="text-slate-300 text-sm mt-4">
              <strong className="text-white">Processing time:</strong> Unsubscribe requests are processed within 48 hours. You may receive one final email if already in flight.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Transactional Emails</h2>
          <div className="bg-yellow-950/20 border border-yellow-900/30 rounded-lg p-6">
            <p className="text-slate-300 leading-relaxed">
              <strong className="text-white">Important:</strong> Unsubscribing from marketing emails does <strong className="text-white">not</strong> opt you out of:
            </p>
            <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4 mt-2">
              <li>Order confirmations and receipts</li>
              <li>Service updates and maintenance notifications</li>
              <li>Security alerts and account notifications</li>
              <li>Billing and payment reminders</li>
              <li>Support ticket responses</li>
              <li>Legal notices and policy updates</li>
            </ul>
            <p className="text-slate-400 text-sm mt-3">
              These are essential service communications required to operate your account.
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Data We Collect</h2>
          <p className="text-slate-300 leading-relaxed">
            When you consent to marketing communications, we collect and process:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Email address (required)</li>
            <li>Name (if provided)</li>
            <li>Company name (if provided)</li>
            <li>Consent timestamp and IP address (for compliance records)</li>
            <li>Email engagement data (opens, clicks) to improve relevance</li>
          </ul>
          <p className="text-slate-400 text-sm mt-4">
            We do not sell, rent, or share your email address with third parties for their marketing purposes.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Your Rights</h2>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-2">
            <p className="text-slate-300 text-sm">
              Under GDPR and UK GDPR, you have the right to:
            </p>
            <ul className="list-disc list-inside space-y-1 text-slate-300 ml-4 text-sm">
              <li>Withdraw consent at any time (no explanation needed)</li>
              <li>Access your marketing data (via{" "}
                <Link href="/data-requests" className="text-emerald-400 hover:underline">
                  data request
                </Link>)
              </li>
              <li>Request deletion of your marketing data</li>
              <li>Object to processing (see{" "}
                <Link href="/privacy-tools/opt-out" className="text-emerald-400 hover:underline">
                  opt-out controls
                </Link>)
              </li>
              <li>Lodge a complaint with the ICO (UK supervisory authority)</li>
            </ul>
          </div>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex flex-wrap gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/email-unsubscribe" className="text-emerald-400 hover:underline">Email Unsubscribe Policy</Link>
            <Link href="/data-requests" className="text-emerald-400 hover:underline">Data Requests</Link>
            <Link href="/settings/marketing" className="text-emerald-400 hover:underline">Manage Preferences</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
