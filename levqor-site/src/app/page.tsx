import Link from 'next/link'

export default function Home() {
  return (
    <main style={{ textAlign: 'center', padding: '4rem 2rem' }}>
      <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>
        Levqor
      </h1>
      <p style={{ fontSize: '1.5rem', color: '#666', marginBottom: '2rem' }}>
        The Self-Driven Automation Engine
      </p>
      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
        <Link 
          href="/pricing" 
          style={{ 
            padding: '0.75rem 2rem', 
            background: '#0070f3', 
            color: 'white', 
            borderRadius: '6px',
            fontWeight: '500'
          }}
        >
          Pricing
        </Link>
        <Link 
          href="/signin" 
          style={{ 
            padding: '0.75rem 2rem', 
            background: '#0070f3', 
            color: 'white', 
            borderRadius: '6px',
            fontWeight: '500'
          }}
        >
          Sign In
        </Link>
        <Link 
          href="/dashboard" 
          style={{ 
            padding: '0.75rem 2rem', 
            border: '2px solid #0070f3', 
            color: '#0070f3', 
            borderRadius: '6px',
            fontWeight: '500'
          }}
        >
          Dashboard
        </Link>
      </div>
      <div style={{ marginTop: '3rem', padding: '2rem', background: 'white', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
        <h2 style={{ marginBottom: '1rem' }}>Features</h2>
        <ul style={{ listStyle: 'none', textAlign: 'left', maxWidth: '600px', margin: '0 auto' }}>
          <li style={{ padding: '0.5rem 0' }}>✅ Magic Link Authentication</li>
          <li style={{ padding: '0.5rem 0' }}>✅ Protected Dashboard</li>
          <li style={{ padding: '0.5rem 0' }}>✅ Backend API Integration</li>
          <li style={{ padding: '0.5rem 0' }}>✅ Production Ready</li>
        </ul>
      </div>
    </main>
  )
}
