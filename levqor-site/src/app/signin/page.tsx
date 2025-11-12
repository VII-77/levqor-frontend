"use client";
import { signIn } from "next-auth/react";

export default function SignIn() {
  return (
    <main className="min-h-[80svh] grid place-items-center px-4">
      <div className="w-full max-w-md rounded-2xl border p-6 shadow-sm bg-white/5 backdrop-blur">
        <h1 className="text-2xl font-semibold mb-2">Sign in to Levqor</h1>
        <p className="text-sm text-neutral-500 mb-6">Access your workflows and run history.</p>
        <div className="space-y-3">
          <button 
            onClick={() => signIn("google", { callbackUrl: "/workflow" })} 
            className="w-full rounded-xl border py-2 hover:bg-gray-50 transition"
          >
            Continue with Google
          </button>
          <button 
            onClick={() => signIn("azure-ad", { callbackUrl: "/workflow" })} 
            className="w-full rounded-xl border py-2 hover:bg-gray-50 transition"
          >
            Continue with Microsoft
          </button>
        </div>
        <p className="mt-6 text-xs text-neutral-500 text-center">
          By continuing you agree to the Terms and Privacy Policy.
        </p>
      </div>
    </main>
  );
}
