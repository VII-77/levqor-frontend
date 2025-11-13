type Plan = { name: string; price: string; period: string; points: string[]; cta: string; href: string; featured?: boolean };

const PLANS: Plan[] = [
  { name: 'Starter', price: '£0', period: '/mo', points: ['100 runs', 'Email + Webhooks', 'Community support'], cta: 'Start free', href: '/signin' },
  { name: 'Pro', price: '£49', period: '/mo', points: ['10k runs', 'All connectors', 'Priority support'], cta: 'Upgrade', href: '/signin', featured: true },
  { name: 'Business', price: '£149', period: '/mo', points: ['50k runs', 'SLA + SSO', 'Audit exports'], cta: 'Talk to sales', href: '/contact' },
];

export default function Pricing() {
  return (
    <div className="grid md:grid-cols-3 gap-4 md:gap-6">
      {PLANS.map((p) => (
        <div
          key={p.name}
          className={`rounded-2xl p-6 border ${p.featured ? 'border-[var(--accent)]' : 'border-white/10'} bg-[var(--card)]`}
        >
          <div className="text-xl font-semibold">{p.name}</div>
          <div className="mt-3 text-3xl font-bold">
            {p.price}
            <span className="text-base opacity-70">{p.period}</span>
          </div>
          <ul className="mt-4 space-y-2 text-sm opacity-90">
            {p.points.map((x) => (
              <li key={x}>• {x}</li>
            ))}
          </ul>
          <a
            href={p.href}
            className={`mt-6 inline-block w-full text-center px-4 py-2 rounded-lg ${
              p.featured ? 'bg-[var(--accent)] text-white' : 'border border-white/10 hover:border-white/20'
            }`}
          >
            {p.cta}
          </a>
        </div>
      ))}
    </div>
  );
}
