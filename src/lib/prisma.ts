import { PrismaClient } from "@prisma/client";
import { copyFileSync, existsSync } from "fs";
import path from "path";

/**
 * On Vercel, local `file:` SQLite is read-only in the deployment bundle.
 * Copy to /tmp so the process can write — but /tmp is ephemeral per instance.
 * Never overwrite a remote DATABASE_URL (Postgres, Turso/libsql, Prisma Accelerate, etc.).
 */
function ensureWritableLocalSqlite() {
  if (!process.env.VERCEL) return;

  const current = process.env.DATABASE_URL ?? "";
  if (current && !current.startsWith("file:")) {
    // Durable remote DB configured in Vercel env — keep it.
    return;
  }

  const dest = "/tmp/purplebook.db";
  if (!existsSync(dest)) {
    const src = path.join(process.cwd(), "prisma", "dev.db");
    if (existsSync(src)) {
      copyFileSync(src, dest);
    }
  }
  process.env.DATABASE_URL = `file:${dest}`;
  console.warn(
    "[prisma] Using ephemeral /tmp SQLite on Vercel. Attempt history will not survive cold starts. Set TURSO_DATABASE_URL (+ TURSO_AUTH_TOKEN) or a remote DATABASE_URL for permanent storage."
  );
}

function createPrismaClient(): PrismaClient {
  const tursoUrl = process.env.TURSO_DATABASE_URL?.trim();
  const tursoToken = process.env.TURSO_AUTH_TOKEN?.trim();

  if (tursoUrl) {
    try {
      // Optional durable SQLite for production (Turso / libSQL).
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const { PrismaLibSql } = require("@prisma/adapter-libsql") as typeof import("@prisma/adapter-libsql");
      const adapter = new PrismaLibSql({
        url: tursoUrl,
        authToken: tursoToken,
      });
      console.info("[prisma] Connected via Turso/libSQL adapter");
      return new PrismaClient({
        adapter,
        log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
      });
    } catch (error) {
      console.error(
        "[prisma] Failed to init Turso adapter — falling back to DATABASE_URL. Install @libsql/client and @prisma/adapter-libsql.",
        error
      );
    }
  }

  ensureWritableLocalSqlite();
  return new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
  });
}

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
