import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  const tests = await prisma.test.findMany({
    include: {
      modules: {
        include: {
          _count: { select: { questions: true } },
          questions: { where: { order: 1 }, take: 1 },
        },
      },
    },
    orderBy: [{ year: "desc" }, { month: "desc" }, { section: "asc" }],
  });

  for (const t of tests) {
    console.log(`\n${t.year}-${t.month} ${t.section} | ${t.title} | ${t.version}`);
    for (const m of t.modules) {
      const q = m.questions[0];
      console.log(
        `  M${m.number} (${m._count.questions}q) Q1=${q?.text.slice(0, 70)} | stim=${Boolean(q?.stimulus)} | img=${q?.imageUrl}`
      );
    }
  }
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
