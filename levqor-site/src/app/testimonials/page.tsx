import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Testimonials - What Our Clients Say",
  description: "Real reviews from real clients. See why businesses trust Levqor for done-for-you automation.",
};

export default function TestimonialsPage() {
  const testimonials = [
    {
      quote: "Levqor saved me 18 hours per week on client reporting alone. The ROI was immediate and the team was incredibly responsive.",
      name: "Sarah M.",
      role: "Agency Owner",
      plan: "Professional DFY"
    },
    {
      quote: "I was skeptical at first, but after seeing the automation live in 5 days, I'm a believer. This is game-changing for small teams.",
      name: "James K.",
      role: "E-Commerce Founder",
      plan: "Enterprise DFY"
    },
    {
      quote: "The white-glove service is unmatched. They didn't just build workflows—they helped me rethink my entire operational strategy.",
      name: "Emma L.",
      role: "Business Coach",
      plan: "Growth Subscription"
    },
    {
      quote: "Finally, automation that actually works. No debugging at 2 AM, no broken workflows, just results.",
      name: "Michael R.",
      role: "SaaS Founder",
      plan: "Business Subscription"
    },
    {
      quote: "Best investment I've made in my business this year. Period.",
      name: "David T.",
      role: "Consultant",
      plan: "Starter DFY"
    },
    {
      quote: "Levqor's team took the time to understand my workflow and delivered exactly what I needed. The revision process was smooth and collaborative.",
      name: "Rachel P.",
      role: "Creative Director",
      plan: "Professional DFY"
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Testimonials
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Trusted by founders<br />who value their time
          </h1>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Don't just take our word for it. Here's what our clients say about Levqor.
          </p>
        </div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          {testimonials.map((t, idx) => (
            <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-xl p-6">
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => (
                  <svg key={i} className="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                ))}
              </div>
              <p className="text-lg text-slate-200 mb-6 italic">"{t.quote}"</p>
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-semibold text-white">{t.name}</div>
                  <div className="text-sm text-slate-400">{t.role}</div>
                </div>
                <div className="text-xs text-emerald-400 font-semibold">{t.plan}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-2">4.9/5</div>
            <div className="text-slate-300">Average Rating</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-2">20+ hrs</div>
            <div className="text-slate-300">Avg. Time Saved/Week</div>
          </div>
          <div className="text-center">
            <div className="text-4xl font-bold text-emerald-400 mb-2">3-7 days</div>
            <div className="text-slate-300">Avg. Delivery Time</div>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-br from-emerald-500/10 to-blue-500/10 border border-emerald-500/30 rounded-2xl p-12">
          <h2 className="text-3xl font-bold mb-4 text-white">Join hundreds of happy clients</h2>
          <p className="text-lg text-slate-300 mb-8">
            Let Levqor automate your busywork so you can focus on growth.
          </p>
          <Link 
            href="/pricing" 
            className="inline-flex items-center justify-center gap-2 px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all shadow-lg"
          >
            Get Started
          </Link>
        </div>
      </div>
    </PublicPageLayout>
  );
}
