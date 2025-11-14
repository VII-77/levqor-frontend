import Link from "next/link";

export default function CookiesPage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Cookie Policy</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <p className="text-slate-300 leading-relaxed">
          Levqor uses cookies to improve user experience and maintain platform security.
        </p>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Types of Cookies</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Essential (authentication, security)</li>
            <li>Analytics (usage metrics)</li>
            <li>Preference (UI settings)</li>
            <li>Marketing (where applicable)</li>
          </ul>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Managing Cookies</h2>
          <p className="text-slate-300 leading-relaxed">
            You may manage cookies in browser settings.
          </p>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Contact</h2>
          <p className="text-slate-300 leading-relaxed">
            Email: <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>
          </p>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
            <Link href="/terms" className="text-emerald-400 hover:underline">Terms of Service</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
