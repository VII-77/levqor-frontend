import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Automation for Agencies",
  description: "DFY automation for agencies: client onboarding, reporting, invoicing, and project management.",
};

export default function AgenciesSolutionPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation for Agencies
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Streamline client work with automated onboarding, reporting, invoicing, and project workflows.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {[
            { title: "Client Onboarding", desc: "Automatically send welcome emails, contracts, intake forms, and project kickoff docs." },
            { title: "Weekly Reporting", desc: "Generate and deliver weekly performance reports to clients automatically." },
            { title: "Invoice Reminders", desc: "Auto-send payment reminders, track overdue invoices, and follow up with clients." },
            { title: "Project Status Updates", desc: "Keep clients informed with automated project milestone and progress updates." },
            { title: "Lead Intake & CRM Sync", desc: "Capture leads from forms, sync to CRM, and trigger follow-up sequences." },
            { title: "Team Task Assignments", desc: "Automatically assign tasks to team members based on project type and workload." }
          ].map((item, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-3">{item.title}</h3>
              <p className="text-slate-300">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Save 20+ hours per week on client work</h2>
          <p className="text-lg text-slate-300 mb-8">
            Let Levqor handle the repetitive tasks so you can focus on delivering great work.
          </p>
          <Link href="/pricing" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg">
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
