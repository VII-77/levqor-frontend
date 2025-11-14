"use client";
import { useSession } from "next-auth/react";
import { useState, useEffect } from "react";
import Link from "next/link";

interface DFYOrder {
  id: number;
  tier: string;
  status: string;
  deadline: string | null;
  revisions_left: number;
  files: Array<{ filename: string; url: string; size: number }>;
  final_package_url: string | null;
  created_at: string;
}

export default function DeliveryDashboard() {
  const { data: session, status } = useSession();
  const [orders, setOrders] = useState<DFYOrder[]>([]);
  const [loading, setLoading] = useState(true);
  const [revisionForm, setRevisionForm] = useState<{ orderId: number | null; description: string }>({
    orderId: null,
    description: ""
  });

  useEffect(() => {
    if (status === "authenticated" && session?.user?.email) {
      fetchOrders(session.user.email);
    } else if (status === "unauthenticated") {
      setLoading(false);
    }
  }, [status, session]);

  const fetchOrders = async (email: string) => {
    try {
      const response = await fetch(`/api/dfy/orders?email=${encodeURIComponent(email)}`);
      const data = await response.json();
      
      if (data.ok) {
        setOrders(data.orders || []);
      }
    } catch (error) {
      console.error("Failed to fetch orders:", error);
    } finally {
      setLoading(false);
    }
  };

  const requestRevision = async () => {
    if (!revisionForm.orderId || !revisionForm.description.trim()) return;

    try {
      const response = await fetch("/api/dfy/revision", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          order_id: revisionForm.orderId,
          description: revisionForm.description
        })
      });

      const data = await response.json();

      if (data.ok) {
        alert("Revision requested successfully!");
        setRevisionForm({ orderId: null, description: "" });
        if (session?.user?.email) {
          fetchOrders(session.user.email);
        }
      } else {
        alert(data.error || "Failed to request revision");
      }
    } catch (error) {
      alert("Network error");
    }
  };

  if (status === "loading" || loading) {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </main>
    );
  }

  if (status === "unauthenticated") {
    return (
      <main className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-4">Sign in required</h1>
          <Link href="/signin" className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
            Sign In
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-950">
      <header className="border-b border-slate-800">
        <nav className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link href="/" className="text-lg font-bold text-white">Levqor</Link>
          <Link href="/dashboard" className="text-sm text-slate-300 hover:text-white transition">Dashboard</Link>
        </nav>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-16">
        <h1 className="text-3xl font-bold text-white mb-8">DFY Delivery Dashboard</h1>

        {orders.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-slate-400 mb-6">No DFY orders found</p>
            <Link href="/pricing#dfy" className="inline-block px-8 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition">
              Order DFY Build
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {orders.map(order => (
              <div key={order.id} className="bg-slate-900/50 border border-slate-800 rounded-2xl p-8">
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-white mb-2">
                      {order.tier.charAt(0).toUpperCase() + order.tier.slice(1)} DFY
                    </h2>
                    <p className="text-slate-400">Order #{order.id}</p>
                  </div>
                  <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                    order.status === "COMPLETE" ? "bg-emerald-500/20 text-emerald-400" :
                    order.status === "IN_PROGRESS" ? "bg-blue-500/20 text-blue-400" :
                    order.status === "REVISION" ? "bg-amber-500/20 text-amber-400" :
                    "bg-slate-700 text-slate-300"
                  }`}>
                    {order.status}
                  </span>
                </div>

                <div className="grid md:grid-cols-3 gap-6 mb-6">
                  <div>
                    <p className="text-slate-500 text-sm mb-1">Deadline</p>
                    <p className="text-white font-semibold">
                      {order.deadline ? new Date(order.deadline).toLocaleDateString() : "TBD"}
                    </p>
                  </div>
                  <div>
                    <p className="text-slate-500 text-sm mb-1">Revisions Left</p>
                    <p className="text-white font-semibold">{order.revisions_left}</p>
                  </div>
                  <div>
                    <p className="text-slate-500 text-sm mb-1">Created</p>
                    <p className="text-white font-semibold">
                      {new Date(order.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                {order.final_package_url && (
                  <div className="mb-6">
                    <a
                      href={order.final_package_url}
                      className="inline-block px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition"
                    >
                      Download Final Package
                    </a>
                  </div>
                )}

                {order.revisions_left > 0 && order.status !== "COMPLETE" && (
                  <div className="pt-6 border-t border-slate-800">
                    <h3 className="text-lg font-bold text-white mb-4">Request Revision</h3>
                    {revisionForm.orderId === order.id ? (
                      <div className="space-y-4">
                        <textarea
                          value={revisionForm.description}
                          onChange={(e) => setRevisionForm({ ...revisionForm, description: e.target.value })}
                          className="w-full px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-white focus:border-emerald-500 focus:outline-none resize-none"
                          rows={4}
                          placeholder="Describe what you'd like revised..."
                        />
                        <div className="flex gap-4">
                          <button
                            onClick={requestRevision}
                            className="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-900 rounded-lg font-semibold transition"
                          >
                            Submit Revision
                          </button>
                          <button
                            onClick={() => setRevisionForm({ orderId: null, description: "" })}
                            className="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition"
                          >
                            Cancel
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button
                        onClick={() => setRevisionForm({ orderId: order.id, description: "" })}
                        className="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-semibold transition"
                      >
                        Request Revision ({order.revisions_left} left)
                      </button>
                    )}
                  </div>
                )}

                {order.revisions_left === 0 && order.status !== "COMPLETE" && (
                  <div className="pt-6 border-t border-slate-800">
                    <p className="text-amber-400">No revisions remaining for this order</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
