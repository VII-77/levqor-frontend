import { NextRequest, NextResponse } from "next/server";

const BACKEND_API = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}));
    const email = body.email || "";

    if (!email) {
      return NextResponse.json(
        { ok: false, error: "Email required" },
        { status: 400 }
      );
    }

    const userResponse = await fetch(`${BACKEND_API}/api/v1/users/upsert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email }),
    });

    if (!userResponse.ok) {
      return NextResponse.json(
        { ok: false, error: "User not found" },
        { status: 404 }
      );
    }

    const userData = await userResponse.json();
    const userId = userData.id;

    const x_forwarded_for = request.headers.get("x-forwarded-for");
    const ip = x_forwarded_for ? x_forwarded_for.split(",")[0].trim() : "unknown";

    const unsubscribeResponse = await fetch(
      `${BACKEND_API}/api/v1/users/${userId}/marketing-unsubscribe`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Forwarded-For": ip,
        },
      }
    );

    if (!unsubscribeResponse.ok) {
      const errorData = await unsubscribeResponse.json().catch(() => ({}));
      return NextResponse.json(
        { ok: false, error: errorData.error || "Failed to unsubscribe" },
        { status: unsubscribeResponse.status }
      );
    }

    const result = await unsubscribeResponse.json();
    
    console.log(`[MARKETING] User ${email} unsubscribed from marketing emails`);

    return NextResponse.json({
      ok: true,
      unsubscribed: true,
      email
    });
  } catch (error) {
    console.error("[MARKETING] Error unsubscribing:", error);
    return NextResponse.json(
      { ok: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
