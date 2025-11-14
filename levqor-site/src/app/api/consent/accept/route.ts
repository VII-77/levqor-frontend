import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { email, tosVersion, privacyVersion, marketingConsent, provider } = body;

    // Get IP from headers (best-effort)
    const forwarded = request.headers.get('x-forwarded-for');
    const ip = forwarded ? forwarded.split(',')[0].trim() : request.headers.get('x-real-ip') || 'unknown';

    // Get user agent
    const userAgent = request.headers.get('user-agent') || 'unknown';

    // Log to server console as structured JSON
    const logEntry = {
      type: 'tos_accept',
      email: email || 'unknown',
      tosVersion: tosVersion || '2024-11-01',
      privacyVersion: privacyVersion || '2024-11-01',
      marketingConsent: marketingConsent || false,
      provider: provider || 'unknown',
      ip,
      userAgent,
      ts: new Date().toISOString(),
    };

    console.log(JSON.stringify(logEntry));

    // If marketing consent is true and email exists, queue double opt-in (stub)
    if (marketingConsent && email) {
      queueMarketingDoubleOptIn(email);
    }

    return NextResponse.json({ ok: true }, { status: 200 });
  } catch (error) {
    console.error('Consent API error:', error);
    return NextResponse.json(
      { ok: false, error: 'Failed to log consent' },
      { status: 500 }
    );
  }
}

/**
 * Stub function for marketing double opt-in
 * TODO: Later integrate with Resend/Mail provider to send confirmation email
 */
function queueMarketingDoubleOptIn(email: string) {
  // This is a stub - just log to console for now
  console.log(JSON.stringify({
    type: 'marketing_double_opt_in_stub',
    email,
    ts: new Date().toISOString(),
  }));
}
