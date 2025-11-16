import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Automation for Coaches",
  description: "DFY automation for coaches: booking, payments, email sequences, and client delivery.",
};

export default function CoachesSolutionPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation for Coaches
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Automate scheduling, payments, client follow-ups, and resource delivery so you can focus on coaching.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {[
            { title: "Booking & Scheduling", desc: "Sync calendars, send confirmations, and automate session reminders for clients." },
            { title: "Payment Collection", desc: "Automatically collect payments via Stripe, send receipts, and track subscriptions." },
            { title: "Email Sequences", desc: "Nurture leads and clients with automated email sequences tailored to their journey." },
            { title: "Resource Delivery", desc: "Auto-deliver workbooks, videos, and resources after purchase or session completion." },
            { title: "Session Reminders", desc: "Send automated reminders 24 hours and 1 hour before coaching sessions." },
            { title: "Client Check-Ins", desc: "Automatically check in with clients between sessions to maintain engagement." }
          ].map((item, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-3">{item.title}</h3>
              <p className="text-slate-300">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Spend more time coaching, less time on admin</h2>
          <p className="text-lg text-slate-300 mb-8">
            Levqor automates the busywork so you can focus on transforming lives.
          </p>
          <Link href="/pricing" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg">
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
