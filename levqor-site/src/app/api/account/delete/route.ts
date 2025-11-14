import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/auth";

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

    const response = await fetch(`${BACKEND_API}/api/account/delete`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Email": session.user.email,
      },
    });

    const data = await response.json();

    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("[ACCOUNT] Error deleting account:", error);
    return NextResponse.json(
      { ok: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
