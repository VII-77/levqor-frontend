'use client';
import { useEffect, useState } from 'react';
import { useSession, signIn } from 'next-auth/react';

type Flow = { id: string; name: string; status: 'healthy' | 'degraded' | 'failed'; runs: number };

export default function Page() {
  const { status, data } = useSession();
  const [items, setItems] = useState<Flow[] | null>(null);
  const [err, setErr] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (status === 'loading') return;
    if (status === 'unauthenticated') {
      signIn(undefined, { callbackUrl: '/workflow' });
      return;
    }
    (async () => {
      try {
        const res = await fetch('/api/workflows', { cache: 'no-store' });
        if (!res.ok) throw new Error(String(res.status));
        const json = await res.json();
        const mapped: Flow[] = Array.isArray(json?.items)
          ? json.items.map((x: any) => ({
              id: String(x.id || x.name),
              name: x.name || 'Flow',
              status: x.status || 'healthy',
              runs: Number(x.runs || 0),
            }))
          : [];
        setItems(mapped);
      } catch (e: any) {
        setErr(e?.message || 'error');
      } finally {
        setLoading(false);
      }
    })();
  }, [status]);

  if (status === 'loading' || loading) return <div className="max-w-6xl mx-auto px-6 py-12">Loading workflows…</div>;
  if (err) return <div className="max-w-6xl mx-auto px-6 py-12 text-sm opacity-80">Error: {err}</div>;

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 space-y-6">
      <h1 className="text-2xl font-bold">Workflows</h1>
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {items?.map((f) => (
          <a
            key={f.id}
            href={`/workflow/${encodeURIComponent(f.id)}`}
            className="rounded-2xl bg-white p-4 border border-gray-200 hover:border-gray-300 hover:shadow-md transition"
          >
            <div className="flex items-center justify-between">
              <div className="font-medium">{f.name}</div>
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-700">{f.status}</span>
            </div>
            <div className="mt-2 text-sm text-gray-600">{f.runs} runs this week</div>
          </a>
        ))}
      </div>
      {items && items.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <p className="mb-4">No workflows yet</p>
          <a href="/docs" className="text-blue-600 hover:underline">
            Learn how to create your first workflow
          </a>
        </div>
      )}
    </div>
  );
}
