'use client';

import { useState } from 'react';
import Link from 'next/link';
import CookieModal from '@/components/cookies/CookieModal';

export default function CookieSettingsPage() {
  const [isModalOpen, setIsModalOpen] = useState(true);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-4">Cookie Settings</h1>
        <p className="text-slate-300 mb-8">
          Manage your cookie preferences. You can change these settings at any time.
        </p>

        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-medium transition"
        >
          Open Cookie Settings
        </button>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <h2 className="text-2xl font-bold text-white mb-4">About Cookies</h2>
          <p className="text-slate-300 mb-4">
            We use cookies to enhance your experience on our platform. You have full control over which cookies you allow.
          </p>
          <Link href="/cookies" className="text-emerald-400 hover:underline">
            Read our full Cookie Policy →
          </Link>
        </div>
      </div>

      <CookieModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </main>
  );
}
