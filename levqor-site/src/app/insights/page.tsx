'use client';

import React, { useEffect, useState } from 'react';

export default function Insights() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('https://api.levqor.ai/api/admin/brief/weekly')
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error('Failed to load insights:', e);
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Operational Insights</h1>
        
        {loading ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-600">Loading insights...</p>
          </div>
        ) : data ? (
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold mb-4">Weekly Brief</h2>
              <p className="text-gray-700 mb-4">{data.summary}</p>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="text-sm text-green-600 font-medium">Uptime</div>
                  <div className="text-2xl font-bold text-green-900">{data.key_metrics?.uptime}</div>
                </div>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="text-sm text-blue-600 font-medium">Errors</div>
                  <div className="text-2xl font-bold text-blue-900">{data.key_metrics?.errors}</div>
                </div>
                
                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                  <div className="text-sm text-purple-600 font-medium">Cost Forecast</div>
                  <div className="text-2xl font-bold text-purple-900">{data.key_metrics?.cost_forecast}</div>
                </div>
              </div>
              
              <div className="mt-4 text-xs text-gray-500">
                Generated at: {new Date(data.generated_at).toLocaleString()}
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <p className="text-red-800">Failed to load insights data</p>
          </div>
        )}
      </div>
    </div>
  );
}
