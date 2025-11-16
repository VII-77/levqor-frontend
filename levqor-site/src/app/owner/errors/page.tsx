"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

interface ErrorEvent {
  id: number;
  created_at: string;
  source: string;
  service: string;
  path_or_screen?: string;
  user_email?: string;
  severity: string;
  message: string;
  stack?: string;
}

interface ErrorResponse {
  ok: boolean;
  errors: ErrorEvent[];
  count: number;
}

export default function OwnerErrorsPage() {
  const [errors, setErrors] = useState<ErrorEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [selectedError, setSelectedError] = useState<ErrorEvent | null>(null);
  const [filter, setFilter] = useState({
    severity: "",
    source: "",
    service: "",
  });

  const fetchErrors = async () => {
    try {
      setLoading(true);
      setErrorMsg(null);

      const internalSecret = process.env.NEXT_PUBLIC_INTERNAL_SECRET || "";
      const apiBase = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";

      const params = new URLSearchParams({ limit: "100" });
      if (filter.severity) params.append("severity", filter.severity);
      if (filter.source) params.append("source", filter.source);
      if (filter.service) params.append("service", filter.service);

      const response = await fetch(`${apiBase}/api/errors/recent?${params.toString()}`, {
        headers: {
          "X-Internal-Secret": internalSecret,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data: ErrorResponse = await response.json();
      setErrors(data.errors);
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "Failed to load errors");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchErrors();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const getSeverityBadge = (severity: string) => {
    const colors = {
      critical: "bg-red-500 text-white",
      error: "bg-orange-500 text-white",
      warning: "bg-yellow-500 text-black",
      info: "bg-blue-500 text-white",
    };
    return colors[severity as keyof typeof colors] || "bg-gray-500 text-white";
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleString("en-GB", {
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="inline-flex items-center gap-2 rounded-full border border-red-500/40 bg-red-500/10 px-3 py-1 text-xs font-medium text-red-200 mb-4">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Owner/Administrator Only - Error Monitoring
          </div>
          <h1 className="text-4xl font-bold mb-2 text-white">Error Dashboard</h1>
          <p className="text-slate-400">
            Real-time error monitoring for frontend and backend (replaces Sentry)
          </p>
        </div>

        {/* Stats */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
            <div className="text-slate-400 text-sm mb-1">Total Errors</div>
            <div className="text-2xl font-bold text-white">{errors.length}</div>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
            <div className="text-slate-400 text-sm mb-1">Critical</div>
            <div className="text-2xl font-bold text-red-400">
              {errors.filter((e) => e.severity === "critical").length}
            </div>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
            <div className="text-slate-400 text-sm mb-1">Errors</div>
            <div className="text-2xl font-bold text-orange-400">
              {errors.filter((e) => e.severity === "error").length}
            </div>
          </div>
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
            <div className="text-slate-400 text-sm mb-1">Warnings</div>
            <div className="text-2xl font-bold text-yellow-400">
              {errors.filter((e) => e.severity === "warning").length}
            </div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4 mb-6">
          <div className="grid md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Severity</label>
              <select
                value={filter.severity}
                onChange={(e) => setFilter({ ...filter, severity: e.target.value })}
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-slate-100 text-sm"
              >
                <option value="">All</option>
                <option value="critical">Critical</option>
                <option value="error">Error</option>
                <option value="warning">Warning</option>
                <option value="info">Info</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Source</label>
              <select
                value={filter.source}
                onChange={(e) => setFilter({ ...filter, source: e.target.value })}
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-slate-100 text-sm"
              >
                <option value="">All</option>
                <option value="backend">Backend</option>
                <option value="frontend">Frontend</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">Service</label>
              <input
                type="text"
                value={filter.service}
                onChange={(e) => setFilter({ ...filter, service: e.target.value })}
                placeholder="Filter by service..."
                className="w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-slate-100 text-sm placeholder-slate-500"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={fetchErrors}
                className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded font-medium transition-colors"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>

        {/* Loading/Error States */}
        {loading && (
          <div className="text-center py-12 text-slate-400">
            <svg className="animate-spin h-8 w-8 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Loading errors...
          </div>
        )}

        {errorMsg && (
          <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-4 mb-6 text-red-200">
            <strong>Error:</strong> {errorMsg}
          </div>
        )}

        {/* Error Table */}
        {!loading && !errorMsg && (
          <div className="bg-slate-900/50 border border-slate-800 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-800/50">
                  <tr className="border-b border-slate-700">
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Time</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Severity</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Source</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Service</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Message</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">User</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {errors.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="px-4 py-8 text-center text-slate-400">
                        No errors found. The system is healthy! 🎉
                      </td>
                    </tr>
                  ) : (
                    errors.map((error) => (
                      <tr
                        key={error.id}
                        className="hover:bg-slate-800/30 transition-colors cursor-pointer"
                        onClick={() => setSelectedError(error)}
                      >
                        <td className="px-4 py-3 text-sm text-slate-300 whitespace-nowrap">
                          {formatDate(error.created_at)}
                        </td>
                        <td className="px-4 py-3 text-sm">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityBadge(error.severity)}`}>
                            {error.severity}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-300">{error.source}</td>
                        <td className="px-4 py-3 text-sm font-mono text-emerald-400">{error.service}</td>
                        <td className="px-4 py-3 text-sm text-slate-300">
                          {error.message.length > 100 ? error.message.substring(0, 100) + "..." : error.message}
                        </td>
                        <td className="px-4 py-3 text-sm text-slate-400">
                          {error.user_email || "-"}
                        </td>
                        <td className="px-4 py-3 text-sm">
                          <button className="text-blue-400 hover:underline text-xs">Details</button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Error Detail Modal */}
        {selectedError && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={() => setSelectedError(null)}>
            <div className="bg-slate-900 border border-slate-700 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
              <div className="sticky top-0 bg-slate-800 px-6 py-4 border-b border-slate-700 flex justify-between items-center">
                <h2 className="text-xl font-bold text-white">Error Details #{selectedError.id}</h2>
                <button
                  onClick={() => setSelectedError(null)}
                  className="text-slate-400 hover:text-white transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              <div className="p-6 space-y-4">
                <div>
                  <div className="text-xs text-slate-400 mb-1">Timestamp</div>
                  <div className="text-slate-100">{formatDate(selectedError.created_at)}</div>
                </div>
                <div className="grid md:grid-cols-3 gap-4">
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Severity</div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityBadge(selectedError.severity)}`}>
                      {selectedError.severity}
                    </span>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Source</div>
                    <div className="text-slate-100">{selectedError.source}</div>
                  </div>
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Service</div>
                    <div className="text-emerald-400 font-mono text-sm">{selectedError.service}</div>
                  </div>
                </div>
                {selectedError.path_or_screen && (
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Path/Screen</div>
                    <div className="text-slate-100 font-mono text-sm">{selectedError.path_or_screen}</div>
                  </div>
                )}
                {selectedError.user_email && (
                  <div>
                    <div className="text-xs text-slate-400 mb-1">User Email</div>
                    <div className="text-slate-100">{selectedError.user_email}</div>
                  </div>
                )}
                <div>
                  <div className="text-xs text-slate-400 mb-1">Message</div>
                  <div className="text-slate-100 bg-slate-800 rounded p-3 font-mono text-sm">{selectedError.message}</div>
                </div>
                {selectedError.stack && (
                  <div>
                    <div className="text-xs text-slate-400 mb-1">Stack Trace</div>
                    <pre className="text-xs text-slate-300 bg-slate-950 rounded p-3 overflow-x-auto border border-slate-700">
                      {selectedError.stack}
                    </pre>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 border-t border-slate-800 pt-6 text-sm text-slate-400">
          <div className="flex gap-6">
            <Link href="/owner/handbook" className="text-blue-400 hover:underline">← Back to Owner Handbook</Link>
            <button onClick={fetchErrors} className="text-blue-400 hover:underline">Refresh Errors</button>
          </div>
          <p className="mt-4">
            This dashboard shows errors logged from both frontend and backend. Critical errors trigger Telegram alerts.
            Daily summaries are sent via email.
          </p>
        </div>
      </div>
    </main>
  );
}
