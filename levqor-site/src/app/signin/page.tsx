"use client";
import { signIn, useSession } from "next-auth/react";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";

export default function SignIn() {
  const { data: session } = useSession();
  const searchParams = useSearchParams();
  const [marketingConsent, setMarketingConsent] = useState(false);
  const [tosAccepted, setTosAccepted] = useState(false);
  
  // Get checkout parameter from URL
  const checkoutData = searchParams.get("checkout");

  useEffect(() => {
    if (session?.user?.email && marketingConsent) {
      handleMarketingConsent();
    }
  }, [session]);

  const logTosAcceptance = async (provider: string) => {
    try {
      await fetch('/api/consent/accept', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tosVersion: '2024-11-01',
          privacyVersion: '2024-11-01',
          marketingConsent,
          provider,
        }),
      });
    } catch (error) {
      console.error('TOS acceptance logging failed:', error);
    }
  };

  const handleSignIn = async (provider: "google" | "azure-ad") => {
    if (!tosAccepted) {
      alert('Please accept the Terms of Service and Privacy Policy to continue.');
      return;
    }
    
    await logTosAcceptance(provider);
    
    // If there's checkout data, redirect to checkout completion page
    const callbackUrl = checkoutData 
      ? `/checkout/complete?data=${checkoutData}`
      : "/workflow";
    
    signIn(provider, { callbackUrl });
  };

  const handleMarketingConsent = async () => {
    if (!session?.user?.email) return;

    try {
      const backendApi = process.env.NEXT_PUBLIC_API_URL || 'https://api.levqor.ai';
      
      const userResponse = await fetch(`${backendApi}/api/v1/users/upsert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: session.user.email,
          name: session.user.name || '',
        }),
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();
        
        await fetch('/api/marketing/consent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ consent: true }),
        });
      }
    } catch (error) {
      console.error('Marketing consent error:', error);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h2 className="text-3xl font-bold mb-2 text-white">Levqor</h2>
          </Link>
          <h1 className="text-2xl font-semibold text-white mb-2">Sign in to Levqor</h1>
          <p className="text-sm text-slate-400">Access your workflows and automation dashboard.</p>
        </div>

        {/* Sign-in Card */}
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl">
          {/* TOS Acceptance Required */}
          <div className="mb-6 p-4 bg-emerald-950/20 border border-emerald-900/30 rounded-lg">
            <label className="flex items-start gap-3 cursor-pointer group">
              <input
                type="checkbox"
                checked={tosAccepted}
                onChange={(e) => setTosAccepted(e.target.checked)}
                className="mt-0.5 h-5 w-5 rounded border-slate-600 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-slate-900 transition"
              />
              <span className="text-sm text-slate-300 group-hover:text-white transition">
                I agree to the{" "}
                <Link href="/terms" target="_blank" className="text-emerald-400 hover:underline font-semibold">
                  Terms of Service
                </Link>
                {" "}and{" "}
                <Link href="/privacy" target="_blank" className="text-emerald-400 hover:underline font-semibold">
                  Privacy Policy
                </Link>
              </span>
            </label>
          </div>

          <div className="space-y-4">
            {/* Google Sign-in */}
            <button 
              onClick={() => handleSignIn("google")} 
              disabled={!tosAccepted}
              className={`w-full flex items-center justify-center gap-3 rounded-xl border-2 py-3 px-4 font-medium shadow-lg transition-all ${
                tosAccepted 
                  ? "border-slate-700 bg-slate-800/50 text-white hover:bg-slate-800 hover:border-emerald-500/50 hover:shadow-emerald-500/20" 
                  : "border-slate-800 bg-slate-900/50 text-slate-600 cursor-not-allowed"
              }`}
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Sign in with Google
            </button>

            {/* Microsoft Sign-in */}
            <button 
              onClick={() => handleSignIn("azure-ad")} 
              disabled={!tosAccepted}
              className={`w-full flex items-center justify-center gap-3 rounded-xl border-2 py-3 px-4 font-medium shadow-lg transition-all ${
                tosAccepted 
                  ? "border-slate-700 bg-slate-800/50 text-white hover:bg-slate-800 hover:border-blue-500/50 hover:shadow-blue-500/20" 
                  : "border-slate-800 bg-slate-900/50 text-slate-600 cursor-not-allowed"
              }`}
            >
              <svg className="w-5 h-5" viewBox="0 0 23 23">
                <path fill="#f35325" d="M0 0h11v11H0z"/>
                <path fill="#81bc06" d="M12 0h11v11H12z"/>
                <path fill="#05a6f0" d="M0 12h11v11H0z"/>
                <path fill="#ffba08" d="M12 12h11v11H12z"/>
              </svg>
              Sign in with Microsoft
            </button>

            {/* Marketing Consent Checkbox */}
            <div className="pt-3 pb-2">
              <label className="flex items-start gap-3 cursor-pointer group">
                <input
                  type="checkbox"
                  checked={marketingConsent}
                  onChange={(e) => setMarketingConsent(e.target.checked)}
                  className="mt-0.5 h-5 w-5 rounded border-slate-600 text-emerald-500 focus:ring-emerald-500 focus:ring-offset-slate-900 transition"
                />
                <span className="text-sm text-slate-300 group-hover:text-white transition">
                  I agree to receive product updates, automation tips, and exclusive offers via email (optional)
                </span>
              </label>
              <p className="mt-2 ml-8 text-xs text-slate-500">
                You'll receive a confirmation email to verify your subscription. Unsubscribe anytime.
              </p>
            </div>

            {/* Divider */}
            <div className="relative my-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-700"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-4 bg-slate-900/80 text-slate-400">or</span>
              </div>
            </div>

            {/* Magic Link (Coming Soon) */}
            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-medium text-slate-300">
                Email address
              </label>
              <input
                id="email"
                type="email"
                placeholder="you@company.com"
                disabled
                className="w-full rounded-xl border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-slate-500 cursor-not-allowed"
              />
              <button
                disabled
                className="w-full rounded-xl border-2 border-slate-700 bg-slate-800/30 py-3 px-4 text-slate-500 font-medium cursor-not-allowed"
              >
                Get magic link (coming soon)
              </button>
            </div>

            {/* Continue Without Account */}
            <button
              disabled
              className="w-full rounded-xl border-2 border-slate-700/50 bg-slate-900/30 py-3 px-4 text-slate-600 font-medium cursor-not-allowed text-sm"
            >
              Continue without account (coming soon)
            </button>
          </div>

          {/* Data Storage Explanation */}
          <div className="mt-6 p-4 bg-slate-950/50 border border-slate-800 rounded-lg">
            <p className="text-xs text-slate-400 leading-relaxed">
              <strong className="text-slate-300">How we protect your data:</strong><br/>
              We store only essential account information (email, name, profile picture) securely using industry-standard encryption. 
              Your authentication is handled by Google/Microsoft OAuth. We never store passwords. 
              You can request data deletion anytime via <a href="mailto:privacy@levqor.ai" className="text-emerald-400 hover:underline">privacy@levqor.ai</a>.
            </p>
          </div>

          {/* GDPR Cookie Disclaimer */}
          <div className="mt-4 p-3 bg-blue-950/20 border border-blue-900/30 rounded-lg">
            <p className="text-xs text-slate-400 leading-relaxed">
              <strong className="text-blue-300">🍪 Cookies:</strong> By signing in, you consent to our use of essential authentication cookies. 
              See our <Link href="/cookies" className="text-blue-400 hover:underline">Cookie Policy</Link> for details.
            </p>
          </div>

          {/* Legal Footer */}
          <div className="mt-6 p-4 bg-emerald-950/20 border border-emerald-900/30 rounded-lg">
            <p className="text-xs text-slate-300 text-center leading-relaxed">
              By continuing, you agree to the Levqor{" "}
              <Link href="/terms" className="text-emerald-400 hover:underline font-semibold">Terms of Service</Link>
              {" "}and{" "}
              <Link href="/privacy" className="text-emerald-400 hover:underline font-semibold">Privacy Policy</Link>.
              <br/>
              <span className="text-slate-400">UK/GDPR compliant. Your data, your rights.</span>
            </p>
          </div>
        </div>

        {/* Back to home */}
        <div className="mt-6 text-center">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>
      </div>
    </main>
  );
}
