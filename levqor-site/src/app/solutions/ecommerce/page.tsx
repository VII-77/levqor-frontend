import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Automation for eCommerce Stores",
  description: "DFY automation for eCommerce: order fulfillment, inventory sync, abandoned carts, and customer support.",
};

export default function EcommerceSolutionPage() {
  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation for eCommerce Stores
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Automate order processing, inventory management, and customer follow-ups to scale your store without the chaos.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          {[
            { title: "Order Fulfillment", desc: "Auto-process orders, update inventory, notify suppliers, and send tracking info to customers." },
            { title: "Abandoned Cart Recovery", desc: "Automatically email customers who left items in their cart with personalized recovery sequences." },
            { title: "Inventory Sync", desc: "Keep stock levels synchronized across Shopify, Amazon, WooCommerce, and fulfillment centers." },
            { title: "Review Requests", desc: "Auto-send review requests after delivery with perfect timing for maximum response rates." },
            { title: "Customer Support Routing", desc: "Automatically categorize and route support tickets to the right team member." },
            { title: "Refund Processing", desc: "Automate refund workflows, update inventory, and notify customers instantly." }
          ].map((item, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
              <h3 className="text-xl font-bold text-white mb-3">{item.title}</h3>
              <p className="text-slate-300">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Ready to scale your eCommerce store?</h2>
          <p className="text-lg text-slate-300 mb-8">
            Let Levqor automate your operations so you can focus on growth.
          </p>
          <Link href="/pricing" className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg">
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
