"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";

export default function MarketingSubscribePage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const backendApi = process.env.NEXT_PUBLIC_API_URL || 'https://api.levqor.ai';
      const response = await fetch(`${backendApi}/api/marketing/subscribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const data = await response.json();

      if (data.ok) {
        setSuccess(true);
        setEmail("");
      } else {
        setError(data.error || "Subscription failed");
      }
    } catch (err) {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Join Our Newsletter</h1>
        <p className="text-slate-400 mb-8">
          Get product updates, automation tips, and exclusive offers delivered to your inbox.
        </p>

        {success ? (
          <div className="bg-emerald-500/20 border border-emerald-500/50 rounded-lg p-6 space-y-3">
            <h2 className="text-2xl font-bold text-emerald-400">✓ Check Your Email</h2>
            <p className="text-slate-300">
              We've sent a confirmation email to verify your subscription. Please click the link in that email to complete your signup.
            </p>
            <p className="text-slate-400 text-sm">
              Didn't receive it? Check your spam folder, or try subscribing again.
            </p>
            <button
              onClick={() => setSuccess(false)}
              className="text-emerald-400 hover:underline text-sm mt-4"
            >
              Subscribe another email →
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                Email Address *
              </label>
              <input
                type="email"
                id="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                disabled={loading}
                className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500 disabled:opacity-50"
              />
            </div>

            {error && (
              <div className="p-4 bg-red-950/50 border border-red-900/50 rounded-lg">
                <p className="text-red-400 text-sm">{error}</p>
              </div>
            )}

            <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
              <p className="text-slate-400 text-sm">
                <strong className="text-white">What you'll receive:</strong>
              </p>
              <ul className="list-disc list-inside space-y-1 text-slate-400 text-sm mt-2 ml-2">
                <li>Product updates and new feature announcements</li>
                <li>Automation tips and best practices</li>
                <li>Exclusive offers and early access</li>
                <li>Monthly insights and case studies</li>
              </ul>
              <p className="text-slate-500 text-xs mt-3">
                Frequency: 2-4 emails per month. Unsubscribe anytime.
              </p>
            </div>

            <button
              type="submit"
              disabled={loading || !email}
              className={`w-full py-3 rounded-lg font-semibold transition ${
                loading || !email
                  ? 'bg-slate-800 text-slate-500 cursor-not-allowed'
                  : 'bg-emerald-500 hover:bg-emerald-600 text-white'
              }`}
            >
              {loading ? 'Subscribing...' : 'Subscribe to Newsletter'}
            </button>

            <p className="text-slate-500 text-xs text-center">
              By subscribing, you agree to our{" "}
              <Link href="/privacy" className="text-emerald-400 hover:underline">
                Privacy Policy
              </Link>{" "}
              and{" "}
              <Link href="/marketing-consent" className="text-emerald-400 hover:underline">
                Marketing Consent Policy
              </Link>
              . We use double opt-in to confirm your subscription.
            </p>
          </form>
        )}

        <div className="mt-8 pt-8 border-t border-slate-800">
          <h3 className="text-lg font-bold text-white mb-3">Privacy & GDPR Compliance</h3>
          <ul className="space-y-2 text-slate-400 text-sm">
            <li>✓ Double opt-in confirmation required</li>
            <li>✓ Easy one-click unsubscribe in every email</li>
            <li>✓ Your email is never shared with third parties</li>
            <li>✓ Full GDPR compliance with EU data protection laws</li>
          </ul>
          <p className="text-slate-500 text-sm mt-4">
            Questions? Contact us at{" "}
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">
              privacy@levqor.ai
            </a>
          </p>
        </div>
      </div>
    </main>
  );
}
