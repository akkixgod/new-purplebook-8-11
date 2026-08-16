const fs = require("fs");
const path = require("path");

const DIR = path.join("prisma", "data", "2025-march-int-a");

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
      return a;
    });
}

const rw1 = load("_rw1.json");
const rw2 = load("_rw2.json");
const math1 = load("_math1.json");
const math2 = load("_math2.json");

const engAnswers1 = Object.keys(rw1)
  .sort((a, b) => Number(a) - Number(b))
  .map((k) => rw1[k].correctAnswer);
const engAnswers2 = Object.keys(rw2)
  .sort((a, b) => Number(a) - Number(b))
  .map((k) => rw2[k].correctAnswer);

const expectedEng1 = "AAAAAADAACDBCAABCACBBBBBAAA".split("");
const expectedEng2 = "BADDABCDABCCBDDDBBDABCBCDBB".split("");
if (engAnswers1.join("") !== expectedEng1.join("")) {
  console.warn("RW1 key mismatch", engAnswers1.join(""), "vs", expectedEng1.join(""));
}
if (engAnswers2.join("") !== expectedEng2.join("")) {
  console.warn("RW2 key mismatch", engAnswers2.join(""), "vs", expectedEng2.join(""));
}

const pageBy = (start, n) => {
  const o = {};
  for (let i = 1; i <= n; i++) o[String(i)] = start + i - 1;
  return o;
};

const math1Pages = {
  1: 55,
  2: 56,
  3: 57,
  4: 55,
  5: 58,
  6: 59,
  7: 59,
  8: 60,
  9: 61,
  10: 62,
  11: 63,
  12: 65,
  13: 66,
  14: 68,
  15: 69,
  16: 70,
  17: 70,
  18: 71,
  19: 72,
  20: 73,
  21: 74,
  22: 75,
};
const math2Pages = {
  1: 76,
  2: 77,
  3: 78,
  4: 79,
  5: 80,
  6: 81,
  7: 82,
  8: 83,
  9: 84,
  10: 85,
  11: 86,
  12: 87,
  13: 88,
  14: 89,
  15: 90,
  16: 90,
  17: 91,
  18: 92,
  19: 94,
  20: 95,
  21: 96,
  22: 96,
};

const meta = {
  slug: "2025-march-int-a",
  title: "2025 March Digital",
  year: 2025,
  month: 3,
  version: "International Form A",
  modules: {
    ENGLISH: {
      1: {
        timeLimit: 1920,
        pageByQuestion: pageBy(1, 27),
        answers: engAnswers1.length === 27 ? engAnswers1 : expectedEng1,
      },
      2: {
        timeLimit: 1920,
        pageByQuestion: pageBy(28, 27),
        answers: engAnswers2.length === 27 ? engAnswers2 : expectedEng2,
      },
    },
    MATH: {
      1: {
        timeLimit: 2100,
        pageByQuestion: Object.fromEntries(
          Object.entries(math1Pages).map(([k, v]) => [k, v])
        ),
        answers: answersFrom(math1),
      },
      2: {
        timeLimit: 2100,
        pageByQuestion: Object.fromEntries(
          Object.entries(math2Pages).map(([k, v]) => [k, v])
        ),
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

// Prefer answer key from PDF for English even if JSON also stores it
meta.modules.ENGLISH["1"].answers = expectedEng1;
meta.modules.ENGLISH["2"].answers = expectedEng2;

fs.writeFileSync(path.join(DIR, "meta.json"), JSON.stringify(meta, null, 2));
fs.writeFileSync(path.join(DIR, "questions.json"), JSON.stringify(questions, null, 2));
console.log("Wrote meta.json and questions.json");
console.log("ENGLISH M1", meta.modules.ENGLISH["1"].answers.length);
console.log("ENGLISH M2", meta.modules.ENGLISH["2"].answers.length);
console.log("MATH M1", meta.modules.MATH["1"].answers.join(" "));
console.log("MATH M2", meta.modules.MATH["2"].answers.join(" "));
