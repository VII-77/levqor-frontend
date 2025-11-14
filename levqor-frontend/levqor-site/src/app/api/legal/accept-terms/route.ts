import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/auth";
import { CURRENT_TERMS_VERSION } from "@/config/legal";

const BACKEND_API = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";

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
    const version = body.version || CURRENT_TERMS_VERSION;

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

    const termsResponse = await fetch(
      `${BACKEND_API}/api/v1/users/${userId}/accept-terms`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Forwarded-For": ip,
        },
        body: JSON.stringify({ version }),
      }
    );

    if (!termsResponse.ok) {
      return NextResponse.json(
        { ok: false, error: "Failed to record terms acceptance" },
        { status: 500 }
      );
    }

    const result = await termsResponse.json();
    
    console.log(`[TOS] User ${session.user.email} accepted terms v${version} from IP ${ip.split(".").slice(0, 3).join(".")}.xxx`);

    return NextResponse.json({
      ok: true,
      version: result.version,
      at: result.at,
    });
  } catch (error) {
    console.error("[TOS] Error accepting terms:", error);
    return NextResponse.json(
      { ok: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
