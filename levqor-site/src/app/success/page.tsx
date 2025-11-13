"use client";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Suspense } from "react";

function SuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const type = searchParams.get("type");
  const isDFY = type === "dfy";

  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
      <div className="max-w-2xl mx-auto text-center">
        {/* Success Icon */}
        <div className="mb-8 inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-500/20 border-2 border-emerald-500">
          <svg className="w-10 h-10 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        </div>

        {/* Success Message */}
        <h1 className="text-4xl sm:text-5xl font-bold text-white mb-4">
          Payment successful! 🎉
        </h1>
        
        <p className="text-xl text-slate-300 mb-8 leading-relaxed">
          {isDFY 
            ? "Thank you for choosing Levqor. We've received your payment and we're ready to build your automation."
            : "Welcome to Levqor! Your subscription is active and we're ready to start automating your workflows."}
        </p>

        {/* What's Next Box */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8 mb-8 text-left">
          <h2 className="text-2xl font-bold text-white mb-4">What happens next?</h2>
          
          <div className="space-y-4 text-slate-300">
            {isDFY ? (
              <>
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mt-0.5">
                    1
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">Kickoff call (within 24 hours)</h3>
                    <p className="text-sm">
                      We'll email you to schedule a quick 15-minute call to understand your workflow requirements and integration needs.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mt-0.5">
                    2
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">We build your automation</h3>
                    <p className="text-sm">
                      Our engineers will design, build, and test your workflows. You'll get a demo once it's ready (delivered within your plan's timeframe).
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mt-0.5">
                    3
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">Go live & support</h3>
                    <p className="text-sm">
                      Your automation goes live and we'll provide hands-on support based on your package (7-30 days depending on your tier).
                    </p>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mt-0.5">
                    1
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">Onboarding call (within 24 hours)</h3>
                    <p className="text-sm">
                      We'll contact you to set up your workspace and understand your automation needs.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mt-0.5">
                    2
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">Dashboard access & workflow creation</h3>
                    <p className="text-sm">
                      Sign in to your dashboard to request workflows, monitor performance, and track your automation health.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400 font-bold text-sm mt-0.5">
                    3
                  </div>
                  <div>
                    <h3 className="font-semibold text-white mb-1">Ongoing support & optimization</h3>
                    <p className="text-sm">
                      We'll continuously monitor, optimize, and support your workflows with self-healing capabilities included.
                    </p>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Session Details (if available) */}
        {sessionId && (
          <div className="bg-slate-900/30 border border-slate-800 rounded-lg p-4 mb-8 text-xs text-slate-400 font-mono">
            <p>Session ref: {sessionId.substring(0, 20)}...</p>
            {!isDFY && <p className="mt-1">If you don't receive a confirmation email within 24 hours, contact support@levqor.ai</p>}
          </div>
        )}

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link 
            href="/"
            className="px-8 py-4 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition"
          >
            Back to homepage
          </Link>
          <Link 
            href="/signin"
            className="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition shadow-lg"
          >
            Sign in to dashboard
          </Link>
        </div>

        {/* Support Note */}
        <p className="mt-12 text-sm text-slate-400">
          Questions? Email us at{" "}
          <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
            support@levqor.ai
          </a>
        </p>
      </div>
    </main>
  );
}

export default function SuccessPage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </main>
    }>
      <SuccessContent />
    </Suspense>
  );
}
