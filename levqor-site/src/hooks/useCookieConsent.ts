'use client';

import { useState, useEffect } from 'react';
import { CookieConsent, getStoredConsent, saveConsent as saveConsentToStorage } from '@/lib/cookies';

export function useCookieConsent() {
  const [consent, setConsent] = useState<CookieConsent | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = getStoredConsent();
    setConsent(stored);
    setIsLoading(false);

    const handleConsentChange = (event: Event) => {
      const customEvent = event as CustomEvent<CookieConsent>;
      setConsent(customEvent.detail);
    };

    window.addEventListener('cookieConsentChanged', handleConsentChange);

    return () => {
      window.removeEventListener('cookieConsentChanged', handleConsentChange);
    };
  }, []);

  const saveConsent = (newConsent: Omit<CookieConsent, 'timestamp' | 'version'>) => {
    saveConsentToStorage(newConsent);
    setConsent(getStoredConsent());
  };

  const acceptAll = () => {
    saveConsent({
      necessary: true,
      functional: true,
      analytics: true,
      marketing: true,
    });
  };

  const rejectAll = () => {
    saveConsent({
      necessary: true,
      functional: false,
      analytics: false,
      marketing: false,
    });
  };

  return {
    consent,
    isLoading,
    saveConsent,
    acceptAll,
    rejectAll,
    needsConsent: consent === null,
  };
}
