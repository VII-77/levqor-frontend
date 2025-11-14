import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getToken } from "next-auth/jwt";

const BACKEND_API = process.env.NEXT_PUBLIC_API_URL || "https://api.levqor.ai";
const CURRENT_TERMS_VERSION = "2025-11-14";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  const publicPaths = [
    "/signin",
    "/terms",
    "/privacy",
    "/cookies",
    "/cookie-settings",
    "/legal",
    "/api/auth",
    "/_next",
    "/public",
  ];
  
  if (publicPaths.some(path => pathname.startsWith(path)) || pathname === "/") {
    return NextResponse.next();
  }
  
  if (pathname === "/legal/accept-terms") {
    return NextResponse.next();
  }
  
  const protectedPaths = ["/workflow", "/dashboard", "/account", "/settings", "/developer", "/api/workflows"];
  
  if (protectedPaths.some(path => pathname.startsWith(path))) {
    const token = await getToken({ 
      req: request,
      secret: process.env.NEXTAUTH_SECRET || process.env.JWT_SECRET
    });
    
    if (!token || !token.email) {
      const url = request.nextUrl.clone();
      url.pathname = "/signin";
      return NextResponse.redirect(url);
    }
    
    try {
      const userResponse = await fetch(`${BACKEND_API}/api/v1/users/upsert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: token.email,
          name: token.name || "",
        }),
      });

      if (userResponse.ok) {
        const userData = await userResponse.json();
        
        if (!userData.terms_accepted_at || userData.terms_version !== CURRENT_TERMS_VERSION) {
          const url = request.nextUrl.clone();
          url.pathname = "/legal/accept-terms";
          url.searchParams.set("returnTo", pathname + (request.nextUrl.search || ""));
          
          console.log(`[TOS Middleware] Redirecting ${token.email} to /legal/accept-terms (terms_version: ${userData.terms_version || 'null'})`);
          
          return NextResponse.redirect(url);
        }
      }
    } catch (error) {
      console.error("[TOS Middleware] Error checking terms:", error);
    }
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ["/workflow/:path*", "/dashboard/:path*", "/account/:path*", "/settings/:path*", "/developer/:path*", "/api/workflows/:path*"],
};
