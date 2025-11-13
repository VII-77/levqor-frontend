import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  const protectedPaths = ["/workflow", "/dashboard"];
  const { pathname } = request.nextUrl;
  
  if (protectedPaths.some(path => pathname.startsWith(path))) {
    const token = request.cookies.get("next-auth.session-token") || request.cookies.get("__Secure-next-auth.session-token");
    
    if (!token) {
      const url = request.nextUrl.clone();
      url.pathname = "/signin";
      return NextResponse.redirect(url);
    }
  }
  
  return NextResponse.next();
}

export const config = {
  matcher: ["/workflow", "/dashboard"],
};
