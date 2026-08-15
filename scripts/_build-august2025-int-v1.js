#!/usr/bin/env node
/** Build meta.json + questions.json for 2025-august-int-v1 from module drafts. */
const fs = require("fs");
const path = require("path");

const DIR = path.join(__dirname, "..", "prisma", "data", "2025-august-int-v1");

function load(name) {
  return JSON.parse(fs.readFileSync(path.join(DIR, name), "utf8"));
}

function cleanQ(q) {
  const out = {
    stimulus: q.stimulus ?? null,
    text: q.text,
    choices: q.choices,
    imageUrl: q.imageUrl ?? null,
  };
  return out;
}

function answersFrom(mod) {
  return Object.keys(mod)
    .sort((a, b) => +a - +b)
    .map((k) => mod[k].correctAnswer);
}

function pageMap(mod, offsetByOrder) {
  const map = {};
  for (const k of Object.keys(mod).sort((a, b) => +a - +b)) {
    const order = Number(k);
    const page = mod[k].page ?? offsetByOrder(order);
    map[String(order)] = page;
  }
  return map;
}

const rw1 = load("_rw1.json");
const rw2 = load("_rw2.json");
const m1 = load("_math1.json");
const m2 = load("_math2.json");

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
  slug: "2025-august-int-v1",
  title: "2025 August Digital",
  year: 2025,
  month: 8,
  version: "International Form V1",
  modules: {
    ENGLISH: {
      "1": {
        timeLimit: 1920,
        pageByQuestion: pageMap(rw1, (o) => o),
        answers: answersFrom(rw1),
      },
      "2": {
        timeLimit: 1920,
        pageByQuestion: pageMap(rw2, (o) => 27 + o),
        answers: answersFrom(rw2),
      },
    },
    MATH: {
      "1": {
        timeLimit: 2100,
        pageByQuestion: pageMap(m1, (o) => 54 + o),
        answers: answersFrom(m1),
      },
      "2": {
        timeLimit: 2100,
        pageByQuestion: pageMap(m2, (o) => 77 + o),
        answers: answersFrom(m2),
      },
    },
  },
};

fs.writeFileSync(path.join(DIR, "meta.json"), JSON.stringify(meta, null, 2) + "\n");
fs.writeFileSync(path.join(DIR, "questions.json"), JSON.stringify(questions, null, 2) + "\n");

console.log("ENGLISH M1", meta.modules.ENGLISH["1"].answers.length, meta.modules.ENGLISH["1"].answers.join(""));
console.log("ENGLISH M2", meta.modules.ENGLISH["2"].answers.length, meta.modules.ENGLISH["2"].answers.join(""));
console.log("MATH M1", meta.modules.MATH["1"].answers.length, meta.modules.MATH["1"].answers.join(","));
console.log("MATH M2", meta.modules.MATH["2"].answers.length, meta.modules.MATH["2"].answers.join(","));
console.log("wrote meta.json + questions.json");
