'use client';

import { useEffect, useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { CURRENT_TERMS_VERSION } from '@/config/legal';

export default function AcceptTermsPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const searchParams = useSearchParams();
  const returnTo = searchParams.get('returnTo') || '/workflow';

  const [agreed, setAgreed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [checkingStatus, setCheckingStatus] = useState(true);

  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push(`/signin?returnTo=${encodeURIComponent('/legal/accept-terms?returnTo=' + returnTo)}`);
      return;
    }

    if (status === 'authenticated' && session?.user?.email) {
      checkTermsStatus();
    }
  }, [status, session, router, returnTo]);

  const checkTermsStatus = async () => {
    try {
      const backendApi = process.env.NEXT_PUBLIC_API_URL || 'https://api.levqor.ai';
      
      const userResponse = await fetch(`${backendApi}/api/v1/users/upsert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: session?.user?.email,
          name: session?.user?.name || '',
        }),
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();
        
        if (userData.terms_accepted_at && userData.terms_version === CURRENT_TERMS_VERSION) {
          router.push(returnTo);
          return;
        }
      }
    } catch (err) {
      console.error('[TOS] Error checking terms status:', err);
    } finally {
      setCheckingStatus(false);
    }
  };

  const handleAccept = async () => {
    if (!agreed) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/legal/accept-terms', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ version: CURRENT_TERMS_VERSION }),
      });

      const data = await response.json();

      if (!response.ok || !data.ok) {
        throw new Error(data.error || 'Failed to accept terms');
      }

      router.push(returnTo);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setLoading(false);
    }
  };

  if (status === 'loading' || checkingStatus) {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-slate-400">Loading...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl">
          <h1 className="text-3xl font-bold text-white mb-4">Accept the Levqor Terms of Service</h1>
          
          <p className="text-slate-300 mb-6">
            Before you can use Levqor, you must read and agree to our Terms of Service and Privacy Policy.
          </p>

          <div className="bg-slate-950/50 border border-slate-800 rounded-lg p-6 mb-6">
            <h2 className="text-lg font-semibold text-white mb-3">Key Points:</h2>
            <ul className="space-y-2 text-slate-300 text-sm">
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">•</span>
                <span>You must be 18+ and authorized to use this service on behalf of your organization</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">•</span>
                <span>Your data is stored securely in EU-based data centers with AES-256 encryption</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">•</span>
                <span>You retain ownership of your data and can request deletion at any time</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">•</span>
                <span>We comply with UK GDPR and provide full data subject rights</span>
              </li>
              <li className="flex items-start">
                <span className="text-emerald-400 mr-2">•</span>
                <span>Prohibited: Illegal activities, scraping, abuse, or automated spam</span>
              </li>
            </ul>
          </div>

          <div className="flex gap-4 mb-6">
            <Link 
              href="/terms" 
              target="_blank"
              className="flex-1 text-center px-4 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-medium transition border border-slate-700"
            >
              Read full Terms of Service →
            </Link>
            <Link 
              href="/privacy" 
              target="_blank"
              className="flex-1 text-center px-4 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-medium transition border border-slate-700"
            >
              Privacy Policy →
            </Link>
          </div>

          <div className="bg-blue-950/20 border border-blue-900/30 rounded-lg p-4 mb-6">
            <label className="flex items-start cursor-pointer">
              <input
                type="checkbox"
                checked={agreed}
                onChange={(e) => setAgreed(e.target.checked)}
                className="mt-1 mr-3 h-5 w-5 rounded border-slate-600 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-slate-900"
                aria-label="I agree to the Terms of Service and Privacy Policy"
              />
              <span className="text-slate-300 text-sm">
                I have read and agree to the Levqor{' '}
                <Link href="/terms" target="_blank" className="text-blue-400 hover:underline font-medium">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link href="/privacy" target="_blank" className="text-blue-400 hover:underline font-medium">
                  Privacy Policy
                </Link>.
              </span>
            </label>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-950/50 border border-red-900/50 rounded-lg">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          <button
            onClick={handleAccept}
            disabled={!agreed || loading}
            className={`w-full py-4 rounded-lg font-semibold text-lg transition ${
              agreed && !loading
                ? 'bg-emerald-500 hover:bg-emerald-600 text-white cursor-pointer'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            }`}
            aria-label="Accept terms and continue"
          >
            {loading ? 'Processing...' : 'Accept and Continue'}
          </button>

          <p className="mt-6 text-xs text-slate-500 text-center">
            Version: {CURRENT_TERMS_VERSION} | Your acceptance is recorded with timestamp and IP address (anonymized)
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
