const fs = require("fs");
const path = require("path");

const DIR = path.join("prisma", "data", "2025-march-int-e");

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

const expectedEng1 = "ABBBDBDCACBDCCCDCCDABADCADD".split("");
const expectedEng2 = "BBABCCACBACBCBABCCBDDCDABCA".split("");
const engAnswers1 = answersFrom(rw1);
const engAnswers2 = answersFrom(rw2);
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

const meta = {
  slug: "2025-march-int-e",
  title: "2025 March Digital",
  year: 2025,
  month: 3,
  version: "International Form E",
  modules: {
    ENGLISH: {
      1: {
        timeLimit: 1920,
        pageByQuestion: pageBy(1, 27),
        answers: expectedEng1,
      },
      2: {
        timeLimit: 1920,
        pageByQuestion: pageBy(28, 27),
        answers: expectedEng2,
      },
    },
    MATH: {
      1: {
        timeLimit: 2100,
        pageByQuestion: pageBy(55, 22),
        answers: answersFrom(math1),
      },
      2: {
        timeLimit: 2100,
        pageByQuestion: pageBy(77, 22),
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
