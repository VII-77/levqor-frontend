import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Our Team - Meet the Levqor Studio",
  description: "Meet the team behind Levqor: automation experts, developers, and strategists dedicated to helping you ship faster.",
};

export default function TeamPage() {
  const team = [
    {
      name: "Levqor Studio",
      role: "Automation Experts & Developers",
      bio: "Our distributed team of automation specialists, full-stack developers, and business strategists work together to deliver world-class DFY automation solutions.",
      avatar: "LS"
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Our Team
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Meet the team behind<br />your automation success
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            A lean, focused team of automation experts dedicated to building workflows that actually work.
          </p>
        </div>

        {/* Team Members */}
        <div className="grid md:grid-cols-1 gap-8 max-w-2xl mx-auto mb-16">
          {team.map((member, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-8 text-center">
              <div className="w-24 h-24 bg-emerald-500/10 border-2 border-emerald-500/30 rounded-full flex items-center justify-center text-3xl font-bold text-emerald-400 mx-auto mb-6">
                {member.avatar}
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">{member.name}</h3>
              <p className="text-emerald-400 mb-4">{member.role}</p>
              <p className="text-slate-300 text-lg">{member.bio}</p>
            </div>
          ))}
        </div>

        {/* What We Bring */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8 text-white text-center">What We Bring to Your Business</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">Strategic Thinking</h3>
              <p className="text-slate-300">
                We don't just build workflows—we design automation strategies that align with your business goals and scale with your growth.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">Technical Excellence</h3>
              <p className="text-slate-300">
                Full-stack developers and automation engineers with years of experience in API integrations, webhooks, and complex workflow design.
              </p>
            </div>

            <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center mb-4">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold mb-3 text-white">White-Glove Service</h3>
              <p className="text-slate-300">
                Real people, fast communication, and hands-on support. We treat your business like our own because your success is our success.
              </p>
            </div>
          </div>
        </section>

        {/* Our Values */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8 text-white text-center">Our Values</h2>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-bold mb-3 text-emerald-400">No BS, Just Results</h3>
                <p className="text-slate-300">
                  We don't oversell, overpromise, or overcharge. Clear pricing, honest timelines, and working automation delivered on time.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-3 text-emerald-400">Security & Privacy First</h3>
                <p className="text-slate-300">
                  GDPR-compliant, EU-based infrastructure, transparent data handling, and zero tolerance for high-risk automation.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-3 text-emerald-400">Long-Term Partnerships</h3>
                <p className="text-slate-300">
                  We're not here for quick wins. We build relationships with clients and support them as they grow.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-bold mb-3 text-emerald-400">Continuous Improvement</h3>
                <p className="text-slate-300">
                  We're constantly learning, improving our processes, and finding better ways to deliver automation that scales.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Join Us CTA */}
        <section className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Let's work together</h2>
          <p className="text-lg text-slate-300 mb-8 max-w-2xl mx-auto">
            Ready to automate your busywork and reclaim 20+ hours per week? Our team is standing by.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/pricing" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
            >
              Get Started
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
