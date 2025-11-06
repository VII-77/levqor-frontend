interface USP {
  title: string;
  description: string;
  icon: string;
}

interface LandingData {
  usp: USP[];
}

async function getLandingData(): Promise<LandingData> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_ASSETS_BASE}/marketing/landing_snippets.json`, {
      cache: 'no-store',
    });
    
    if (!res.ok) {
      throw new Error('Failed to fetch landing data');
    }
    
    return res.json();
  } catch (error) {
    console.error('Error fetching landing data:', error);
    return { usp: [] };
  }
}

export default async function USPGrid() {
  const data = await getLandingData();

  if (!data.usp || data.usp.length === 0) {
    return null;
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
      gap: '24px',
      margin: '40px 0',
    }}>
      {data.usp.map((item, index) => (
        <div
          key={index}
          style={{
            padding: '24px',
            border: '1px solid #e0e0e0',
            borderRadius: '8px',
            backgroundColor: '#fff',
          }}
        >
          <div style={{ fontSize: '32px', marginBottom: '12px' }}>
            {item.icon === 'rocket' && '🚀'}
            {item.icon === 'shield' && '🛡️'}
            {item.icon === 'chart' && '📊'}
            {item.icon === 'plug' && '🔌'}
          </div>
          <h3 style={{ fontSize: '20px', fontWeight: 600, marginBottom: '8px' }}>
            {item.title}
          </h3>
          <p style={{ color: '#666', lineHeight: 1.6 }}>
            {item.description}
          </p>
        </div>
      ))}
    </div>
  );
}
