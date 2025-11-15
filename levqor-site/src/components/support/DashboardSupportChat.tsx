"use client";

import SupportChat from "./SupportChat";

interface DashboardSupportChatProps {
  email?: string;
}

export default function DashboardSupportChat({ email }: DashboardSupportChatProps) {
  return (
    <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-6">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-slate-100">Need Help?</h2>
        <p className="text-sm text-slate-400 mt-1">
          Ask about your automations, orders, or account. Get instant AI-powered support.
        </p>
      </div>

      <div className="h-96">
        <SupportChat 
          mode="private" 
          title="Account Support" 
          showEscalate={true} 
          defaultEmail={email} 
        />
      </div>
    </div>
  );
}
