import Link from "next/link";

export default function AccessibilityPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Accessibility Statement</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">WCAG 2.1 AA Compliance Intention</h2>
          <p className="text-slate-300 leading-relaxed">
            We aim for WCAG 2.1 AA compliance across our platform.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Continuous improvements made to meet accessibility standards.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Keyboard Navigation</h2>
          <p className="text-slate-300 leading-relaxed">
            Full keyboard navigation supported across all pages.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Focus indicators visible for all interactive elements.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Tab order follows logical flow.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Screen-Reader Support</h2>
          <p className="text-slate-300 leading-relaxed">
            Semantic HTML structure for proper screen-reader interpretation.
          </p>
          <p className="text-slate-300 leading-relaxed">
            Alt text provided for all meaningful images.
          </p>
          <p className="text-slate-300 leading-relaxed">
            ARIA labels used where necessary.
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Contact for Accessibility Issues</h2>
          <p className="text-slate-300 leading-relaxed">
            For accessibility requests or to report issues: <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">support@levqor.ai</a>
          </p>
          <p className="text-slate-300 leading-relaxed">
            Users may request accessible formats for documentation.
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/support-policy" className="text-emerald-400 hover:underline">Support Policy</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
