import { prisma } from "@/lib/prisma";

type SessionUser = {
  id: string;
  email?: string | null;
  name?: string | null;
  image?: string | null;
};

/**
 * JWT session user ids can point at users that never landed in this
 * serverless SQLite instance (/tmp copy). Ensure a matching User row
 * exists so Attempt FK inserts succeed.
 */
export async function resolveSessionUserId(user: SessionUser): Promise<string> {
  const existing = await prisma.user.findUnique({
    where: { id: user.id },
    select: { id: true },
  });
  if (existing) return existing.id;

  const email =
    typeof user.email === "string" && user.email.includes("@")
      ? user.email.trim().toLowerCase()
      : `user-${user.id}@purplebook.local`;

  const byEmail = await prisma.user.findUnique({
    where: { email },
    select: { id: true },
  });
  if (byEmail) return byEmail.id;

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
      (await prisma.user.findUnique({ where: { email }, select: { id: true } }));
    if (again) return again.id;
    throw new Error("Unable to resolve session user for attempt write");
  }
}
