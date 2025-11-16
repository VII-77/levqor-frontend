import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Levqor vs Zapier, Make.com, ActivePieces",
  description: "Compare Levqor's DFY automation service with DIY tools like Zapier, Make.com, and ActivePieces.",
};

export default function ComparisonPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Comparison
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Levqor vs DIY Automation Tools
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Why choose done-for-you over do-it-yourself? Here's how we compare.
          </p>
        </div>

        {/* Comparison Table */}
        <div className="overflow-x-auto mb-16">
          <table className="w-full border-collapse">
            <thead>
              <tr className="border-b border-slate-800">
                <th className="text-left p-4 text-white font-semibold">Feature</th>
                <th className="p-4 text-emerald-400 font-semibold bg-emerald-500/5">Levqor</th>
                <th className="p-4 text-slate-400 font-semibold">Zapier</th>
                <th className="p-4 text-slate-400 font-semibold">Make.com</th>
                <th className="p-4 text-slate-400 font-semibold">ActivePieces</th>
              </tr>
            </thead>
            <tbody className="text-slate-300">
              <tr className="border-b border-slate-800/50">
                <td className="p-4 font-semibold text-white">Setup Time</td>
                <td className="p-4 text-center bg-emerald-500/5">
                  <span className="text-emerald-400">3-7 days</span>
                  <div className="text-xs text-slate-400">We build it</div>
                </td>
                <td className="p-4 text-center">Weeks (DIY)</td>
                <td className="p-4 text-center">Weeks (DIY)</td>
                <td className="p-4 text-center">Weeks (DIY)</td>
              </tr>
              <tr className="border-b border-slate-800/50">
                <td className="p-4 font-semibold text-white">Learning Curve</td>
                <td className="p-4 text-center bg-emerald-500/5">
                  <span className="text-emerald-400">✓ None</span>
                </td>
                <td className="p-4 text-center">High</td>
                <td className="p-4 text-center">Very High</td>
                <td className="p-4 text-center">High</td>
              </tr>
              <tr className="border-b border-slate-800/50">
                <td className="p-4 font-semibold text-white">Strategy & Consultation</td>
                <td className="p-4 text-center bg-emerald-500/5">
                  <span className="text-emerald-400">✓ Included</span>
                </td>
                <td className="p-4 text-center">✗</td>
                <td className="p-4 text-center">✗</td>
                <td className="p-4 text-center">✗</td>
              </tr>
              <tr className="border-b border-slate-800/50">
                <td className="p-4 font-semibold text-white">Maintenance</td>
                <td className="p-4 text-center bg-emerald-500/5">
                  <span className="text-emerald-400">✓ We handle it</span>
                </td>
                <td className="p-4 text-center">DIY</td>
                <td className="p-4 text-center">DIY</td>
                <td className="p-4 text-center">DIY</td>
              </tr>
              <tr className="border-b border-slate-800/50">
                <td className="p-4 font-semibold text-white">Human Support</td>
                <td className="p-4 text-center bg-emerald-500/5">
                  <span className="text-emerald-400">✓ 24-48hr</span>
                </td>
                <td className="p-4 text-center">Limited</td>
                <td className="p-4 text-center">Limited</td>
                <td className="p-4 text-center">Community</td>
              </tr>
              <tr className="border-b border-slate-800/50">
                <td className="p-4 font-semibold text-white">Best For</td>
                <td className="p-4 text-center bg-emerald-500/5">
                  <span className="text-emerald-400">Busy founders</span>
                </td>
                <td className="p-4 text-center">Tech-savvy users</td>
                <td className="p-4 text-center">Advanced users</td>
                <td className="p-4 text-center">Developers</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Key Differences */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">Why Choose Levqor?</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">White-Glove Service</h3>
              <p className="text-slate-300">
                We don't just give you tools—we build, test, and deliver working automation tailored to your business.
              </p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">Strategy First</h3>
              <p className="text-slate-300">
                We help you identify what to automate, design optimal workflows, and implement best practices.
              </p>
            </div>
            <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <h3 className="text-xl font-bold text-white mb-3">Zero Maintenance</h3>
              <p className="text-slate-300">
                We handle updates, monitor for failures, and fix issues so you can focus on your business, not debugging workflows.
              </p>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to skip the DIY headache?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Get professional automation delivered in days, not weeks.
          </p>
          <Link 
            href="/pricing" 
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
          >
            View Pricing
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
