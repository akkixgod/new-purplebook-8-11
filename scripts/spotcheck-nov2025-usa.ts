import { PrismaClient } from "@prisma/client";

const p = new PrismaClient();

async function main() {
  const en = await p.module.findFirst({
    where: {
      number: 1,
      test: { year: 2025, month: 11, section: "ENGLISH", version: "US Form A" },
    },
    include: {
      test: true,
      questions: { where: { order: { in: [1, 2, 4, 10, 12] } }, orderBy: { order: "asc" } },
    },
  });
  const math = await p.module.findFirst({
    where: {
      number: 1,
      test: { year: 2025, month: 11, section: "MATH", version: "US Form A" },
    },
    include: {
      questions: { where: { order: { in: [1, 5] } }, orderBy: { order: "asc" } },
    },
  });

  console.log("EN module:", en?.id);
  console.log("MATH module:", math?.id);
  for (const q of en?.questions ?? []) {
    console.log(
      `EN Q${q.order} ans=${q.correctAnswer} u=${(q.stimulus || "").includes("<u>")} img=${q.imageUrl}`
    );
    console.log("  ", (q.stimulus || "").slice(0, 100));
    console.log("  ", q.text);
    console.log("  ", q.choices);
  }
  for (const q of math?.questions ?? []) {
    console.log(
      `MA Q${q.order} ans=${q.correctAnswer} img=${q.imageUrl}`
    );
    console.log("  ", q.text);
    console.log("  ", q.choices);
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => p.$disconnect());
