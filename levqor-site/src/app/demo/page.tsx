import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Demo - Watch Levqor in Action",
  description: "Watch a demo of Levqor's DFY automation platform and see how we deliver working workflows in days.",
};

export default function DemoPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-5xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Demo
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Watch Levqor in action
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            See how we deliver done-for-you automation from intake to live workflows.
          </p>
        </div>

        {/* Video Placeholder */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-12 mb-12">
          <div className="aspect-video bg-slate-950 rounded-lg flex items-center justify-center border border-slate-700">
            <div className="text-center">
              <svg className="w-24 h-24 text-emerald-400 mx-auto mb-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-slate-400 text-lg">Video demo coming soon</p>
              <p className="text-sm text-slate-500 mt-2">In the meantime, book a call for a live walkthrough</p>
            </div>
          </div>
        </div>

        {/* What You'll See */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">What the demo covers:</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              "How to submit a DFY automation request",
              "The intake and strategy consultation process",
              "Workflow design and approval",
              "Testing and delivery timeline",
              "Dashboard monitoring and alerts",
              "Ongoing support and revisions"
            ].map((item, idx) => (
              <div key={idx} className="flex items-start gap-3 bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                <svg className="w-6 h-6 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                <span className="text-slate-200">{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Want a personalized demo?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Book a call with our team and we'll walk you through exactly how Levqor can automate your workflow.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/contact" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
            >
              Book a Call
            </Link>
            <Link 
              href="/pricing" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 border border-slate-700 text-slate-100 hover:border-emerald-400/60 hover:bg-slate-900/60 rounded-lg font-semibold transition-all"
            >
              View Pricing
            </Link>
          </div>
        </div>
      </div>
    </PublicPageLayout>
  );
}
