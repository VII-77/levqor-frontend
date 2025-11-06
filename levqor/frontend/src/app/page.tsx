'use client'

import { useState, useEffect } from 'react'
import StatusCard from '@/components/StatusCard'

export default function Home() {
  const [systemStatus, setSystemStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://7bcf7cfb-abac-4066-a19e-5fbe1b6c0854-00-msem1k2vhtji.kirk.replit.dev'
        const response = await fetch(`${apiUrl}/ops/heartbeat`)
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        
        const data = await response.json()
        setSystemStatus(data)
        setError(null)
      } catch (err) {
        console.error('Failed to fetch system status:', err)
        setError('Unable to connect to backend')
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <main style={{
      minHeight: '100vh',
      padding: '2rem',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center'
    }}>
      <div style={{
        maxWidth: '1200px',
        width: '100%'
      }}>
        <header style={{
          textAlign: 'center',
          marginBottom: '3rem'
        }}>
          <h1 style={{
            fontSize: '3.5rem',
            fontWeight: 'bold',
            marginBottom: '1rem',
            background: 'linear-gradient(to right, #fff, #e0e7ff)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            Levqor
          </h1>
          <p style={{
            fontSize: '1.25rem',
            opacity: 0.9,
            maxWidth: '600px',
            margin: '0 auto'
          }}>
            AI-Powered Enterprise Automation Platform
          </p>
          <div style={{
            marginTop: '1rem',
            display: 'flex',
            gap: '1rem',
            justifyContent: 'center',
            flexWrap: 'wrap'
          }}>
            <a 
              href={`${process.env.NEXT_PUBLIC_API_URL || 'https://7bcf7cfb-abac-4066-a19e-5fbe1b6c0854-00-msem1k2vhtji.kirk.replit.dev'}/legal/privacy`}
              style={{
                padding: '0.5rem 1rem',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '0.5rem',
                fontSize: '0.875rem',
                transition: 'background 0.2s'
              }}
            >
              Privacy Policy
            </a>
            <a 
              href={`${process.env.NEXT_PUBLIC_API_URL || 'https://7bcf7cfb-abac-4066-a19e-5fbe1b6c0854-00-msem1k2vhtji.kirk.replit.dev'}/legal/terms`}
              style={{
                padding: '0.5rem 1rem',
                background: 'rgba(255,255,255,0.1)',
                borderRadius: '0.5rem',
                fontSize: '0.875rem',
                transition: 'background 0.2s'
              }}
            >
              Terms of Service
            </a>
          </div>
        </header>

        <StatusCard
          status={systemStatus}
          loading={loading}
          error={error}
        />

        <footer style={{
          marginTop: '3rem',
          textAlign: 'center',
          opacity: 0.7,
          fontSize: '0.875rem'
        }}>
          <p>Production-Ready Enterprise AI Automation</p>
          <p style={{ marginTop: '0.5rem' }}>
            Powered by EchoPilot AI
          </p>
        </footer>
      </div>
    </main>
  )
}
