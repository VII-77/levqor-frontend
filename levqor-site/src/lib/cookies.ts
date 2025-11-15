export function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()!.split(";").shift() || null;
  return null;
}

export function setCookie(name: string, value: string, days = 365): void {
  if (typeof document === "undefined") return;
  const expires = new Date(Date.now() + days * 86400000).toUTCString();
  document.cookie = `${name}=${value}; expires=${expires}; path=/; SameSite=Lax`;
}

export function deleteCookie(name: string): void {
  if (typeof document === "undefined") return;
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

export interface CookieConsent {
  necessary: boolean;
  functional: boolean;
  analytics: boolean;
  marketing: boolean;
  timestamp: string;
  version: string;
}

const CONSENT_KEY = 'levqor_cookie_consent';
const CONSENT_VERSION = '1.0';

export function getStoredConsent(): CookieConsent | null {
  if (typeof window === 'undefined') return null;
  
  try {
    const stored = localStorage.getItem(CONSENT_KEY);
    if (!stored) return null;
    
    const consent = JSON.parse(stored) as CookieConsent;
    
    if (consent.version !== CONSENT_VERSION) {
      return null;
    }
    
    return consent;
  } catch {
    return null;
  }
}

export function saveConsent(consent: Omit<CookieConsent, 'timestamp' | 'version'>): void {
  if (typeof window === 'undefined') return;
  
  const fullConsent: CookieConsent = {
    ...consent,
    timestamp: new Date().toISOString(),
    version: CONSENT_VERSION,
  };
  
  localStorage.setItem(CONSENT_KEY, JSON.stringify(fullConsent));
  
  window.dispatchEvent(new CustomEvent('cookieConsentChanged', { detail: fullConsent }));
}

export function clearConsent(): void {
  if (typeof window === 'undefined') return;
  localStorage.removeItem(CONSENT_KEY);
}

export function needsConsent(): boolean {
  return getStoredConsent() === null;
}
