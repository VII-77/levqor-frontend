import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/auth";
import { Resend } from "resend";

const BACKEND_API = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";
const resend = new Resend(process.env.RESEND_API_KEY);

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || !session.user?.email) {
      return NextResponse.json(
        { ok: false, error: "UNAUTHENTICATED" },
        { status: 401 }
      );
    }

    const body = await request.json().catch(() => ({}));
    const consent = body.consent || false;

    const userResponse = await fetch(`${BACKEND_API}/api/v1/users/upsert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: session.user.email,
        name: session.user.name || "",
      }),
    });

    if (!userResponse.ok) {
      return NextResponse.json(
        { ok: false, error: "Failed to upsert user" },
        { status: 500 }
      );
    }

    const userData = await userResponse.json();
    const userId = userData.id;

    const x_forwarded_for = request.headers.get("x-forwarded-for");
    const ip = x_forwarded_for ? x_forwarded_for.split(",")[0].trim() : "unknown";

    const consentResponse = await fetch(
      `${BACKEND_API}/api/v1/users/${userId}/marketing-consent`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Forwarded-For": ip,
        },
        body: JSON.stringify({ consent }),
      }
    );

    if (!consentResponse.ok) {
      return NextResponse.json(
        { ok: false, error: "Failed to record marketing consent" },
        { status: 500 }
      );
    }

    const result = await consentResponse.json();
    
    if (consent && result.token && process.env.RESEND_API_KEY) {
      const confirmUrl = `https://www.levqor.ai/marketing/confirm?token=${result.token}`;
      
      try {
        await resend.emails.send({
          from: process.env.AUTH_FROM_EMAIL || "Levqor <no-reply@levqor.ai>",
          to: session.user.email,
          subject: "Confirm your Levqor subscription",
          html: `
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="utf-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="margin: 0; padding: 0; background-color: #0f172a; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
              <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #0f172a; padding: 40px 20px;">
                <tr>
                  <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #1e293b; border-radius: 12px; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);">
                      <tr>
                        <td style="padding: 40px 40px 30px;">
                          <h1 style="color: #ffffff; font-size: 28px; font-weight: bold; margin: 0 0 16px;">
                            Confirm your subscription
                          </h1>
                          <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
                            Hi${result.name ? ` ${result.name}` : ''},
                          </p>
                          <p style="color: #cbd5e1; font-size: 16px; line-height: 1.6; margin: 0 0 24px;">
                            You've opted in to receive product updates, automation tips, and exclusive offers from Levqor. 
                            To complete your subscription, please confirm your email address by clicking the button below:
                          </p>
                          <table cellpadding="0" cellspacing="0" style="margin: 0 0 24px;">
                            <tr>
                              <td style="border-radius: 8px; background-color: #10b981;">
                                <a href="${confirmUrl}" target="_blank" style="display: inline-block; padding: 14px 32px; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 16px;">
                                  Confirm Subscription
                                </a>
                              </td>
                            </tr>
                          </table>
                          <p style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 0 0 24px;">
                            Or copy and paste this link into your browser:<br/>
                            <a href="${confirmUrl}" style="color: #10b981; text-decoration: none; word-break: break-all;">${confirmUrl}</a>
                          </p>
                          <p style="color: #94a3b8; font-size: 14px; line-height: 1.6; margin: 0;">
                            This link will expire in 7 days. If you didn't request this, you can safely ignore this email.
                          </p>
                        </td>
                      </tr>
                      <tr>
                        <td style="background-color: #0f172a; padding: 30px 40px; border-top: 1px solid #334155;">
                          <p style="color: #64748b; font-size: 12px; line-height: 1.6; margin: 0 0 12px;">
                            <strong style="color: #94a3b8;">Levqor</strong><br/>
                            AI-powered workflow automation<br/>
                            www.levqor.ai
                          </p>
                          <p style="color: #64748b; font-size: 12px; line-height: 1.6; margin: 0;">
                            Don't want to receive these emails? <a href="https://www.levqor.ai/marketing/unsubscribe?email=${encodeURIComponent(session.user.email)}" style="color: #10b981; text-decoration: none;">Unsubscribe</a>
                          </p>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>
            </body>
            </html>
          `,
        });
        
        console.log(`[MARKETING] Confirmation email sent to ${session.user.email}`);
      } catch (emailError) {
        console.error("[MARKETING] Failed to send confirmation email:", emailError);
      }
    }

    console.log(`[MARKETING] User ${session.user.email} ${consent ? 'opted in' : 'opted out'} for marketing`);

    return NextResponse.json({
      ok: true,
      consent,
      emailSent: consent && !!process.env.RESEND_API_KEY
    });
  } catch (error) {
    console.error("[MARKETING] Error setting consent:", error);
    return NextResponse.json(
      { ok: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
