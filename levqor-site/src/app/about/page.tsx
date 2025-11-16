import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "About Levqor - DFY Automation Platform",
  description: "Learn about Levqor's mission to make professional automation accessible to everyone through done-for-you setups and AI-powered workflows.",
};

export default function AboutPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            About Levqor
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            We build DFY automation<br />so you can focus on growth
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Levqor is a done-for-you automation platform that combines white-glove service with AI-powered workflows to help busy founders and teams ship faster.
          </p>
        </div>

        {/* Mission Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-6 text-white">Our Mission</h2>
          <div className="prose prose-invert max-w-none">
            <p className="text-lg text-slate-300 mb-4">
              Most automation tools require weeks of learning, countless hours of setup, and constant maintenance. We believe there's a better way.
            </p>
            <p className="text-lg text-slate-300 mb-4">
              Levqor exists to make professional-grade automation accessible to everyone—without the technical complexity, without the time investment, and without the headaches.
            </p>
            <p className="text-lg text-slate-300">
              We handle the strategy, design, and implementation. You get working automations that save you 20+ hours per week, delivered in days, not months.
            </p>
          </div>
        </section>

        {/* What We Do */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8 text-white">What We Do</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">DFY Automation Builds</h3>
              <p className="text-slate-300">
                One-time projects where we design, build, and deliver complete automation workflows tailored to your business. Fixed pricing, fast delivery.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">Subscription Plans</h3>
              <p className="text-slate-300">
                Ongoing automation support with monthly workflows, monitoring, maintenance, and unlimited updates to keep your systems running smoothly.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">Security & Compliance</h3>
              <p className="text-slate-300">
                GDPR-compliant, secure data handling, EU-based infrastructure, and transparent policies. Your data stays private and protected.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">White-Glove Support</h3>
              <p className="text-slate-300">
                Real humans, fast response times, and hands-on guidance. We're here to help you succeed every step of the way.
              </p>
            </div>
          </div>
        </section>

        {/* Our Approach */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-6 text-white">Our Approach</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <div className="w-6 h-6 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <strong className="text-white">Strategy first:</strong>
                  <span className="text-slate-300"> We start by understanding your workflow, identifying bottlenecks, and designing the right solution.</span>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-6 h-6 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <strong className="text-white">Built for you:</strong>
                  <span className="text-slate-300"> Custom workflows tailored to your unique business needs, not one-size-fits-all templates.</span>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-6 h-6 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <strong className="text-white">Delivered fast:</strong>
                  <span className="text-slate-300"> Most DFY projects go live within 3-7 days, not weeks or months.</span>
                </div>
              </li>
              <li className="flex items-start gap-3">
                <div className="w-6 h-6 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <svg className="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <strong className="text-white">Ongoing support:</strong>
                  <span className="text-slate-300"> We don't disappear after delivery. Revisions, updates, and technical support included.</span>
                </div>
              </li>
            </ul>
          </div>
        </section>

        {/* CTA Section */}
        <section className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to automate your business?</h2>
          <p className="text-lg text-slate-300 mb-8 max-w-2xl mx-auto">
            Join hundreds of founders who've reclaimed their time with Levqor's DFY automation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/pricing" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl"
            >
              View Pricing
            </Link>
            <Link 
              href="/contact" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all"
            >
              Contact Us
            </Link>
          </div>
        </section>
      </div>
    </PublicPageLayout>
  );
}
