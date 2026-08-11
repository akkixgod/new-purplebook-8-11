import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

// Answer keys from the answer key page of the PDF
// R&W Module 1: 27 questions
const rwMod1Answers = [
  "C","B","B","D","A","C","D","B","A","C",
  "C","B","C","A","B","C","C","A","D","D",
  "A","D","C","D","C","B","D",
];

// R&W Module 2: 27 questions
const rwMod2Answers = [
  "C","B","A","D","D","C","D","C","A","D",
  "C","D","B","B","B","C","A","A","D","D",
  "B","C","A","C","A","D","B",
];

// Math Module 1: 22 questions (some grid-in)
// 1-10: D D C [28] A [10.8] C C B B
// 11-20: A C C A [10.8] B [189] [8] [65/54] A
// 21-22: B C
const mathMod1Answers = [
  "D","D","C","28","A","10.8","C","C","B","B",
  "A","C","C","A","10.8","B","189","8","65/54","A",
  "B","C",
];

// Math Module 2: 22 questions (some grid-in)
// 1-10: D D A C [558] B A [22] B B
// 11-20: A C D C A [10] A A [56] C
// 21-22: [1200] [122]
const mathMod2Answers = [
  "D","D","A","C","558","B","A","22","B","B",
  "A","C","D","C","A","10","A","A","56","C",
  "1200","122",
];

function isGridIn(answer: string): boolean {
  return !["A","B","C","D"].includes(answer);
}

function makeChoices(answer: string): string {
  if (isGridIn(answer)) {
    return JSON.stringify({ gridIn: true });
  }
  return JSON.stringify({ A: "", B: "", C: "", D: "" });
}

async function main() {
  console.log("Seeding SAT 2024 March Digital (International Form A)...");

  // --- ENGLISH (Reading & Writing) ---
  const rwTest = await prisma.test.create({
    data: {
      title: "2024 March Digital",
      year: 2024,
      month: 3,
      section: "ENGLISH",
      version: "International Form A",
      isFree: true,
    },
  });
  console.log("Created ENGLISH test:", rwTest.id);

  const rwMod1 = await prisma.module.create({
    data: { testId: rwTest.id, number: 1, timeLimit: 1920 }, // 32 min
  });
  const rwMod2 = await prisma.module.create({
    data: { testId: rwTest.id, number: 2, timeLimit: 1920 },
  });

  for (let i = 0; i < rwMod1Answers.length; i++) {
    await prisma.question.create({
      data: {
        moduleId: rwMod1.id,
        order: i + 1,
        text: `[Question ${i + 1} — text not available, PDF is image-based. Edit in admin panel.]`,
        choices: makeChoices(rwMod1Answers[i]),
        correctAnswer: rwMod1Answers[i],
      },
    });
  }
  console.log(`Created ${rwMod1Answers.length} questions for R&W Module 1`);

  for (let i = 0; i < rwMod2Answers.length; i++) {
    await prisma.question.create({
      data: {
        moduleId: rwMod2.id,
        order: i + 1,
        text: `[Question ${i + 1} — text not available, PDF is image-based. Edit in admin panel.]`,
        choices: makeChoices(rwMod2Answers[i]),
        correctAnswer: rwMod2Answers[i],
      },
    });
  }
  console.log(`Created ${rwMod2Answers.length} questions for R&W Module 2`);

  // --- MATH ---
  const mathTest = await prisma.test.create({
    data: {
      title: "2024 March Digital",
      year: 2024,
      month: 3,
      section: "MATH",
      version: "International Form A",
      isFree: true,
    },
  });
  console.log("Created MATH test:", mathTest.id);

  const mathMod1 = await prisma.module.create({
    data: { testId: mathTest.id, number: 1, timeLimit: 2100 }, // 35 min
  });
  const mathMod2 = await prisma.module.create({
    data: { testId: mathTest.id, number: 2, timeLimit: 2100 },
  });

  for (let i = 0; i < mathMod1Answers.length; i++) {
    await prisma.question.create({
      data: {
        moduleId: mathMod1.id,
        order: i + 1,
        text: `[Question ${i + 1} — text not available, PDF is image-based. Edit in admin panel.]`,
        choices: makeChoices(mathMod1Answers[i]),
        correctAnswer: mathMod1Answers[i],
      },
    });
  }
  console.log(`Created ${mathMod1Answers.length} questions for Math Module 1`);

  for (let i = 0; i < mathMod2Answers.length; i++) {
    await prisma.question.create({
      data: {
        moduleId: mathMod2.id,
        order: i + 1,
        text: `[Question ${i + 1} — text not available, PDF is image-based. Edit in admin panel.]`,
        choices: makeChoices(mathMod2Answers[i]),
        correctAnswer: mathMod2Answers[i],
      },
    });
  }
  console.log(`Created ${mathMod2Answers.length} questions for Math Module 2`);

  console.log("\nDone! Summary:");
  console.log(`  ENGLISH test id: ${rwTest.id}`);
  console.log(`    Module 1 id: ${rwMod1.id} (${rwMod1Answers.length} questions)`);
  console.log(`    Module 2 id: ${rwMod2.id} (${rwMod2Answers.length} questions)`);
  console.log(`  MATH test id: ${mathTest.id}`);
  console.log(`    Module 1 id: ${mathMod1.id} (${mathMod1Answers.length} questions)`);
  console.log(`    Module 2 id: ${mathMod2.id} (${mathMod2Answers.length} questions)`);
}

main()
  .catch(console.error)
  .finally(() => prisma.$disconnect());
