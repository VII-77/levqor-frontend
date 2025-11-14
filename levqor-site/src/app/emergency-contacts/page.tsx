import Link from "next/link";

export default function EmergencyContactsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-6 mb-8">
          <h1 className="text-3xl font-bold text-red-400 mb-2">Emergency Contacts & Incident Procedures</h1>
          <p className="text-slate-300">
            For Severity 1 issues only (critical outages, data incidents, major system failures)
          </p>
        </div>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">⚠️ When to Use Emergency Contacts</h2>
          <p className="text-slate-300 leading-relaxed">
            Emergency contacts are reserved for <strong className="text-white">Severity 1 incidents only</strong>. Use these channels when:
          </p>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
            <ul className="space-y-3 text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold mt-1">•</span>
                <div>
                  <strong className="text-white">Complete Service Outage:</strong> The entire Levqor platform is inaccessible or non-functional
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold mt-1">•</span>
                <div>
                  <strong className="text-white">Critical Data Incident:</strong> Suspected data breach, unauthorized access, or data loss
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold mt-1">•</span>
                <div>
                  <strong className="text-white">Major Billing Error:</strong> Critical billing issue affecting multiple customers or large sums
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-red-400 font-bold mt-1">•</span>
                <div>
                  <strong className="text-white">Security Vulnerability:</strong> You've discovered a critical security flaw that needs immediate attention
                </div>
              </li>
            </ul>
          </div>
          
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4 mt-4">
            <p className="text-yellow-200 text-sm">
              <strong>Not for routine issues:</strong> Standard support requests, feature questions, minor bugs, or general inquiries should go through{" "}
              <a href="mailto:support@levqor.ai" className="text-yellow-400 underline">
                support@levqor.ai
              </a>
            </p>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">📞 Emergency Contact Channels</h2>
          
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <div>
              <h3 className="text-lg font-bold text-white mb-2">Primary Emergency Contact</h3>
              <p className="text-slate-300 mb-2">
                Email:{" "}
                <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline font-mono">
                  support@levqor.ai
                </a>
              </p>
              <p className="text-slate-400 text-sm">
                <strong className="text-white">Subject line format:</strong> Start with <code className="bg-slate-950 px-2 py-1 rounded text-red-400">[SEV1]</code> followed by a brief description
              </p>
              <p className="text-slate-400 text-sm mt-1">
                Example: <code className="bg-slate-950 px-2 py-1 rounded text-emerald-400">[SEV1] Complete platform outage since 14:30 UTC</code>
              </p>
            </div>

            <div className="border-t border-slate-700 pt-4">
              <h3 className="text-lg font-bold text-white mb-2">Enterprise Customers</h3>
              <p className="text-slate-300 text-sm">
                Business plan holders may receive a dedicated emergency hotline in the future. For now, use the email channel above with the [SEV1] tag for priority routing.
              </p>
            </div>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">📋 What to Include in Your Emergency Report</h2>
          <p className="text-slate-300 leading-relaxed">
            To help us respond quickly and effectively, please include:
          </p>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <div>
                  <strong className="text-white">Account Information:</strong> Company name, account email, plan type
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <div>
                  <strong className="text-white">Impact Description:</strong> What's broken? How many users affected?
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <div>
                  <strong className="text-white">Timeline:</strong> When did the issue start? Exact time if possible (include timezone)
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <div>
                  <strong className="text-white">Screenshots/Logs:</strong> Any error messages, screenshots, or relevant logs
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <div>
                  <strong className="text-white">Steps to Reproduce:</strong> What actions lead to the issue? (if applicable)
                </div>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-400 mt-1">✓</span>
                <div>
                  <strong className="text-white">Business Impact:</strong> Revenue loss, customer impact, compliance concerns, etc.
                </div>
              </li>
            </ul>
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">⏱️ What Happens Next</h2>
          <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
            <div>
              <h3 className="text-white font-bold mb-1">1. Immediate Acknowledgment</h3>
              <p className="text-slate-300 text-sm">
                You'll receive an automated acknowledgment immediately, followed by human confirmation within <strong className="text-white">1 hour</strong> for Severity 1 incidents.
              </p>
            </div>
            
            <div>
              <h3 className="text-white font-bold mb-1">2. Incident Assessment</h3>
              <p className="text-slate-300 text-sm">
                Our on-call engineer will assess the issue and begin investigation. You'll receive an initial status update within 2 hours.
              </p>
            </div>
            
            <div>
              <h3 className="text-white font-bold mb-1">3. Regular Updates</h3>
              <p className="text-slate-300 text-sm">
                We'll provide status updates every 2–4 hours until the issue is resolved, or more frequently for critical outages.
              </p>
            </div>
            
            <div>
              <h3 className="text-white font-bold mb-1">4. Resolution & Post-Mortem</h3>
              <p className="text-slate-300 text-sm">
                Once resolved, you'll receive a confirmation. For major incidents, we'll provide a detailed post-mortem within 5 business days.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
          <h3 className="text-lg font-bold text-white">Related Policies</h3>
          <ul className="space-y-2">
            <li>
              <Link href="/sla" className="text-emerald-400 hover:underline text-sm">
                Service Level Agreement (SLA)
              </Link>
            </li>
            <li>
              <Link href="/incident-response" className="text-emerald-400 hover:underline text-sm">
                Incident Response Plan
              </Link>
            </li>
            <li>
              <Link href="/business-continuity" className="text-emerald-400 hover:underline text-sm">
                Business Continuity Policy
              </Link>
            </li>
            <li>
              <Link href="/status" className="text-emerald-400 hover:underline text-sm">
                System Status Page
              </Link>
            </li>
          </ul>
        </section>

        <section className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-6">
          <h3 className="text-lg font-bold text-emerald-400 mb-2">For Non-Emergency Issues</h3>
          <p className="text-slate-300 text-sm mb-3">
            For all routine support needs, please use our standard channels:
          </p>
          <ul className="space-y-1 text-slate-300 text-sm">
            <li>
              Standard Support:{" "}
              <a href="mailto:support@levqor.ai" className="text-emerald-400 underline">
                support@levqor.ai
              </a>
            </li>
            <li>
              Billing Questions:{" "}
              <a href="mailto:billing@levqor.ai" className="text-emerald-400 underline">
                billing@levqor.ai
              </a>
            </li>
            <li>
              Sales Inquiries:{" "}
              <a href="mailto:sales@levqor.ai" className="text-emerald-400 underline">
                sales@levqor.ai
              </a>
            </li>
          </ul>
        </section>
      </div>
    </main>
  );
}
