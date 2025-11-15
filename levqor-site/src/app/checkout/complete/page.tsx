"use client";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { useSession } from "next-auth/react";

export default function CheckoutComplete() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { data: session, status } = useSession();
  const [error, setError] = useState<string | null>(null);
  const [processing, setProcessing] = useState(true);

  useEffect(() => {
    const completeCheckout = async () => {
      // Wait for session to be loaded
      if (status === "loading") {
        return;
      }

      // If not authenticated, redirect to signin
      if (status === "unauthenticated") {
        router.push("/signin");
        return;
      }

      // Get checkout data from URL
      const dataParam = searchParams.get("data");
      if (!dataParam) {
        setError("Missing checkout data");
        setProcessing(false);
        return;
      }

      try {
        // Decode checkout parameters
        const checkoutParams = JSON.parse(decodeURIComponent(dataParam));
        console.log("Completing checkout:", checkoutParams);

        // Make checkout request with authentication
        const response = await fetch("/api/checkout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(checkoutParams)
        });

        const result = await response.json();

        if (response.ok && result.url) {
          // Redirect to Stripe checkout
          window.location.href = result.url;
        } else {
          setError(result.error || "Failed to create checkout session");
          setProcessing(false);
        }
      } catch (err) {
        console.error("Checkout completion error:", err);
        setError("Failed to process checkout. Please try again.");
        setProcessing(false);
      }
    };

    completeCheckout();
  }, [status, session, searchParams, router]);

  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
      <div className="w-full max-w-md text-center">
        {processing ? (
          <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-12">
            <div className="flex justify-center mb-6">
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-500"></div>
            </div>
            <h2 className="text-2xl font-bold text-white mb-3">Preparing your checkout...</h2>
            <p className="text-slate-400">
              You'll be redirected to Stripe in a moment.
            </p>
          </div>
        ) : error ? (
          <div className="bg-slate-900/80 backdrop-blur border border-red-500/30 rounded-2xl p-12">
            <div className="text-red-500 text-5xl mb-6">⚠️</div>
            <h2 className="text-2xl font-bold text-white mb-3">Checkout Error</h2>
            <p className="text-slate-400 mb-6">{error}</p>
            <button
              onClick={() => router.push("/pricing")}
              className="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition"
            >
              Back to Pricing
            </button>
          </div>
        ) : null}
      </div>
    </main>
  );
}
