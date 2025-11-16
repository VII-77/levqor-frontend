import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Integrations - Connect Your Favorite Tools",
  description: "Levqor integrates with Stripe, Gmail, Notion, Google Drive, Telegram, and 100+ other tools.",
};

export default function IntegrationsPage() {
  const integrations = [
    { name: "Stripe", category: "Payments", desc: "Process payments, manage subscriptions" },
    { name: "Gmail", category: "Email", desc: "Send emails, manage inbox automation" },
    { name: "Google Drive", category: "Storage", desc: "Upload files, organize documents" },
    { name: "Notion", category: "Productivity", desc: "Create databases, update pages" },
    { name: "Telegram", category: "Messaging", desc: "Send notifications, bot commands" },
    { name: "Airtable", category: "Databases", desc: "Update records, create views" },
    { name: "Slack", category: "Team Chat", desc: "Post messages, manage channels" },
    { name: "Shopify", category: "E-Commerce", desc: "Sync orders, update inventory" },
    { name: "Make.com", category: "Automation", desc: "Trigger workflows, pass data" },
    { name: "Zapier", category: "Automation", desc: "Connect apps, automate tasks" },
    { name: "Calendly", category: "Scheduling", desc: "Book meetings, sync calendars" },
    { name: "HubSpot", category: "CRM", desc: "Manage contacts, track deals" }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Integrations
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Connect your favorite tools
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Levqor integrates with 100+ tools to automate your entire workflow.
          </p>
        </div>

        <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6 mb-16">
          {integrations.map((int, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6 hover:border-emerald-400/50 transition">
              <div className="text-sm font-semibold text-emerald-400 mb-2">{int.category}</div>
              <h3 className="text-lg font-bold text-white mb-2">{int.name}</h3>
              <p className="text-sm text-slate-400">{int.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-2xl font-bold mb-4 text-white">Need a custom integration?</h2>
          <p className="text-slate-300 mb-8">We can connect any tool with a public API.</p>
          <Link href="/contact" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg">
            Contact Us
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
