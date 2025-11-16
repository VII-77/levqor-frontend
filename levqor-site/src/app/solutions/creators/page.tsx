import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Automation for Creators",
  description: "DFY automation for content creators: publishing, subscriber management, sponsorships, and analytics.",
};

export default function CreatorsSolutionPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation for Creators
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Automate content publishing, subscriber workflows, sponsorship tracking, and analytics so you can focus on creating.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {[
            { title: "Content Publishing", desc: "Auto-publish content across YouTube, Twitter, LinkedIn, and newsletters on schedule." },
            { title: "Subscriber Welcome Sequences", desc: "Automatically welcome new subscribers with personalized email sequences." },
            { title: "Membership Access Management", desc: "Grant and revoke membership site access based on payment status." },
            { title: "Sponsorship Tracking", desc: "Track sponsorship deliverables, send invoices, and automate reporting to sponsors." },
            { title: "Social Media Cross-Posting", desc: "Automatically share new content across all your social media platforms." },
            { title: "Analytics Aggregation", desc: "Compile analytics from all platforms into one automated weekly report." }
          ].map((item, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-3">{item.title}</h3>
              <p className="text-slate-300">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Create more, automate the rest</h2>
          <p className="text-lg text-slate-300 mb-8">
            Let Levqor handle distribution and admin so you can focus on what you do best: creating.
          </p>
          <Link href="/pricing" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg">
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
