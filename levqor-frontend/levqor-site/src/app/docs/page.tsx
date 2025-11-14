import Link from "next/link";

export default function DocsPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-5xl font-bold text-white mb-8">Documentation</h1>
        
        <div className="space-y-12">
          <section>
            <h2 className="text-3xl font-bold text-white mb-4">Getting Started</h2>
            <p className="text-slate-300 mb-6 leading-relaxed">
              Welcome to Levqor! Our done-for-you automation platform helps you automate work and ship faster. 
              We build, configure, and monitor your workflows so you can focus on your business.
            </p>
            
            <h3 className="text-2xl font-bold text-white mt-8 mb-4">How It Works</h3>
            <ol className="list-decimal list-inside space-y-3 text-slate-300">
              <li className="leading-relaxed"><strong className="text-white">Choose your package:</strong> Starter (£99), Professional (£249), or Enterprise (£599).</li>
              <li className="leading-relaxed"><strong className="text-white">Kickoff call:</strong> We discuss your workflow requirements and integrations.</li>
              <li className="leading-relaxed"><strong className="text-white">We build it:</strong> Our engineers design and test your automation.</li>
              <li className="leading-relaxed"><strong className="text-white">Delivered in 48 hours:</strong> Your workflows are live and monitored.</li>
              <li className="leading-relaxed"><strong className="text-white">Ongoing support:</strong> 7-30 days of support depending on your package.</li>
            </ol>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-white mb-4">What We Can Automate</h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-2">Data Sync</h3>
                <p className="text-sm text-slate-300">
                  Keep Sheets, CRMs, and databases in sync automatically.
                </p>
              </div>
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-2">Email Automation</h3>
                <p className="text-sm text-slate-300">
                  Send notifications, alerts, and reports on schedule or trigger.
                </p>
              </div>
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-2">Webhooks & APIs</h3>
                <p className="text-sm text-slate-300">
                  Connect third-party tools and custom APIs seamlessly.
                </p>
              </div>
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <h3 className="text-lg font-bold text-white mb-2">Self-Healing</h3>
                <p className="text-sm text-slate-300">
                  Detect failures, retry, rollback, or route to backups automatically.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-white mb-4">API Reference</h2>
            <p className="text-slate-300 mb-6 leading-relaxed">
              For advanced users and developers, Levqor provides a REST API to integrate automation into your applications.
            </p>
            
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 mb-6">
              <h4 className="font-mono text-sm font-bold text-white mb-2">Base URL</h4>
              <code className="text-emerald-400 bg-slate-950 px-3 py-1 rounded">https://api.levqor.ai/api</code>
            </div>

            <h3 className="text-2xl font-bold text-white mt-8 mb-4">Authentication</h3>
            <p className="text-slate-300 mb-4 leading-relaxed">
              All API requests require an API key passed in the <code className="bg-slate-800 px-2 py-1 rounded text-emerald-400">X-Api-Key</code> header.
            </p>
            <p className="text-slate-300 mb-4 leading-relaxed">
              Contact <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a> to request API access.
            </p>
          </section>

          <section>
            <h2 className="text-3xl font-bold text-white mb-4">Support</h2>
            <p className="text-slate-300 mb-4 leading-relaxed">
              Need help? Our support team is available via email:
            </p>
            <ul className="space-y-2 text-slate-300">
              <li>
                <strong className="text-white">General support:</strong>{" "}
                <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>
              </li>
              <li>
                <strong className="text-white">Security issues:</strong>{" "}
                <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline">security@levqor.ai</a>
              </li>
            </ul>
          </section>
        </div>

        <div className="mt-16 bg-gradient-to-br from-emerald-500/10 via-slate-900/50 to-blue-500/10 border border-slate-800 rounded-2xl p-8 text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Ready to get started?</h2>
          <p className="text-slate-300 mb-6">
            View our pricing and choose the package that fits your needs.
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
