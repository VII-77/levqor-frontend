"use client";
import { useState, useEffect, useRef } from "react";

export default function LogsPage() {
  const [logs, setLogs] = useState<any[]>([]);
  const [connected, setConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    // Fetch recent logs first
    fetch("/api/logs/recent")
      .then(r => r.json())
      .then(data => {
        if (data.logs) {
          setLogs(data.logs);
        }
      })
      .catch(console.error);

    // Connect to SSE stream
    const sse = new EventSource("/api/logs/stream");
    
    sse.onopen = () => {
      setConnected(true);
    };

    sse.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLogs(prev => [...prev, data].slice(-100)); // Keep last 100
      } catch (err) {
        console.error("Failed to parse event:", err);
      }
    };

    sse.onerror = () => {
      setConnected(false);
    };

    eventSourceRef.current = sse;

    return () => {
      sse.close();
    };
  }, []);

  const formatTime = (ts: number) => {
    return new Date(ts * 1000).toLocaleTimeString();
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-12">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-semibold">Realtime Logs</h1>
        <div className="flex items-center gap-2">
          <span
            className={`inline-block w-2 h-2 rounded-full ${
              connected ? "bg-green-500" : "bg-red-500"
            }`}
          ></span>
          <span className="text-sm text-gray-600">
            {connected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>

      <div className="rounded border bg-gray-50 dark:bg-gray-900 p-4 h-[600px] overflow-y-auto font-mono text-xs">
        {logs.length === 0 && (
          <p className="text-gray-500">No logs yet. Waiting for events...</p>
        )}
        {logs.map((log, i) => (
          <div key={i} className="mb-1 hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded">
            <span className="text-gray-500">[{formatTime(log.ts)}]</span>{" "}
            <span className="text-blue-600 dark:text-blue-400">{log.event}</span>{" "}
            <span className="text-gray-700 dark:text-gray-300">
              {JSON.stringify(log, null, 0).slice(0, 200)}
            </span>
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-500 mt-3">
        Server-Sent Events (SSE) stream. Last 100 events displayed.
      </p>
    </main>
  );
}
