#!/usr/bin/env node
/** Build meta.json + questions.json for 2025-june-us-a. */
const fs = require("fs");
const path = require("path");

const DIR = path.join(__dirname, "..", "prisma", "data", "2025-june-us-a");

function load(name) {
  return JSON.parse(fs.readFileSync(path.join(DIR, name), "utf8"));
}

function cleanQ(q) {
  return {
    stimulus: q.stimulus ?? null,
    text: q.text,
    choices: q.choices,
    imageUrl: q.imageUrl ?? null,
  };
}

function answersFrom(mod) {
  return Object.keys(mod)
    .sort((a, b) => +a - +b)
    .map((k) => mod[k].correctAnswer);
}

function pageMap(mod) {
  const map = {};
  for (const k of Object.keys(mod).sort((a, b) => +a - +b)) {
    map[String(k)] = mod[k].page ?? null;
  }
  return map;
}

function assertCount(label, mod, n) {
  const keys = Object.keys(mod)
    .map(Number)
    .sort((a, b) => a - b);
  if (keys.length !== n || keys[0] !== 1 || keys[keys.length - 1] !== n) {
    throw new Error(`${label} expected 1..${n}, got ${keys.join(",")}`);
  }
  for (const k of keys) {
    const q = mod[String(k)];
    if (!q.text || !q.choices || q.correctAnswer == null || q.correctAnswer === "") {
      throw new Error(`${label} Q${k} incomplete`);
    }
  }
}

const rw1 = load("_rw1.json");
const rw2 = load("_rw2.json");
const m1 = load("_math1.json");
const m2 = load("_math2.json");

assertCount("RW1", rw1, 27);
assertCount("RW2", rw2, 27);
assertCount("MATH1", m1, 22);
assertCount("MATH2", m2, 22);

const expected = {
  RW1: "ABCABCCDADCBAAABCDDAAACBBAB",
  RW2: "DBDCAADAADDCDBDCDCCACBCCDAB",
  MATH1: ["D", "100", "B", "D", "A", "B", "B", "B", "C", "5940", "A", "1", "C", "D", "A", "7", "C", "168", "D", "A", "13", "1.732"],
  MATH2: ["B", "C", "A", "D", "A", "D", "252", "D", "80", "C", "D", "C", "D", "C", "A", "B", "A", "A", "D", "152", "-15", "900"],
};

const a1 = answersFrom(rw1).join("");
const a2 = answersFrom(rw2).join("");
if (a1 !== expected.RW1) throw new Error(`RW1 keys mismatch\n got ${a1}\n want ${expected.RW1}`);
if (a2 !== expected.RW2) throw new Error(`RW2 keys mismatch\n got ${a2}\n want ${expected.RW2}`);
const m1a = answersFrom(m1);
const m2a = answersFrom(m2);
if (JSON.stringify(m1a) !== JSON.stringify(expected.MATH1)) {
  throw new Error(`MATH1 keys mismatch\n got ${m1a}\n want ${expected.MATH1}`);
}
if (JSON.stringify(m2a) !== JSON.stringify(expected.MATH2)) {
  throw new Error(`MATH2 keys mismatch\n got ${m2a}\n want ${expected.MATH2}`);
}

const questions = {
  ENGLISH: {
    "1": Object.fromEntries(Object.keys(rw1).map((k) => [k, cleanQ(rw1[k])])),
    "2": Object.fromEntries(Object.keys(rw2).map((k) => [k, cleanQ(rw2[k])])),
  },
  MATH: {
    "1": Object.fromEntries(Object.keys(m1).map((k) => [k, cleanQ(m1[k])])),
    "2": Object.fromEntries(Object.keys(m2).map((k) => [k, cleanQ(m2[k])])),
  },
};

const meta = {
  slug: "2025-june-us-a",
  title: "2025 June Digital",
  year: 2025,
  month: 6,
  version: "US Form A",
  modules: {
    ENGLISH: {
      "1": {
        timeLimit: 1920,
        pageByQuestion: pageMap(rw1),
        answers: answersFrom(rw1),
      },
      "2": {
        timeLimit: 1920,
        pageByQuestion: pageMap(rw2),
        answers: answersFrom(rw2),
      },
    },
    MATH: {
      "1": {
        timeLimit: 2100,
        pageByQuestion: pageMap(m1),
        answers: answersFrom(m1),
      },
      "2": {
        timeLimit: 2100,
        pageByQuestion: pageMap(m2),
        answers: answersFrom(m2),
      },
    },
  },
  notes: [
    "RW2 Q26–27 filled from prior June mocks (PDF capture had only Q1–25).",
    "Math M1 Q9 filled from 2025-june-int-b Math M1 Q1 (key blank / choices cut off).",
    "Math M1 Q12 also accepts 8 and 11; primary scoring key stored as 1.",
    "RW2 Q19 key printed C/D?; seeded as C.",
  ],
};

fs.writeFileSync(path.join(DIR, "meta.json"), JSON.stringify(meta, null, 2));
fs.writeFileSync(path.join(DIR, "questions.json"), JSON.stringify(questions, null, 2));
console.log("ENGLISH M1", a1);
console.log("ENGLISH M2", a2);
console.log("MATH M1", m1a.join(","));
console.log("MATH M2", m2a.join(","));
console.log("wrote meta.json + questions.json");
