'use client';

import { useState } from 'react';
import { useSession, signIn } from 'next-auth/react';
import Link from 'next/link';

export default function EmergencyPage() {
  const { data: session, status } = useSession();
  const [formData, setFormData] = useState({
    summary: '',
    impact: ''
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.summary || !formData.impact) {
      setError('All fields are required');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/emergency/report', {
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
        setError(data.error || 'Failed to submit report');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="max-w-2xl mx-auto px-4">
          <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-8 text-center">
            <svg className="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h1 className="text-3xl font-bold mb-4 text-red-300">Emergency Report Received</h1>
            <p className="text-slate-300 mb-6">
              Your severity-1 incident report has been escalated to our on-call engineering team. 
              You should receive an acknowledgment within <strong>15 minutes</strong>.
            </p>
            <p className="text-sm text-slate-400 mb-6">
              For immediate assistance, you can also contact: <br/>
              <a href="mailto:emergency@levqor.ai" className="text-red-400 hover:underline font-semibold">emergency@levqor.ai</a>
            </p>
            <Link href="/status" className="inline-block px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-semibold transition">
              View System Status
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link href="/incident-response" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to Incident Response
          </Link>
        </div>

        <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-8 mb-8">
          <div className="flex items-start gap-4">
            <svg className="w-12 h-12 text-red-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-3 text-red-300">Emergency Contact & Severity-1 Incidents</h1>
              <p className="text-slate-300 text-lg">
                For critical, time-sensitive issues affecting production systems
              </p>
            </div>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mb-12">
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-red-400 mb-3">🔥 Severity 1</h3>
            <ul className="text-sm text-slate-300 space-y-2">
              <li>• Complete service outage</li>
              <li>• Data breach or security incident</li>
              <li>• Payment processing failure</li>
              <li>• Critical data loss</li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-amber-400 mb-3">⚠️ Response Time</h3>
            <div className="text-sm text-slate-300 space-y-2">
              <p><strong>Acknowledgment:</strong> 15 minutes</p>
              <p><strong>Investigation Start:</strong> 30 minutes</p>
              <p><strong>Status Updates:</strong> Every 1 hour</p>
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
            <h3 className="text-xl font-bold text-emerald-400 mb-3">📧 Contact Methods</h3>
            <div className="text-sm text-slate-300 space-y-2">
              <p><strong>Email:</strong> emergency@levqor.ai</p>
              <p><strong>Report Form:</strong> Below</p>
              <p className="text-xs text-slate-400">24/7 on-call rotation</p>
            </div>
          </div>
        </div>

        <div className="bg-amber-950/20 border-2 border-amber-900/50 rounded-lg p-6 mb-8">
          <h2 className="text-lg font-bold text-amber-300 mb-3">⚠️ When NOT to Use Emergency Contact</h2>
          <p className="text-slate-300 text-sm mb-3">
            For non-critical issues, please use standard support channels to ensure appropriate prioritization:
          </p>
          <ul className="text-sm text-slate-300 space-y-2">
            <li>• <strong>Feature requests:</strong> Submit via product feedback</li>
            <li>• <strong>Billing questions:</strong> Contact billing@levqor.ai</li>
            <li>• <strong>Minor bugs:</strong> Use standard support ticket</li>
            <li>• <strong>Account changes:</strong> Use account settings or support@levqor.ai</li>
          </ul>
        </div>

        {status === 'authenticated' && !submitted && (
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Report Severity-1 Incident</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="summary" className="block text-sm font-medium text-slate-300 mb-2">
                  Incident Summary *
                </label>
                <input
                  id="summary"
                  type="text"
                  value={formData.summary}
                  onChange={(e) => setFormData({ ...formData, summary: e.target.value })}
                  placeholder="Brief description of the critical issue"
                  className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-red-500 focus:outline-none"
                  required
                />
              </div>

              <div>
                <label htmlFor="impact" className="block text-sm font-medium text-slate-300 mb-2">
                  Business Impact *
                </label>
                <textarea
                  id="impact"
                  value={formData.impact}
                  onChange={(e) => setFormData({ ...formData, impact: e.target.value })}
                  rows={6}
                  placeholder="Describe the impact on your business operations, affected workflows, error messages, and when the issue started..."
                  className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-red-500 focus:outline-none resize-none"
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
                    : 'bg-red-600 hover:bg-red-700 text-white cursor-pointer'
                }`}
              >
                {loading ? 'Submitting Emergency Report...' : '🚨 Submit Emergency Report'}
              </button>

              <p className="text-xs text-slate-400 text-center">
                This will immediately alert our on-call engineering team (24/7)
              </p>
            </form>
          </div>
        )}

        {status === 'unauthenticated' && (
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8 text-center">
            <p className="text-slate-300 mb-6">
              Sign in to submit an emergency report via the form, or email <a href="mailto:emergency@levqor.ai" className="text-red-400 hover:underline font-semibold">emergency@levqor.ai</a> directly.
            </p>
            <button
              onClick={() => signIn(undefined, { callbackUrl: '/emergency' })}
              className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
            >
              Sign In →
            </button>
          </div>
        )}

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/status" className="text-emerald-400 hover:underline">System Status</Link>
            <Link href="/incident-response" className="text-emerald-400 hover:underline">Incident Response Policy</Link>
            <a href="mailto:emergency@levqor.ai" className="text-red-400 hover:underline font-semibold">emergency@levqor.ai</a>
          </div>
        </div>
      </div>
    </main>
  );
}
