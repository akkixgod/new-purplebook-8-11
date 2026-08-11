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

    // Always return the same message to avoid account enumeration.
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

    try {
      await sendEmail({ to: email, ...content });
    } catch (err) {
      console.error("Forgot-password email failed:", err);
      // Clear token if email could not be sent so the user can retry cleanly.
      await prisma.user.update({
        where: { id: user.id },
        data: {
          passwordResetToken: null,
          passwordResetTokenExpiry: null,
        },
      });
      return NextResponse.json(
        { error: "Could not send reset email. Please try again later." },
        { status: 502 }
      );
    }

    return NextResponse.json({ message: GENERIC_OK });
  } catch (err) {
    console.error("Forgot-password error:", err);
    return NextResponse.json({ error: "Request failed" }, { status: 500 });
  }
}
