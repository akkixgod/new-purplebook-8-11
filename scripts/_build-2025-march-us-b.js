const fs = require("fs");
const path = require("path");

const DIR = path.join("prisma", "data", "2025-march-us-b");

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
  if (!out.text || out.text === "PLACEHOLDER_MISSING_PAGE") {
    throw new Error("Unresolved placeholder question");
  }
  if (!out.choices) throw new Error(`Missing choices: ${out.text.slice(0, 40)}`);
  return out;
}

function answersFrom(mod) {
  return Object.keys(mod)
    .sort((a, b) => Number(a) - Number(b))
    .map((k) => {
      const a = mod[k].correctAnswer;
      if (a == null || a === "") throw new Error(`Missing answer for Q${k}`);
      return String(a);
    });
}

const rw1 = load("_rw1.json");
const rw2 = load("_rw2.json");
const math1 = load("_math1.json");
const math2 = load("_math2.json");

const n = (mod) => Object.keys(mod).length;
if (n(rw1) !== 27 || n(rw2) !== 27) throw new Error(`English counts ${n(rw1)}/${n(rw2)}`);
if (n(math1) !== 22 || n(math2) !== 22) throw new Error(`Math counts ${n(math1)}/${n(math2)}`);

function pageByFrom(mod, fallbackStart) {
  const o = {};
  for (const k of Object.keys(mod).sort((a, b) => Number(a) - Number(b))) {
    o[k] = mod[k].page ?? fallbackStart + Number(k) - 1;
  }
  return o;
}

const meta = {
  slug: "2025-march-us-b",
  title: "2025 March Digital",
  year: 2025,
  month: 3,
  version: "US Form B",
  modules: {
    ENGLISH: {
      1: {
        timeLimit: 1920,
        pageByQuestion: pageByFrom(rw1, 1),
        answers: answersFrom(rw1),
      },
      2: {
        timeLimit: 1920,
        pageByQuestion: pageByFrom(rw2, 29),
        answers: answersFrom(rw2),
      },
    },
    MATH: {
      1: {
        timeLimit: 2100,
        pageByQuestion: pageByFrom(math1, 56),
        answers: answersFrom(math1),
      },
      2: {
        timeLimit: 2100,
        pageByQuestion: pageByFrom(math2, 76),
        answers: answersFrom(math2),
      },
    },
  },
};

function sectionContent(modMap) {
  const out = {};
  for (const [qn, q] of Object.entries(modMap)) {
    out[qn] = cleanQ(q);
  }
  return out;
}

const questions = {
  ENGLISH: {
    1: sectionContent(rw1),
    2: sectionContent(rw2),
  },
  MATH: {
    1: sectionContent(math1),
    2: sectionContent(math2),
  },
};

fs.writeFileSync(path.join(DIR, "meta.json"), JSON.stringify(meta, null, 2));
fs.writeFileSync(path.join(DIR, "questions.json"), JSON.stringify(questions, null, 2));
console.log("Wrote meta.json and questions.json");
console.log("ENGLISH M1", meta.modules.ENGLISH["1"].answers.join(""));
console.log("ENGLISH M2", meta.modules.ENGLISH["2"].answers.join(""));
console.log("MATH M1", meta.modules.MATH["1"].answers.join(" "));
console.log("MATH M2", meta.modules.MATH["2"].answers.join(" "));
