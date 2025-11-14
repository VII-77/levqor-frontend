'use client';

import { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

function DownloadPageContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!token || !otp) {
      setError('Please enter your 6-digit passcode');
      return;
    }

    if (otp.length !== 6 || !/^\d+$/.test(otp)) {
      setError('Passcode must be exactly 6 digits');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('/api/data-export/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token, otp }),
      });

      if (res.ok) {
        // File download
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `levqor-data-export-${new Date().toISOString().split('T')[0]}.zip`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        setSuccess(true);
      } else {
        const data = await res.json();
        
        if (data.error === 'TOKEN_EXPIRED') {
          setError('This download link has expired. Please request a new export from your account.');
        } else if (data.error === 'OTP_EXPIRED') {
          setError('Your passcode has expired (15 minute limit). Please request a new export.');
        } else if (data.error === 'INVALID_OTP') {
          setError('Incorrect passcode. Please check the code from your email and try again.');
        } else if (data.error === 'FILE_NOT_FOUND') {
          setError('Export file not found. Please request a new export.');
        } else {
          setError('Download failed. The link may be invalid or expired. Please request a new export.');
        }
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="max-w-md mx-auto px-4 text-center">
          <div className="bg-red-950/30 border-2 border-red-900/50 rounded-lg p-8">
            <svg className="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h1 className="text-2xl font-bold mb-2 text-red-300">Invalid Link</h1>
            <p className="text-slate-300 mb-6">
              This link is invalid or incomplete. Please use the link from your export email.
            </p>
            <Link href="/privacy-tools" className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition">
              Go to Privacy Tools →
            </Link>
          </div>
        </div>
      </main>
    );
  }

  if (success) {
    return (
      <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="max-w-md mx-auto px-4 text-center">
          <div className="bg-emerald-950/30 border-2 border-emerald-900/50 rounded-lg p-8">
            <svg className="w-16 h-16 text-emerald-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h1 className="text-2xl font-bold mb-2 text-emerald-300">Download Complete!</h1>
            <p className="text-slate-300 mb-6">
              Your data export has been downloaded successfully. You can now close this page.
            </p>
            <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 text-left">
              <h3 className="text-sm font-semibold text-white mb-2">⚠️ Important:</h3>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>• The ZIP file contains your personal data - keep it secure</li>
                <li>• Do not share the file with unauthorized parties</li>
                <li>• Delete the file when no longer needed</li>
              </ul>
            </div>
            <div className="mt-6">
              <Link href="/privacy" className="text-emerald-400 hover:underline text-sm">
                Privacy Policy
              </Link>
              <span className="text-slate-600 mx-2">•</span>
              <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline text-sm">
                Contact Privacy Team
              </a>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
      <div className="max-w-md mx-auto px-4">
        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
          <div className="text-center mb-8">
            <div className="flex justify-center mb-4">
              <svg className="w-16 h-16 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold mb-2">Download Your Data</h1>
            <p className="text-slate-400 text-sm">
              Enter the 6-digit passcode from your email to download your data export
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label htmlFor="otp" className="block text-sm font-medium text-slate-300 mb-2">
                One-Time Passcode
              </label>
              <input
                id="otp"
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                maxLength={6}
                value={otp}
                onChange={(e) => {
                  const value = e.target.value.replace(/\D/g, '');
                  setOtp(value);
                  setError('');
                }}
                placeholder="000 000"
                className="w-full text-center text-2xl tracking-[0.5em] rounded-lg border-2 border-slate-700 bg-slate-800/50 py-4 px-4 text-white focus:border-emerald-500 focus:outline-none font-mono"
                disabled={loading}
                autoFocus
              />
              <p className="text-xs text-slate-400 mt-2 text-center">
                Check your email for the 6-digit code
              </p>
            </div>

            {error && (
              <div className="mb-6 bg-red-950/30 border border-red-900/50 rounded-lg p-4">
                <p className="text-red-300 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || otp.length !== 6}
              className={`w-full py-4 rounded-lg font-semibold transition flex items-center justify-center gap-2 ${
                loading || otp.length !== 6
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
                  <span>Verifying...</span>
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  <span>Download Export</span>
                </>
              )}
            </button>

            <div className="mt-6 text-center text-xs text-slate-400">
              <p>⏱️ Passcode valid for 15 minutes</p>
              <p className="mt-1">🔒 Link valid for 24 hours</p>
            </div>
          </form>

          <div className="mt-8 pt-6 border-t border-slate-800 text-center">
            <p className="text-sm text-slate-400 mb-3">
              Need help or didn't receive your email?
            </p>
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline text-sm">
              Contact Privacy Team →
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}

export default function DownloadPage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="text-slate-400">Loading...</div>
      </main>
    }>
      <DownloadPageContent />
    </Suspense>
  );
}
