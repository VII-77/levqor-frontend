'use client';

import { useState } from 'react';
import { useSession, signIn, signOut } from 'next-auth/react';
import Link from 'next/link';

export default function DeleteAccountPage() {
  const { data: session, status } = useSession();
  const [confirmed, setConfirmed] = useState(false);
  const [typedConfirm, setTypedConfirm] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleDelete = async () => {
    if (typedConfirm !== 'DELETE MY ACCOUNT') {
      setError('Please type the confirmation phrase exactly as shown');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/account/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      const data = await res.json();

      if (data.ok) {
        await signOut({ callbackUrl: '/?deleted=true' });
      } else {
        setError(data.error || 'Failed to delete account');
        setLoading(false);
      }
    } catch (err) {
      setError('Network error. Please try again.');
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
          <h1 className="text-4xl font-bold mb-4">Delete Account</h1>
          <div className="bg-slate-800 border-2 border-slate-700 rounded-lg p-8">
            <p className="text-slate-300 mb-6">
              You must be signed in to delete your account.
            </p>
            <button
              onClick={() => signIn(undefined, { callbackUrl: '/delete-account' })}
              className="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
            >
              Sign In →
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link href="/account" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to Account
          </Link>
        </div>

        <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-8 mb-8">
          <div className="flex items-start gap-4">
            <svg className="w-12 h-12 text-red-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <div className="flex-1">
              <h1 className="text-4xl font-bold mb-3 text-red-300">Delete Account & All Data</h1>
              <p className="text-slate-300 text-lg">
                This action is permanent and cannot be undone
              </p>
            </div>
          </div>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-white mb-4">⚠️ What will be deleted:</h2>
          <ul className="space-y-2 text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>Your user account and profile</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>All workflows and automation history</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>All logs and execution records</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>Developer API keys and integrations</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>Billing history and payment methods</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>Partnership registrations and marketplace data</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-1">×</span>
              <span>All DSAR exports and compliance records</span>
            </li>
          </ul>
        </div>

        <div className="bg-blue-950/20 border-2 border-blue-900/50 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-blue-300 mb-4">💡 Before you delete:</h2>
          <ul className="space-y-3 text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Download your data:</strong> Request a data export from <Link href="/privacy-tools" className="text-blue-400 hover:underline">Privacy Tools</Link> before deletion</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Cancel subscriptions:</strong> Visit <Link href="/account/billing" className="text-blue-400 hover:underline">Billing</Link> to cancel active subscriptions</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>Alternative:</strong> Consider pausing your subscription instead of deleting</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-blue-400 mt-1">•</span>
              <span><strong>30-day retention:</strong> We keep minimal audit logs for compliance (anonymized)</span>
            </li>
          </ul>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Confirm Account Deletion</h2>
          
          <div className="space-y-6">
            <div className="bg-slate-950/50 border border-slate-700 rounded-lg p-4">
              <label className="flex items-start cursor-pointer">
                <input
                  type="checkbox"
                  checked={confirmed}
                  onChange={(e) => setConfirmed(e.target.checked)}
                  className="mt-1 mr-3 h-5 w-5 rounded border-slate-600 text-red-500 focus:ring-red-500 focus:ring-offset-slate-900"
                />
                <span className="text-slate-300 text-sm">
                  I understand that this action is <strong className="text-red-400">permanent and irreversible</strong>. 
                  All my data will be deleted and I will lose access to my account immediately.
                </span>
              </label>
            </div>

            <div>
              <label htmlFor="confirmText" className="block text-sm font-medium text-slate-300 mb-2">
                Type <code className="bg-slate-800 px-2 py-1 rounded text-red-400">DELETE MY ACCOUNT</code> to confirm
              </label>
              <input
                id="confirmText"
                type="text"
                value={typedConfirm}
                onChange={(e) => setTypedConfirm(e.target.value)}
                placeholder="DELETE MY ACCOUNT"
                disabled={!confirmed || loading}
                className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-red-500 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>

            {error && (
              <div className="bg-red-950/30 border border-red-900/50 rounded-lg p-4">
                <p className="text-red-300">{error}</p>
              </div>
            )}

            <div className="flex gap-4">
              <Link
                href="/account"
                className="flex-1 text-center px-6 py-4 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition"
              >
                Cancel
              </Link>
              <button
                onClick={handleDelete}
                disabled={!confirmed || typedConfirm !== 'DELETE MY ACCOUNT' || loading}
                className={`flex-1 py-4 rounded-lg font-semibold transition ${
                  confirmed && typedConfirm === 'DELETE MY ACCOUNT' && !loading
                    ? 'bg-red-600 hover:bg-red-700 text-white cursor-pointer'
                    : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                }`}
              >
                {loading ? 'Deleting Account...' : 'Delete My Account Permanently'}
              </button>
            </div>

            <p className="text-xs text-slate-400 text-center">
              This action complies with GDPR Article 17 (Right to Erasure)
            </p>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/privacy-tools" className="text-emerald-400 hover:underline">Download My Data First</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/data-requests" className="text-emerald-400 hover:underline">Data Rights</Link>
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">Contact Privacy Team</a>
          </div>
        </div>
      </div>
    </main>
  );
}
