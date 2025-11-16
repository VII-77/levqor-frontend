import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "FAQ - Frequently Asked Questions",
  description: "Common questions about Levqor's DFY automation, pricing, security, and support.",
};

export default function FAQPage() {
  const faqs = [
    {
      category: "General",
      questions: [
        {
          q: "What is Levqor?",
          a: "Levqor is a done-for-you (DFY) automation platform. We build, test, and deliver working automation workflows for your business so you can save 20+ hours per week without technical skills or weeks of learning."
        },
        {
          q: "How is this different from Zapier or Make.com?",
          a: "Tools like Zapier require you to learn, build, and maintain automations yourself. Levqor provides white-glove service: we handle strategy, design, implementation, testing, and ongoing support. You get working automation delivered in days, not DIY tools dumped in your lap."
        },
        {
          q: "How long does it take to get automation live?",
          a: "Most DFY projects are delivered within 3-7 days. Subscription plans include ongoing workflows delivered on a monthly cadence."
        }
      ]
    },
    {
      category: "Pricing & Billing",
      questions: [
        {
          q: "What payment methods do you accept?",
          a: "We accept all major credit cards via Stripe. All payments are secure and GDPR-compliant."
        },
        {
          q: "Can I upgrade or downgrade my plan?",
          a: "Yes! You can upgrade to a higher-tier DFY plan or switch to a subscription at any time. Contact us for assistance."
        },
        {
          q: "Do you offer refunds?",
          a: "Yes, we offer a 14-day money-back guarantee on all DFY plans. If you're not satisfied, we'll refund your purchase in full. See our refund policy for details."
        }
      ]
    },
    {
      category: "DFY Projects",
      questions: [
        {
          q: "What happens after I purchase a DFY plan?",
          a: "After purchase, you'll receive an intake form or scheduling link. We'll gather details about your workflow, tools, and goals, then design and build your automation within 3-7 days."
        },
        {
          q: "Do I get revisions?",
          a: "Yes! Every DFY plan includes 1 round of revisions to ensure the automation works exactly as you need it."
        },
        {
          q: "What if I need more workflows later?",
          a: "You can purchase additional DFY builds or upgrade to a subscription plan for unlimited monthly workflows."
        }
      ]
    },
    {
      category: "Data & Security",
      questions: [
        {
          q: "Is my data secure?",
          a: "Absolutely. We use EU-based data centers, encrypt all data in transit and at rest, and are fully GDPR-compliant. We never sell or share your data."
        },
        {
          q: "Do you access my accounts?",
          a: "Only with your explicit permission and only to set up automation. We use OAuth and API keys (never passwords) and follow industry-standard security practices."
        },
        {
          q: "What automations do you NOT support?",
          a: "We do not automate medical, legal, financial advice, or any high-risk workflows where incorrect automation could cause harm. See our high-risk data policy for details."
        }
      ]
    },
    {
      category: "Cancellations & Refunds",
      questions: [
        {
          q: "Can I cancel my subscription?",
          a: "Yes, you can cancel anytime. No lock-in contracts. Cancellations take effect at the end of your current billing period."
        },
        {
          q: "What happens to my automation if I cancel?",
          a: "Your automation continues to work! For DFY builds, you own the workflows. For subscriptions, workflows remain active but won't receive updates or support after cancellation."
        }
      ]
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            FAQ
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Frequently asked questions
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Everything you need to know about Levqor's DFY automation service.
          </p>
        </div>

        <div className="space-y-12">
          {faqs.map((cat, idx) => (
            <div key={idx}>
              <h2 className="text-2xl font-bold mb-6 text-white">{cat.category}</h2>
              <div className="space-y-6">
                {cat.questions.map((faq, i) => (
                  <div key={i} className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                    <h3 className="text-lg font-semibold text-white mb-3">{faq.q}</h3>
                    <p className="text-slate-300">{faq.a}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-2xl font-bold mb-4 text-white">Still have questions?</h2>
          <p className="text-slate-300 mb-8">
            Can't find what you're looking for? Our team is here to help.
          </p>
          <Link 
            href="/contact" 
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
          >
            Contact Support
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
