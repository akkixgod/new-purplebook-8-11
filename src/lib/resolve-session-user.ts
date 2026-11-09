import { prisma } from "@/lib/prisma";
import { findUserByEmail, normalizeEmail } from "@/lib/find-user-by-email";

type SessionUser = {
  id: string;
  email?: string | null;
  name?: string | null;
  image?: string | null;
};

/**
 * JWT session user ids can point at users that never landed in this DB instance,
 * or at a stale id after email-based restore. Ensure a matching User row exists
 * and migrate orphaned attempts onto the canonical account id.
 */
export async function resolveSessionUserId(user: SessionUser): Promise<string> {
  const existing = await prisma.user.findUnique({
    where: { id: user.id },
    select: { id: true },
  });
  if (existing) return existing.id;

  const email =
    typeof user.email === "string" && user.email.includes("@")
      ? normalizeEmail(user.email)
      : `user-${user.id}@purplebook.local`;

  const byEmail = await findUserByEmail(email);
  if (byEmail) {
    if (byEmail.id !== user.id) {
      try {
        const moved = await prisma.attempt.updateMany({
          where: { userId: user.id },
          data: { userId: byEmail.id },
        });
        if (moved.count > 0) {
          console.info("[resolveSessionUserId] migrated attempts to canonical user", {
            from: user.id,
            to: byEmail.id,
            count: moved.count,
          });
        }
      } catch (error) {
        console.warn("[resolveSessionUserId] attempt migration failed", error);
      }
    }
    return byEmail.id;
  }

  try {
    const created = await prisma.user.create({
      data: {
        id: user.id,
        email,
        name: user.name ?? null,
        image: user.image ?? null,
      },
      select: { id: true },
    });
    return created.id;
  } catch {
    // Race: another instance created the same email/id.
    const again =
      (await prisma.user.findUnique({ where: { id: user.id }, select: { id: true } })) ??
      (await findUserByEmail(email));
    if (again) return again.id;
    throw new Error("Unable to resolve session user for attempt write");
  }
}
