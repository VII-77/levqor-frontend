import { auth, signOut } from '@/auth'
import { redirect } from 'next/navigation'

export default async function Dashboard() {
  const session = await auth()
  
  if (!session?.user) {
    redirect('/signin')
  }

  return (
    <main style={{ minHeight: '100vh', background: '#f5f5f5', padding: '2rem' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <header style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '2rem',
          padding: '1.5rem',
          background: 'white',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <div>
            <h1 style={{ fontSize: '1.5rem', marginBottom: '0.25rem' }}>Dashboard</h1>
            <p style={{ color: '#666' }}>Welcome, {session.user.email}</p>
          </div>
          <form action={async () => {
            'use server'
            await signOut()
          }}>
            <button
              type="submit"
              style={{
                padding: '0.5rem 1.5rem',
                background: '#ff4444',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                fontWeight: '500'
              }}
            >
              Sign Out
            </button>
          </form>
        </header>

        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: '1.5rem' 
        }}>
          <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Active Jobs</h2>
            <p style={{ fontSize: '2rem', fontWeight: 'bold', color: '#0070f3' }}>0</p>
            <p style={{ color: '#666', fontSize: '0.875rem' }}>No active automation jobs</p>
          </div>

          <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>API Status</h2>
            <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#10b981' }}>Operational</p>
            <p style={{ color: '#666', fontSize: '0.875rem' }}>Backend: api.levqor.ai</p>
          </div>

          <div style={{ background: 'white', padding: '2rem', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
            <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>Account</h2>
            <p style={{ fontSize: '1rem', fontWeight: '500', color: '#333' }}>{session.user.email}</p>
            <p style={{ color: '#666', fontSize: '0.875rem' }}>Free tier</p>
          </div>
        </div>

        <div style={{ 
          marginTop: '2rem', 
          background: 'white', 
          padding: '2rem', 
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>Quick Actions</h2>
          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <button style={{
              padding: '0.75rem 1.5rem',
              background: '#0070f3',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontWeight: '500'
            }}>
              Create New Job
            </button>
            <button style={{
              padding: '0.75rem 1.5rem',
              border: '2px solid #0070f3',
              color: '#0070f3',
              background: 'transparent',
              borderRadius: '6px',
              fontWeight: '500'
            }}>
              View API Docs
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}
