import { NextResponse } from "next/server";

export const AUTH_BACKUP_COOKIE = "pb_auth_backup";

const BACKUP_MAX_AGE_SEC = 60 * 60 * 24 * 180;

export function readAuthBackupFromCookieHeader(
  cookieHeader: string | null | undefined
): string {
  if (!cookieHeader) return "";
  for (const part of cookieHeader.split(";")) {
    const idx = part.indexOf("=");
    if (idx < 0) continue;
    const name = part.slice(0, idx).trim();
    if (name !== AUTH_BACKUP_COOKIE) continue;
    try {
      return decodeURIComponent(part.slice(idx + 1).trim());
    } catch {
      return part.slice(idx + 1).trim();
    }
  }
  return "";
}

export function attachAuthBackupCookie(res: NextResponse, token: string): NextResponse {
  res.cookies.set({
    name: AUTH_BACKUP_COOKIE,
    value: token,
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    secure: process.env.NODE_ENV === "production",
    maxAge: BACKUP_MAX_AGE_SEC,
  });
  return res;
}
