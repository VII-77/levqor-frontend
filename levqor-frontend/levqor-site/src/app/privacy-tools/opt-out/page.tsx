"use client";

import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';

interface OptOutStatus {
  marketing: boolean;
  profiling: boolean;
  automation: boolean;
  analytics: boolean;
  all: boolean;
  timestamp: number | null;
}

export default function OptOutPage() {
  const { data: session, status } = useSession();
  const router = useRouter();
  
  const [optOuts, setOptOuts] = useState<OptOutStatus>({
    marketing: false,
    profiling: false,
    automation: false,
    analytics: false,
    all: false,
    timestamp: null
  });
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<{type: 'success' | 'error', text: string} | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (status === 'unauthenticated') {
      router.push('/signin');
    }
  }, [status, router]);

  // Load current opt-out status
  useEffect(() => {
    if (status === 'authenticated' && session?.user) {
      fetchOptOutStatus();
    }
  }, [status, session]);

  const fetchOptOutStatus = async () => {
    try {
      const res = await fetch('/api/gdpr/opt-out', {
        headers: {
          'Authorization': `Bearer ${(session as any)?.accessToken || ''}`
        }
      });
      
      if (res.ok) {
        const data = await res.json();
        setOptOuts({
          marketing: data.marketing || false,
          profiling: data.profiling || false,
          automation: data.automation || false,
          analytics: data.analytics || false,
          all: data.all || false,
          timestamp: data.timestamp || null
        });
      }
    } catch (error) {
      console.error('Failed to fetch opt-out status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (scope: string) => {
    setSaving(true);
    setMessage(null);
    
    try {
      const res = await fetch('/api/gdpr/opt-out', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${(session as any)?.accessToken || ''}`
        },
        body: JSON.stringify({ scope })
      });
      
      const data = await res.json();
      
      if (res.ok) {
        setMessage({
          type: 'success',
          text: `Successfully opted out of ${scope}. Changes will take effect immediately.`
        });
        
        // Refresh status
        await fetchOptOutStatus();
      } else {
        setMessage({
          type: 'error',
          text: data.message || 'Failed to update preferences'
        });
      }
    } catch (error) {
      setMessage({
        type: 'error',
        text: 'An error occurred while updating your preferences'
      });
    } finally {
      setSaving(false);
    }
  };

  const handleDisableAll = async () => {
    await handleToggle('all');
  };

  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  if (status === 'unauthenticated') {
    return null; // Will redirect
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white shadow rounded-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Privacy & Data Preferences
          </h1>
          <p className="text-gray-600 mb-8">
            Control how Levqor uses your data. You have the right to object to certain types of data processing under GDPR.
          </p>

          {message && (
            <div className={`mb-6 p-4 rounded-md ${
              message.type === 'success' 
                ? 'bg-green-50 border border-green-200 text-green-800' 
                : 'bg-red-50 border border-red-200 text-red-800'
            }`}>
              {message.text}
            </div>
          )}

          <div className="space-y-6 mb-8">
            <div className="border-b border-gray-200 pb-4">
              <label className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  checked={optOuts.marketing}
                  onChange={() => handleToggle('marketing')}
                  disabled={saving || optOuts.all}
                  className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 disabled:opacity-50"
                />
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Marketing Communications</div>
                  <div className="text-sm text-gray-600">
                    Opt out of promotional emails, newsletters, and marketing campaigns. 
                    You'll still receive important transactional emails about your account.
                  </div>
                </div>
              </label>
            </div>

            <div className="border-b border-gray-200 pb-4">
              <label className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  checked={optOuts.profiling}
                  onChange={() => handleToggle('profiling')}
                  disabled={saving || optOuts.all}
                  className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 disabled:opacity-50"
                />
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Profiling & Personalization</div>
                  <div className="text-sm text-gray-600">
                    Opt out of AI-driven recommendations, personalized suggestions, and behavioral profiling. 
                    You'll see generic content instead of personalized recommendations.
                  </div>
                </div>
              </label>
            </div>

            <div className="border-b border-gray-200 pb-4">
              <label className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  checked={optOuts.automation}
                  onChange={() => handleToggle('automation')}
                  disabled={saving || optOuts.all}
                  className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 disabled:opacity-50"
                />
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Automated Workflows</div>
                  <div className="text-sm text-gray-600">
                    Opt out of background automated workflow triggers and suggestions. 
                    Your manually triggered workflows will continue to work normally.
                  </div>
                </div>
              </label>
            </div>

            <div className="border-b border-gray-200 pb-4">
              <label className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  checked={optOuts.analytics}
                  onChange={() => handleToggle('analytics')}
                  disabled={saving || optOuts.all}
                  className="mt-1 h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 disabled:opacity-50"
                />
                <div className="flex-1">
                  <div className="font-medium text-gray-900">Analytics Tracking</div>
                  <div className="text-sm text-gray-600">
                    Opt out of usage analytics and behavioral tracking. 
                    We won't record your activity for analytics purposes.
                  </div>
                </div>
              </label>
            </div>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-6">
            <div className="font-medium text-yellow-900 mb-2">Opt Out of Everything</div>
            <p className="text-sm text-yellow-800 mb-4">
              This will disable all non-essential data processing: marketing, profiling, automation, and analytics.
            </p>
            <button
              onClick={handleDisableAll}
              disabled={saving || optOuts.all}
              className="bg-yellow-600 text-white px-6 py-2 rounded-md hover:bg-yellow-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {optOuts.all ? 'All Disabled' : 'Disable Everything'}
            </button>
          </div>

          <div className="text-sm text-gray-600 space-y-2">
            <p>
              <strong>Important:</strong> Changes take effect immediately and apply across our entire platform.
            </p>
            <p>
              These are your GDPR rights under Article 21 (Right to Object). 
              For other privacy requests, see our{' '}
              <a href="/data-requests" className="text-blue-600 hover:underline">
                data request portal
              </a>.
            </p>
            <p>
              Questions? Contact our Data Protection Officer at{' '}
              <a href="mailto:privacy@levqor.ai" className="text-blue-600 hover:underline">
                privacy@levqor.ai
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
