'use client';

import Link from 'next/link';

interface HighRiskBlockedModalProps {
  isOpen: boolean;
  onClose: () => void;
  matchedKeywords?: string[];
  errorMessage?: string;
}

export default function HighRiskBlockedModal({
  isOpen,
  onClose,
  matchedKeywords = [],
  errorMessage
}: HighRiskBlockedModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative w-full max-w-md bg-slate-900 border-2 border-red-900/50 rounded-2xl shadow-2xl overflow-hidden">
        {/* Red accent bar */}
        <div className="h-2 bg-gradient-to-r from-red-600 to-red-500" />
        
        <div className="p-8">
          {/* Icon */}
          <div className="flex items-center justify-center w-16 h-16 mx-auto mb-6 bg-red-950/50 rounded-full border-2 border-red-900/50">
            <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-white text-center mb-4">
            Workflow Not Allowed
          </h2>

          {/* Message */}
          <div className="space-y-4 mb-6">
            <p className="text-slate-300 text-center">
              {errorMessage || "This workflow contains prohibited high-risk content and cannot be created."}
            </p>

            <div className="p-4 bg-red-950/20 border border-red-900/30 rounded-lg">
              <p className="text-sm text-slate-300 mb-2">
                <strong className="text-red-300">Prohibited Categories:</strong>
              </p>
              <ul className="text-sm text-slate-400 space-y-1.5 ml-4">
                <li>• Medical, healthcare, or health advice</li>
                <li>• Legal advice or document generation</li>
                <li>• Financial, investment, or trading automation</li>
                <li>• Processing of child/minor data (under 18)</li>
                <li>• Special category data (biometrics, religion, race, etc.)</li>
              </ul>
            </div>

            {matchedKeywords && matchedKeywords.length > 0 && (
              <div className="p-3 bg-slate-950/50 border border-slate-800 rounded-lg">
                <p className="text-xs text-slate-400 mb-2">Detected keywords:</p>
                <div className="flex flex-wrap gap-2">
                  {matchedKeywords.slice(0, 6).map((keyword, index) => (
                    <span 
                      key={index}
                      className="px-2 py-1 bg-red-950/30 border border-red-900/30 rounded text-xs text-red-300"
                    >
                      {keyword}
                    </span>
                  ))}
                  {matchedKeywords.length > 6 && (
                    <span className="px-2 py-1 text-xs text-slate-500">
                      +{matchedKeywords.length - 6} more
                    </span>
                  )}
                </div>
              </div>
            )}

            <div className="flex items-start gap-2 p-3 bg-blue-950/20 border border-blue-900/30 rounded-lg">
              <svg className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-xs text-slate-300">
                This restriction protects both you and Levqor from legal liability. These workflows require licensed professionals.
              </p>
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-3">
            <button
              onClick={onClose}
              className="w-full py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition"
            >
              I Understand
            </button>
            
            <Link
              href="/risk-disclosure"
              className="block text-center py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition"
            >
              Learn More About Risk Policy
            </Link>
          </div>

          {/* Footer */}
          <p className="text-xs text-slate-500 text-center mt-6">
            Questions? Contact{' '}
            <a href="mailto:compliance@levqor.ai" className="text-emerald-400 hover:underline">
              compliance@levqor.ai
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
