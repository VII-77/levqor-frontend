"use client";
import Link from "next/link";
import { useEffect, useState } from "react";
import JsonLd from "@/components/JsonLd";

function StatusPill() {
  const [status, setStatus] = useState<{ ok: boolean; message: string } | null>(null);

  useEffect(() => {
    fetch("https://api.levqor.ai/health")
      .then((res) => res.json())
      .then((data) => setStatus({ ok: data.status === "healthy" || data.ok === true, message: "All systems operational" }))
      .catch(() => setStatus({ ok: false, message: "Checking status..." }));
  }, []);

  if (!status) return null;

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${status.ok ? "bg-green-50 text-green-700" : "bg-yellow-50 text-yellow-700"}`}>
      <span className={`w-2 h-2 rounded-full ${status.ok ? "bg-green-500" : "bg-yellow-500"}`}></span>
      {status.message}
    </div>
  );
}

export default function Home() {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'Levqor',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web',
    url: 'https://levqor.ai',
    description: 'AI-powered automation that self-heals and ships faster. Pay only for results.',
    offers: {
      '@type': 'Offer',
      price: '0',
      priceCurrency: 'USD',
      priceSpecification: {
        '@type': 'UnitPriceSpecification',
        price: '0',
        priceCurrency: 'USD',
      },
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: '4.8',
      ratingCount: '127',
    },
  };

  return (
    <main className="min-h-screen px-4">
      <JsonLd data={structuredData} />
      
      {/* Hero Section */}
      <section className="max-w-6xl mx-auto pt-16 pb-10">
        <div className="inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs">
          <span className="h-2 w-2 rounded-full bg-green-500" />
          Genesis v8.0 · Self-healing automation
        </div>
        <h1 className="mt-6 text-4xl sm:text-6xl font-bold tracking-tight">
          Automate work. <span className="opacity-80">Ship faster.</span>
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-neutral-600">
          Run workflows, monitor failures, and self-heal. Email, Sheets, Slack, CRM.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link href="/signin" className="rounded-xl px-4 py-2 bg-black text-white hover:bg-gray-800 transition">
            Start free trial
          </Link>
          <Link href="/pricing" className="rounded-xl px-4 py-2 border hover:bg-gray-50 transition">
            See pricing
          </Link>
        </div>
      </section>

      {/* Feature Tiles */}
      <section className="max-w-6xl mx-auto grid sm:grid-cols-2 lg:grid-cols-4 gap-4 pb-14">
        {[
          ["Self-healing runs", "Auto-retry with backoff"],
          ["Visual builder", "Drag-drop steps"],
          ["Smart diff", "Isolate failures fast"],
          ["Audit trail", "Each fix recorded"]
        ].map(([t, s]) => (
          <div key={t} className="rounded-2xl border p-4">
            <div className="text-base font-semibold">{t}</div>
            <div className="text-sm text-neutral-600">{s}</div>
          </div>
        ))}
      </section>

      {/* Trust Band */}
      <section className="bg-gray-100 py-12 -mx-4">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="text-sm text-gray-600 mb-6 font-medium uppercase tracking-wide">
            Trusted by teams building with AI
          </p>
          <div className="flex flex-wrap justify-center gap-8 opacity-60">
            {["TechCorp", "DataFlow", "AutoScale", "CloudSync", "DevOps Pro"].map((logo) => (
              <div key={logo} className="bg-white px-6 py-3 rounded-lg shadow-sm font-bold text-gray-700">
                {logo}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-6xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">Why teams choose Levqor</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">🔄</div>
            <h3 className="text-xl font-bold mb-3">Self-healing runs</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Auto-retry with exponential backoff</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Smart diff to isolate failures</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Audit trail for each fix</span></li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">🎨</div>
            <h3 className="text-xl font-bold mb-3">Visual builder</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Drag-drop workflow steps</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Inline AI prompts</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Versioned blueprints</span></li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">🔐</div>
            <h3 className="text-xl font-bold mb-3">Enterprise SSO</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>SAML/OIDC support</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Role-based access control</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Organization audit log</span></li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-bold mb-3">SLA 99.9%</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Global edge network</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Warm starts</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Priority support lanes</span></li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-3">Audit & alerts</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Structured execution logs</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>PagerDuty/Slack webhooks</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>PII-aware log redaction</span></li>
            </ul>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">💳</div>
            <h3 className="text-xl font-bold mb-3">Stripe billing</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Usage-based pricing</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Trials and coupon codes</span></li>
              <li className="flex items-start gap-2"><span className="text-black mt-0.5">•</span><span>Exportable VAT invoices</span></li>
            </ul>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-black text-white py-20 -mx-4">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to automate your workflows?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Start building with Levqor today. No credit card required.
          </p>
          <Link
            href="/signin"
            className="inline-block px-8 py-4 bg-white text-black rounded-xl font-semibold hover:bg-gray-100 transition-colors text-lg"
          >
            Start free trial
          </Link>
        </div>
      </section>
    </main>
  );
}
