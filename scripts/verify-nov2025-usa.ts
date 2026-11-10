import { PrismaClient } from "@prisma/client";

const p = new PrismaClient();

async function main() {
  const tests = await p.test.findMany({
    where: { year: 2025, month: 11 },
    include: {
      modules: { include: { _count: { select: { questions: true } } } },
    },
    orderBy: [{ version: "asc" }, { section: "asc" }],
  });

  for (const t of tests) {
    const counts = t.modules
      .map((m) => `M${m.number}:${m._count.questions}q/${m.timeLimit}s`)
      .join(", ");
    console.log(t.section, "|", t.version, "|", counts);
  }

  const eq1 = await p.question.findFirst({
    where: {
      order: 1,
      module: {
        number: 1,
        test: {
          year: 2025,
          month: 11,
          section: "ENGLISH",
          version: "US Form A",
        },
      },
    },
  });
  console.log("\nEN M1 Q1 answer:", eq1?.correctAnswer);
  console.log("stim:", eq1?.stimulus?.slice(0, 140));
  console.log("text:", eq1?.text);
  console.log("choices:", eq1?.choices);

  const mq5 = await p.question.findFirst({
    where: {
      order: 5,
      module: {
        number: 1,
        test: { year: 2025, month: 11, section: "MATH", version: "US Form A" },
      },
    },
  });
  console.log("\nMA M1 Q5 answer:", mq5?.correctAnswer);
  console.log("image:", mq5?.imageUrl);
  console.log("text:", mq5?.text);
  console.log("choices:", mq5?.choices);

  const empty = tests.filter((t) =>
    t.modules.some((m) => m._count.questions === 0)
  );
  console.log(
    "\nempty modules:",
    empty.map((t) => `${t.section} ${t.version}`)
  );
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => p.$disconnect());
