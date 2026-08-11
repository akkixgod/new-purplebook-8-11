import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { sendEmail, passwordResetEmailContent } from "@/lib/email";
import { findUserByEmail, normalizeEmail } from "@/lib/find-user-by-email";
import {
  PASSWORD_RESET_TTL_MS,
  buildPasswordResetUrl,
  generatePasswordResetToken,
  hashPasswordResetToken,
} from "@/lib/password-reset";

const GENERIC_OK =
  "If an account exists for that email, we sent a password reset link. Check your inbox.";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const email =
      typeof body.email === "string" ? normalizeEmail(body.email) : "";

    if (!email || !email.includes("@")) {
      return NextResponse.json({ error: "Valid email required" }, { status: 400 });
    }

    const user = await findUserByEmail(email);

    // Always return the same message when no account exists (anti-enumeration).
    if (!user) {
      return NextResponse.json({ message: GENERIC_OK });
    }

    const rawToken = generatePasswordResetToken();
    const tokenHash = hashPasswordResetToken(rawToken);
    const expiry = new Date(Date.now() + PASSWORD_RESET_TTL_MS);

    await prisma.user.update({
      where: { id: user.id },
      data: {
        passwordResetToken: tokenHash,
        passwordResetTokenExpiry: expiry,
      },
    });

    const resetUrl = buildPasswordResetUrl(rawToken);
    const content = passwordResetEmailContent(resetUrl);
    const result = await sendEmail({ to: email, ...content });

    if (!result.ok) {
      console.error("[forgot-password] email not delivered:", result.reason, result.detail);
      console.info("[forgot-password] DEV/FALLBACK reset link (copy from server logs):", resetUrl);

      // Keep token so the logged link still works in local/dev testing.
      // Client gets an explicit error (no false "Sent" success).
      const isDev = process.env.NODE_ENV !== "production";
      return NextResponse.json(
        {
          error:
            result.reason === "not_configured"
              ? "Email is not configured. Set RESEND_API_KEY (and EMAIL_FROM) on the server, or use the reset link from the server console / local test link below."
              : "Could not send reset email. Please try again later.",
          ...(isDev ? { devResetUrl: resetUrl } : {}),
        },
        { status: 502 }
      );
    }

    return NextResponse.json({ message: GENERIC_OK });
  } catch (err) {
    console.error("Forgot-password error:", err);
    return NextResponse.json({ error: "Request failed" }, { status: 500 });
  }
}
