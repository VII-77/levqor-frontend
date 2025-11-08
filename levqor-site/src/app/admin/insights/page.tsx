'use client';

import React, { useState } from 'react';

export default function AdminInsights() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function runAction(url: string, method: string = 'POST', body?: any) {
    setLoading(true);
    try {
      const response = await fetch(`https://api.levqor.ai${url}`, {
        method,
        headers: body ? { 'Content-Type': 'application/json' } : {},
        body: body ? JSON.stringify(body) : undefined
      });
      const data = await response.json();
      setResult(data);
    } catch (e) {
      setResult({ error: String(e) });
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Admin Insights Panel</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Incident Management</h2>
            <div className="space-y-2">
              <button 
                onClick={() => runAction('/api/admin/incidents/summarize', 'POST', { type: 'api_error', severity: 'high' })}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                Summarize Incident
              </button>
              
              <button 
                onClick={() => runAction('/api/admin/postmortem', 'POST', { 
                  incident: { summary: 'API outage', severity: 'critical', resolution_note: 'Fixed by restarting service' }
                })}
                className="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                Generate Postmortem
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Anomaly Detection</h2>
            <div className="space-y-2">
              <button 
                onClick={() => runAction('/api/admin/anomaly/explain?latency_ms=150', 'GET')}
                className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                Explain Anomaly (150ms)
              </button>
              
              <button 
                onClick={() => runAction('/api/admin/anomaly/explain?latency_ms=500', 'GET')}
                className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                Explain Anomaly (500ms)
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Operational Runbooks</h2>
            <div className="space-y-2">
              <button 
                onClick={() => runAction('/api/admin/runbooks', 'GET')}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                List Runbooks
              </button>
              
              <button 
                onClick={() => runAction('/api/admin/runbooks/apply', 'POST', { key: 'restart_worker', apply: false })}
                className="w-full bg-yellow-600 hover:bg-yellow-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                Preview: Restart Worker
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Reports</h2>
            <div className="space-y-2">
              <button 
                onClick={() => runAction('/api/admin/brief/weekly', 'GET')}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded"
                disabled={loading}
              >
                Weekly Brief
              </button>
            </div>
          </div>
        </div>

        {loading && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
            <p className="text-blue-800">Loading...</p>
          </div>
        )}

        {result && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Result</h2>
            <pre className="bg-gray-100 p-4 rounded overflow-x-auto text-sm">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
