import { NextResponse } from 'next/server';
import { auth } from '@/auth';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'https://api.levqor.ai';

export async function GET(request: Request) {
  const session = await auth();
  
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    const response = await fetch(`${API_BASE}/api/intelligence/recommendations`, {
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error(`Backend API returned ${response.status}`);
    }

    const data = await response.json();
    
    const items = Array.isArray(data?.items) ? data.items : [];
    
    return NextResponse.json({ items });
  } catch (error: any) {
    console.error('Workflows API error:', error);
    return NextResponse.json(
      { items: [], error: error.message },
      { status: 500 }
    );
  }
}
