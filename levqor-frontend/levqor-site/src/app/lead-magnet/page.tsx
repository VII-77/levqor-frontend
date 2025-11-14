"use client";
import Link from "next/link";
import { useState } from "react";

export default function LeadMagnetPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    business_type: "",
    problem: "",
    phone: ""
  });
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setErrorMessage("");

    try {
      const response = await fetch("/api/lead-magnet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (data.ok) {
        setStatus("success");
      } else {
        setStatus("error");
        setErrorMessage(data.error || "Submission failed");
      }
    } catch (error) {
      setStatus("error");
      setErrorMessage("Network error");
    }
  };

  if (status === "success") {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
        <div className="max-w-2xl text-center">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-emerald-500/20 flex items-center justify-center">
            <svg className="w-10 h-10 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white mb-4">Check your email!</h1>
          <p className="text-lg text-slate-400 mb-8">
            We've sent your free automation guide to <strong className="text-white">{formData.email}</strong>
          </p>
          <Link href="/" className="inline-block px-8 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
            Back to Home
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">Levqor</Link>
        </nav>
      </header>

      <div className="max-w-2xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4">
            Get Your Free Automation Guide
          </h1>
          <p className="text-lg text-slate-400">
            Learn the 5 most common business automations + step-by-step setup guides
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
          {status === "error" && (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
              {errorMessage}
            </div>
          )}

          <div>
            <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-2">Name *</label>
            <input
              type="text"
              id="name"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">Email *</label>
            <input
              type="email"
              id="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div>
            <label htmlFor="business_type" className="block text-sm font-medium text-slate-300 mb-2">Business Type</label>
            <select
              id="business_type"
              value={formData.business_type}
              onChange={(e) => setFormData({ ...formData, business_type: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="">Select...</option>
              <option value="Agency">Agency</option>
              <option value="E-commerce">E-commerce</option>
              <option value="SaaS">SaaS</option>
              <option value="Consulting">Consulting</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label htmlFor="problem" className="block text-sm font-medium text-slate-300 mb-2">What do you want to automate?</label>
            <textarea
              id="problem"
              rows={4}
              value={formData.problem}
              onChange={(e) => setFormData({ ...formData, problem: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none resize-none"
              placeholder="e.g., Lead data entry, weekly reports, email sequences..."
            />
          </div>

          <div>
            <label htmlFor="phone" className="block text-sm font-medium text-slate-300 mb-2">Phone (optional)</label>
            <input
              type="tel"
              id="phone"
              value={formData.phone}
              onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={status === "loading"}
            className="w-full py-4 px-6 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-bold text-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {status === "loading" ? "Sending..." : "Get Free Guide"}
          </button>
        </form>
      </div>
    </main>
  );
}
