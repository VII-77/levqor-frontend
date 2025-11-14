import Link from "next/link";

export default function SecurityDisclosurePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">Security Vulnerability Disclosure</h1>
        <p className="text-slate-400 mb-12">
          Last updated: {new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" })}
        </p>

        <section className="space-y-4">
          <p className="text-slate-300 leading-relaxed">
            We welcome responsible disclosure of security vulnerabilities.
          </p>
          <p className="text-slate-300 leading-relaxed">
            If you have discovered a security issue, please report it to:
          </p>
          <p className="text-slate-300 leading-relaxed">
            <a href="mailto:security@levqor.ai" className="text-emerald-400 hover:underline font-semibold">security@levqor.ai</a>
          </p>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">What to Include</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Description of the vulnerability</li>
            <li>Steps to reproduce</li>
            <li>Potential impact</li>
            <li>Your contact information</li>
          </ul>
        </section>

        <section className="space-y-4 mt-8">
          <h2 className="text-2xl font-bold text-white">Our Commitment</h2>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Acknowledge receipt within 48 hours</li>
            <li>Provide a timeline for resolution</li>
            <li>Keep you informed of progress</li>
          </ul>
        </section>

        <div className="mt-12 pt-8 border-t border-slate-800">
          <div className="flex gap-4 text-sm">
            <Link href="/security" className="text-emerald-400 hover:underline">Security</Link>
            <Link href="/privacy" className="text-emerald-400 hover:underline">Privacy Policy</Link>
          </div>
        </div>
      </div>
    </main>
  );
}
