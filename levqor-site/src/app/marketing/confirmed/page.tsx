"use client";

import { useSearchParams } from "next/navigation";
import Link from "next/link";

export default function MarketingConfirmedPage() {
  const searchParams = useSearchParams();
  const success = searchParams.get('success') === 'true';
  const error = searchParams.get('error');

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        {success ? (
          <div className="bg-emerald-500/20 border border-emerald-500/50 rounded-lg p-8 space-y-4">
            <div className="text-6xl mb-4">✓</div>
            <h1 className="text-4xl font-bold text-emerald-400">Subscription Confirmed!</h1>
            <p className="text-slate-300 text-lg">
              Thank you for subscribing to the Levqor newsletter. You're all set!
            </p>
            <p className="text-slate-400">
              You'll start receiving product updates, automation tips, and exclusive offers in your inbox.
            </p>
            <div className="mt-6 pt-6 border-t border-emerald-500/30">
              <p className="text-slate-400 text-sm">
                <strong className="text-white">What's next?</strong>
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-400 text-sm mt-2 ml-2">
                <li>Watch for our welcome email (check spam if you don't see it)</li>
                <li>Explore our{" "}
                  <Link href="/pricing" className="text-emerald-400 hover:underline">
                    pricing plans
                  </Link>
                </li>
                <li>Read our{" "}
                  <Link href="/docs" className="text-emerald-400 hover:underline">
                    documentation
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        ) : error === 'invalid_token' ? (
          <div className="bg-yellow-950/20 border border-yellow-900/30 rounded-lg p-8 space-y-4">
            <div className="text-6xl mb-4">⚠️</div>
            <h1 className="text-4xl font-bold text-yellow-400">Invalid or Missing Token</h1>
            <p className="text-slate-300">
              This confirmation link is invalid or has already been used.
            </p>
            <p className="text-slate-400">
              If you're trying to subscribe, please{" "}
              <Link href="/marketing/subscribe" className="text-emerald-400 hover:underline">
                start a new subscription
              </Link>.
            </p>
          </div>
        ) : error === 'expired_token' ? (
          <div className="bg-yellow-950/20 border border-yellow-900/30 rounded-lg p-8 space-y-4">
            <div className="text-6xl mb-4">⏰</div>
            <h1 className="text-4xl font-bold text-yellow-400">Confirmation Link Expired</h1>
            <p className="text-slate-300">
              This confirmation link has expired (valid for 7 days).
            </p>
            <p className="text-slate-400">
              Please{" "}
              <Link href="/marketing/subscribe" className="text-emerald-400 hover:underline">
                subscribe again
              </Link>{" "}
              to receive a new confirmation email.
            </p>
          </div>
        ) : error === 'server_error' ? (
          <div className="bg-red-950/20 border border-red-900/30 rounded-lg p-8 space-y-4">
            <div className="text-6xl mb-4">⚠️</div>
            <h1 className="text-4xl font-bold text-red-400">Server Error</h1>
            <p className="text-slate-300">
              We encountered an error processing your confirmation.
            </p>
            <p className="text-slate-400">
              Please try again later, or contact{" "}
              <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                support@levqor.ai
              </a>{" "}
              if the problem persists.
            </p>
          </div>
        ) : (
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-8 space-y-4">
            <h1 className="text-4xl font-bold text-white">Newsletter Subscription</h1>
            <p className="text-slate-300">
              Ready to stay updated with Levqor?
            </p>
            <Link
              href="/marketing/subscribe"
              className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition mt-4"
            >
              Subscribe to Newsletter
            </Link>
          </div>
        )}

        <div className="mt-8 pt-8 border-t border-slate-800">
          <h3 className="text-lg font-bold text-white mb-3">Manage Your Subscription</h3>
          <ul className="space-y-2 text-slate-400 text-sm">
            <li>
              <Link href="/settings/marketing" className="text-emerald-400 hover:underline">
                Update email preferences
              </Link>
            </li>
            <li>
              <Link href="/email-unsubscribe" className="text-emerald-400 hover:underline">
                Learn about unsubscribing
              </Link>
            </li>
            <li>
              <Link href="/privacy" className="text-emerald-400 hover:underline">
                View our Privacy Policy
              </Link>
            </li>
            <li>
              <Link href="/marketing-consent" className="text-emerald-400 hover:underline">
                Marketing Consent Policy
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </main>
  );
}
