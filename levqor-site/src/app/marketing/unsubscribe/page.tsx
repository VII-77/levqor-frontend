'use client';

import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

export default function MarketingUnsubscribePage() {
  const searchParams = useSearchParams();
  const emailParam = searchParams.get('email');

  const [email, setEmail] = useState(emailParam || '');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleUnsubscribe = async () => {
    if (!email) {
      setStatus('error');
      setMessage('Please provide your email address');
      return;
    }

    setStatus('loading');
    setMessage('');

    try {
      const response = await fetch('/api/marketing/unsubscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok || !data.ok) {
        throw new Error(data.error || 'Failed to unsubscribe');
      }

      setStatus('success');
      setMessage('You have been successfully unsubscribed.');
    } catch (err) {
      setStatus('error');
      setMessage(err instanceof Error ? err.message : 'Failed to unsubscribe');
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl">
          {status === 'success' ? (
            <div className="text-center">
              <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h1 className="text-3xl font-bold text-white mb-4">You've been unsubscribed</h1>
              <p className="text-slate-300 mb-6">
                Your email preferences have been updated. You will no longer receive marketing emails from Levqor.
              </p>

              <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-6 mb-6">
                <p className="text-slate-400 text-sm">
                  <strong className="text-white">Changed your mind?</strong><br/>
                  You can resubscribe anytime by signing into your account and updating your email preferences.
                </p>
              </div>

              <Link
                href="/"
                className="inline-block px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition"
              >
                Back to home →
              </Link>
            </div>
          ) : (
            <>
              <h1 className="text-3xl font-bold text-white mb-4">Unsubscribe from marketing emails</h1>
              <p className="text-slate-300 mb-6">
                We're sorry to see you go. Enter your email address below to unsubscribe from Levqor marketing communications.
              </p>

              <div className="mb-6">
                <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                  Email address
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your@email.com"
                  className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none"
                  disabled={status === 'loading'}
                />
              </div>

              {status === 'error' && (
                <div className="mb-6 p-4 bg-red-950/50 border border-red-900/50 rounded-lg">
                  <p className="text-red-400 text-sm">{message}</p>
                </div>
              )}

              <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-4 mb-6">
                <p className="text-slate-400 text-sm">
                  <strong className="text-white">Note:</strong> This will only unsubscribe you from marketing emails. 
                  You'll still receive important account-related notifications and transactional emails.
                </p>
              </div>

              <button
                onClick={handleUnsubscribe}
                disabled={!email || status === 'loading'}
                className={`w-full py-3 rounded-lg font-semibold transition ${
                  email && status !== 'loading'
                    ? 'bg-red-600 hover:bg-red-700 text-white cursor-pointer'
                    : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                }`}
              >
                {status === 'loading' ? 'Processing...' : 'Unsubscribe'}
              </button>

              <p className="mt-6 text-xs text-slate-500 text-center">
                Questions? Contact us at{' '}
                <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                  support@levqor.ai
                </a>
              </p>
            </>
          )}
        </div>

        <div className="mt-6 text-center">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>
      </div>
    </main>
  );
}
