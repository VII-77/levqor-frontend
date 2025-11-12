import { getServerSession } from "next-auth";
import { NextResponse } from "next/server";
import { authOptions } from "../../auth/[...nextauth]/route";

export async function GET() {
  try {
    const session = await getServerSession(authOptions as any);
    if (!session) {
      console.log("No session");
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const upstream = await fetch("https://api.levqor.ai/api/intelligence/recommendations");
    const text = await upstream.text();
    console.log("Upstream status:", upstream.status, "body:", text.slice(0, 100));
    return NextResponse.json({ status: upstream.status, body: text });
  } catch (e: any) {
    console.error("Workflows route error", e);
    return NextResponse.json({ error: e?.message || "Internal error" }, { status: 500 });
  }
}
