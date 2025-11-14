"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";

export default function SLACreditsPage() {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    accountName: "",
    plan: "",
    incidentDate: "",
    description: ""
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("SLA request", formData);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setFormData({
        fullName: "",
        email: "",
        accountName: "",
        plan: "",
        incidentDate: "",
        description: ""
      });
    }, 5000);
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-3xl mx-auto px-4 py-12 space-y-6">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-white mb-2">SLA Credits & Downtime Claims</h1>
        <p className="text-slate-400 mb-8">
          Request service credits for incidents covered under our{" "}
          <Link href="/sla" className="text-emerald-400 hover:underline">
            Service Level Agreement
          </Link>
        </p>

        <section className="space-y-4 mb-8">
          <h2 className="text-2xl font-bold text-white">Eligibility</h2>
          <p className="text-slate-300 leading-relaxed">
            SLA credits are available according to the terms in our SLA. Please review the following requirements:
          </p>
          <ul className="list-disc list-inside space-y-2 text-slate-300 ml-4">
            <li>Only account owners or billing contacts can submit credit requests</li>
            <li>Requests must be submitted within 30 days of the incident</li>
            <li>You must provide proof of impact (timestamps, screenshots, error logs)</li>
            <li>Credits are calculated based on documented downtime per our SLA tiers</li>
            <li>Credits are applied to future invoices, not refunded as cash</li>
          </ul>
        </section>

        <section className="space-y-4 mb-8">
          <h2 className="text-2xl font-bold text-white">Submit a Request</h2>
          
          {submitted ? (
            <div className="bg-emerald-500/20 border border-emerald-500/50 rounded-lg p-6">
              <p className="text-emerald-400 font-medium">
                ✓ We've received your SLA credit request. We'll review within 5–7 business days.
              </p>
              <p className="text-slate-400 text-sm mt-2">
                You'll receive an email confirmation shortly with your reference number.
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
              <div>
                <label htmlFor="fullName" className="block text-sm font-medium text-slate-300 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  id="fullName"
                  required
                  value={formData.fullName}
                  onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-300 mb-2">
                  Work Email *
                </label>
                <input
                  type="email"
                  id="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label htmlFor="accountName" className="block text-sm font-medium text-slate-300 mb-2">
                  Account / Company Name *
                </label>
                <input
                  type="text"
                  id="accountName"
                  required
                  value={formData.accountName}
                  onChange={(e) => setFormData({ ...formData, accountName: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label htmlFor="plan" className="block text-sm font-medium text-slate-300 mb-2">
                  Current Plan *
                </label>
                <select
                  id="plan"
                  required
                  value={formData.plan}
                  onChange={(e) => setFormData({ ...formData, plan: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="">Select your plan</option>
                  <option value="starter">Starter</option>
                  <option value="growth">Growth</option>
                  <option value="pro">Pro</option>
                  <option value="business">Business</option>
                </select>
              </div>

              <div>
                <label htmlFor="incidentDate" className="block text-sm font-medium text-slate-300 mb-2">
                  Incident Date & Time *
                </label>
                <input
                  type="text"
                  id="incidentDate"
                  required
                  placeholder="e.g., 14 Nov 2025, 14:30 UTC"
                  value={formData.incidentDate}
                  onChange={(e) => setFormData({ ...formData, incidentDate: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-slate-300 mb-2">
                  Description of Impact *
                </label>
                <textarea
                  id="description"
                  required
                  rows={5}
                  placeholder="Describe the downtime, affected services, and business impact. Include any error messages, screenshots, or logs."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-4 py-2 bg-slate-950 border border-slate-700 rounded-lg text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <button
                type="submit"
                className="w-full px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition"
              >
                Submit SLA Credit Request
              </button>

              <p className="text-sm text-slate-500 text-center">
                By submitting, you confirm all information is accurate and you have the authority to request credits on behalf of your account.
              </p>
            </form>
          )}
        </section>

        <section className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
          <h3 className="text-lg font-bold text-white">What Happens Next?</h3>
          <ul className="list-disc list-inside space-y-2 text-slate-400 text-sm ml-4">
            <li>We'll review your request within 5–7 business days</li>
            <li>You'll receive a confirmation email with a reference number</li>
            <li>If approved, credits will be applied to your next invoice</li>
            <li>If we need additional information, we'll contact you via email</li>
          </ul>
        </section>
      </div>
    </main>
  );
}
