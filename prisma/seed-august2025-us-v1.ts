import { PrismaClient } from "@prisma/client";
import fs from "fs";
import path from "path";

const prisma = new PrismaClient();
const DATA_DIR = path.join(__dirname, "data", "2025-august-us-v1");

type Choices = Record<string, string> | { gridIn: true };

interface QContent {
  stimulus?: string | null;
  text: string;
  choices: Choices;
  imageUrl?: string | null;
  correctAnswer?: string;
}

interface ModuleMeta {
  timeLimit: number;
  pageByQuestion: Record<string, number>;
  answers: string[];
}

function isGridIn(answer: string): boolean {
  return !["A", "B", "C", "D"].includes(answer);
}

function defaultChoices(answer: string): Choices {
  if (isGridIn(answer)) return { gridIn: true };
  return { A: "", B: "", C: "", D: "" };
}

async function seedSection(
  section: "ENGLISH" | "MATH",
  modules: Record<string, ModuleMeta>,
  content: Record<string, Record<string, QContent>>
) {
  const existing = await prisma.test.findFirst({
    where: {
      year: 2025,
      month: 8,
      section,
      version: "US Form V1",
    },
  });
  if (existing) {
    await prisma.test.delete({ where: { id: existing.id } });
    console.log(`Removed existing ${section} test`);
  }

  const test = await prisma.test.create({
    data: {
      title: "2025 August Digital",
      year: 2025,
      month: 8,
      section,
      version: "US Form V1",
      isFree: true,
    },
  });

  for (const modNum of ["1", "2"] as const) {
    const meta = modules[modNum];
    if (!meta) continue;
    const mod = await prisma.module.create({
      data: {
        testId: test.id,
        number: Number(modNum),
        timeLimit: meta.timeLimit,
      },
    });

    let transcribed = 0;
    let withImages = 0;
    for (let i = 0; i < meta.answers.length; i++) {
      const order = i + 1;
      const answer = meta.answers[i];
      const filled = content[modNum]?.[String(order)];
      const choices = filled?.choices ?? defaultChoices(answer);
      const imageUrl = filled?.imageUrl ?? null;
      const correctAnswer = filled?.correctAnswer ?? answer;

      if (!filled?.text) {
        throw new Error(`Missing transcription for ${section} Module ${modNum} Q${order}`);
      }

      await prisma.question.create({
        data: {
          moduleId: mod.id,
          order,
          stimulus: filled.stimulus ?? null,
          text: filled.text,
          imageUrl,
          choices: JSON.stringify(choices),
          correctAnswer,
        },
      });
      transcribed++;
      if (imageUrl) withImages++;
    }
    console.log(
      `  ${section} M${modNum}: ${meta.answers.length}q, ${transcribed} transcribed, ${withImages} with figures → ${mod.id}`
    );
  }

  return test.id;
}

async function main() {
  const meta = JSON.parse(fs.readFileSync(path.join(DATA_DIR, "meta.json"), "utf8"));
  const questions = JSON.parse(
    fs.readFileSync(path.join(DATA_DIR, "questions.json"), "utf8")
  );

  console.log("Seeding 2025 August US V1 (exact text + figures)...");

  const englishId = await seedSection(
    "ENGLISH",
    meta.modules.ENGLISH,
    questions.ENGLISH ?? {}
  );
  const mathId = await seedSection("MATH", meta.modules.MATH, questions.MATH ?? {});

  console.log("\nDone!");
  console.log(`  ENGLISH: ${englishId}`);
  console.log(`  MATH:    ${mathId}`);
  console.log("Card: 2025 → 2025 August Digital → US Form V1");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
