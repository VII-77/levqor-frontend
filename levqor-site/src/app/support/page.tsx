import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Support Center - Get Help with Levqor",
  description: "Find answers, contact support, and get help with your Levqor automation.",
};

export default function SupportPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Support Center
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            We're here to help—worldwide
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Get fast, friendly support from our global team of automation experts, no matter where you're located.
          </p>
        </div>

        {/* Support Options */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 text-center">
            <div className="w-16 h-16 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Email Support</h3>
            <p className="text-slate-300 mb-4">Get help via email. We respond within 24-48 hours.</p>
            <a 
              href="mailto:support@levqor.ai" 
              className="inline-block px-6 py-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-lg font-semibold hover:bg-emerald-500/20 transition"
            >
              support@levqor.ai
            </a>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 text-center">
            <div className="w-16 h-16 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Live Chat</h3>
            <p className="text-slate-300 mb-4">Chat with our AI assistant or request human support.</p>
            <button className="px-6 py-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-lg font-semibold hover:bg-emerald-500/20 transition">
              Open Chat Widget
            </button>
            <p className="text-xs text-slate-400 mt-2">(Widget available on all pages)</p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 text-center">
            <div className="w-16 h-16 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-white mb-3">Help Docs</h3>
            <p className="text-slate-300 mb-4">Browse guides, FAQs, and documentation.</p>
            <Link 
              href="/faq" 
              className="inline-block px-6 py-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 rounded-lg font-semibold hover:bg-emerald-500/20 transition"
            >
              View FAQ
            </Link>
          </div>
        </div>

        {/* Response Times */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 mb-16">
          <h2 className="text-2xl font-bold text-white mb-6">Our Response Times</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Email Support</h3>
              <p className="text-slate-300">24-48 hours for all plans</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Priority Support</h3>
              <p className="text-slate-300">4-12 hours for Growth & Business plans</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Live Chat</h3>
              <p className="text-slate-300">Instant AI responses, human handoff as needed</p>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Emergency Issues</h3>
              <p className="text-slate-300">Same-day response for critical failures</p>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h3 className="text-xl font-bold text-white mb-4">Popular Resources</h3>
            <ul className="space-y-3">
              <li><Link href="/faq" className="text-emerald-400 hover:underline">FAQ</Link></li>
              <li><Link href="/how-it-works" className="text-emerald-400 hover:underline">How It Works</Link></li>
              <li><Link href="/pricing" className="text-emerald-400 hover:underline">Pricing</Link></li>
              <li><Link href="/security" className="text-emerald-400 hover:underline">Security & Compliance</Link></li>
              <li><Link href="/guarantee" className="text-emerald-400 hover:underline">Money-Back Guarantee</Link></li>
            </ul>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
            <h3 className="text-xl font-bold text-white mb-4">Account & Billing</h3>
            <ul className="space-y-3">
              <li><Link href="/my-data" className="text-emerald-400 hover:underline">Request My Data</Link></li>
              <li><Link href="/cancellation" className="text-emerald-400 hover:underline">Cancellation Policy</Link></li>
              <li><Link href="/refunds" className="text-emerald-400 hover:underline">Refunds</Link></li>
              <li><Link href="/disputes" className="text-emerald-400 hover:underline">Disputes</Link></li>
              <li><Link href="/emergency-contacts" className="text-emerald-400 hover:underline">Emergency Contacts</Link></li>
            </ul>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Can't find what you need?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Our team is standing by to help with any questions or issues.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="mailto:support@levqor.ai" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
            >
              Email Support
            </a>
            <Link 
              href="/contact" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all"
            >
              Contact Form
            </Link>
          </div>
        </div>
      </div>
    </PublicPageLayout>
  );
}
