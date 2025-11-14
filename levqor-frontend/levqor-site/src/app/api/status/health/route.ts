/**
 * System Health Check API
 * Returns JSON health status for monitoring and status page
 */

import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET() {
  const timestamp = new Date().toISOString();
  
  try {
    // Check backend health
    const backendHealthResponse = await fetch(`${BACKEND_URL}/health`, {
      cache: 'no-store',
      signal: AbortSignal.timeout(5000) // 5 second timeout
    });
    
    const backendHealth = await backendHealthResponse.json();
    const backendOk = backendHealthResponse.ok && backendHealth.ok;
    
    // Overall system health
    const systemOk = backendOk;
    
    return NextResponse.json({
      ok: systemOk,
      timestamp,
      components: {
        frontend: {
          ok: true,
          service: 'Next.js Frontend',
          latencyMs: 0
        },
        backend: {
          ok: backendOk,
          service: 'Flask API',
          latencyMs: backendHealth.ts ? Date.now() - (backendHealth.ts * 1000) : null
        },
        database: {
          ok: backendOk, // Backend health implies DB is working
          service: 'SQLite/PostgreSQL'
        },
        scheduler: {
          ok: backendOk, // Assume scheduler is working if backend is up
          service: 'APScheduler'
        }
      },
      status: systemOk ? 'operational' : 'degraded'
    }, { 
      status: systemOk ? 200 : 503,
      headers: {
        'Cache-Control': 'no-store, must-revalidate',
        'Content-Type': 'application/json'
      }
    });
    
  } catch (error) {
    // Backend is down or unreachable
    return NextResponse.json({
      ok: false,
      timestamp,
      components: {
        frontend: {
          ok: true,
          service: 'Next.js Frontend',
          latencyMs: 0
        },
        backend: {
          ok: false,
          service: 'Flask API',
          error: 'Connection failed'
        },
        database: {
          ok: false,
          service: 'SQLite/PostgreSQL',
          error: 'Backend unreachable'
        },
        scheduler: {
          ok: false,
          service: 'APScheduler',
          error: 'Backend unreachable'
        }
      },
      status: 'major_outage',
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { 
      status: 503,
      headers: {
        'Cache-Control': 'no-store, must-revalidate',
        'Content-Type': 'application/json'
      }
    });
  }
}
