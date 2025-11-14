import Link from "next/link";

export default function ContactPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">Contact Us</h1>
          <p className="text-xl text-slate-400">
            We're here to help. Reach out to our team.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 hover:border-emerald-400/50 transition-all">
            <h3 className="text-lg font-bold text-white mb-4">Email Support</h3>
            <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline font-medium">
              support@levqor.ai
            </a>
            <p className="text-sm text-slate-400 mt-2">
              General questions, technical support, and billing inquiries.
            </p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 hover:border-emerald-400/50 transition-all">
            <h3 className="text-lg font-bold text-white mb-4">Security</h3>
            <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline font-medium">
              security@levqor.ai
            </a>
            <p className="text-sm text-slate-400 mt-2">
              Report security vulnerabilities or privacy concerns.
            </p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 hover:border-emerald-400/50 transition-all">
            <h3 className="text-lg font-bold text-white mb-4">Documentation</h3>
            <Link href="/docs" className="text-emerald-400 hover:underline font-medium">
              View Documentation
            </Link>
            <p className="text-sm text-slate-400 mt-2">
              API reference, guides, and tutorials.
            </p>
          </div>

          <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 hover:border-emerald-400/50 transition-all">
            <h3 className="text-lg font-bold text-white mb-4">System Status</h3>
            <a href="https://api.levqor.ai/health" target="_blank" rel="noopener noreferrer" className="text-emerald-400 hover:underline font-medium">
              View Status
            </a>
            <p className="text-sm text-slate-400 mt-2">
              Check platform health and uptime.
            </p>
          </div>
        </div>

        <div className="bg-gradient-to-br from-emerald-500/10 via-slate-900/50 to-blue-500/10 border border-slate-800 rounded-2xl p-8 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Ready to automate?</h2>
          <p className="text-slate-300 mb-6">
            Choose your package and we'll have your automation running in 48 hours.
          </p>
          <Link 
            href="/pricing" 
            className="inline-block px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all"
          >
            View Pricing
          </Link>
        </div>
      </div>
    </main>
  );
}
