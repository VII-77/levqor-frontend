"use client";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function CookieBanner() {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem("levqor_cookie_consent");
    if (!consent) {
      setShowBanner(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem("levqor_cookie_consent", "accepted");
    setShowBanner(false);
  };

  if (!showBanner) return null;

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur-md border-t border-slate-800 shadow-2xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex-1 text-sm text-slate-300">
            We use essential and analytics cookies to run Levqor and improve your experience. 
            See our{" "}
            <Link href="/cookies" className="text-emerald-400 hover:underline font-medium">
              Cookie Policy
            </Link>{" "}
            for details.
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleAccept}
              className="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition-all whitespace-nowrap"
            >
              Accept
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
