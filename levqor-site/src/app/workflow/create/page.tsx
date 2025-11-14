'use client';

import { useState } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import HighRiskWarning from '@/components/HighRiskWarning';

export default function CreateWorkflowPage() {
  const { data: session, status } = useSession();
  const router = useRouter();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [steps, setSteps] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/workflows/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description, steps }),
      });

      const data = await response.json();

      if (!response.ok || !data.ok) {
        throw new Error(data.error || 'Failed to create workflow');
      }

      router.push('/workflow');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setLoading(false);
    }
  };

  if (status === 'loading') {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </main>
    );
  }

  if (status === 'unauthenticated') {
    router.push('/signin?returnTo=/workflow/create');
    return null;
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="max-w-3xl mx-auto px-4 py-12">
        <div className="mb-8">
          <Link href="/workflow" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to workflows
          </Link>
        </div>

        <h1 className="text-4xl font-bold mb-2">Create New Workflow</h1>
        <p className="text-slate-400 mb-8">
          Design and automate your business processes
        </p>

        <HighRiskWarning />

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="title" className="block text-sm font-medium text-slate-300 mb-2">
              Workflow Title *
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g., Daily sales report automation"
              className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none"
              required
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium text-slate-300 mb-2">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what this workflow does..."
              rows={4}
              className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none resize-none"
              disabled={loading}
            />
          </div>

          <div>
            <label htmlFor="steps" className="block text-sm font-medium text-slate-300 mb-2">
              Workflow Steps
            </label>
            <textarea
              id="steps"
              value={steps}
              onChange={(e) => setSteps(e.target.value)}
              placeholder="Describe the automation steps..."
              rows={6}
              className="w-full rounded-lg border-2 border-slate-700 bg-slate-800/50 py-3 px-4 text-white focus:border-emerald-500 focus:outline-none resize-none"
              disabled={loading}
            />
          </div>

          {error && (
            <div className="p-4 bg-red-950/50 border border-red-900/50 rounded-lg">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={!title || loading}
              className={`flex-1 py-3 rounded-lg font-semibold transition ${
                title && !loading
                  ? 'bg-emerald-500 hover:bg-emerald-600 text-white cursor-pointer'
                  : 'bg-slate-800 text-slate-500 cursor-not-allowed'
              }`}
            >
              {loading ? 'Creating...' : 'Create Workflow'}
            </button>
            <Link
              href="/workflow"
              className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-semibold transition"
            >
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </main>
  );
}
