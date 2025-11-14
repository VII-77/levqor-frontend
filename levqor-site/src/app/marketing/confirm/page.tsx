'use client';

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

export default function MarketingConfirmPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setMessage('Invalid confirmation link. No token provided.');
      return;
    }

    confirmSubscription();
  }, [token]);

  const confirmSubscription = async () => {
    try {
      const response = await fetch('/api/marketing/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token }),
      });

      const data = await response.json();

      if (!response.ok || !data.ok) {
        throw new Error(data.error || 'Failed to confirm subscription');
      }

      setStatus('success');
      setEmail(data.email || '');
      setMessage('Your subscription is confirmed!');
    } catch (err) {
      setStatus('error');
      setMessage(err instanceof Error ? err.message : 'Failed to confirm subscription');
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl text-center">
          {status === 'loading' && (
            <>
              <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-emerald-500 mx-auto mb-6"></div>
              <h1 className="text-2xl font-bold text-white mb-2">Confirming your subscription...</h1>
              <p className="text-slate-400">Please wait while we process your request.</p>
            </>
          )}

          {status === 'success' && (
            <>
              <div className="mb-6">
                <div className="w-16 h-16 bg-emerald-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <h1 className="text-3xl font-bold text-white mb-4">{message}</h1>
                {email && (
                  <p className="text-slate-300 mb-6">
                    <strong>{email}</strong> has been added to our mailing list.
                  </p>
                )}
                <p className="text-slate-400 mb-8">
                  You'll now receive product updates, automation tips, and exclusive offers from Levqor.
                </p>
              </div>

              <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-6 mb-6">
                <h2 className="text-lg font-semibold text-white mb-3">What's next?</h2>
                <ul className="space-y-2 text-slate-300 text-sm text-left">
                  <li className="flex items-start">
                    <span className="text-emerald-400 mr-2">✓</span>
                    <span>You'll receive our latest product updates and feature releases</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-emerald-400 mr-2">✓</span>
                    <span>Get early access to new automation templates and integrations</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-emerald-400 mr-2">✓</span>
                    <span>Exclusive tips and best practices for workflow automation</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-emerald-400 mr-2">✓</span>
                    <span>Special offers and promotions (unsubscribe anytime)</span>
                  </li>
                </ul>
              </div>

              <Link
                href="/signin"
                className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
              >
                Sign in to your account →
              </Link>
            </>
          )}

          {status === 'error' && (
            <>
              <div className="mb-6">
                <div className="w-16 h-16 bg-red-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </div>
                <h1 className="text-3xl font-bold text-white mb-4">Confirmation failed</h1>
                <p className="text-slate-300 mb-6">{message}</p>
              </div>

              <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-6 mb-6">
                <h2 className="text-lg font-semibold text-white mb-3">Possible reasons:</h2>
                <ul className="space-y-2 text-slate-400 text-sm text-left">
                  <li>• The confirmation link has expired (links are valid for 7 days)</li>
                  <li>• The link has already been used</li>
                  <li>• The link is invalid or corrupted</li>
                </ul>
              </div>

              <Link
                href="/signin"
                className="inline-block px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition"
              >
                Back to sign in →
              </Link>
            </>
          )}

          <p className="mt-8 text-xs text-slate-500">
            Need help? Contact us at{' '}
            <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
              support@levqor.ai
            </a>
          </p>
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
