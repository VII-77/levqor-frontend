import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, tosVersion, privacyVersion, marketingConsent, provider } = body;

    if (!email) {
      return NextResponse.json({ ok: false, error: 'Email required' }, { status: 400 });
    }

    const backendApi = process.env.NEXT_PUBLIC_API_URL || 'https://api.levqor.ai';

    // Log TOS acceptance to backend
    const tosResponse = await fetch(`${backendApi}/api/legal/accept-terms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        tos_version: tosVersion || '2025-Genesis-v1',
        privacy_version: privacyVersion || '2025-Genesis-v1'
      })
    });

    const tosData = await tosResponse.json();

    if (!tosData.ok) {
      console.error('TOS acceptance logging failed:', tosData.error);
    }

    // If marketing consent was given, start subscription process
    if (marketingConsent && email) {
      const marketingResponse = await fetch(`${backendApi}/api/marketing/subscribe`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      const marketingData = await marketingResponse.json();

      if (!marketingData.ok) {
        console.error('Marketing consent logging failed:', marketingData.error);
      }
    }

    return NextResponse.json({ ok: true }, { status: 200 });

  } catch (error) {
    console.error('Consent acceptance error:', error);
    return NextResponse.json({ ok: true }, { status: 200 });
  }
}
