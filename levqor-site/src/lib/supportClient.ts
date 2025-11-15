const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "https://api.levqor.ai";

export interface SupportReply {
  reply: string;
  escalationSuggested?: boolean;
  conversationId?: string;
  ticketId?: string;
}

export interface TicketResponse {
  status: string;
  ticketId?: string;
  message?: string;
}

export async function callPublicSupport(message: string, conversationId?: string): Promise<SupportReply> {
  const response = await fetch(`${API_BASE}/api/support/public`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, conversationId }),
  });

  if (!response.ok) {
    throw new Error(`Support API error: ${response.status}`);
  }

  return response.json();
}

export async function callPrivateSupport(message: string, email?: string, conversationId?: string): Promise<SupportReply> {
  const response = await fetch(`${API_BASE}/api/support/private`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ message, email, conversationId }),
  });

  if (!response.ok) {
    throw new Error(`Support API error: ${response.status}`);
  }

  return response.json();
}

export async function escalateSupport(email: string, message: string, context?: Record<string, any>): Promise<TicketResponse> {
  const response = await fetch(`${API_BASE}/api/support/escalate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, message, context }),
  });

  if (!response.ok) {
    throw new Error(`Escalation API error: ${response.status}`);
  }

  return response.json();
}
