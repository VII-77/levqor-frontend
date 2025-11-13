"use client";
import { signIn } from "next-auth/react";
import Link from "next/link";

export default function SignIn() {
  return (
    <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        {/* Logo & Header */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-block">
            <h2 className="text-3xl font-bold mb-2 text-white">Levqor</h2>
          </Link>
          <h1 className="text-2xl font-semibold text-white mb-2">Sign in to Levqor</h1>
          <p className="text-sm text-slate-400">Access your workflows and run history.</p>
        </div>

        {/* Sign-in Card */}
        <div className="bg-slate-900/80 backdrop-blur border border-slate-800 rounded-2xl p-8 shadow-2xl">
          <div className="space-y-4">
            {/* Google Sign-in */}
            <button 
              onClick={() => signIn("google", { callbackUrl: "/workflow" })} 
              className="w-full flex items-center justify-center gap-3 rounded-xl border-2 border-slate-700 bg-slate-800/50 text-white py-3 px-4 hover:bg-slate-800 hover:border-slate-600 transition-all font-medium"
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
              onClick={() => signIn("azure-ad", { callbackUrl: "/workflow" })} 
              className="w-full flex items-center justify-center gap-3 rounded-xl border-2 border-slate-700 bg-slate-800/50 text-white py-3 px-4 hover:bg-slate-800 hover:border-slate-600 transition-all font-medium"
            >
              <svg className="w-5 h-5" viewBox="0 0 23 23">
                <path fill="#f35325" d="M0 0h11v11H0z"/>
                <path fill="#81bc06" d="M12 0h11v11H12z"/>
                <path fill="#05a6f0" d="M0 12h11v11H0z"/>
                <path fill="#ffba08" d="M12 12h11v11H12z"/>
              </svg>
              Sign in with Microsoft
            </button>

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
          </div>

          {/* Footer */}
          <p className="mt-8 text-xs text-slate-400 text-center">
            By continuing, you agree to our{" "}
            <Link href="/terms" className="underline hover:text-white">Terms</Link>
            {" "}and{" "}
            <Link href="/privacy" className="underline hover:text-white">Privacy Policy</Link>.
          </p>
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
// FORCE GIT CHANGE 1763048430
