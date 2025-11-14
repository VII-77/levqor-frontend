export default function HighRiskWarning() {
  return (
    <div className="bg-red-950/20 border-2 border-red-900/50 rounded-lg p-6 mb-6">
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-0.5">
          <svg className="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-red-300 mb-2">High-Risk Data Restrictions</h3>
          <p className="text-sm text-slate-300 mb-3">
            For legal compliance and user safety, Levqor cannot automate workflows involving:
          </p>
          <ul className="space-y-1.5 text-sm text-slate-300">
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-0.5">•</span>
              <span>Medical or health workflows (diagnosis, treatment, health advice)</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-0.5">•</span>
              <span>Legal advice or contract generation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-0.5">•</span>
              <span>Financial, trading, or tax automation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-0.5">•</span>
              <span>Processing of child or minor data (under 18)</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-red-400 mt-0.5">•</span>
              <span>Special category data (race, religion, biometrics, etc.)</span>
            </li>
          </ul>
          <p className="text-xs text-slate-400 mt-3">
            Workflows containing prohibited keywords will be automatically rejected.
          </p>
        </div>
      </div>
    </div>
  );
}
