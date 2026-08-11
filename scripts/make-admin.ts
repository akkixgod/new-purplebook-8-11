/**
 * Usage: npx ts-node scripts/make-admin.ts your@email.com
 * Makes a user admin by email.
 */
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const email = process.argv[2];
  if (!email) {
    console.error("Usage: npx ts-node scripts/make-admin.ts your@email.com");
    process.exit(1);
  }

  const user = await prisma.user.update({
    where: { email },
    data: { role: "admin" },
  });

  console.log(`✓ ${user.email} is now admin`);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
