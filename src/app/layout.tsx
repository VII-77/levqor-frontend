import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Levqor - AI-Powered Automation Platform',
  description: 'Production-ready enterprise AI automation with real-time monitoring and analytics',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
