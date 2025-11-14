"use client";

import { useSession, signIn } from "next-auth/react";
import Link from "next/link";
import { useState } from "react";

export default function MarketingSettingsPage() {
  const { data: session, status } = useSession();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleUnsubscribe = async () => {
    if (status !== 'authenticated' || !session?.user?.email) {
      signIn(undefined, { callbackUrl: '/settings/marketing' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${backendUrl}/api/marketing/unsubscribe`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: session.user.email,
          scope: 'marketing'
        }),
      });

      const data = await res.json();

      if (data.ok) {
        setMessage({
          type: 'success',
          text: 'You have been unsubscribed from marketing communications. You will still receive transactional emails (receipts, account notifications).',
        });
      } else {
        setMessage({
          type: 'error',
          text: data.message || 'Failed to unsubscribe. Please try again.',
        });
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Network error. Please try again later.',
      });
    } finally {
      setLoading(false);
    }
  };

  if (status === 'loading') {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-slate-400">Loading...</div>
      </main>
    );
  }

  if (status === 'unauthenticated') {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Sign In Required</h1>
          <p className="text-slate-400 mb-6">Please sign in to manage your marketing preferences.</p>
          <button
            onClick={() => signIn(undefined, { callbackUrl: '/settings/marketing' })}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold transition"
          >
            Sign In
          </button>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-2xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/account" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to account
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Marketing Preferences</h1>
        <p className="text-slate-400 mb-8">
          Manage your marketing communication preferences.
        </p>

        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 space-y-6">
          <div>
            <h2 className="text-xl font-bold mb-3">Marketing Emails</h2>
            <p className="text-slate-300 leading-relaxed mb-4">
              We send occasional marketing emails about new features, product updates, and special offers. 
              You can unsubscribe at any time.
            </p>
            <p className="text-sm text-slate-400 mb-4">
              Note: You'll still receive important transactional emails (receipts, account notifications, security alerts) 
              even if you unsubscribe from marketing.
            </p>
          </div>

          {message && (
            <div className={`rounded-lg p-4 ${
              message.type === 'success' 
                ? 'bg-emerald-950/30 border border-emerald-900/50' 
                : 'bg-red-950/30 border border-red-900/50'
            }`}>
              <p className={message.type === 'success' ? 'text-emerald-300' : 'text-red-300'}>
                {message.text}
              </p>
            </div>
          )}

          <div>
            <button
              onClick={handleUnsubscribe}
              disabled={loading}
              className={`w-full py-3 rounded-lg font-semibold transition ${
                loading
                  ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                  : 'bg-slate-700 hover:bg-slate-600 text-white'
              }`}
            >
              {loading ? 'Processing...' : 'Unsubscribe from Marketing Emails'}
            </button>
          </div>

          <div className="pt-4 border-t border-slate-700">
            <h3 className="text-sm font-semibold text-slate-400 mb-2">Email Footer</h3>
            <p className="text-xs text-slate-500">
              You can also unsubscribe using the link at the bottom of any marketing email.
            </p>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm flex-wrap">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
            <Link href="/privacy-tools" className="text-emerald-400 hover:underline">Privacy Tools</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
