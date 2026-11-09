import { PrismaClient } from "@prisma/client";
import { copyFileSync, existsSync } from "fs";
import path from "path";

export type DbMode = "turso" | "remote" | "local" | "ephemeral";

let resolvedDbMode: DbMode = "local";

export function getDbMode(): DbMode {
  return resolvedDbMode;
}

/**
 * On Vercel, local `file:` SQLite is read-only in the deployment bundle.
 * Copy to /tmp so the process can write — but /tmp is ephemeral per isolate.
 *
 * Production MUST set TURSO_DATABASE_URL (+ TURSO_AUTH_TOKEN) or a remote DATABASE_URL.
 * When REQUIRE_DURABLE_DB=1, missing Turso/remote throws (no silent /tmp fallback).
 */
function ensureWritableLocalSqlite() {
  if (!process.env.VERCEL) return;

  const current = process.env.DATABASE_URL ?? "";
  if (current && !current.startsWith("file:")) {
    resolvedDbMode = "remote";
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
  resolvedDbMode = "ephemeral";
  console.error(
    "[prisma] CRITICAL: Using ephemeral /tmp SQLite on Vercel. Practice history will not persist across isolates. Set TURSO_DATABASE_URL (+ TURSO_AUTH_TOKEN), then set REQUIRE_DURABLE_DB=1."
  );
}

function createPrismaClient(): PrismaClient {
  const tursoUrl = process.env.TURSO_DATABASE_URL?.trim();
  const tursoToken = process.env.TURSO_AUTH_TOKEN?.trim();
  const onVercel = Boolean(process.env.VERCEL);
  const requireDurable = process.env.REQUIRE_DURABLE_DB === "1";
  const databaseUrl = process.env.DATABASE_URL ?? "";

  if (tursoUrl) {
    try {
      // Durable SQLite for production (Turso / libSQL).
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const { PrismaLibSQL } = require("@prisma/adapter-libsql") as typeof import("@prisma/adapter-libsql");
      const adapter = new PrismaLibSQL({
        url: tursoUrl,
        authToken: tursoToken,
      });
      resolvedDbMode = "turso";
      console.info("[prisma] Connected via Turso/libSQL adapter");
      return new PrismaClient({
        adapter,
        log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
      });
    } catch (error) {
      console.error(
        "[prisma] Failed to init Turso adapter. Install matching @prisma/adapter-libsql@6.19.x and @libsql/client.",
        error
      );
      // Never silently fall back when Turso was explicitly configured.
      throw new Error(
        "[prisma] Turso adapter failed — refusing ephemeral SQLite fallback so attempt history is not silently lost."
      );
    }
  }

  if (onVercel && requireDurable) {
    if (!databaseUrl || databaseUrl.startsWith("file:")) {
      throw new Error(
        "[prisma] REQUIRE_DURABLE_DB=1 but TURSO_DATABASE_URL / remote DATABASE_URL is missing."
      );
    }
  }

  if (onVercel) {
    ensureWritableLocalSqlite();
  } else if (!databaseUrl || databaseUrl.startsWith("file:")) {
    resolvedDbMode = "local";
  } else {
    resolvedDbMode = "remote";
  }

  return new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
  });
}

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
