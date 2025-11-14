'use client';

import { useState } from 'react';
import { useSession, signIn } from 'next-auth/react';
import Link from 'next/link';

export default function PrivacyToolsPage() {
  const { data: session, status } = useSession();
  const [loading, setLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [deleteMessage, setDeleteMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const handleRequestExport = async () => {
    if (status !== 'authenticated' || !session?.user?.email) {
      signIn(undefined, { callbackUrl: '/privacy-tools' });
      return;
    }

    setLoading(true);
    setMessage(null);

    try {
      const res = await fetch('/api/data-export/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-User-Email': session.user.email,
        },
      });

      const data = await res.json();

      if (data.ok) {
        setMessage({
          type: 'success',
          text: data.message || 'If an export is available, you will receive an email shortly with download instructions.',
        });
      } else {
        if (data.error === 'RATE_LIMITED') {
          setMessage({
            type: 'error',
            text: 'You already requested an export in the last 24 hours. Please wait before requesting again.',
          });
        } else {
          setMessage({
            type: 'error',
            text: data.message || 'Failed to request export. Please try again later.',
          });
        }
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'Network error. Please check your connection and try again.',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteMyData = async () => {
    if (status !== 'authenticated' || !session?.user?.email) {
      signIn(undefined, { callbackUrl: '/privacy-tools' });
      return;
    }

    setDeleteLoading(true);
    setDeleteMessage(null);

    try {
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${backendUrl}/api/privacy/delete-my-data?email=${encodeURIComponent(session.user.email)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await res.json();

      if (data.ok) {
        setDeleteMessage({
          type: 'success',
          text: data.message || 'Your data has been deleted successfully. Billing records are retained as required by law.',
        });
        setShowDeleteConfirm(false);
      } else {
        setDeleteMessage({
          type: 'error',
          text: data.message || 'Failed to delete data. Please contact support.',
        });
      }
    } catch (error) {
      setDeleteMessage({
        type: 'error',
        text: 'Network error. Please try again later.',
      });
    } finally {
      setDeleteLoading(false);
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
          <h1 className="text-4xl font-bold mb-4">Privacy Tools</h1>
          <div className="bg-slate-800 border-2 border-slate-700 rounded-lg p-8">
            <p className="text-slate-300 mb-6">
              You must be signed in to access privacy tools and request your data export.
            </p>
            <button
              onClick={() => signIn(undefined, { callbackUrl: '/privacy-tools' })}
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
          <Link href="/privacy" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to Privacy Policy
          </Link>
        </div>

        <h1 className="text-4xl font-bold mb-2">Privacy Tools</h1>
        <p className="text-slate-400 mb-8">
          Manage your personal data and exercise your GDPR rights
        </p>

        {/* Data Retention Policy */}
        <div className="bg-blue-950/20 border-2 border-blue-900/50 rounded-lg p-6 mb-8">
          <h2 className="text-xl font-bold text-blue-300 mb-4">📋 Data Retention Policy</h2>
          <div className="grid md:grid-cols-2 gap-4 text-sm text-slate-300">
            <div>
              <p className="font-semibold text-white mb-2">Personal Data:</p>
              <ul className="space-y-1">
                <li>• Account data: Retained while active</li>
                <li>• Workflow logs: 90 days</li>
                <li>• Audit logs: 90 days</li>
                <li>• DSAR exports: 24 hours</li>
              </ul>
            </div>
            <div>
              <p className="font-semibold text-white mb-2">Billing Data:</p>
              <ul className="space-y-1">
                <li>• Invoices: 7 years (legal requirement)</li>
                <li>• Stripe IDs: 7 years</li>
                <li>• Payment history: 7 years</li>
              </ul>
            </div>
          </div>
          <p className="text-xs text-slate-400 mt-4">
            DSAR requests are processed within 30 days. Account deletion removes all personal data except legally required billing records.
          </p>
        </div>

        {/* Data Export Section */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8 mb-6">
          <div className="flex items-start gap-4 mb-6">
            <div className="flex-shrink-0 mt-1">
              <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2">Download Your Data</h2>
              <p className="text-slate-300 mb-4 leading-relaxed">
                Request a complete export of your personal data from Levqor. Under UK GDPR and EU GDPR (Article 15 - Right of Access), 
                you have the right to receive a copy of all data we hold about you.
              </p>
              
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 mb-6">
                <h3 className="text-sm font-semibold text-emerald-400 mb-2">What's included:</h3>
                <ul className="space-y-1.5 text-sm text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5">•</span>
                    <span>Account information (email, name, preferences)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5">•</span>
                    <span>Workflows and automation history</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5">•</span>
                    <span>Billing and subscription records</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5">•</span>
                    <span>Referral and partnership data (if applicable)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-emerald-400 mt-0.5">•</span>
                    <span>API keys and developer tools (prefixes only, not full secrets)</span>
                  </li>
                </ul>
              </div>

              <div className="bg-blue-950/30 border border-blue-900/50 rounded-lg p-4 mb-6">
                <h3 className="text-sm font-semibold text-blue-300 mb-2">📧 How it works:</h3>
                <ol className="space-y-2 text-sm text-slate-300">
                  <li className="flex items-start gap-3">
                    <span className="font-bold text-blue-400">1.</span>
                    <span>Click "Request Data Export" below</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="font-bold text-blue-400">2.</span>
                    <span>We'll prepare a ZIP file with all your data</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="font-bold text-blue-400">3.</span>
                    <span>You'll receive an email with a secure download link and one-time passcode</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="font-bold text-blue-400">4.</span>
                    <span>Link valid for 24 hours, passcode valid for 15 minutes</span>
                  </li>
                </ol>
              </div>

              {message && (
                <div className={`rounded-lg p-4 mb-6 ${
                  message.type === 'success' 
                    ? 'bg-emerald-950/30 border border-emerald-900/50' 
                    : 'bg-red-950/30 border border-red-900/50'
                }`}>
                  <p className={message.type === 'success' ? 'text-emerald-300' : 'text-red-300'}>
                    {message.text}
                  </p>
                </div>
              )}

              <button
                onClick={handleRequestExport}
                disabled={loading}
                className={`w-full py-4 rounded-lg font-semibold transition flex items-center justify-center gap-2 ${
                  loading
                    ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                    : 'bg-emerald-500 hover:bg-emerald-600 text-white cursor-pointer'
                }`}
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Preparing Export...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                    </svg>
                    <span>Request Data Export</span>
                  </>
                )}
              </button>

              <p className="text-xs text-slate-400 mt-3 text-center">
                Rate limit: One request per 24 hours
              </p>
            </div>
          </div>
        </div>

        {/* Delete My Data Section */}
        <div className="bg-red-950/20 border-2 border-red-900/50 rounded-lg p-8 mb-6">
          <div className="flex items-start gap-4 mb-6">
            <div className="flex-shrink-0 mt-1">
              <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold mb-2 text-red-300">Delete My Data (GDPR)</h2>
              <p className="text-slate-300 mb-4 leading-relaxed">
                Exercise your right to erasure under GDPR Article 17. This will permanently delete your personal data from Levqor.
              </p>
              
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 mb-4">
                <h3 className="text-sm font-semibold text-amber-400 mb-2">⚠️ What will be deleted:</h3>
                <ul className="space-y-1.5 text-sm text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-red-400 mt-0.5">•</span>
                    <span>Workflows, jobs, and automation logs</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-400 mt-0.5">•</span>
                    <span>API keys and developer tools</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-400 mt-0.5">•</span>
                    <span>Referral and partnership data</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-red-400 mt-0.5">•</span>
                    <span>Account information (anonymized)</span>
                  </li>
                </ul>
              </div>

              <div className="bg-blue-950/30 border border-blue-900/50 rounded-lg p-4 mb-6">
                <h3 className="text-sm font-semibold text-blue-300 mb-2">🔒 What will be kept (legal requirement):</h3>
                <ul className="space-y-1.5 text-sm text-slate-300">
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 mt-0.5">•</span>
                    <span>Billing records and invoices (7 years for tax compliance)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 mt-0.5">•</span>
                    <span>Stripe payment history (financial audit requirements)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-400 mt-0.5">•</span>
                    <span>Anonymized user ID (for billing reference only)</span>
                  </li>
                </ul>
              </div>

              {deleteMessage && (
                <div className={`rounded-lg p-4 mb-6 ${
                  deleteMessage.type === 'success' 
                    ? 'bg-emerald-950/30 border border-emerald-900/50' 
                    : 'bg-red-950/30 border border-red-900/50'
                }`}>
                  <p className={deleteMessage.type === 'success' ? 'text-emerald-300' : 'text-red-300'}>
                    {deleteMessage.text}
                  </p>
                </div>
              )}

              {!showDeleteConfirm ? (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  className="w-full py-4 rounded-lg font-semibold transition bg-red-600 hover:bg-red-700 text-white"
                >
                  Delete My Data (GDPR)
                </button>
              ) : (
                <div className="bg-red-950/50 border-2 border-red-700 rounded-lg p-6">
                  <h3 className="text-lg font-bold text-red-300 mb-3">⚠️ Are you sure?</h3>
                  <p className="text-slate-300 mb-6">
                    This will delete your workflows, logs, and related data. Billing records and invoices will be kept as required by law. 
                    <strong className="text-white block mt-2">This action cannot be undone.</strong>
                  </p>
                  <div className="flex gap-3">
                    <button
                      onClick={handleDeleteMyData}
                      disabled={deleteLoading}
                      className={`flex-1 py-3 rounded-lg font-semibold transition ${
                        deleteLoading
                          ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                          : 'bg-red-600 hover:bg-red-700 text-white'
                      }`}
                    >
                      {deleteLoading ? (
                        <span className="flex items-center justify-center gap-2">
                          <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Deleting...
                        </span>
                      ) : (
                        'Yes, delete my data'
                      )}
                    </button>
                    <button
                      onClick={() => setShowDeleteConfirm(false)}
                      disabled={deleteLoading}
                      className="flex-1 py-3 rounded-lg font-semibold transition bg-slate-700 hover:bg-slate-600 text-white"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              )}

              <p className="text-xs text-slate-400 mt-3">
                This deletes your workflows, logs, and related data. We keep limited billing records to comply with tax and accounting laws.
              </p>
            </div>
          </div>
        </div>

        {/* Other Privacy Rights */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
          <h2 className="text-xl font-bold mb-4">Other Privacy Rights</h2>
          <div className="space-y-4 text-sm text-slate-300">
            <div>
              <h3 className="font-semibold text-white mb-1">Right to Rectification</h3>
              <p>Update incorrect or incomplete personal data in your <Link href="/account" className="text-emerald-400 hover:underline">account settings</Link>.</p>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-1">Right to Restrict Processing</h3>
              <p>Contact <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a> to temporarily suspend processing of your data.</p>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-1">Right to Object</h3>
              <p>Manage marketing preferences in <Link href="/cookie-settings" className="text-emerald-400 hover:underline">cookie settings</Link> or contact privacy@levqor.ai.</p>
            </div>
          </div>
        </div>

        <div className="mt-8 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/gdpr" className="text-emerald-400 hover:underline">GDPR Compliance</Link>
            <Link href="/data-requests" className="text-emerald-400 hover:underline">Data Requests Info</Link>
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">Contact Privacy Team</a>
          </div>
        </div>
      </div>
    </main>
  );
}
