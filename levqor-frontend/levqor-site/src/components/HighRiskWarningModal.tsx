"use client";
import { useState, useEffect } from "react";

interface HighRiskWarningModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAccept: () => void;
}

export default function HighRiskWarningModal({ isOpen, onClose, onAccept }: HighRiskWarningModalProps) {
  const [understood, setUnderstood] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setUnderstood(false);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50 p-4">
      <div className="bg-slate-900 border-2 border-red-500/50 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6 sm:p-8">
          {/* Warning Icon */}
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0">
              <svg className="w-8 h-8 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">High-Risk Automation Prohibited</h2>
              <p className="text-red-400 font-semibold">Please read carefully before proceeding</p>
            </div>
          </div>

          {/* Warning Content */}
          <div className="space-y-6">
            <div className="p-4 bg-red-950/30 border border-red-900/50 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-3">Levqor CANNOT Automate:</h3>
              <ul className="space-y-2 text-slate-300">
                <li className="flex items-start gap-2">
                  <span className="text-red-400 mt-1 font-bold">✕</span>
                  <span><strong className="text-white">Medical decisions:</strong> Diagnosis, treatment plans, prescription management, patient triage</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-400 mt-1 font-bold">✕</span>
                  <span><strong className="text-white">Legal decisions:</strong> Legal advice, case management, contract execution, compliance decisions</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-400 mt-1 font-bold">✕</span>
                  <span><strong className="text-white">Financial decisions:</strong> Investment advice, trading execution, loan approvals, credit decisions</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-400 mt-1 font-bold">✕</span>
                  <span><strong className="text-white">Healthcare records:</strong> Protected health information (PHI), medical record updates</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-400 mt-1 font-bold">✕</span>
                  <span><strong className="text-white">Life-critical systems:</strong> Emergency services, safety systems, life-support equipment</span>
                </li>
              </ul>
            </div>

            <div className="p-4 bg-amber-950/30 border border-amber-900/50 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-3">Why This Matters:</h3>
              <ul className="space-y-2 text-slate-300 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-1">•</span>
                  <span>These decisions require human judgment and professional expertise</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-1">•</span>
                  <span>Regulatory requirements prohibit automated decision-making in these areas</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-1">•</span>
                  <span>Errors in these domains can cause serious harm or legal liability</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-amber-400 mt-1">•</span>
                  <span>Professional licenses may be required for these activities</span>
                </li>
              </ul>
            </div>

            <div className="p-4 bg-emerald-950/30 border border-emerald-900/50 rounded-lg">
              <h3 className="text-lg font-bold text-white mb-3">What We CAN Automate:</h3>
              <ul className="space-y-2 text-slate-300 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span><strong>Administrative tasks:</strong> Scheduling, data entry, reporting, notifications</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span><strong>Business operations:</strong> CRM sync, invoice processing, lead management</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span><strong>Marketing:</strong> Email campaigns, social media posting, analytics reporting</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span><strong>Customer service:</strong> Ticket routing, response templates, FAQ automation</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-emerald-400 mt-1">✓</span>
                  <span><strong>Analytics:</strong> Data collection, dashboard updates, performance tracking</span>
                </li>
              </ul>
            </div>

            <div className="p-4 bg-slate-800 border border-slate-700 rounded-lg">
              <label className="flex items-start gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={understood}
                  onChange={(e) => setUnderstood(e.target.checked)}
                  className="mt-0.5 h-5 w-5 rounded border-slate-600 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-slate-900 transition"
                />
                <span className="text-sm text-slate-300 group-hover:text-white transition">
                  I understand that Levqor cannot automate high-risk decisions in medical, legal, financial, or life-critical domains. I confirm my workflow does not involve these prohibited use cases.
                </span>
              </label>
            </div>
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-3 mt-6">
            <button
              onClick={onClose}
              className="flex-1 px-6 py-3 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition"
            >
              Cancel
            </button>
            <button
              onClick={onAccept}
              disabled={!understood}
              className="flex-1 px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              I Understand, Continue
            </button>
          </div>

          <p className="text-xs text-slate-500 mt-4 text-center">
            For full details, see our{" "}
            <a href="/risk-disclosure" target="_blank" className="text-emerald-400 hover:underline">
              Risk Disclosure Policy
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
