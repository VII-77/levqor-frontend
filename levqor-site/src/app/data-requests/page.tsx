"use client";
import Link from "next/link";
import { useState, useEffect } from "react";
import { useSession } from "next-auth/react";

export default function DataRequestsPage() {
  const { data: session } = useSession();
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    if (session?.user?.email) {
      setEmail(session.user.email);
    }
  }, [session]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!email) {
      setMessage({ type: "error", text: "Please enter your email address" });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const backendApi = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";
      const response = await fetch(`${backendApi}/api/dsar/request`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (data.ok || response.status === 202) {
        setMessage({
          type: "success",
          text: data.message || "Request received. If an account exists, you'll receive your data export via email shortly.",
        });
        if (data.reference) {
          setMessage({
            type: "success",
            text: `${data.message} Reference: ${data.reference}`,
          });
        }
      } else {
        setMessage({
          type: "error",
          text: data.message || data.error || "Request failed. Please try again.",
        });
      }
    } catch (error) {
      setMessage({
        type: "error",
        text: "Network error. Please try again later.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Data Subject Requests</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Your Rights</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Right to access</li>
            <li>Right to rectification</li>
            <li>Right to erasure</li>
            <li>Right to restrict processing</li>
            <li>Right to data portability</li>
            <li>Right to object</li>
            <li>Right to withdraw consent</li>
          </ul>
        </section>

        <section className="bg-emerald-950/30 border-2 border-emerald-900/50 rounded-lg p-6 mt-8">
          <h2 className="text-2xl font-bold text-white mb-4">🔐 Request Your Data Export</h2>
          <p className="text-slate-300 leading-relaxed mb-6">
            Request a complete copy of your personal data sent directly to your email.
            This exercises your right of access under GDPR Article 15.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                Email Address
              </label>
              {session?.user?.email ? (
                <div className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-slate-300">
                  {session.user.email}
                </div>
              ) : (
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  required
                  className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white placeholder-slate-500 focus:border-emerald-500 focus:outline-none transition"
                />
              )}
            </div>

            <button
              type="submit"
              disabled={loading}
              className={`w-full py-3 px-6 rounded-lg font-semibold transition ${
                loading
                  ? "bg-slate-700 text-slate-400 cursor-not-allowed"
                  : "bg-emerald-500 hover:bg-emerald-400 text-slate-900"
              }`}
            >
              {loading ? "Processing..." : "Request My Data Export"}
            </button>
          </form>

          {message && (
            <div
              className={`mt-4 p-4 rounded-lg ${
                message.type === "success"
                  ? "bg-emerald-500/10 border border-emerald-500/30 text-emerald-400"
                  : "bg-red-500/10 border border-red-500/30 text-red-400"
              }`}
            >
              <p className="text-sm">{message.text}</p>
            </div>
          )}

          <div className="mt-6 bg-slate-800/50 border border-slate-700 rounded-lg p-4">
            <h3 className="text-sm font-semibold text-emerald-400 mb-2">What's included in your export:</h3>
            <ul className="space-y-1 text-sm text-slate-300 ml-4">
              <li>• User profile and account information</li>
              <li>• Workflows and automation history</li>
              <li>• API keys (prefixes only, for security)</li>
              <li>• Partnerships and referrals</li>
              <li>• Audit logs and activity records</li>
            </ul>
          </div>

          <p className="text-xs text-slate-400 mt-4">
            Your export will be sent as a ZIP attachment to your email if it matches our records.
            We typically process requests within minutes, but may take up to 30 days as required by law.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Other Data Subject Requests</h2>
          <p className="text-slate-300 leading-relaxed">
            For other rights (rectification, erasure, restriction, portability, objection), please contact:
          </p>
          <p className="text-slate-300 leading-relaxed">
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline font-semibold">privacy@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Identity verification required for all requests. Response within 30 days (extendable to 60 days in complex cases).
          </p>
        </section>

        <section className="bg-red-950/20 border-2 border-red-900/50 rounded-lg p-6 mt-8">
          <h2 className="text-2xl font-bold text-white mb-4">🗑️ Automated Data Deletion</h2>
          <p className="text-slate-300 leading-relaxed mb-4">
            You can now delete your personal data instantly using the "Delete My Data (GDPR)" button in Privacy Tools. 
            This exercises your right to erasure under GDPR Article 17.
          </p>
          <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 mb-4">
            <h3 className="text-sm font-semibold text-amber-400 mb-2">What gets deleted:</h3>
            <ul className="space-y-1 text-sm text-slate-300 ml-4">
              <li>• Workflows, jobs, and automation logs</li>
              <li>• API keys and developer tools</li>
              <li>• Referral and partnership data</li>
              <li>• Account information (anonymized)</li>
            </ul>
          </div>
          <div className="bg-blue-950/30 border border-blue-900/50 rounded-lg p-4 mb-4">
            <h3 className="text-sm font-semibold text-blue-300 mb-2">What's preserved (legal requirement):</h3>
            <ul className="space-y-1 text-sm text-slate-300 ml-4">
              <li>• Billing records and invoices (7 years)</li>
              <li>• Stripe payment history (financial audit requirements)</li>
            </ul>
          </div>
          <Link 
            href="/privacy-tools"
            className="inline-flex items-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Go to Privacy Tools
          </Link>
          <p className="text-xs text-slate-400 mt-3">
            Automated cleanup also runs daily, deleting expired records based on our retention policy.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/privacy-tools" className="text-emerald-400 hover:underline font-semibold">Privacy Tools</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/gdpr" className="text-emerald-400 hover:underline">GDPR Compliance</Link>
            <Link href="/dpa" className="text-emerald-400 hover:underline">Data Processing Agreement</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
