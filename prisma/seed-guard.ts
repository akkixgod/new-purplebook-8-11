import type { PrismaClient } from "@prisma/client";

/**
 * Catalog reseed that deletes Test rows cascade-deletes Modules → Attempts → Answers.
 * Refuse that against Turso unless the operator explicitly opts in.
 */
export function assertCanWipeCatalog(): void {
  const turso = process.env.TURSO_DATABASE_URL?.trim();
  if (turso && process.env.ALLOW_PROD_SEED_WIPE !== "1") {
    throw new Error(
      "[seed] Refusing destructive test.delete against Turso. " +
        "Re-running seeds wipes user attempt history via FK cascade. " +
        "Set ALLOW_PROD_SEED_WIPE=1 only if you intentionally want that."
    );
  }
}

/** Delete a test for local reseed — blocked on Turso without ALLOW_PROD_SEED_WIPE=1. */
export async function deleteTestForReseed(
  prisma: PrismaClient,
  id: string
): Promise<void> {
  assertCanWipeCatalog();
  await prisma.test.delete({ where: { id } });
}
