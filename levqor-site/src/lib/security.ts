// SECURITY NOTE: Client-side rate limiting and abuse prevention utilities
// Prevents excessive API calls, implements exponential backoff, logs security events

type RateLimitConfig = {
  maxAttempts: number;
  windowMs: number;
};

const RATE_LIMITS: Record<string, RateLimitConfig> = {
  checkout: { maxAttempts: 3, windowMs: 60000 }, // 3 attempts per minute
  auth: { maxAttempts: 5, windowMs: 300000 }, // 5 attempts per 5 minutes
  api: { maxAttempts: 10, windowMs: 60000 }, // 10 requests per minute
};

class RateLimiter {
  private attempts: Map<string, number[]> = new Map();

  check(key: string, limit: RateLimitConfig): { allowed: boolean; retryAfter?: number } {
    const now = Date.now();
    const windowStart = now - limit.windowMs;

    // Get and clean old attempts
    const userAttempts = (this.attempts.get(key) || []).filter(t => t > windowStart);
    
    if (userAttempts.length >= limit.maxAttempts) {
      const oldestAttempt = userAttempts[0];
      const retryAfter = Math.ceil((oldestAttempt + limit.windowMs - now) / 1000);
      return { allowed: false, retryAfter };
    }

    // Record new attempt
    userAttempts.push(now);
    this.attempts.set(key, userAttempts);
    
    return { allowed: true };
  }

  reset(key: string) {
    this.attempts.delete(key);
  }
}

export const rateLimiter = new RateLimiter();

export function checkRateLimit(
  identifier: string,
  type: keyof typeof RATE_LIMITS
): { allowed: boolean; retryAfter?: number } {
  const config = RATE_LIMITS[type];
  if (!config) return { allowed: true };
  
  return rateLimiter.check(`${type}:${identifier}`, config);
}

export function resetRateLimit(identifier: string, type: keyof typeof RATE_LIMITS) {
  rateLimiter.reset(`${type}:${identifier}`);
}

// Exponential backoff for failed requests
export function calculateBackoff(attemptNumber: number): number {
  const baseDelay = 1000; // 1 second
  const maxDelay = 30000; // 30 seconds
  const delay = Math.min(baseDelay * Math.pow(2, attemptNumber), maxDelay);
  return delay;
}

// Secure API fetch with rate limiting and retry logic
export async function secureFetch(
  url: string,
  options: RequestInit = {},
  rateLimitKey?: string
): Promise<Response> {
  // Check rate limit if key provided
  if (rateLimitKey) {
    const check = checkRateLimit(rateLimitKey, 'api');
    if (!check.allowed) {
      throw new Error(`Rate limit exceeded. Retry after ${check.retryAfter}s`);
    }
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    // Handle rate limit responses from server
    if (response.status === 429) {
      const retryAfter = response.headers.get('Retry-After') || '60';
      throw new Error(`Server rate limit exceeded. Retry after ${retryAfter}s`);
    }

    return response;
  } catch (error) {
    console.error('[secureFetch] Error:', error);
    throw error;
  }
}

// Validate and sanitize user input (basic XSS prevention)
export function sanitizeInput(input: string): string {
  return input
    .replace(/[<>]/g, '') // Remove angle brackets
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+=/gi, '') // Remove event handlers
    .trim()
    .slice(0, 1000); // Max length
}

// Check if user is potentially abusive based on behavior patterns
export function detectSuspiciousActivity(actions: string[]): boolean {
  // Too many failed actions in short time
  if (actions.length > 10) {
    const recentActions = actions.slice(-10);
    const allFailed = recentActions.every(a => a.includes('failed'));
    if (allFailed) return true;
  }

  return false;
}
