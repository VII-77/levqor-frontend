import PublicPageLayout from "@/components/PublicPageLayout";

export const metadata = {
  title: "Screenshots - See Levqor's Dashboard & Features",
  description: "Explore Levqor's dashboard, workflow monitoring, and automation features through screenshots.",
};

export default function ScreenshotsPage() {
  const screenshots = [
    { title: "Dashboard Overview", desc: "Monitor all workflows at a glance" },
    { title: "Workflow Status", desc: "Real-time health monitoring" },
    { title: "DFY Intake Form", desc: "Submit automation requests easily" },
    { title: "Delivery Timeline", desc: "Track project progress" },
    { title: "Analytics & Reports", desc: "See time saved and ROI" },
    { title: "Settings & Config", desc: "Manage integrations and preferences" }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Screenshots
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            See Levqor in action
          </h1>
          <p className="text-xl text-slate-400">
            Explore our dashboard, monitoring tools, and automation features.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {screenshots.map((s, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-xl overflow-hidden">
              <div className="aspect-video bg-slate-950 flex items-center justify-center border-b border-slate-800">
                <div className="text-center p-8">
                  <svg className="w-16 h-16 text-emerald-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <p className="text-slate-400 text-sm">Screenshot placeholder</p>
                </div>
              </div>
              <div className="p-6">
                <h3 className="text-lg font-bold text-white mb-2">{s.title}</h3>
                <p className="text-slate-400 text-sm">{s.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </PublicPageLayout>
  );
}
