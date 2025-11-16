import PublicPageLayout from "@/components/PublicPageLayout";
import Link from "next/link";

export const metadata = {
  title: "Blog - Automation Tips & Insights",
  description: "Learn automation best practices, tips, and strategies from the Levqor team.",
};

export default function BlogPage() {
  const posts = [
    {
      title: "How to Save 20 Hours Per Week with Automation",
      excerpt: "Discover the most common time-wasting tasks and how to automate them effectively.",
      date: "Nov 15, 2025",
      readTime: "5 min",
      slug: "#"
    },
    {
      title: "DFY vs DIY Automation: Which is Right for You?",
      excerpt: "Compare done-for-you automation services with DIY tools like Zapier and Make.com.",
      date: "Nov 10, 2025",
      readTime: "7 min",
      slug: "#"
    },
    {
      title: "How Levqor Handles Data Security & GDPR Compliance",
      excerpt: "A deep dive into our security practices, EU data centers, and GDPR compliance.",
      date: "Nov 5, 2025",
      readTime: "6 min",
      slug: "#"
    },
    {
      title: "5 Automation Workflows Every Agency Needs",
      excerpt: "Essential automation workflows for agencies to save time on client work.",
      date: "Oct 28, 2025",
      readTime: "8 min",
      slug: "#"
    },
    {
      title: "The Hidden Cost of Manual Work",
      excerpt: "Calculate how much manual, repetitive tasks are actually costing your business.",
      date: "Oct 20, 2025",
      readTime: "4 min",
      slug: "#"
    }
  ];

  return (
    <PublicPageLayout>
      <div className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-500/40 bg-emerald-500/10 px-3 py-1 text-xs font-medium text-emerald-200 mb-6">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
            Blog
          </div>
          <h1 className="text-4xl sm:text-5xl font-bold mb-6 text-white">
            Automation tips & insights
          </h1>
          <p className="text-xl text-slate-400">
            Learn how to automate smarter and ship faster.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {posts.map((post, idx) => (
            <article key={idx} className="bg-slate-900/50 border border-slate-800 rounded-xl p-8 hover:border-emerald-400/50 transition">
              <div className="flex items-center gap-3 text-sm text-slate-400 mb-4">
                <span>{post.date}</span>
                <span>•</span>
                <span>{post.readTime} read</span>
              </div>
              <h2 className="text-2xl font-bold text-white mb-4 hover:text-emerald-400 transition">
                <Link href={post.slug}>{post.title}</Link>
              </h2>
              <p className="text-slate-300 mb-6">{post.excerpt}</p>
              <Link href={post.slug} className="text-emerald-400 hover:underline font-semibold">
                Read more →
              </Link>
            </article>
          ))}
        </div>
      </div>
    </PublicPageLayout>
  );
}
