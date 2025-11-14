"use client";

import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useState, useEffect, Suspense } from "react";

function UnsubscribeContent() {
  const searchParams = useSearchParams();
  const email = searchParams.get('email');
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    if (!email) {
      setStatus('error');
      setMessage('No email provided in unsubscribe link.');
      return;
    }

    const unsubscribe = async () => {
      try {
        const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${backendUrl}/api/marketing/unsubscribe`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            scope: 'marketing'
          }),
        });

        const data = await res.json();

        if (data.ok) {
          setStatus('success');
          setMessage('You have been successfully unsubscribed from marketing emails.');
        } else {
          setStatus('error');
          setMessage(data.message || 'Failed to unsubscribe. Please try again or contact support.');
        }
      } catch (error) {
        setStatus('error');
        setMessage('Network error. Please try again later.');
      }
    };

    unsubscribe();
  }, [email]);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-6">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-8">Unsubscribe</h1>

          {status === 'loading' && (
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-12">
              <div className="flex items-center justify-center gap-3">
                <svg className="animate-spin h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="text-slate-300">Processing your request...</span>
              </div>
            </div>
          )}

          {status === 'success' && (
            <div className="bg-emerald-950/30 border-2 border-emerald-900/50 rounded-lg p-8 space-y-4">
              <div className="flex justify-center mb-4">
                <svg className="w-16 h-16 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-emerald-300 mb-4">Unsubscribed Successfully</h2>
              <p className="text-slate-300 leading-relaxed">
                {message}
              </p>
              <p className="text-slate-400 text-sm mt-4">
                You will still receive important transactional emails such as receipts, account notifications, and security alerts.
              </p>
              <div className="mt-6">
                <Link
                  href="/"
                  className="inline-block px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold transition"
                >
                  Return to Home
                </Link>
              </div>
            </div>
          )}

          {status === 'error' && (
            <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-8 space-y-4">
              <div className="flex justify-center mb-4">
                <svg className="w-16 h-16 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-red-300 mb-4">Unsubscribe Failed</h2>
              <p className="text-slate-300 leading-relaxed">
                {message}
              </p>
              <p className="text-slate-400 text-sm mt-4">
                If you continue to experience issues, please contact us at{' '}
                <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
                  support@levqor.ai
                </a>
              </p>
              <div className="mt-6 flex gap-3 justify-center">
                <Link
                  href="/"
                  className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition"
                >
                  Return to Home
                </Link>
                <Link
                  href="/settings/marketing"
                  className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold transition"
                >
                  Manage Preferences
                </Link>
              </div>
            </div>
          )}
        </div>

        <div className="mt-12 pt-8 border-t border-slate-800 text-center">
          <div className="flex gap-4 text-sm justify-center flex-wrap">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/contact" className="text-emerald-400 hover:underline">Contact Support</Link>
            <Link href="/settings/marketing" className="text-emerald-400 hover:underline">Marketing Preferences</Link>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function UnsubscribePage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400">Loading...</div>
      </main>
    }>
      <UnsubscribeContent />
    </Suspense>
  );
}
