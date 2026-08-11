import NextAuth, { CredentialsSignin } from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";
import bcrypt from "bcryptjs";
import { prisma } from "./prisma";
import { verifyAuthBackup } from "./auth-backup";
import { findUserByEmail, normalizeEmail } from "./find-user-by-email";

const googleConfigured =
  Boolean(process.env.GOOGLE_CLIENT_ID) && Boolean(process.env.GOOGLE_CLIENT_SECRET);

class InvalidCredentialsError extends CredentialsSignin {
  code = "invalid_credentials";
}

class NoPasswordError extends CredentialsSignin {
  code = "no_password";
}

class AuthServiceError extends CredentialsSignin {
  code = "service_error";
}

function looksLikeBcryptHash(value: string): boolean {
  return /^\$2[aby]?\$\d{2}\$/.test(value);
}

async function restoreUserFromBackup(backupToken: string, email: string, password: string) {
  const payload = verifyAuthBackup(backupToken);
  if (!payload) {
    console.warn("[auth/credentials] auth backup invalid or expired");
    return null;
  }
  if (normalizeEmail(payload.email) !== email) {
    console.warn("[auth/credentials] auth backup email mismatch");
    return null;
  }
  if (!looksLikeBcryptHash(payload.passwordHash)) {
    console.warn("[auth/credentials] auth backup hash malformed");
    return null;
  }

  const matched = await bcrypt.compare(password, payload.passwordHash);
  if (!matched) {
    console.warn("[auth/credentials] auth backup password mismatch");
    return null;
  }

  // Rehydrate the user row on this serverless SQLite instance.
  try {
    const existing = await findUserByEmail(email);
    if (existing) {
      return prisma.user.update({
        where: { id: existing.id },
        data: {
          email,
          password: payload.passwordHash,
        },
      });
    }
    return prisma.user.create({
      data: {
        id: payload.id,
        email: payload.email,
        password: payload.passwordHash,
        name: email.split("@")[0],
      },
    });
  } catch (err) {
    console.error("[auth/credentials] failed to restore user from backup", err);
    // Still allow sign-in from the verified backup payload.
    return {
      id: payload.id,
      email: payload.email,
      name: email.split("@")[0],
      image: null,
      password: payload.passwordHash,
      role: "user",
      emailVerified: null,
      passwordResetToken: null,
      passwordResetTokenExpiry: null,
      createdAt: new Date(),
    };
  }
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(prisma),
  secret: process.env.AUTH_SECRET ?? process.env.NEXTAUTH_SECRET,
  trustHost: true,
  session: { strategy: "jwt" },
  providers: [
    ...(googleConfigured
      ? [
          Google({
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
          }),
        ]
      : []),
    Credentials({
      id: "credentials",
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
        backup: { label: "Backup", type: "text" },
      },
      async authorize(credentials) {
        const email =
          typeof credentials?.email === "string" ? normalizeEmail(credentials.email) : "";
        const password =
          typeof credentials?.password === "string" ? credentials.password : "";
        const backup =
          typeof credentials?.backup === "string" ? credentials.backup.trim() : "";

        console.info("[auth/credentials] authorize start", {
          email,
          passwordProvided: Boolean(password),
          passwordLength: password.length,
          backupProvided: Boolean(backup),
        });

        if (!email || !password) {
          console.warn("[auth/credentials] missing email or password");
          throw new InvalidCredentialsError();
        }

        let user;
        try {
          user = await findUserByEmail(email);
        } catch (err) {
          console.error("[auth/credentials] database lookup failed", err);
          throw new AuthServiceError();
        }

        if (!user?.password && backup) {
          console.info("[auth/credentials] restoring user from signed auth backup");
          user = await restoreUserFromBackup(backup, email, password);
        }

        if (!user) {
          console.warn("[auth/credentials] user not found for email", email);
          throw new InvalidCredentialsError();
        }

        console.info("[auth/credentials] user found", {
          userId: user.id,
          storedEmail: user.email,
          hasPassword: Boolean(user.password),
          passwordHashLooksValid: user.password ? looksLikeBcryptHash(user.password) : false,
        });

        if (!user.password) {
          console.warn("[auth/credentials] user has no password (OAuth-only?)", user.id);
          throw new NoPasswordError();
        }

        if (!looksLikeBcryptHash(user.password)) {
          console.error("[auth/credentials] stored password is not a bcrypt hash", {
            userId: user.id,
            prefix: user.password.slice(0, 4),
          });
          throw new AuthServiceError();
        }

        let valid = false;
        try {
          valid = await bcrypt.compare(password, user.password);
        } catch (err) {
          console.error("[auth/credentials] bcrypt.compare threw", err);
          throw new AuthServiceError();
        }

        console.info("[auth/credentials] password compare result", {
          userId: user.id,
          matched: valid,
        });

        if (!valid) {
          throw new InvalidCredentialsError();
        }

        return {
          id: user.id,
          email: user.email,
          name: user.name,
          image: user.image,
          role: user.role,
        };
      },
    }),
  ],
  callbacks: {
    async signIn({ user }) {
      if (user.email) {
        const normalized = normalizeEmail(user.email);
        if (normalized !== user.email) {
          user.email = normalized;
          try {
            if (user.id) {
              await prisma.user.updateMany({
                where: { id: user.id },
                data: { email: normalized },
              });
            }
          } catch (err) {
            console.warn("[auth] failed to normalize OAuth email", err);
          }
        }
      }
      return true;
    },
    jwt({ token, user }) {
      if (user) {
        token.id = user.id!;
        token.role = (user as { role?: string }).role ?? "user";
      }
      return token;
    },
    session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        (session.user as { role?: string }).role = token.role as string;
      }
      return session;
    },
  },
  pages: {
    signIn: "/auth/signin",
  },
});
