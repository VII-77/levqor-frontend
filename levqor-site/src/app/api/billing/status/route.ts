import { NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';

export async function GET() {
  try {
    const session = await getServerSession();
    
    if (!session?.user?.email) {
      return NextResponse.json({ ok: true, status: 'ok' });
    }

    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    const response = await fetch(`${backendUrl}/api/billing/status?user_id=${encodeURIComponent(session.user.email)}`, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      return NextResponse.json({ ok: true, status: 'ok' });
    }

    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('[Billing Status Error]', error);
    return NextResponse.json({ ok: true, status: 'ok' });
  }
}
