'use client';

import { useEffect } from 'react';
import { useCookieConsent } from '@/hooks/useCookieConsent';

export default function LoadAnalytics() {
  const { consent } = useCookieConsent();

  useEffect(() => {
    if (consent?.analytics) {
      console.log('[Analytics] Consent granted - Analytics scripts would load here');
    } else if (consent && !consent.analytics) {
      console.log('[Analytics] Consent denied - Analytics blocked');
    }
  }, [consent]);

  return null;
}
