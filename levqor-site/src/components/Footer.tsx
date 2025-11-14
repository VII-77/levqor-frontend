import Link from "next/link";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-slate-950 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8 mb-8">
          <div>
            <h3 className="text-white font-bold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><Link href="/terms" className="text-slate-400 hover:text-white transition text-sm">Terms</Link></li>
              <li><Link href="/privacy" className="text-slate-400 hover:text-white transition text-sm">Privacy</Link></li>
              <li><Link href="/cookies" className="text-slate-400 hover:text-white transition text-sm">Cookies</Link></li>
              <li><Link href="/legal/data-processing" className="text-slate-400 hover:text-white transition text-sm">DPA</Link></li>
              <li><Link href="/privacy-tools" className="text-slate-400 hover:text-white transition text-sm">GDPR Tools</Link></li>
              <li><Link href="/marketing-consent" className="text-slate-400 hover:text-white transition text-sm">Marketing Consent</Link></li>
              <li><Link href="/email-unsubscribe" className="text-slate-400 hover:text-white transition text-sm">Email Unsubscribe</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-white font-bold mb-4">Policies</h3>
            <ul className="space-y-2">
              <li><Link href="/risk-disclosure" className="text-slate-400 hover:text-white transition text-sm">Risk Disclosure</Link></li>
              <li><Link href="/fair-use" className="text-slate-400 hover:text-white transition text-sm">Fair Use</Link></li>
              <li><Link href="/acceptable-use" className="text-slate-400 hover:text-white transition text-sm">Acceptable Use</Link></li>
              <li><Link href="/sla" className="text-slate-400 hover:text-white transition text-sm">SLA</Link></li>
              <li><Link href="/support-policy" className="text-slate-400 hover:text-white transition text-sm">Support Policy</Link></li>
              <li><Link href="/cancellation" className="text-slate-400 hover:text-white transition text-sm">Cancellation</Link></li>
              <li><Link href="/refunds" className="text-slate-400 hover:text-white transition text-sm">Refunds</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-white font-bold mb-4">Compliance</h3>
            <ul className="space-y-2">
              <li><Link href="/subprocessors" className="text-slate-400 hover:text-white transition text-sm">Subprocessors</Link></li>
              <li><Link href="/incident-response" className="text-slate-400 hover:text-white transition text-sm">Incident Response</Link></li>
              <li><Link href="/security" className="text-slate-400 hover:text-white transition text-sm">Security</Link></li>
              <li><Link href="/business-continuity" className="text-slate-400 hover:text-white transition text-sm">Business Continuity</Link></li>
              <li><Link href="/high-risk-data" className="text-slate-400 hover:text-white transition text-sm">High-Risk Data</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-white font-bold mb-4">Operations</h3>
            <ul className="space-y-2">
              <li><Link href="/status" className="text-slate-400 hover:text-white transition text-sm">Status</Link></li>
              <li><Link href="/sla-credits" className="text-slate-400 hover:text-white transition text-sm">SLA Credits</Link></li>
              <li><Link href="/disputes" className="text-slate-400 hover:text-white transition text-sm">Disputes</Link></li>
              <li><Link href="/emergency-contacts" className="text-slate-400 hover:text-white transition text-sm">Emergency Contacts</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-slate-800 pt-8">
          <div className="text-center text-sm text-slate-500 mb-2">
            All data stored in EU-based data centers.
          </div>
          <div className="text-center text-sm text-slate-500 mb-4">
            Levqor does not automate medical, legal, financial, or other high-risk workflows. Learn more at{' '}
            <Link href="/risk-disclosure" className="text-emerald-400 hover:underline">
              /risk-disclosure
            </Link>.
          </div>
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-slate-400 text-sm">
              © {currentYear} Levqor. All rights reserved.
            </div>
            <div className="flex gap-6">
              <a href="https://twitter.com/levqor" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                </svg>
              </a>
              <a href="https://github.com/levqor" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-white transition">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
