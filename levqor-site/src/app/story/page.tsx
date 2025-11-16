import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Our Story - Why Levqor Exists",
  description: "The story behind Levqor: from manual chaos to automated efficiency. Learn why we built a done-for-you automation platform for busy founders.",
};

export default function StoryPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-4xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Our Story
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            From manual chaos<br />to automated efficiency
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Every great product starts with a problem. Here's ours.
          </p>
        </div>

        {/* Story Content */}
        <div className="prose prose-invert max-w-none space-y-12">
          {/* The Problem */}
          <section>
            <h2 className="text-3xl font-bold mb-6 text-white">The Problem: Drowning in Manual Work</h2>
            <p className="text-lg text-slate-300 mb-4">
              In 2023, we were running a small digital agency. Every week looked the same: client onboarding emails, invoice reminders, status updates, data syncing between tools, report generation... the list went on.
            </p>
            <p className="text-lg text-slate-300 mb-4">
              We knew automation existed. We tried Zapier, Make.com, n8n. But each tool came with the same problems:
            </p>
            <ul className="space-y-2 text-slate-300">
              <li className="flex items-start gap-3">
                <span className="text-red-400 mt-1">✗</span>
                <span>Weeks of learning curve before you could build anything useful</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-red-400 mt-1">✗</span>
                <span>Constant maintenance when APIs changed or workflows broke</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-red-400 mt-1">✗</span>
                <span>No strategy guidance—just tools dumped in your lap</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-red-400 mt-1">✗</span>
                <span>Hours wasted debugging instead of building our business</span>
              </li>
            </ul>
            <p className="text-lg text-slate-300 mt-4">
              We spent more time maintaining automation than we saved using it. That's when the "aha moment" hit.
            </p>
          </section>

          {/* The Insight */}
          <section className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
            <h2 className="text-3xl font-bold mb-6 text-white">The Insight: What If Someone Just Did It For You?</h2>
            <p className="text-lg text-slate-300 mb-4">
              We didn't need another automation tool. We needed someone to:
            </p>
            <ul className="space-y-2 text-slate-300 mb-4">
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Understand our workflow and identify what to automate</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Build it for us, professionally and securely</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Deliver it working, tested, and ready to use</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-emerald-400 mt-1">✓</span>
                <span>Handle maintenance and updates so we could focus on clients</span>
              </li>
            </ul>
            <p className="text-lg text-slate-300">
              That's when Levqor was born. Not as a tool, but as a <strong className="text-white">service</strong>.
            </p>
          </section>

          {/* Building Levqor */}
          <section>
            <h2 className="text-3xl font-bold mb-6 text-white">Building Levqor: Strategy First, Tools Second</h2>
            <p className="text-lg text-slate-300 mb-4">
              We started with a simple premise: <em>what if we combined white-glove service with automation platform power?</em>
            </p>
            <p className="text-lg text-slate-300 mb-4">
              Instead of giving clients a tool and saying "figure it out," we:
            </p>
            <div className="grid md:grid-cols-2 gap-6 my-8">
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-emerald-400 mb-2">1</div>
                <h3 className="text-xl font-bold mb-3 text-white">Listen & Strategize</h3>
                <p className="text-slate-300">
                  We learn about your business, identify bottlenecks, and design a custom automation strategy.
                </p>
              </div>
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-emerald-400 mb-2">2</div>
                <h3 className="text-xl font-bold mb-3 text-white">Build & Test</h3>
                <p className="text-slate-300">
                  Our team builds your workflows, tests them thoroughly, and makes sure everything works before delivery.
                </p>
              </div>
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-emerald-400 mb-2">3</div>
                <h3 className="text-xl font-bold mb-3 text-white">Deliver & Support</h3>
                <p className="text-slate-300">
                  We hand over working automation, train your team, and provide ongoing support as you scale.
                </p>
              </div>
              <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                <div className="text-3xl font-bold text-emerald-400 mb-2">4</div>
                <h3 className="text-xl font-bold mb-3 text-white">Maintain & Improve</h3>
                <p className="text-slate-300">
                  We monitor, maintain, and continuously improve your workflows so you never have to worry about them breaking.
                </p>
              </div>
            </div>
          </section>

          {/* Today */}
          <section>
            <h2 className="text-3xl font-bold mb-6 text-white">Today: Helping Hundreds Save 20+ Hours Per Week</h2>
            <p className="text-lg text-slate-300 mb-4">
              Since launch, we've helped agencies, coaches, eCommerce founders, and small businesses reclaim thousands of hours through automation.
            </p>
            <p className="text-lg text-slate-300 mb-4">
              Our clients don't spend weekends learning Zapier. They don't debug broken workflows at 2 AM. They don't wonder if automation is "worth it."
            </p>
            <p className="text-lg text-slate-300 mb-4">
              They just <strong className="text-white">use it</strong>—because we built it for them.
            </p>
          </section>

          {/* Vision */}
          <section className="bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-8">
            <h2 className="text-3xl font-bold mb-6 text-white">Our Vision: Automation for Everyone</h2>
            <p className="text-lg text-slate-300 mb-4">
              We believe automation should be accessible to every business—not just enterprises with dedicated dev teams.
            </p>
            <p className="text-lg text-slate-300 mb-4">
              Whether you're a solo founder juggling client work, an agency scaling operations, or a small team drowning in repetitive tasks, you deserve automation that <em>just works</em>.
            </p>
            <p className="text-lg text-white font-semibold">
              That's what Levqor is here to deliver.
            </p>
          </section>
        </div>

        {/* CTA */}
        <div className="text-center mt-16">
          <h2 className="text-2xl font-bold mb-4 text-white">Ready to reclaim your time?</h2>
          <p className="text-slate-300 mb-8">
            Join the founders who've automated their busywork and focused on what actually grows their business.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/pricing" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
            >
              Get Started
            </Link>
            <Link 
              href="/case-studies" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all"
            >
              Read Case Studies
            </Link>
          </div>
        </div>
      </div>
    </PublicPageLayout>
  );
}
