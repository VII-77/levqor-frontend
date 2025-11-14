'use client';

import { useState } from 'react';
import { useSession, signIn } from 'next-auth/react';
import Link from 'next/link';

export default function DisputesPage() {
  const { data: session, status } = useSession();
  const [formData, setFormData] = useState({
    subject: '',
    description: '',
    category: 'billing'
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.subject || !formData.description) {
      setError('Subject and description are required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/disputes', {
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
        setError(data.error || 'Failed to submit dispute');
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
          <h1 className="text-4xl font-bold mb-4">Dispute Resolution</h1>
          <div className="bg-slate-800 border-2 border-slate-700 rounded-lg p-8">
            <p className="text-slate-300 mb-6">
              You must be signed in to raise a concern or dispute.
            </p>
            <button
              onClick={() => signIn(undefined, { callbackUrl: '/disputes' })}
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
            <h1 className="text-3xl font-bold mb-4 text-emerald-300">Dispute Received</h1>
            <p className="text-slate-300 mb-2">
              Your concern has been recorded and assigned a tracking number.
            </p>
            <p className="text-slate-300 mb-6">
              We will acknowledge your dispute within <strong>3 business days</strong> and aim to resolve it within <strong>14 days</strong>.
            </p>
            <div className="flex gap-4 justify-center">
              <Link href="/account" className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition">
                Back to Account
              </Link>
              <a href="mailto:disputes@levqor.ai" className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition">
                Email Disputes Team
              </a>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold mb-2">Dispute Resolution & Complaints</h1>
        <p className="text-slate-400 mb-12">
          Fair, transparent process for resolving concerns
        </p>

        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-blue-950/20 border-2 border-blue-900/50 rounded-lg p-6">
            <h2 className="text-xl font-bold text-blue-300 mb-3">🤝 Informal Resolution</h2>
            <p className="text-slate-300 text-sm mb-3">
              Most issues can be resolved quickly through direct communication with our support team.
            </p>
            <p className="text-slate-400 text-xs">
              Response time: Same business day
            </p>
          </div>

          <div className="bg-amber-950/20 border-2 border-amber-900/50 rounded-lg p-6">
            <h2 className="text-xl font-bold text-amber-300 mb-3">📋 Formal Complaint</h2>
            <p className="text-slate-300 text-sm mb-3">
              If informal resolution fails, submit a formal dispute using the form below.
            </p>
            <p className="text-slate-400 text-xs">
              Acknowledged within: 3 business days<br/>
              Resolution target: 14 days
            </p>
          </div>

          <div className="bg-purple-950/20 border-2 border-purple-900/50 rounded-lg p-6">
            <h2 className="text-xl font-bold text-purple-300 mb-3">⚡ Escalation</h2>
            <p className="text-slate-300 text-sm mb-3">
              If unresolved after 14 days, your dispute can be escalated to senior management.
            </p>
            <p className="text-slate-400 text-xs">
              Email: escalations@levqor.ai
            </p>
          </div>

          <div className="bg-slate-800 border-2 border-slate-700 rounded-lg p-6">
            <h2 className="text-xl font-bold text-slate-300 mb-3">🏛️ External Mediation</h2>
            <p className="text-slate-300 text-sm mb-3">
              As a final step, disputes may be referred to an independent mediation service.
            </p>
            <p className="text-slate-400 text-xs">
              We'll provide mediation options if needed
            </p>
          </div>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Submit a Formal Complaint</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-slate-300 mb-2">
                Category
              </label>
              <select
                id="category"
                value={formData.category}
                onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none"
              >
                <option value="billing">Billing Dispute</option>
                <option value="service">Service Quality</option>
                <option value="refund">Refund Request</option>
                <option value="data">Data or Privacy Concern</option>
                <option value="contract">Contract Dispute</option>
                <option value="other">Other</option>
              </select>
            </div>

            <div>
              <label htmlFor="subject" className="block text-sm font-medium text-slate-300 mb-2">
                Subject
              </label>
              <input
                id="subject"
                type="text"
                value={formData.subject}
                onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                placeholder="Brief summary of your dispute"
                className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none"
                required
              />
            </div>

            <div>
              <label htmlFor="description" className="block text-sm font-medium text-slate-300 mb-2">
                Description
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={8}
                placeholder="Please provide full details including dates, amounts, previous communications, and desired resolution..."
                className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none resize-none"
                required
              />
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
              {loading ? 'Submitting...' : 'Submit Formal Complaint'}
            </button>

            <p className="text-xs text-slate-400 text-center">
              By submitting, you agree to participate in good-faith resolution discussions
            </p>
          </form>
        </div>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/refunds" className="text-emerald-400 hover:underline">Refund Policy</Link>
            <Link href="/cancellation" className="text-emerald-400 hover:underline">Cancellation Policy</Link>
            <Link href="/billing" className="text-emerald-400 hover:underline">Billing Information</Link>
            <a href="mailto:disputes@levqor.ai" className="text-emerald-400 hover:underline">disputes@levqor.ai</a>
          </div>
        </div>
      </div>
    </main>
  );
}
