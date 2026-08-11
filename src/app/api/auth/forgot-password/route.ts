import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { sendEmail, passwordResetEmailContent, isEmailConfigured } from "@/lib/email";
import { findUserByEmail, normalizeEmail } from "@/lib/find-user-by-email";
import {
  PASSWORD_RESET_TTL_MS,
  buildPasswordResetUrl,
  generatePasswordResetToken,
  hashPasswordResetToken,
} from "@/lib/password-reset";

const GENERIC_OK =
  "If an account exists for that email, we sent a password reset link. Check your inbox.";

function shouldExposeResetLink(): boolean {
  if (process.env.AUTH_EXPOSE_RESET_LINK === "1") return true;
  if (process.env.NODE_ENV !== "production") return true;
  // Local `next start` sometimes runs with NODE_ENV=production but no Resend key.
  if (!isEmailConfigured() && !process.env.VERCEL) return true;
  return false;
}

function logFallbackResetLink(email: string, resetUrl: string, reason: string) {
  // Extremely visible so local testing does not depend on digging through warn noise.
  console.log("\n========== PASSWORD RESET (EMAIL NOT SENT) ==========");
  console.log(`reason: ${reason}`);
  console.log(`to:     ${email}`);
  console.log(`link:   ${resetUrl}`);
  console.log("Copy the link above into your browser to reset the password.");
  console.log("=====================================================\n");
}

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
      if (!isEmailConfigured()) {
        console.log(
          `[forgot-password] no account for ${email}; email provider also not configured`
        );
      }
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
      logFallbackResetLink(email, resetUrl, `${result.reason}: ${result.detail}`);

      // Keep token so the logged / returned link still works for testing.
      const exposeLink = shouldExposeResetLink();
      const error =
        result.reason === "not_configured"
          ? exposeLink
            ? "Email is not configured (RESEND_API_KEY missing). Use the local test link below, or copy the reset URL from the server terminal."
            : "Email is not configured. Set RESEND_API_KEY and EMAIL_FROM in Vercel (Project → Settings → Environment Variables), then redeploy."
          : "Could not send reset email. Please try again later.";

      return NextResponse.json(
        {
          error,
          ...(exposeLink ? { devResetUrl: resetUrl } : {}),
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
