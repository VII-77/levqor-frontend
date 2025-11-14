'use client';

import { useState, useEffect, useRef } from 'react';
import { useCookieConsent } from '@/hooks/useCookieConsent';

interface CookieModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CookieModal({ isOpen, onClose }: CookieModalProps) {
  const { consent, saveConsent, acceptAll, rejectAll } = useCookieConsent();
  const modalRef = useRef<HTMLDivElement>(null);
  
  const [preferences, setPreferences] = useState({
    necessary: true,
    functional: consent?.functional ?? true,
    analytics: consent?.analytics ?? true,
    marketing: consent?.marketing ?? true,
  });

  useEffect(() => {
    if (consent) {
      setPreferences({
        necessary: true,
        functional: consent.functional,
        analytics: consent.analytics,
        marketing: consent.marketing,
      });
    }
  }, [consent]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
      
      modalRef.current?.focus();
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  const handleSavePreferences = () => {
    saveConsent(preferences);
    onClose();
  };

  const handleAcceptAll = () => {
    acceptAll();
    onClose();
  };

  const handleRejectAll = () => {
    rejectAll();
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50 p-4"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="cookie-modal-title"
    >
      <div
        ref={modalRef}
        className="bg-slate-800 rounded-xl shadow-xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
      >
        <h2 id="cookie-modal-title" className="text-2xl font-bold text-white mb-4">
          Cookie Settings
        </h2>

        <p className="text-slate-300 text-sm mb-6">
          We use cookies to enhance your experience. You can choose which types of cookies to allow.
        </p>

        <div className="space-y-4 mb-6">
          <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-semibold text-white mb-1">Strictly Necessary</h3>
                <p className="text-sm text-slate-400">
                  Essential for the website to function. These cannot be disabled.
                </p>
              </div>
              <div className="ml-4">
                <div className="w-12 h-6 bg-emerald-500 rounded-full flex items-center px-1">
                  <div className="w-4 h-4 bg-white rounded-full ml-auto"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-semibold text-white mb-1">Functional Cookies</h3>
                <p className="text-sm text-slate-400">
                  Remember your preferences and settings.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setPreferences(p => ({ ...p, functional: !p.functional }))}
                className={`ml-4 w-12 h-6 rounded-full flex items-center px-1 transition-colors ${
                  preferences.functional ? 'bg-emerald-500' : 'bg-slate-600'
                }`}
                aria-label="Toggle functional cookies"
                aria-pressed={preferences.functional}
              >
                <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                  preferences.functional ? 'ml-auto' : ''
                }`}></div>
              </button>
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-semibold text-white mb-1">Analytics Cookies</h3>
                <p className="text-sm text-slate-400">
                  Help us understand how you use our platform.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setPreferences(p => ({ ...p, analytics: !p.analytics }))}
                className={`ml-4 w-12 h-6 rounded-full flex items-center px-1 transition-colors ${
                  preferences.analytics ? 'bg-emerald-500' : 'bg-slate-600'
                }`}
                aria-label="Toggle analytics cookies"
                aria-pressed={preferences.analytics}
              >
                <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                  preferences.analytics ? 'ml-auto' : ''
                }`}></div>
              </button>
            </div>
          </div>

          <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <h3 className="font-semibold text-white mb-1">Marketing Cookies</h3>
                <p className="text-sm text-slate-400">
                  Track effectiveness of marketing campaigns.
                </p>
              </div>
              <button
                type="button"
                onClick={() => setPreferences(p => ({ ...p, marketing: !p.marketing }))}
                className={`ml-4 w-12 h-6 rounded-full flex items-center px-1 transition-colors ${
                  preferences.marketing ? 'bg-emerald-500' : 'bg-slate-600'
                }`}
                aria-label="Toggle marketing cookies"
                aria-pressed={preferences.marketing}
              >
                <div className={`w-4 h-4 bg-white rounded-full transition-transform ${
                  preferences.marketing ? 'ml-auto' : ''
                }`}></div>
              </button>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-3">
          <button
            onClick={handleSavePreferences}
            className="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-medium transition"
          >
            Save Preferences
          </button>
          <button
            onClick={handleAcceptAll}
            className="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-medium transition"
          >
            Accept All
          </button>
          <button
            onClick={handleRejectAll}
            className="flex-1 bg-slate-700 hover:bg-slate-600 text-white px-6 py-3 rounded-lg font-medium transition"
          >
            Reject All
          </button>
        </div>
      </div>
    </div>
  );
}
