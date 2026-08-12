import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { prisma } from "@/lib/prisma";
import { createAuthBackup } from "@/lib/auth-backup";
import { findUserByEmail, normalizeEmail } from "@/lib/find-user-by-email";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json().catch(() => null);
    if (!body || typeof body !== "object") {
      return NextResponse.json({ error: "Invalid request body" }, { status: 400 });
    }

    const name = typeof body.name === "string" ? body.name.trim() : "";
    const email = typeof body.email === "string" ? normalizeEmail(body.email) : "";
    const password = typeof body.password === "string" ? body.password : "";

    console.info("[auth/register] start", { email, passwordLength: password.length });

    if (!email || !email.includes("@") || !password) {
      return NextResponse.json({ error: "Email and password required" }, { status: 400 });
    }

    if (password.length < 6) {
      return NextResponse.json({ error: "Password must be at least 6 characters" }, { status: 400 });
    }

    const existing = await findUserByEmail(email);
    if (existing?.password) {
      console.warn("[auth/register] email already in use", email);
      return NextResponse.json({ error: "Email already in use" }, { status: 409 });
    }

    const hashed = await bcrypt.hash(password, 12);

    let user;
    try {
      if (existing && !existing.password) {
        // OAuth-only row: attach a password so credentials sign-in works.
        user = await prisma.user.update({
          where: { id: existing.id },
          data: {
            name: name || existing.name || email.split("@")[0],
            email,
            password: hashed,
          },
        });
        console.info("[auth/register] attached password to existing OAuth user", user.id);
      } else {
        user = await prisma.user.create({
          data: {
            name: name || email.split("@")[0],
            email,
            password: hashed,
          },
        });
        console.info("[auth/register] created user", { id: user.id, email: user.email });
      }
    } catch (err) {
      console.error("[auth/register] database write failed", err);
      return NextResponse.json(
        { error: "Could not save account. Please try again." },
        { status: 500 }
      );
    }

    // Round-trip verify so we never claim "created" if the row isn't readable/usable.
    const saved = await findUserByEmail(email);
    if (!saved?.password) {
      console.error("[auth/register] user missing after write", email);
      return NextResponse.json(
        { error: "Account write could not be verified. Please try again." },
        { status: 500 }
      );
    }

    const passwordOk = await bcrypt.compare(password, saved.password);
    if (!passwordOk) {
      console.error("[auth/register] password verify failed after write", saved.id);
      return NextResponse.json(
        { error: "Account created but password check failed. Please try signing in again." },
        { status: 500 }
      );
    }

    let authBackup: string | null = null;
    try {
      authBackup = createAuthBackup({
        id: saved.id,
        email: saved.email,
        passwordHash: saved.password,
      });
    } catch (err) {
      console.warn("[auth/register] auth backup unavailable", err);
    }

    return NextResponse.json(
      {
        id: saved.id,
        email: saved.email,
        authBackup,
      },
      { status: 201 }
    );
  } catch (err) {
    console.error("[auth/register] unexpected error:", err);
    return NextResponse.json({ error: "Registration failed" }, { status: 500 });
  }
}
