'use client';

import { useState } from 'react';
import { useCookieConsent } from '@/hooks/useCookieConsent';
import CookieModal from './CookieModal';

export default function CookieBanner() {
  const { needsConsent, acceptAll, rejectAll } = useCookieConsent();
  const [isModalOpen, setIsModalOpen] = useState(false);

  if (!needsConsent) return null;

  return (
    <>
      <div
        className="fixed bottom-0 left-0 right-0 w-full bg-slate-900 text-white p-4 border-t border-slate-700 shadow-xl z-40"
        role="region"
        aria-label="Cookie consent banner"
      >
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-200 flex-1">
            Levqor uses cookies to improve your experience. You can accept or reject non-essential cookies.
          </p>
          
          <div className="flex flex-wrap gap-3 items-center">
            <button
              onClick={acceptAll}
              className="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-2 rounded-lg font-medium transition whitespace-nowrap"
              aria-label="Accept all cookies"
            >
              Accept All
            </button>
            
            <button
              onClick={rejectAll}
              className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-2 rounded-lg font-medium transition whitespace-nowrap"
              aria-label="Reject all non-essential cookies"
            >
              Reject All
            </button>
            
            <button
              onClick={() => setIsModalOpen(true)}
              className="bg-slate-700 hover:bg-slate-600 text-white px-6 py-2 rounded-lg font-medium transition whitespace-nowrap"
              aria-label="Open cookie settings"
            >
              Cookie Settings
            </button>
          </div>
        </div>
      </div>

      <CookieModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </>
  );
}
