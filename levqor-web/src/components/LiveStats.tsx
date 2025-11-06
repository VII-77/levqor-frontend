interface MarketingStats {
  visits?: number;
  conversions?: number;
  mrr?: number;
  active_users?: number;
  jobs_processed_total?: number;
  uptime_7d?: number;
}

async function getMarketingStats(): Promise<MarketingStats | null> {
  try {
    const res = await fetch(process.env.NEXT_PUBLIC_BACKEND_SUMMARY || '', {
      next: { revalidate: 60 },
    });
    
    if (!res.ok) {
      return null;
    }
    
    return res.json();
  } catch (error) {
    console.error('Error fetching marketing stats:', error);
    return null;
  }
}

export default async function LiveStats() {
  const stats = await getMarketingStats();

  if (!stats || Object.keys(stats).length === 0) {
    return null;
  }

  const metrics = [
    { label: 'Active Users', value: stats.active_users, suffix: '+' },
    { label: 'Jobs Processed', value: stats.jobs_processed_total, suffix: '+' },
    { label: 'Monthly Visits', value: stats.visits, suffix: '+' },
    { label: 'Uptime', value: stats.uptime_7d, suffix: '%' },
  ].filter(m => m.value !== undefined);

  if (metrics.length === 0) {
    return null;
  }

  return (
    <div style={{
      padding: '40px 20px',
      backgroundColor: '#f5f7fa',
      borderRadius: '8px',
      margin: '40px 0',
    }}>
      <h3 style={{
        fontSize: '24px',
        fontWeight: 600,
        textAlign: 'center',
        marginBottom: '32px',
        color: '#333',
      }}>
        Platform Stats
      </h3>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '24px',
        maxWidth: '900px',
        margin: '0 auto',
      }}>
        {metrics.map((metric, index) => (
          <div
            key={index}
            style={{
              textAlign: 'center',
              padding: '20px',
              backgroundColor: '#fff',
              borderRadius: '6px',
            }}
          >
            <div style={{
              fontSize: '32px',
              fontWeight: 700,
              color: '#0066cc',
              marginBottom: '8px',
            }}>
              {metric.value?.toLocaleString()}{metric.suffix}
            </div>
            <div style={{ fontSize: '14px', color: '#666', fontWeight: 500 }}>
              {metric.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
