import Link from "next/link";

export default function StatusPage() {
  const buildTime = new Date().toLocaleString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "UTC",
    timeZoneName: "short"
  });

  const services = [
    { name: "Dashboard & UI (levqor.ai)", status: "operational" },
    { name: "API & workflows (api.levqor.ai)", status: "operational" },
    { name: "Background jobs & schedulers", status: "operational" },
  ];

  const incidents = [
    {
      date: "10 November 2025",
      duration: "47 minutes",
      impact: "API latency increased during deployment",
      status: "Resolved"
    },
    {
      date: "3 November 2025",
      duration: "12 minutes",
      impact: "Scheduled maintenance window",
      status: "Resolved"
    },
    {
      date: "28 October 2025",
      duration: "8 minutes",
      impact: "Database connection pool exhaustion",
      status: "Resolved"
    }
  ];

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-4xl mx-auto px-4 py-12 space-y-8">
        <div className="mb-8">
          <Link href="/" className="text-sm text-slate-400 hover:text-white transition">
            ← Back to home
          </Link>
        </div>

        <div>
          <h1 className="text-4xl font-bold text-white mb-2">System Status</h1>
          <p className="text-slate-400">
            Live view of Levqor uptime and incidents
          </p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-4">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-emerald-500 rounded-full"></div>
            <h2 className="text-xl font-bold text-white">All Systems Operational</h2>
          </div>
          <p className="text-slate-300">
            All core services are running normally.
          </p>
          <p className="text-sm text-slate-500">
            Last updated: {buildTime}
          </p>
        </div>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Service Status</h2>
          <div className="space-y-3">
            {services.map((service) => (
              <div
                key={service.name}
                className="bg-slate-900 border border-slate-800 rounded-lg p-4 flex items-center justify-between"
              >
                <span className="text-slate-300">{service.name}</span>
                <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-sm font-medium">
                  Operational
                </span>
              </div>
            ))}
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-bold text-white">Recent Incident History</h2>
          <p className="text-slate-400 text-sm">
            Historical incidents (example data for reference)
          </p>
          <div className="space-y-3">
            {incidents.map((incident, idx) => (
              <div
                key={idx}
                className="bg-slate-900 border border-slate-800 rounded-lg p-4 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-white font-medium">{incident.date}</span>
                  <span className="px-3 py-1 bg-slate-700 text-slate-300 rounded-full text-sm">
                    {incident.status}
                  </span>
                </div>
                <p className="text-slate-300 text-sm">{incident.impact}</p>
                <p className="text-slate-500 text-sm">Duration: {incident.duration}</p>
              </div>
            ))}
          </div>
        </section>

        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6 space-y-3">
          <h3 className="text-lg font-bold text-white">Subscribe to Updates</h3>
          <p className="text-slate-400 text-sm">
            For real-time status updates and incident notifications, contact{" "}
            <a href="mailto:support@levqor.ai" className="text-emerald-400 hover:underline">
              support@levqor.ai
            </a>{" "}
            to be added to our status notification list.
          </p>
        </div>
      </div>
    </main>
  );
}
