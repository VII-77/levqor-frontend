/**
 * Frontend Error Reporting Client
 * Logs frontend errors to the backend error monitoring system
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";

export interface ErrorLogEvent {
  service: string;
  message: string;
  severity?: "info" | "warning" | "error" | "critical";
  path?: string;
  userEmail?: string;
  stack?: string;
}

/**
 * Log a client-side error to the backend
 * 
 * This is best-effort only - will not throw if the call fails
 */
export async function logClientError(event: ErrorLogEvent): Promise<void> {
  try {
    const payload = {
      source: "frontend",
      service: event.service,
      path_or_screen: event.path || (typeof window !== 'undefined' ? window.location.pathname : '/unknown'),
      user_email: event.userEmail || null,
      severity: event.severity || "error",
      message: event.message,
      stack: event.stack || null
    };

    await fetch(`${API_BASE}/api/errors/log`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    // Intentionally not checking response - best effort only
  } catch (err) {
    // Silent failure - don't disrupt user experience
    console.debug("Failed to log error to backend:", err);
  }
}

/**
 * Log a JavaScript error with automatic stack trace extraction
 */
export function logJSError(
  service: string,
  error: Error | unknown,
  severity: "info" | "warning" | "error" | "critical" = "error",
  userEmail?: string
): void {
  const message = error instanceof Error ? error.message : String(error);
  const stack = error instanceof Error ? error.stack : undefined;

  logClientError({
    service,
    message,
    severity,
    stack,
    userEmail,
  });
}
