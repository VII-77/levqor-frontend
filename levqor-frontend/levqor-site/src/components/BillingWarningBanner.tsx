'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

interface BillingStatus {
  status: string;
  next_action_at?: number;
}

export function BillingWarningBanner() {
  const [billingStatus, setBillingStatus] = useState<BillingStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function checkBillingStatus() {
      try {
        const res = await fetch('/api/billing/status');
        if (res.ok) {
          const data = await res.json();
          setBillingStatus(data);
        }
      } catch (error) {
        console.error('Failed to fetch billing status:', error);
      } finally {
        setLoading(false);
      }
    }

    checkBillingStatus();
    const interval = setInterval(checkBillingStatus, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading || !billingStatus || billingStatus.status === 'ok' || billingStatus.status === 'none') {
    return null;
  }

  const getBannerConfig = (status: string) => {
    switch (status) {
      case 'day1_notice':
        return {
          bg: 'bg-yellow-50 border-yellow-200',
          text: 'text-yellow-900',
          icon: '⚠️',
          title: 'Payment Issue',
          message: 'We couldn\'t process your payment. Please update your billing details to avoid service interruption.',
          urgency: 'low'
        };
      case 'day7_notice':
        return {
          bg: 'bg-orange-50 border-orange-300',
          text: 'text-orange-900',
          icon: '⚠️',
          title: 'Urgent: Service at Risk',
          message: 'Your payment has failed multiple times. Service will be paused soon if payment is not received.',
          urgency: 'medium'
        };
      case 'day14_final':
        return {
          bg: 'bg-red-50 border-red-300',
          text: 'text-red-900',
          icon: '🚨',
          title: 'Final Notice',
          message: 'Your service will be paused within 3 days. Update your payment method immediately to prevent interruption.',
          urgency: 'high'
        };
      case 'suspended':
        return {
          bg: 'bg-red-100 border-red-400',
          text: 'text-red-900',
          icon: '🚫',
          title: 'Account Suspended',
          message: 'Your account is suspended due to payment failure. All workflows are paused. Update your payment to restore service.',
          urgency: 'critical'
        };
      default:
        return null;
    }
  };

  const config = getBannerConfig(billingStatus.status);
  
  if (!config) return null;

  return (
    <div className={`border-b-2 ${config.bg} ${config.text} px-4 py-3`}>
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-2xl" role="img" aria-label="warning">{config.icon}</span>
          <div>
            <p className="font-semibold">{config.title}</p>
            <p className="text-sm">{config.message}</p>
          </div>
        </div>
        <Link 
          href="/billing" 
          className="bg-white px-4 py-2 rounded-md font-medium hover:bg-opacity-90 transition-colors shadow-sm whitespace-nowrap ml-4"
        >
          Update Billing
        </Link>
      </div>
    </div>
  );
}
