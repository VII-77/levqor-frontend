import { NextRequest, NextResponse } from "next/server";

const BACKEND_API = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}));
    const token = body.token || "";

    if (!token) {
      return NextResponse.json(
        { ok: false, error: "Token required" },
        { status: 400 }
      );
    }

    const x_forwarded_for = request.headers.get("x-forwarded-for");
    const ip = x_forwarded_for ? x_forwarded_for.split(",")[0].trim() : "unknown";

    const confirmResponse = await fetch(
      `${BACKEND_API}/api/v1/marketing/confirm`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Forwarded-For": ip,
        },
        body: JSON.stringify({ token }),
      }
    );

    if (!confirmResponse.ok) {
      const errorData = await confirmResponse.json().catch(() => ({}));
      return NextResponse.json(
        { ok: false, error: errorData.error || "Invalid or expired token" },
        { status: confirmResponse.status }
      );
    }

    const result = await confirmResponse.json();
    
    console.log(`[MARKETING] Double opt-in confirmed for ${result.email}`);

    return NextResponse.json({
      ok: true,
      confirmed: true,
      email: result.email
    });
  } catch (error) {
    console.error("[MARKETING] Error confirming subscription:", error);
    return NextResponse.json(
      { ok: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
