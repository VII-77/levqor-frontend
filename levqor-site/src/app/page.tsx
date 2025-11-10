"use client";
import Link from "next/link";
import { useEffect, useState } from "react";

function StatusPill() {
  const [status, setStatus] = useState<{ ok: boolean; message: string } | null>(null);

  useEffect(() => {
    fetch("https://api.levqor.ai/health")
      .then((res) => res.json())
      .then((data) => setStatus({ ok: data.status === "healthy", message: "All systems operational" }))
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
  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 py-20 text-center">
        <div className="mb-6">
          <StatusPill />
        </div>
        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          Automate work. Ship faster.<br />Pay only for results.
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Levqor runs your workflows, monitors failures, and self-heals. Email, Sheets, Slack, CRM, and more.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/signin"
            className="px-8 py-4 bg-black text-white rounded-xl font-semibold hover:bg-gray-800 transition-colors text-lg"
          >
            Start free trial
          </Link>
          <Link
            href="/pricing"
            className="px-8 py-4 border-2 border-black rounded-xl font-semibold hover:bg-gray-50 transition-colors text-lg"
          >
            See pricing
          </Link>
        </div>
      </section>

      {/* Trust Band */}
      <section className="bg-gray-100 py-12">
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
            <h3 className="text-xl font-bold mb-2">Self-healing runs</h3>
            <p className="text-gray-600">
              Automatic retries with exponential backoff. Failed jobs resume from last checkpoint, not from scratch.
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">🎨</div>
            <h3 className="text-xl font-bold mb-2">Visual builder</h3>
            <p className="text-gray-600">
              No-code workflow designer with 100+ templates. Drag, drop, connect. Deploy in minutes.
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">🔐</div>
            <h3 className="text-xl font-bold mb-2">Enterprise SSO</h3>
            <p className="text-gray-600">
              Google, Microsoft, and SAML support. Role-based access control and audit logs built in.
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">⚡</div>
            <h3 className="text-xl font-bold mb-2">SLA 99.9%</h3>
            <p className="text-gray-600">
              Business plans include guaranteed uptime, priority support, and dedicated infrastructure.
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-xl font-bold mb-2">Audit & alerts</h3>
            <p className="text-gray-600">
              Real-time monitoring, Slack/email alerts, full execution history with searchable logs.
            </p>
          </div>
          <div className="bg-white p-6 rounded-2xl shadow-sm border hover:shadow-md transition-shadow">
            <div className="text-4xl mb-4">💳</div>
            <h3 className="text-xl font-bold mb-2">Stripe billing</h3>
            <p className="text-gray-600">
              Pay-as-you-go with usage-based pricing. Cancel anytime, prorated refunds. VAT invoices included.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-black text-white py-20">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to automate your workflow?</h2>
          <p className="text-xl text-gray-300 mb-8">
            Join hundreds of teams shipping faster with Levqor. Start free, no credit card required.
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
