export const runtime = 'nodejs';

import { authOptions } from "@/auth";
import { getServerSession } from "next-auth";
import { NextRequest, NextResponse } from "next/server";
import { logHighRiskReject } from "@/lib/logHighRiskReject";

const PROHIBITED_KEYWORDS = [
  "medical", "healthcare", "diagnosis", "treatment", "doctor", "patient",
  "legal", "lawsuit", "attorney", "contract", "solicitor", "barrister",
  "financial", "investment", "trading", "forex", "cryptocurrency", "crypto",
  "tax", "accounting", "audit", "hmrc", "tax return",
  "minor", "child", "under 18", "children", "kid",
  "race", "ethnicity", "religion", "biometric", "fingerprint", "facial recognition"
];

function scanForProhibitedContent(text: string): string[] {
  const lowercaseText = text.toLowerCase();
  const matched: string[] = [];

  for (const keyword of PROHIBITED_KEYWORDS) {
    if (lowercaseText.includes(keyword)) {
      matched.push(keyword);
    }
  }

  return matched;
}

export async function POST(request: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || !session.user?.email) {
      return NextResponse.json(
        { ok: false, error: "Unauthorized" },
        { status: 401 }
      );
    }

    const body = await request.json().catch(() => ({}));
    const { title, description, steps, prompt } = body;

    if (!title) {
      return NextResponse.json(
        { ok: false, error: "Workflow title is required" },
        { status: 400 }
      );
    }

    const combinedText = [
      title || '',
      description || '',
      steps || '',
      prompt || ''
    ].join(' ');

    const matchedKeywords = scanForProhibitedContent(combinedText);

    if (matchedKeywords.length > 0) {
      logHighRiskReject({
        userId: session.user.email,
        timestamp: new Date().toISOString(),
        matchedKeywords,
        workflowTitle: title,
        description: description || ''
      });

      return NextResponse.json(
        { 
          ok: false, 
          error: "High-risk workflows are prohibited. Please modify your request.",
          rejectedKeywords: matchedKeywords
        },
        { status: 400 }
      );
    }

    const backendApi = process.env.NEXT_PUBLIC_API_URL || 'https://api.levqor.ai';
    
    const createResponse = await fetch(`${backendApi}/api/v1/intake`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-Email': session.user.email,
      },
      body: JSON.stringify({
        name: title,
        description,
        steps,
        prompt,
        user_email: session.user.email
      }),
    });

    if (!createResponse.ok) {
      const errorData = await createResponse.json().catch(() => ({}));
      return NextResponse.json(
        { ok: false, error: errorData.error || "Failed to create workflow" },
        { status: createResponse.status }
      );
    }

    const result = await createResponse.json();
    
    console.log(`[WORKFLOW CREATE] User ${session.user.email} created workflow: "${title}"`);

    return NextResponse.json({
      ok: true,
      workflow: result
    });
  } catch (error) {
    console.error("[WORKFLOW CREATE] Error:", error);
    return NextResponse.json(
      { ok: false, error: "Internal server error" },
      { status: 500 }
    );
  }
}
