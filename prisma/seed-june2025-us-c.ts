import { PrismaClient } from "@prisma/client";
import fs from "fs";
import path from "path";

const prisma = new PrismaClient();
const DATA_DIR = path.join(__dirname, "data", "2025-june-us-c");

type Choices = Record<string, string> | { gridIn: true };

interface QContent {
  stimulus?: string | null;
  text: string;
  choices: Choices;
  imageUrl?: string | null;
}

interface ModuleMeta {
  timeLimit: number;
  pageByQuestion: Record<string, number>;
  answers: string[];
}

async function seedSection(
  section: "ENGLISH" | "MATH",
  modules: Record<string, ModuleMeta>,
  content: Record<string, Record<string, QContent>>,
  meta: { title: string; year: number; month: number; version: string }
) {
  const existing = await prisma.test.findFirst({
    where: {
      year: meta.year,
      month: meta.month,
      section,
      version: meta.version,
    },
  });
  if (existing) {
    await prisma.test.delete({ where: { id: existing.id } });
    console.log(`Removed existing ${section} test`);
  }

  const test = await prisma.test.create({
    data: {
      title: meta.title,
      year: meta.year,
      month: meta.month,
      section,
      version: meta.version,
      isFree: true,
    },
  });

  for (const modNum of Object.keys(modules).sort()) {
    const modMeta = modules[modNum];
    const mod = await prisma.module.create({
      data: {
        testId: test.id,
        number: Number(modNum),
        timeLimit: modMeta.timeLimit,
      },
    });

    let withImages = 0;
    for (let i = 0; i < modMeta.answers.length; i++) {
      const order = i + 1;
      const answer = modMeta.answers[i];
      const filled = content[modNum]?.[String(order)];
      if (!filled?.text) {
        throw new Error(`Missing transcription for ${section} Module ${modNum} Q${order}`);
      }
      const imageUrl = filled.imageUrl ?? null;
      if (imageUrl) withImages++;

      await prisma.question.create({
        data: {
          moduleId: mod.id,
          order,
          stimulus: filled.stimulus ?? null,
          text: filled.text,
          imageUrl,
          choices: JSON.stringify(filled.choices),
          correctAnswer: answer,
        },
      });
    }
    console.log(
      `  ${section} M${modNum}: ${modMeta.answers.length}q, ${withImages} figures → ${mod.id}`
    );
  }

  return test.id;
}

async function main() {
  const meta = JSON.parse(fs.readFileSync(path.join(DATA_DIR, "meta.json"), "utf8"));
  const questions = JSON.parse(
    fs.readFileSync(path.join(DATA_DIR, "questions.json"), "utf8")
  );

  console.log("Seeding 2025 June US-C (ENGLISH + MATH)...");

  const englishId = await seedSection(
    "ENGLISH",
    meta.modules.ENGLISH,
    questions.ENGLISH ?? {},
    meta
  );
  const mathId = await seedSection("MATH", meta.modules.MATH, questions.MATH ?? {}, meta);

  const empties = await prisma.test.findMany({
    where: { year: 2025, month: 6, version: meta.version },
    include: { modules: { include: { _count: { select: { questions: true } } } } },
  });
  for (const t of empties) {
    const total = t.modules.reduce((s, m) => s + m._count.questions, 0);
    if (total === 0) {
      await prisma.test.delete({ where: { id: t.id } });
      console.log(`Removed empty placeholder ${t.section} ${t.version}`);
    }
  }

  console.log("\nDone!");
  console.log(`  ENGLISH: ${englishId}`);
  console.log(`  MATH:    ${mathId}`);
  console.log("Card: 2025 → 2025 June Digital → US Form C");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
