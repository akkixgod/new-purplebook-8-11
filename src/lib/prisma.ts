import { PrismaClient } from "@prisma/client";
import { copyFileSync, existsSync } from "fs";
import path from "path";

/**
 * Vercel serverless has a read-only filesystem except /tmp.
 * Copy the bundled SQLite DB into /tmp on cold start so queries work.
 * Note: writes (signups/attempts) are ephemeral per instance — fine for viewing mocks;
 * move to Postgres/Turso for durable production data later.
 */
function ensureWritableSqlite() {
  if (!process.env.VERCEL) return;

  const dest = "/tmp/purplebook.db";
  if (!existsSync(dest)) {
    const src = path.join(process.cwd(), "prisma", "dev.db");
    if (existsSync(src)) {
      copyFileSync(src, dest);
    }
  }
  process.env.DATABASE_URL = `file:${dest}`;
}

ensureWritableSqlite();

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
