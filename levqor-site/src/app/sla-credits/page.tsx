'use client';

import { useState } from 'react';
import { useSession, signIn } from 'next-auth/react';
import Link from 'next/link';

export default function SLACreditsPage() {
  const { data: session, status } = useSession();
  const [formData, setFormData] = useState({
    periodStart: '',
    periodEnd: '',
    claimedIssue: ''
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.periodStart || !formData.periodEnd || !formData.claimedIssue) {
      setError('All fields are required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/sla/claim', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await res.json();

      if (data.ok) {
        setSubmitted(true);
      } else {
        setError(data.error || 'Failed to submit request');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (status === 'loading') {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </main>
    );
  }

  if (status === 'unauthenticated') {
    return (
      <main className="min-h-screen bg-slate-950 text-white">
        <div className="max-w-3xl mx-auto px-4 py-12">
          <h1 className="text-4xl font-bold mb-4">SLA Credits Request</h1>
          <div className="bg-slate-800 border-2 border-slate-700 rounded-lg p-8">
            <p className="text-slate-300 mb-6">
              You must be signed in to request SLA credits.
            </p>
            <button
              onClick={() => signIn(undefined, { callbackUrl: '/sla-credits' })}
              className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
            >
              Sign In →
            </button>
          </div>
        </div>
      </main>
    );
  }

  if (submitted) {
    return (
      <main className="min-h-screen bg-slate-950 text-white">
        <div className="max-w-3xl mx-auto px-4 py-12">
          <div className="bg-emerald-950/30 border-2 border-emerald-900/50 rounded-lg p-8 text-center">
            <svg className="w-16 h-16 text-emerald-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h1 className="text-3xl font-bold mb-4 text-emerald-300">Request Submitted</h1>
            <p className="text-slate-300 mb-6">
              Your SLA credit request has been received. Our team will review it and respond within 3 business days.
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/account" className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition">
                Back to Account
              </Link>
              <Link href="/sla" className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition">
                View SLA Terms
              </Link>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link href="/sla" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to SLA
          </Link>
        </div>

        <h1 className="text-4xl font-bold mb-2">Request SLA Credits</h1>
        <p className="text-slate-400 mb-12">
          Submit a request for service-level agreement compensation
        </p>

        <div className="bg-blue-950/20 border-2 border-blue-900/50 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-blue-300 mb-3">📋 When SLA Credits Apply</h2>
          <ul className="space-y-2 text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Business/Pro plans:</strong> Platform uptime below 99.5% in a calendar month</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Enterprise/99.9% SLA:</strong> Uptime below guaranteed threshold</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Credit calculation:</strong> Pro-rata based on downtime impact</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Maximum:</strong> 100% of monthly subscription fee</span>
            </li>
          </ul>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="periodStart" className="block text-sm font-medium text-slate-300 mb-2">
              Affected Period Start
            </label>
            <input
              id="periodStart"
              type="date"
              value={formData.periodStart}
              onChange={(e) => setFormData({ ...formData, periodStart: e.target.value })}
              className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none"
              required
            />
          </div>

          <div>
            <label htmlFor="periodEnd" className="block text-sm font-medium text-slate-300 mb-2">
              Affected Period End
            </label>
            <input
              id="periodEnd"
              type="date"
              value={formData.periodEnd}
              onChange={(e) => setFormData({ ...formData, periodEnd: e.target.value })}
              className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none"
              required
            />
          </div>

          <div>
            <label htmlFor="claimedIssue" className="block text-sm font-medium text-slate-300 mb-2">
              Describe the Issue
            </label>
            <textarea
              id="claimedIssue"
              value={formData.claimedIssue}
              onChange={(e) => setFormData({ ...formData, claimedIssue: e.target.value })}
              rows={6}
              placeholder="Please describe the outage or service degradation you experienced, including specific workflows affected and business impact..."
              className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none resize-none"
              required
            />
            <p className="text-xs text-slate-400 mt-2">
              Include specific timestamps, error messages, and affected workflow IDs if available
            </p>
          </div>

          {error && (
            <div className="bg-red-950/30 border border-red-900/50 rounded-lg p-4">
              <p className="text-red-300">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 rounded-lg font-semibold transition ${
              loading
                ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                : 'bg-emerald-500 hover:bg-emerald-600 text-white cursor-pointer'
            }`}
          >
            {loading ? 'Submitting...' : 'Submit SLA Credit Request'}
          </button>

          <p className="text-xs text-slate-400 text-center">
            Requests are typically reviewed within 3 business days. Credits are applied to your next invoice.
          </p>
        </form>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/sla" className="text-emerald-400 hover:underline">SLA Terms</Link>
            <Link href="/status" className="text-emerald-400 hover:underline">System Status</Link>
            <a href="mailto:sla@levqor.ai" className="text-emerald-400 hover:underline">Contact SLA Team</a>
          </div>
        </div>
      </div>
    </main>
  );
}
