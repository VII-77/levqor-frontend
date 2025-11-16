import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Product Tour - Explore Levqor's Features",
  description: "Take a guided tour of Levqor's dashboard, DFY delivery flow, monitoring, and automation features.",
};

export default function TourPage() {
  const features = [
    {
      title: "Dashboard Overview",
      desc: "Monitor all your workflows, view health status, and track automation performance from one central dashboard.",
      icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
    },
    {
      title: "DFY Intake Process",
      desc: "Submit your automation request via our simple intake form. We'll gather all necessary details to build your custom workflows.",
      icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
    },
    {
      title: "Delivery Timeline",
      desc: "Track your DFY project from intake to delivery. See design reviews, build progress, and testing milestones in real-time.",
      icon: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
    },
    {
      title: "Workflow Monitoring",
      desc: "Real-time health checks, error alerts, and performance metrics for all your automation workflows.",
      icon: "M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Product Tour
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Explore Levqor's features
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            A guided tour of how Levqor delivers done-for-you automation.
          </p>
        </div>

        <div className="space-y-16">
          {features.map((f, idx) => (
            <div key={idx} className="grid md:grid-cols-2 gap-12 items-center">
              <div className={idx % 2 === 1 ? "md:order-2" : ""}>
                <h2 className="text-3xl font-bold text-white mb-4">{f.title}</h2>
                <p className="text-lg text-slate-300">{f.desc}</p>
              </div>
              <div className={idx % 2 === 1 ? "md:order-1" : ""}>
                <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-12 flex items-center justify-center">
                  <svg className="w-24 h-24 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={f.icon} />
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to see it in action?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Get started with Levqor and experience professional automation delivered in days.
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
