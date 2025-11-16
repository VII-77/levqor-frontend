import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Before & After - Life with Levqor Automation",
  description: "See the transformation: from manual chaos to automated efficiency with Levqor's DFY automation.",
};

export default function TransformationPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Life Before vs After Levqor
          </h1>
          <p className="text-xl text-slate-400">
            See the transformation from manual busywork to automated efficiency.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Before */}
          <div className="bg-red-500/5 border border-red-500/30 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-red-400 mb-6 flex items-center gap-3">
              <span className="text-3xl">❌</span>
              Before Levqor
            </h2>
            <ul className="space-y-4">
              {[
                "15+ hours/week on repetitive manual tasks",
                "Constant context switching between tools",
                "Missed follow-ups and delayed responses",
                "Late-night work to catch up on admin",
                "Errors from manual data entry",
                "No time to focus on growth",
                "Overwhelmed and stressed"
              ].map((item, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <span className="text-red-400 mt-1">✗</span>
                  <span className="text-slate-300">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* After */}
          <div className="bg-emerald-500/5 border border-emerald-500/30 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-emerald-400 mb-6 flex items-center gap-3">
              <span className="text-3xl">✅</span>
              After Levqor
            </h2>
            <ul className="space-y-4">
              {[
                "20+ hours saved every week",
                "Workflows run automatically in the background",
                "Zero missed follow-ups",
                "Evenings and weekends free again",
                "Automated accuracy, zero errors",
                "Time to focus on strategy and growth",
                "Calm, confident, in control"
              ].map((item, idx) => (
                <li key={idx} className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span className="text-slate-200 font-medium">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-16 text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready for your transformation?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Join hundreds of founders who've automated their busywork and reclaimed their time.
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
