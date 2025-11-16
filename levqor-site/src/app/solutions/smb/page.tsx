import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Automation for Small Businesses",
  description: "DFY automation for small businesses: lead capture, appointment reminders, invoicing, and team coordination.",
};

export default function SMBSolutionPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation for Small Businesses
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Automate lead follow-ups, appointments, invoicing, and team tasks to run your business more efficiently.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {[
            { title: "Lead Capture & Follow-Up", desc: "Automatically capture leads from your website and send personalized follow-up sequences." },
            { title: "Appointment Reminders", desc: "Send automated reminders to clients 24 hours and 1 hour before appointments." },
            { title: "Customer Feedback Collection", desc: "Auto-send feedback surveys after service delivery to improve your offerings." },
            { title: "Receipt & Invoice Generation", desc: "Automatically generate and send receipts and invoices after each transaction." },
            { title: "Team Task Assignments", desc: "Assign tasks to team members automatically based on project type and availability." },
            { title: "Customer Re-Engagement", desc: "Automatically re-engage inactive customers with win-back email sequences." }
          ].map((item, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-3">{item.title}</h3>
              <p className="text-slate-300">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Run your business smarter, not harder</h2>
          <p className="text-lg text-slate-300 mb-8">
            Levqor automates the repetitive tasks so you can focus on growth and customer service.
          </p>
          <Link href="/pricing" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg">
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
