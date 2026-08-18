import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { createAuthBackup } from "@/lib/auth-backup";
import { attachAuthBackupCookie } from "@/lib/auth-backup-cookie";
import { findUserByEmail, normalizeEmail } from "@/lib/find-user-by-email";

/**
 * Issues a signed auth backup after verifying email+password.
 * Used so later logins still work on ephemeral serverless SQLite instances.
 */
export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const email = typeof body.email === "string" ? normalizeEmail(body.email) : "";
    const password = typeof body.password === "string" ? body.password : "";

    if (!email || !password) {
      return NextResponse.json({ error: "Email and password required" }, { status: 400 });
    }

    const user = await findUserByEmail(email);
    if (!user?.password) {
      return NextResponse.json({ error: "Invalid email or password" }, { status: 401 });
    }

    const ok = await bcrypt.compare(password, user.password);
    if (!ok) {
      return NextResponse.json({ error: "Invalid email or password" }, { status: 401 });
    }

    const authBackup = createAuthBackup({
      id: user.id,
      email: user.email,
      passwordHash: user.password,
    });

    const res = NextResponse.json({ authBackup });
    attachAuthBackupCookie(res, authBackup);
    return res;
  } catch (err) {
    console.error("[auth/issue-backup] error", err);
    return NextResponse.json({ error: "Could not issue backup" }, { status: 500 });
  }
}
