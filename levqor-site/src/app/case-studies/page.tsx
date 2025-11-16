import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Case Studies - Real Results from Levqor Automation",
  description: "See how businesses save 20+ hours per week with Levqor's DFY automation. Real case studies, real results.",
};

export default function CaseStudiesPage() {
  const cases = [
    {
      company: "Digital Marketing Agency",
      industry: "Marketing Services",
      challenge: "Spending 15+ hours/week on client onboarding, reporting, and invoice follow-ups",
      solution: "Automated client intake, weekly report generation, and payment reminders",
      results: ["18 hours saved per week", "100% on-time invoicing", "Clients receive reports automatically"],
      tier: "Professional DFY"
    },
    {
      company: "E-Commerce Store",
      industry: "Retail",
      challenge: "Manual order processing, inventory updates, and customer support tickets",
      solution: "Order fulfillment automation, inventory sync across platforms, support ticket routing",
      results: ["22 hours saved per week", "Zero inventory errors", "30% faster order processing"],
      tier: "Enterprise DFY"
    },
    {
      company: "Coaching Business",
      industry: "Education",
      challenge: "Manual scheduling, payment collection, and client follow-ups consuming 12+ hours weekly",
      solution: "Automated booking system, Stripe payment flows, email sequences for follow-ups",
      results: ["12 hours saved per week", "95% payment collection rate", "Zero missed follow-ups"],
      tier: "Starter DFY"
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Case Studies
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Real businesses.<br />Real time savings.<br />Real results.
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            See how Levqor's DFY automation has helped founders reclaim 20+ hours per week and focus on growth.
          </p>
        </div>

        {/* Case Studies */}
        <div className="space-y-12 mb-16">
          {cases.map((c, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
              <div className="flex flex-wrap items-center gap-4 mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-white">{c.company}</h2>
                  <p className="text-emerald-400">{c.industry}</p>
                </div>
                <div className="ml-auto">
                  <span className="px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-xs font-semibold text-emerald-200">
                    {c.tier}
                  </span>
                </div>
              </div>

              <div className="grid md:grid-cols-3 gap-8">
                <div>
                  <h3 className="text-sm font-semibold text-slate-400 uppercase mb-2">Challenge</h3>
                  <p className="text-slate-200">{c.challenge}</p>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-slate-400 uppercase mb-2">Solution</h3>
                  <p className="text-slate-200">{c.solution}</p>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-slate-400 uppercase mb-2">Results</h3>
                  <ul className="space-y-2">
                    {c.results.map((r, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span className="text-slate-200">{r}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to write your success story?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Let's automate your busywork and free up 20+ hours per week.
          </p>
          <Link 
            href="/pricing" 
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
          >
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
