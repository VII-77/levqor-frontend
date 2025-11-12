'use client';
import { useEffect, useState } from 'react';
import { useSession, signIn } from 'next-auth/react';

type Flow = { id: string; name: string; status: string; runs?: number };

export default function Page() {
  const { status } = useSession();
  const [items, setItems] = useState<Flow[] | null>(null);
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
        if (res.status === 401) return;
        const { items: data = [] } = await res.json().catch(() => ({ items: [] }));
        setItems(data);
      } catch (e) {
        setItems([]);
      } finally {
        setLoading(false);
      }
    })();
  }, [status]);

  if (status === 'loading' || loading) {
    return (
      <main className="max-w-6xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-semibold mb-4">Workflows</h1>
        <div className="h-24 rounded-2xl border animate-pulse bg-gray-50" />
      </main>
    );
  }

  return (
    <main className="max-w-6xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold mb-4">Workflows</h1>
      {!items || items.length === 0 ? (
        <div className="rounded-2xl border p-6 text-sm text-neutral-600">
          No workflows yet. Create one from the builder.
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((w: Flow) => (
            <div key={w.id} className="rounded-2xl border p-4 hover:shadow-md transition">
              <div className="text-base font-semibold">{w.name || 'Workflow'}</div>
              <div className="text-xs mt-1 opacity-70">{w.status || 'idle'}</div>
              {w.runs !== undefined && (
                <div className="text-sm mt-2 text-neutral-600">{w.runs} runs</div>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
