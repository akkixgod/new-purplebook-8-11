import { PrismaClient } from "@prisma/client";
import fs from "fs";
import path from "path";

/**
 * Seeds 2026 August Digital ENGLISH as ONE test with Module 1 + Module 2.
 * (Separate Module 1 / Module 2 tests break next-module + continue-to-M2.)
 */
const prisma = new PrismaClient();
const M1_DIR = path.join(__dirname, "data", "2026-august-m1");
const M2_DIR = path.join(__dirname, "data", "2026-august-m2");

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
  answers: (string | null)[];
}

function isGridIn(answer: string): boolean {
  return !["A", "B", "C", "D"].includes(answer);
}

function defaultChoices(answer: string): Choices {
  if (isGridIn(answer)) return { gridIn: true };
  return { A: "", B: "", C: "", D: "" };
}

async function seedModule(
  testId: string,
  modNum: number,
  modMeta: ModuleMeta,
  content: Record<string, QContent>
) {
  const mod = await prisma.module.create({
    data: {
      testId,
      number: modNum,
      timeLimit: modMeta.timeLimit,
    },
  });

  let transcribed = 0;
  let withImages = 0;
  let skipped = 0;

  for (let i = 0; i < modMeta.answers.length; i++) {
    const order = i + 1;
    const answer = modMeta.answers[i];
    if (answer == null || answer === "") {
      skipped++;
      continue;
    }
    const filled = content[String(order)];
    if (!filled?.text) {
      throw new Error(`Missing transcription for ENGLISH Module ${modNum} Q${order}`);
    }
    const choices = filled.choices ?? defaultChoices(answer);
    const imageUrl = filled.imageUrl ?? null;

    await prisma.question.create({
      data: {
        moduleId: mod.id,
        order,
        stimulus: filled.stimulus ?? null,
        text: filled.text,
        imageUrl,
        choices: JSON.stringify(choices),
        correctAnswer: answer,
      },
    });
    transcribed++;
    if (imageUrl) withImages++;
  }

  console.log(
    `  ENGLISH M${modNum}: ${transcribed}q transcribed (${skipped} skipped), ${withImages} with figures → ${mod.id}`
  );
  return mod.id;
}

async function main() {
  const m1Meta = JSON.parse(fs.readFileSync(path.join(M1_DIR, "meta.json"), "utf8"));
  const m1Questions = JSON.parse(fs.readFileSync(path.join(M1_DIR, "questions.json"), "utf8"));
  const m2Meta = JSON.parse(fs.readFileSync(path.join(M2_DIR, "meta.json"), "utf8"));
  const m2Questions = JSON.parse(fs.readFileSync(path.join(M2_DIR, "questions.json"), "utf8"));

  const title = (m1Meta.title as string) || "2026 August Digital";
  const year = m1Meta.year as number;
  const month = m1Meta.month as number;

  console.log("Seeding 2026 August Digital ENGLISH (Module 1 + Module 2 on one test)...");

  // Remove any prior August 2026 English cards (old split Module 1 / Module 2 versions).
  const existing = await prisma.test.findMany({
    where: { year, month, section: "ENGLISH" },
    select: { id: true, version: true },
  });
  for (const t of existing) {
    await prisma.test.delete({ where: { id: t.id } });
    console.log(`Removed existing ENGLISH test version=${JSON.stringify(t.version)}`);
  }

  const test = await prisma.test.create({
    data: {
      title,
      year,
      month,
      section: "ENGLISH",
      version: null,
      isFree: true,
    },
  });

  const m1Id = await seedModule(
    test.id,
    1,
    m1Meta.modules.ENGLISH["1"],
    m1Questions.ENGLISH?.["1"] ?? {}
  );
  const m2Id = await seedModule(
    test.id,
    2,
    m2Meta.modules.ENGLISH["2"],
    m2Questions.ENGLISH?.["2"] ?? {}
  );

  console.log("\nDone!");
  console.log(`  TEST: ${test.id}`);
  console.log(`  Module 1: ${m1Id}`);
  console.log(`  Module 2: ${m2Id}`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
