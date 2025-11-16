import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "How It Works - Levqor DFY Automation Process",
  description: "See how Levqor delivers done-for-you automation: from strategy consultation to live workflows in 3-7 days.",
};

export default function HowItWorksPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            How It Works
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            From idea to live automation<br />in 4 simple steps
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            No technical skills needed. No weeks of setup. Just working automation delivered fast, anywhere in the world.
          </p>
        </div>

        {/* Steps */}
        <div className="space-y-16 mb-20">
          {/* Step 1 */}
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-emerald-500/10 border-2 border-emerald-500/30 rounded-full flex items-center justify-center text-xl font-bold text-emerald-400">
                  1
                </div>
                <h2 className="text-3xl font-bold text-white">Pick Your Plan</h2>
              </div>
              <p className="text-lg text-slate-300 mb-6">
                Choose between one-time DFY builds or ongoing subscription automation. Not sure? Book a call and we'll recommend the best option for your business.
              </p>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-slate-300">Fixed pricing—no hidden fees or surprise charges</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-slate-300">Starter, Professional, or Enterprise tiers</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-slate-300">14-day money-back guarantee on all plans</span>
                </li>
              </ul>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
              <div className="bg-slate-950 border border-slate-700 rounded-lg p-6 mb-4">
                <div className="text-sm text-emerald-400 font-semibold mb-2">MOST POPULAR</div>
                <div className="text-2xl font-bold text-white mb-2">Professional DFY</div>
                <div className="text-3xl font-bold text-white mb-4">£299 <span className="text-lg text-slate-400 font-normal">one-time</span></div>
                <div className="text-slate-300">3 workflows • 7-day delivery</div>
              </div>
              <div className="text-sm text-center text-slate-400">
                <Link href="/pricing" className="text-emerald-400 hover:underline">View all pricing →</Link>
              </div>
            </div>
          </div>

          {/* Step 2 */}
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="order-2 md:order-1 bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
              <h3 className="text-xl font-bold text-white mb-4">What we'll ask about:</h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="text-slate-300">Current workflow and pain points</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="text-slate-300">Tools you currently use (Stripe, Gmail, etc.)</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="text-slate-300">Goals and priorities (save time, reduce errors, etc.)</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span className="text-slate-300">Access credentials (API keys, OAuth, etc.)</span>
                </li>
              </ul>
            </div>
            <div className="order-1 md:order-2">
              <div className="inline-flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-emerald-500/10 border-2 border-emerald-500/30 rounded-full flex items-center justify-center text-xl font-bold text-emerald-400">
                  2
                </div>
                <h2 className="text-3xl font-bold text-white">Tell Us About Your Workflow</h2>
              </div>
              <p className="text-lg text-slate-300 mb-6">
                After purchase, you'll fill out a simple intake form or schedule a quick call. We'll ask about your current process, tools, and what you want to automate.
              </p>
              <p className="text-slate-400 text-sm bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                <strong className="text-white">Tip:</strong> The more detail you provide, the better we can tailor the automation to your exact needs.
              </p>
            </div>
          </div>

          {/* Step 3 */}
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-emerald-500/10 border-2 border-emerald-500/30 rounded-full flex items-center justify-center text-xl font-bold text-emerald-400">
                  3
                </div>
                <h2 className="text-3xl font-bold text-white">We Build, Test & Deliver</h2>
              </div>
              <p className="text-lg text-slate-300 mb-6">
                Our team designs your workflows, builds them securely, tests everything thoroughly, and delivers working automation within 3-7 days.
              </p>
              <div className="space-y-4">
                <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                  <div className="font-semibold text-white mb-2">Day 1-2: Design & Strategy</div>
                  <p className="text-sm text-slate-300">We map out your automation workflow and confirm the approach with you.</p>
                </div>
                <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                  <div className="font-semibold text-white mb-2">Day 3-5: Build & Test</div>
                  <p className="text-sm text-slate-300">We build the workflows, integrate your tools, and test everything end-to-end.</p>
                </div>
                <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                  <div className="font-semibold text-white mb-2">Day 6-7: Delivery & Training</div>
                  <p className="text-sm text-slate-300">We hand over the working automation and show you how to use/monitor it.</p>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-8">
              <h3 className="text-xl font-bold text-white mb-4">What you get:</h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-white">Fully functional, tested workflows</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-white">Documentation and setup guide</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-white">Access to monitoring dashboard</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-white">Training on how to use and maintain</span>
                </li>
              </ul>
            </div>
          </div>

          {/* Step 4 */}
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="order-2 md:order-1 bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
              <h3 className="text-xl font-bold text-white mb-6">Ongoing support includes:</h3>
              <div className="space-y-4">
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">1 Revision Round</div>
                    <p className="text-sm text-slate-300">Included with every DFY plan</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Email Support</div>
                    <p className="text-sm text-slate-300">24-48 hour response time</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <svg className="w-6 h-6 text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <div className="font-semibold text-white">Monitoring & Alerts</div>
                    <p className="text-sm text-slate-300">We watch for failures and notify you</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="order-1 md:order-2">
              <div className="inline-flex items-center gap-3 mb-4">
                <div className="w-12 h-12 bg-emerald-500/10 border-2 border-emerald-500/30 rounded-full flex items-center justify-center text-xl font-bold text-emerald-400">
                  4
                </div>
                <h2 className="text-3xl font-bold text-white">You Ship. We Support.</h2>
              </div>
              <p className="text-lg text-slate-300 mb-6">
                Once automation is live, we provide ongoing support, revisions, and monitoring. Focus on growing your business while we handle the technical details.
              </p>
              <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-4">
                <p className="text-emerald-200 font-semibold mb-2">Want ongoing automation?</p>
                <p className="text-sm text-slate-300 mb-4">
                  Upgrade to a subscription plan for unlimited workflows, priority support, and continuous optimization.
                </p>
                <Link href="/pricing" className="text-emerald-400 hover:underline text-sm font-semibold">
                  View subscription plans →
                </Link>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <section className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to automate your busywork?</h2>
          <p className="text-lg text-slate-300 mb-8 max-w-2xl mx-auto">
            Join hundreds of founders who've saved 20+ hours per week with Levqor's DFY automation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/pricing" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
            >
              View Pricing
            </Link>
            <Link 
              href="/contact" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all"
            >
              Book a Call
            </Link>
          </div>
        </section>
      </div>
    </PublicPageLayout>
  );
}
