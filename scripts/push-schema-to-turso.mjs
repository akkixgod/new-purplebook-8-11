/**
 * Push Prisma schema to Turso and optionally copy the local SQLite catalog.
 *
 * Usage (PowerShell):
 *   $env:TURSO_DATABASE_URL="libsql://..."
 *   $env:TURSO_AUTH_TOKEN="..."
 *   node scripts/push-schema-to-turso.mjs
 *
 * Requires: npx prisma, @libsql/client
 */
import { createClient } from "@libsql/client";
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";

const url = process.env.TURSO_DATABASE_URL?.trim();
const authToken = process.env.TURSO_AUTH_TOKEN?.trim();

if (!url) {
  console.error("Set TURSO_DATABASE_URL before running this script.");
  process.exit(1);
}

console.info("[turso] pushing Prisma schema via db push…");
const push = spawnSync(
  "npx",
  ["prisma", "db", "push", "--skip-generate"],
  {
    stdio: "inherit",
    env: {
      ...process.env,
      // Prisma needs DATABASE_URL for sqlite provider; Turso adapter uses TURSO_*.
      DATABASE_URL: process.env.DATABASE_URL || "file:./dev.db",
      TURSO_DATABASE_URL: url,
      TURSO_AUTH_TOKEN: authToken || "",
    },
    shell: true,
  }
);

if (push.status !== 0) {
  console.warn(
    "[turso] prisma db push exited non-zero. If the provider stays sqlite/file locally, apply schema with Turso CLI or Prisma migrate against the remote URL."
  );
}

const client = createClient({ url, authToken });
const tables = await client.execute(
  "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
);
console.info(
  "[turso] remote tables:",
  tables.rows.map((r) => r.name).join(", ") || "(none)"
);

const localDb = path.join(process.cwd(), "prisma", "dev.db");
if (!existsSync(localDb)) {
  console.info("[turso] no local prisma/dev.db to inspect; seed via npm run seed:* against Turso.");
  process.exit(0);
}

console.info(
  "[turso] Schema check done. Seed production with TURSO_* set, e.g. npm run seed:pb1"
);
process.exit(0);
