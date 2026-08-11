import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { prisma } from "@/lib/prisma";
import { hashPasswordResetToken } from "@/lib/password-reset";

export async function GET(req: NextRequest) {
  try {
    const token = req.nextUrl.searchParams.get("token")?.trim() ?? "";
    if (!token) {
      return NextResponse.json({ valid: false, error: "Missing token" }, { status: 400 });
    }

    const tokenHash = hashPasswordResetToken(token);
    const user = await prisma.user.findFirst({
      where: {
        passwordResetToken: tokenHash,
        passwordResetTokenExpiry: { gt: new Date() },
      },
      select: { id: true, email: true },
    });

    if (!user) {
      return NextResponse.json({ valid: false, error: "Invalid or expired reset link" }, { status: 400 });
    }

    return NextResponse.json({ valid: true, email: user.email });
  } catch (err) {
    console.error("Reset-password validate error:", err);
    return NextResponse.json({ valid: false, error: "Validation failed" }, { status: 500 });
  }
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => ({}));
    const token = typeof body.token === "string" ? body.token.trim() : "";
    const password = typeof body.password === "string" ? body.password : "";
    const confirmPassword =
      typeof body.confirmPassword === "string" ? body.confirmPassword : "";

    if (!token) {
      return NextResponse.json({ error: "Missing token" }, { status: 400 });
    }
    if (password.length < 6) {
      return NextResponse.json(
        { error: "Password must be at least 6 characters" },
        { status: 400 }
      );
    }
    if (password !== confirmPassword) {
      return NextResponse.json({ error: "Passwords do not match" }, { status: 400 });
    }

    const tokenHash = hashPasswordResetToken(token);
    const user = await prisma.user.findFirst({
      where: {
        passwordResetToken: tokenHash,
        passwordResetTokenExpiry: { gt: new Date() },
      },
    });

    if (!user) {
      return NextResponse.json(
        { error: "Invalid or expired reset link. Request a new one." },
        { status: 400 }
      );
    }

    const hashed = await bcrypt.hash(password, 12);

    await prisma.user.update({
      where: { id: user.id },
      data: {
        password: hashed,
        passwordResetToken: null,
        passwordResetTokenExpiry: null,
      },
    });

    return NextResponse.json({ message: "Password updated. You can sign in now." });
  } catch (err) {
    console.error("Reset-password error:", err);
    return NextResponse.json({ error: "Could not reset password" }, { status: 500 });
  }
}
