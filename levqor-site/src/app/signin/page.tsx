import { signIn } from '@/auth'

export default function SignIn() {
  return (
    <main style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div style={{ 
        background: 'white', 
        padding: '3rem', 
        borderRadius: '12px', 
        boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        maxWidth: '400px',
        width: '100%'
      }}>
        <h1 style={{ marginBottom: '0.5rem', fontSize: '2rem' }}>Welcome to Levqor</h1>
        <p style={{ color: '#666', marginBottom: '2rem' }}>Sign in with your email to continue</p>
        
        <form action={async (formData: FormData) => {
          'use server'
          await signIn('resend', formData)
        }}>
          <input
            type="email"
            name="email"
            placeholder="your@email.com"
            required
            style={{
              width: '100%',
              padding: '0.75rem',
              border: '1px solid #ddd',
              borderRadius: '6px',
              fontSize: '1rem',
              marginBottom: '1rem'
            }}
          />
          <button
            type="submit"
            style={{
              width: '100%',
              padding: '0.75rem',
              background: '#0070f3',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontSize: '1rem',
              fontWeight: '500'
            }}
          >
            Send Magic Link
          </button>
        </form>
        
        <p style={{ marginTop: '1.5rem', fontSize: '0.875rem', color: '#666', textAlign: 'center' }}>
          We&apos;ll send you a magic link to sign in
        </p>
      </div>
    </main>
  )
}
