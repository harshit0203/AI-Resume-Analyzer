import { NextResponse, type NextRequest } from "next/server";

const PROTECTED_PREFIXES = ["/dashboard"];
const AUTH_ROUTES = ["/login", "/register"];

/**
 * Edge proxy (formerly "middleware") gate.
 *
 * The backend issues httpOnly cookies (`ara_access_token` + `ara_refresh_token`).
 * The edge cannot cheaply verify JWT signatures, so it checks for the presence
 * of a session cookie to gate protected routes and bounce authenticated users
 * away from auth pages. Full verification still happens on every API call.
 */
export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession =
    request.cookies.has("ara_refresh_token") || request.cookies.has("ara_access_token");

  const isProtected = PROTECTED_PREFIXES.some((p) => pathname.startsWith(p));
  const isAuthRoute = AUTH_ROUTES.some((p) => pathname.startsWith(p));

  if (isProtected && !hasSession) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }

  if (isAuthRoute && hasSession) {
    const url = request.nextUrl.clone();
    url.pathname = "/dashboard";
    url.search = "";
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/register"],
};
