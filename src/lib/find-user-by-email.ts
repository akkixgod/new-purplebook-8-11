import { prisma } from "@/lib/prisma";

export type AuthUserRow = {
  id: string;
  name: string | null;
  email: string;
  emailVerified: Date | null;
  image: string | null;
  password: string | null;
  role: string;
  createdAt: Date;
};

function normalizeEmail(email: string): string {
  return email.trim().toLowerCase();
}

/**
 * SQLite UNIQUE/equality is case-sensitive. Prefer exact lowercase match,
 * then fall back to lower(email) so OAuth/legacy rows still resolve.
 */
export async function findUserByEmail(email: string): Promise<AuthUserRow | null> {
  const normalized = normalizeEmail(email);
  if (!normalized) return null;

  const exact = await prisma.user.findUnique({ where: { email: normalized } });
  if (exact) return exact;

  const rows = await prisma.$queryRawUnsafe<AuthUserRow[]>(
    `SELECT * FROM User WHERE lower(email) = ? LIMIT 1`,
    normalized
  );
  const match = rows[0] ?? null;
  if (!match) return null;

  // Normalize stored email so future lookups hit the unique index.
  if (match.email !== normalized) {
    try {
      await prisma.user.update({
        where: { id: match.id },
        data: { email: normalized },
      });
      return { ...match, email: normalized };
    } catch (err) {
      console.warn("[auth] could not normalize email casing for user", match.id, err);
    }
  }

  return match;
}

export { normalizeEmail };
