#!/usr/bin/env node
/** Merge June 2025 Int-A RW drafts into meta.json + questions.json (ENGLISH only). */
const fs = require("fs");
const path = require("path");

const DIR = path.join(__dirname, "..", "prisma", "data", "2025-june-int-a");

function load(name) {
  return JSON.parse(fs.readFileSync(path.join(DIR, name), "utf8"));
}

function mergeParts(...parts) {
  const out = {};
  for (const p of parts) Object.assign(out, p);
  return out;
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
    map[String(k)] = mod[k].page;
  }
  return map;
}

const rw1 = mergeParts(load("_rw1_part1.json"), load("_rw1_part2.json"));
const rw2 = mergeParts(load("_rw2_part1.json"), load("_rw2_part2.json"));

for (const [label, mod, n] of [
  ["RW1", rw1, 27],
  ["RW2", rw2, 27],
]) {
  const keys = Object.keys(mod).map(Number).sort((a, b) => a - b);
  if (keys.length !== n || keys[0] !== 1 || keys[keys.length - 1] !== n) {
    throw new Error(`${label} expected 1..${n}, got ${keys.join(",")}`);
  }
  for (const k of keys) {
    const q = mod[String(k)];
    if (!q.text || !q.choices || !q.correctAnswer) {
      throw new Error(`${label} Q${k} incomplete`);
    }
  }
}

fs.writeFileSync(path.join(DIR, "_rw1.json"), JSON.stringify(rw1, null, 2) + "\n");
fs.writeFileSync(path.join(DIR, "_rw2.json"), JSON.stringify(rw2, null, 2) + "\n");

const questions = {
  ENGLISH: {
    "1": Object.fromEntries(Object.keys(rw1).map((k) => [k, cleanQ(rw1[k])])),
    "2": Object.fromEntries(Object.keys(rw2).map((k) => [k, cleanQ(rw2[k])])),
  },
};

const meta = {
  slug: "2025-june-int-a",
  title: "2025 June Digital",
  year: 2025,
  month: 6,
  version: "International Form A",
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
  },
  notes:
    "Source PDF contains Reading & Writing only. Math modules/keys for Int-A are absent from the EliteXSAT packet.",
};

fs.writeFileSync(path.join(DIR, "meta.json"), JSON.stringify(meta, null, 2) + "\n");
fs.writeFileSync(path.join(DIR, "questions.json"), JSON.stringify(questions, null, 2) + "\n");

console.log("ENGLISH M1", meta.modules.ENGLISH["1"].answers.join(""));
console.log("ENGLISH M2", meta.modules.ENGLISH["2"].answers.join(""));
console.log("wrote meta.json + questions.json (_rw1/_rw2)");
