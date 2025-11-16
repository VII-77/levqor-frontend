import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Use Cases - Automation Examples by Industry",
  description: "Discover automation use cases for agencies, coaches, eCommerce, creators, and small businesses.",
};

export default function UseCasesPage() {
  const useCases = [
    {
      industry: "Agencies",
      icon: "M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z",
      examples: [
        "Automated client onboarding workflows",
        "Weekly report generation and delivery",
        "Invoice reminders and payment tracking",
        "Project status updates to clients",
        "Lead intake and CRM sync"
      ]
    },
    {
      industry: "Coaches",
      icon: "M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253",
      examples: [
        "Booking and scheduling automation",
        "Payment collection via Stripe",
        "Automated email sequences for clients",
        "Resource delivery after purchase",
        "Session reminder notifications"
      ]
    },
    {
      industry: "eCommerce",
      icon: "M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z",
      examples: [
        "Order fulfillment workflows",
        "Inventory sync across platforms",
        "Abandoned cart recovery emails",
        "Customer support ticket routing",
        "Review request automation"
      ]
    },
    {
      industry: "Creators",
      icon: "M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z",
      examples: [
        "Content publishing automation",
        "Subscriber welcome sequences",
        "Membership site access management",
        "Sponsorship tracking and invoicing",
        "Social media cross-posting"
      ]
    },
    {
      industry: "Small Business",
      icon: "M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4",
      examples: [
        "Lead capture and follow-up",
        "Appointment reminders",
        "Customer feedback collection",
        "Receipt and invoice generation",
        "Team task assignments"
      ]
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Use Cases
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation for every industry
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            See what's possible with Levqor's DFY automation across different business types.
          </p>
        </div>

        <div className="space-y-8">
          {useCases.map((uc, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-xl p-8">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 bg-emerald-500/10 border border-emerald-500/30 rounded-lg flex items-center justify-center flex-shrink-0">
                  <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={uc.icon} />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-white">{uc.industry}</h2>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {uc.examples.map((ex, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <svg className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span className="text-slate-300">{ex}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Don't see your use case?</h2>
          <p className="text-lg text-slate-300 mb-8">
            We build custom automation for any workflow. Let's talk about your specific needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/contact" 
              className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
            >
              Contact Us
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
