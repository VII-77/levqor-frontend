import PublicPageLayout from "@/components/PublicPageLayout";

export const metadata = {
  title: "Roadmap - What's Coming to Levqor",
  description: "See what's coming next to Levqor: upcoming features, improvements, and releases.",
};

export default function RoadmapPage() {
  const roadmap = [
    {
      phase: "Now (Q4 2025)",
      features: [
        "Genesis v8.0 multi-tenancy live",
        "Support AI widget with escalation",
        "Enhanced DFY delivery workflows",
        "Compliance dashboard improvements"
      ]
    },
    {
      phase: "Next (Q1 2026)",
      features: [
        "Self-service workflow builder (beta)",
        "Advanced analytics & reporting",
        "Team collaboration features",
        "API access for enterprise clients",
        "Mobile app for monitoring"
      ]
    },
    {
      phase: "Later (Q2 2026+)",
      features: [
        "AI workflow suggestions",
        "Marketplace for pre-built templates",
        "White-label options for agencies",
        "Advanced scheduling & triggers",
        "Multi-language support"
      ]
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Roadmap
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            What's coming to Levqor
          </h1>
          <p className="text-xl text-slate-400">
            Our product roadmap: upcoming features, improvements, and releases.
          </p>
        </div>

        <div className="space-y-12">
          {roadmap.map((phase, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-xl p-8">
              <h2 className="text-2xl font-bold text-white mb-6">{phase.phase}</h2>
              <ul className="space-y-3">
                {phase.features.map((f, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-slate-200">{f}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-16 bg-emerald-500/10 border border-emerald-500/30 rounded-lg p-8 text-center">
          <p className="text-slate-300">
            <strong className="text-white">Have a feature request?</strong> We'd love to hear from you. Email us at <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>
          </p>
        </div>
      </div>
    </PublicPageLayout>
  );
}
