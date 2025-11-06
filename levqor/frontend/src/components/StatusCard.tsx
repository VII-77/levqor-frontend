'use client'

interface StatusCardProps {
  status: any
  loading: boolean
  error: string | null
}

export default function StatusCard({ status, loading, error }: StatusCardProps) {
  if (loading) {
    return (
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)',
        borderRadius: '1rem',
        padding: '2rem',
        textAlign: 'center'
      }}>
        <p>Loading system status...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div style={{
        background: 'rgba(239, 68, 68, 0.2)',
        backdropFilter: 'blur(10px)',
        borderRadius: '1rem',
        padding: '2rem',
        textAlign: 'center',
        border: '1px solid rgba(239, 68, 68, 0.3)'
      }}>
        <p style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>⚠️ {error}</p>
        <p style={{ opacity: 0.8, fontSize: '0.875rem' }}>
          Backend: {process.env.NEXT_PUBLIC_API_URL || 'https://7bcf7cfb-abac-4066-a19e-5fbe1b6c0854-00-msem1k2vhtji.kirk.replit.dev'}
        </p>
      </div>
    )
  }

  const data = status?.data || status
  const overall = data?.overall || 'unknown'
  const sloUptime = data?.components?.slo?.current_uptime || 0
  
  return (
    <div style={{
      background: 'rgba(255,255,255,0.1)',
      backdropFilter: 'blur(10px)',
      borderRadius: '1rem',
      padding: '2rem',
      border: '1px solid rgba(255,255,255,0.2)'
    }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1.5rem'
      }}>
        <div>
          <p style={{ opacity: 0.8, fontSize: '0.875rem', marginBottom: '0.5rem' }}>Status</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            {overall === 'healthy' ? '✅ Online' : '⚠️ ' + overall}
          </p>
        </div>
        
        <div>
          <p style={{ opacity: 0.8, fontSize: '0.875rem', marginBottom: '0.5rem' }}>SLO Uptime</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            {sloUptime.toFixed(1)}%
          </p>
        </div>
        
        <div>
          <p style={{ opacity: 0.8, fontSize: '0.875rem', marginBottom: '0.5rem' }}>Scheduler</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            {data?.components?.scheduler?.status === 'stopped' ? '⚠️ Stopped' : '✅ Running'}
          </p>
        </div>
        
        <div>
          <p style={{ opacity: 0.8, fontSize: '0.875rem', marginBottom: '0.5rem' }}>Error Budget</p>
          <p style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
            {data?.components?.slo?.error_budget_remaining?.toFixed(1) || '0'}%
          </p>
        </div>
      </div>
      
      {data?.ts && (
        <p style={{
          marginTop: '1.5rem',
          opacity: 0.6,
          fontSize: '0.75rem',
          textAlign: 'center'
        }}>
          Last updated: {new Date(data.ts).toLocaleString()}
        </p>
      )}
    </div>
  )
}
