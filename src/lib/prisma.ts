import { PrismaClient } from "@prisma/client";

export type DbMode = "turso" | "remote" | "local" | "ephemeral";

let resolvedDbMode: DbMode = "local";

export function getDbMode(): DbMode {
  return resolvedDbMode;
}

function createPrismaClient(): PrismaClient {
  const tursoUrl = process.env.TURSO_DATABASE_URL?.trim();
  const tursoToken = process.env.TURSO_AUTH_TOKEN?.trim();
  const onVercel = Boolean(process.env.VERCEL);
  const databaseUrl = process.env.DATABASE_URL ?? "";
  const hasRemoteDatabase = Boolean(databaseUrl) && !databaseUrl.startsWith("file:");

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

  // On Vercel, durable storage is mandatory — never fall through to /tmp SQLite.
  if (onVercel && !hasRemoteDatabase) {
    throw new Error(
      "[prisma] Vercel requires TURSO_DATABASE_URL (or a non-file DATABASE_URL). Refusing ephemeral /tmp SQLite so attempt history is not silently lost."
    );
  }

  if (onVercel || hasRemoteDatabase) {
    resolvedDbMode = "remote";
  } else {
    resolvedDbMode = "local";
  }

  return new PrismaClient({
    log: process.env.NODE_ENV === "development" ? ["error", "warn"] : ["error"],
  });
}

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma = globalForPrisma.prisma || createPrismaClient();

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
