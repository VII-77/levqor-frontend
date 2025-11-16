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
          a: "Levqor is a done-for-you (DFY) automation platform serving clients worldwide. We build, test, and deliver working automation workflows for your business so you can save 20+ hours per week without technical skills or weeks of learning."
        },
        {
          q: "How is this different from Zapier or Make.com?",
          a: "Tools like Zapier require you to learn, build, and maintain automations yourself. Levqor provides white-glove service globally: we handle strategy, design, implementation, testing, and ongoing support. You get working automation delivered in days, not DIY tools dumped in your lap."
        },
        {
          q: "How fast can you deliver?",
          a: "Starter DFY = 48 hours. Professional = 3-4 days. Enterprise = 7 days. We don't rush and deliver broken automations. We build, test, and deliver production-ready workflows that work from day 1."
        }
      ]
    },
    {
      category: "DFY Process & Delivery",
      questions: [
        {
          q: "What happens after I purchase a DFY plan?",
          a: "After purchase, you'll receive an instant confirmation email with a link to a 5-minute intake form. We'll gather details about your workflow, tools, and goals, then design and build your automation within 24 hours to 7 days (depending on your tier)."
        },
        {
          q: "What if I don't know which tools to use?",
          a: "No problem! On our kickoff call, we'll audit your current process and recommend the best tools to connect. Most clients use Gmail, Google Sheets, and a CRM (HubSpot, Pipedrive, etc.). We make it work."
        },
        {
          q: "Do I need to know how to code?",
          a: "Absolutely not. That's the whole point of Done-For-You. You describe the problem, we build the solution. Zero coding required."
        },
        {
          q: "What happens after the 7-30 day support period?",
          a: "Your automation keeps running forever (it's yours). If you need updates or new workflows later, you can: (1) Buy another DFY plan for one-off builds, (2) Subscribe to our monthly plans for ongoing automation (£29-£149/month), or (3) Pay for one-off fixes (£49-99 per fix)."
        },
        {
          q: "Can I modify the automation later?",
          a: "Yes, you own it 100%. We build it in your accounts using your tools. You can modify, duplicate, or delete it anytime. We also provide documentation so you (or your team) can tweak it if needed."
        },
        {
          q: "What if my automation breaks?",
          a: "During the support period (7-30 days), we fix it for free. After that, you can: (1) Pay for one-off fixes (£49-99), (2) Subscribe for ongoing maintenance (£29+/month), or (3) Fix it yourself using the documentation we provide."
        },
        {
          q: "Do I get revisions?",
          a: "Yes! Starter includes 1 round of revisions, Professional includes 2 rounds, and Enterprise includes 3 rounds to ensure the automation works exactly as you need it."
        }
      ]
    },
    {
      category: "Pricing & ROI",
      questions: [
        {
          q: "What payment methods do you accept?",
          a: "We accept all major credit cards via Stripe. All payments are secure and GDPR-compliant. We serve clients globally with support for international payments."
        },
        {
          q: "Can I upgrade or downgrade my plan?",
          a: "Yes! You can upgrade to a higher-tier DFY plan or switch to a subscription at any time. Contact us for assistance."
        },
        {
          q: "Do you offer refunds?",
          a: "Yes, we offer a 14-day money-back guarantee on all DFY plans. If we deliver your automation and it doesn't work as described, we'll either: (1) Fix it immediately (usually within 24 hours), OR (2) Refund you 100%, no questions asked. We've never had to issue a refund because we test everything before handoff."
        },
        {
          q: "Can I upgrade from DFY to a subscription later?",
          a: "Absolutely! Many customers start with DFY Starter (£99) to test, then subscribe to Growth (£79/month) to keep building."
        },
        {
          q: "What if I need more than 7 workflows?",
          a: "Buy DFY Enterprise (7 workflows) + a subscription plan. Example: Buy DFY Enterprise (£599) to automate your top 7 pain points immediately, then subscribe to Growth (£79/month) to build 3 new workflows every month as you scale."
        }
      ]
    },
    {
      category: "Tools & Integrations",
      questions: [
        {
          q: "What tools do you support?",
          a: "We support 100+ tools globally, including: Email (Gmail, Outlook, SendGrid, Mailchimp), CRM (HubSpot, Pipedrive, Salesforce, Airtable), Spreadsheets (Google Sheets, Excel, Airtable), Messaging (Slack, Discord, WhatsApp, SMS via Twilio), Payment (Stripe, PayPal, Gumroad), and Custom APIs. If you have a custom tool, we can connect it. If you're not sure, just ask!"
        }
      ]
    },
    {
      category: "Data & Security",
      questions: [
        {
          q: "Is my data secure?",
          a: "Absolutely. We use EU-based data centers with global compliance standards, encrypt all data in transit and at rest, and are fully GDPR-compliant. We never sell or share your data. We serve clients worldwide with the same high security standards."
        },
        {
          q: "Do you access my accounts?",
          a: "Only with your explicit permission and only to set up automation. We use OAuth and API keys (never passwords) and follow industry-standard security practices."
        },
        {
          q: "How do I know you won't mess up my data?",
          a: "We work in test/staging environments first, then move to production. For DFY builds, we: (1) Ask for read-only access where possible, (2) Test with dummy data first, (3) Run 5-10 real examples in a sandbox, (4) Only move to production after you approve the test results. We also use error handling to ensure if something fails, it doesn't corrupt your data—it just alerts you."
        },
        {
          q: "What automations do you NOT support?",
          a: "We do not automate medical, legal, financial advice, or any high-risk workflows where incorrect automation could cause harm. See our high-risk data policy for details."
        }
      ]
    },
    {
      category: "Support & Service",
      questions: [
        {
          q: "Do you offer support worldwide?",
          a: "Yes! Levqor provides global support to clients anywhere in the world. Our team operates across time zones to ensure fast response times no matter where you're located."
        },
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
