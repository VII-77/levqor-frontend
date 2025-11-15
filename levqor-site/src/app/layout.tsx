import type { Metadata } from "next";
import { Providers } from "@/components/providers";
import CookieBanner from "@/components/cookies/CookieBanner";
import LoadAnalytics from "@/components/cookies/LoadAnalytics";
import { BillingWarningBanner } from "@/components/BillingWarningBanner";
import PublicHelpWidget from "@/components/support/PublicHelpWidget";
import "./globals.css";

export const metadata: Metadata = {
  title: "Levqor — Automate work. Ship faster.",
  description:
    "Genesis v8.0 • Self-healing automation. Run workflows, monitor failures, and self-heal across your tools.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-50 antialiased tracking-tight">
        <BillingWarningBanner />
        <Providers>{children}</Providers>
        <CookieBanner />
        <LoadAnalytics />
        <PublicHelpWidget />
      </body>
    </html>
  );
}
