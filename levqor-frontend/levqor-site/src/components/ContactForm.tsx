"use client";
import { useState } from "react";

export default function ContactForm({ source = "landing_page" }: { source?: string }) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    message: ""
  });
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    setErrorMessage("");

    try {
      const response = await fetch("/api/sales/lead", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...formData, source })
      });

      const data = await response.json();

      if (data.ok) {
        setStatus("success");
        setFormData({ name: "", email: "", company: "", message: "" });
      } else {
        setStatus("error");
        setErrorMessage(data.error || "Submission failed");
      }
    } catch (error) {
      setStatus("error");
      setErrorMessage("Network error. Please try again.");
    }
  };

  if (status === "success") {
    return (
      <div className="rounded-xl bg-emerald-500/20 border border-emerald-500/50 p-8 text-center">
        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-emerald-500/20 flex items-center justify-center">
          <svg className="w-8 h-8 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-white mb-2">Message received!</h3>
        <p className="text-slate-400 mb-6">
          We'll get back to you within 24 hours.
        </p>
        <button
          onClick={() => setStatus("idle")}
          className="text-sm text-emerald-400 hover:underline"
        >
          Send another message
        </button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {status === "error" && (
        <div className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
          {errorMessage}
        </div>
      )}

      <div>
        <label htmlFor="name" className="block text-sm font-medium text-slate-300 mb-2">
          Name *
        </label>
        <input
          type="text"
          id="name"
          required
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
          placeholder="Your name"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
          Email *
        </label>
        <input
          type="email"
          id="email"
          required
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
          placeholder="you@company.com"
        />
      </div>

      <div>
        <label htmlFor="company" className="block text-sm font-medium text-slate-300 mb-2">
          Company
        </label>
        <input
          type="text"
          id="company"
          value={formData.company}
          onChange={(e) => setFormData({ ...formData, company: e.target.value })}
          className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
          placeholder="Your company name (optional)"
        />
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-slate-300 mb-2">
          Message
        </label>
        <textarea
          id="message"
          rows={4}
          value={formData.message}
          onChange={(e) => setFormData({ ...formData, message: e.target.value })}
          className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none resize-none"
          placeholder="Tell us about your automation needs..."
        />
      </div>

      <button
        type="submit"
        disabled={status === "loading"}
        className="w-full py-3 px-6 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {status === "loading" ? "Sending..." : "Send Message"}
      </button>

      <p className="text-xs text-slate-500 text-center">
        We'll respond within 24 hours. Or email <a href="mailto:sales@levqor.ai" className="text-emerald-400 hover:underline">sales@levqor.ai</a> directly.
      </p>
    </form>
  );
}
