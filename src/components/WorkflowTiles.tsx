type Tile = { title: string; desc: string; href: string };

const TILES: Tile[] = [
  { title: 'Self-healing runs', desc: 'Auto-retry with backoff and diff isolation.', href: '/workflow' },
  { title: 'Visual builder', desc: 'Drag-drop steps, inline AI prompts, reusable blocks.', href: '/workflow' },
  { title: 'Audit & governance', desc: 'Signed, searchable, exportable changes.', href: '/workflow' },
  { title: 'Connect anything', desc: 'Email, Sheets, Slack, Webhooks, CRMs.', href: '/workflow' },
];

export default function WorkflowTiles() {
  return (
    <section className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
      {TILES.map((t) => (
        <a
          key={t.title}
          href={t.href}
          className="rounded-2xl bg-[var(--card)] p-4 md:p-5 border border-white/5 hover:border-white/15 transition"
        >
          <div className="font-semibold">{t.title}</div>
          <div className="mt-2 text-sm opacity-80">{t.desc}</div>
        </a>
      ))}
    </section>
  );
}
