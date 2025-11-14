"use client";
import { useSession } from "next-auth/react";
import { useState } from "react";
import Link from "next/link";

export default function MyDataPage() {
  const { data: session, status: sessionStatus } = useSession();
  const [requesting, setRequesting] = useState(false);
  const [requestStatus, setRequestStatus] = useState<"idle" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleRequest = async () => {
    if (!session?.user?.email) {
      setMessage("You must be signed in to request your data");
      setRequestStatus("error");
      return;
    }

    setRequesting(true);
    setRequestStatus("idle");
    setMessage("");

    try {
      const backendApi = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      
      const response = await fetch(`${backendApi}/api/dsar/request`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: session.user.email,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setRequestStatus("success");
        setMessage("Your data export request has been submitted. You'll receive an email with your data within 30 days as required by GDPR.");
      } else {
        setRequestStatus("error");
        setMessage(data.error || "Failed to submit data request. Please try again.");
      }
    } catch (error) {
      setRequestStatus("error");
      setMessage("Network error. Please check your connection and try again.");
    } finally {
      setRequesting(false);
    }
  };

  if (sessionStatus === "loading") {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </main>
    );
  }

  if (sessionStatus === "unauthenticated") {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
        <div className="max-w-md text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Sign In Required</h1>
          <p className="text-slate-400 mb-6">You must be signed in to request your data</p>
          <Link
            href="/signin"
            className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition"
          >
            Sign In
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">
            Levqor
          </Link>
          <Link href="/dashboard" className="text-sm text-slate-300 hover:text-white transition">
            Dashboard
          </Link>
        </nav>
      </header>

      <div className="max-w-3xl mx-auto px-4 py-16">
        <h1 className="text-3xl font-bold text-white mb-4">Request My Data</h1>
        <p className="text-lg text-slate-400 mb-8">
          Under GDPR Article 15, you have the right to access your personal data.
        </p>

        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 mb-8">
          <h2 className="text-xl font-bold text-white mb-4">What You'll Receive</h2>
          <ul className="space-y-3 text-slate-300 mb-6">
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>All personal information we hold about you</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Your workflow configurations and automation settings</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Billing history and subscription details</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Activity logs and usage data</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-emerald-400 mt-1">✓</span>
              <span>Consent records and preferences</span>
            </li>
          </ul>

          <div className="p-4 bg-blue-950/20 border border-blue-900/30 rounded-lg mb-6">
            <h3 className="font-semibold text-white mb-2">Delivery Method</h3>
            <p className="text-sm text-slate-300">
              Your data will be sent as a secure ZIP file attachment to your registered email address ({session?.user?.email}) within 30 days.
            </p>
          </div>

          <div className="p-4 bg-amber-950/20 border border-amber-900/30 rounded-lg mb-6">
            <h3 className="font-semibold text-white mb-2">Rate Limit</h3>
            <p className="text-sm text-slate-300">
              You can request your data once every 24 hours to prevent abuse.
            </p>
          </div>

          {requestStatus === "success" && (
            <div className="p-4 bg-emerald-950/20 border border-emerald-900/30 rounded-lg mb-6">
              <p className="text-emerald-400 font-semibold">{message}</p>
            </div>
          )}

          {requestStatus === "error" && (
            <div className="p-4 bg-red-950/20 border border-red-900/30 rounded-lg mb-6">
              <p className="text-red-400">{message}</p>
            </div>
          )}

          <button
            onClick={handleRequest}
            disabled={requesting}
            className="w-full px-6 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-bold text-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {requesting ? "Submitting Request..." : "Request My Data Export"}
          </button>
        </div>

        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
          <h2 className="text-xl font-bold text-white mb-4">Your Privacy Rights</h2>
          <div className="space-y-4 text-slate-300 text-sm">
            <div>
              <h3 className="font-semibold text-white mb-2">Right to Access (Article 15)</h3>
              <p>Request a copy of your personal data (this page)</p>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-2">Right to Rectification (Article 16)</h3>
              <p>
                Correct inaccurate data via{" "}
                <Link href="/dashboard/settings" className="text-emerald-400 hover:underline">
                  account settings
                </Link>
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-2">Right to Erasure (Article 17)</h3>
              <p>
                Delete your account and all data via{" "}
                <Link href="/dashboard/settings" className="text-emerald-400 hover:underline">
                  account settings
                </Link>
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-2">Right to Object (Article 21)</h3>
              <p>
                Object to processing via{" "}
                <Link href="/privacy-tools/opt-out" className="text-emerald-400 hover:underline">
                  opt-out settings
                </Link>
              </p>
            </div>
            <div>
              <h3 className="font-semibold text-white mb-2">Right to Data Portability (Article 20)</h3>
              <p>Export your data in machine-readable format (included in data export)</p>
            </div>
          </div>
        </div>

        <div className="mt-8 text-center text-sm text-slate-400">
          <p>
            Questions about your data?{" "}
            <Link href="/contact" className="text-emerald-400 hover:underline">
              Contact us
            </Link>{" "}
            or email{" "}
            <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">
              privacy@levqor.ai
            </a>
          </p>
        </div>
      </div>
    </main>
  );
}
