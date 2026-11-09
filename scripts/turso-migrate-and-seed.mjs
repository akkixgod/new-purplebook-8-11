/**
 * Apply SQLite schema to Turso and import catalog from prisma/dev.db (batched).
 * Loads TURSO_* from .env.turso.local / .env.local (never prints secrets).
 */
import { createClient } from "@libsql/client";
import { readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";

function loadEnvFile(filePath) {
  if (!existsSync(filePath)) return;
  for (const line of readFileSync(filePath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 0) continue;
    const key = trimmed.slice(0, eq);
    let val = trimmed.slice(eq + 1);
    if (
      (val.startsWith('"') && val.endsWith('"')) ||
      (val.startsWith("'") && val.endsWith("'"))
    ) {
      val = val.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = val;
  }
}

loadEnvFile(path.join(process.cwd(), ".env.turso.local"));
loadEnvFile(path.join(process.cwd(), ".env.local"));

const url = process.env.TURSO_DATABASE_URL?.trim();
const authToken = process.env.TURSO_AUTH_TOKEN?.trim();
if (!url || !authToken) {
  console.error("Missing TURSO_DATABASE_URL or TURSO_AUTH_TOKEN");
  process.exit(1);
}

const remote = createClient({ url, authToken });

const SCHEMA_SQL = `
CREATE TABLE IF NOT EXISTS User (
  id TEXT PRIMARY KEY NOT NULL,
  name TEXT,
  email TEXT NOT NULL,
  emailVerified DATETIME,
  image TEXT,
  password TEXT,
  role TEXT NOT NULL DEFAULT 'user',
  createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE UNIQUE INDEX IF NOT EXISTS User_email_key ON User(email);

CREATE TABLE IF NOT EXISTS Account (
  id TEXT PRIMARY KEY NOT NULL,
  userId TEXT NOT NULL,
  type TEXT NOT NULL,
  provider TEXT NOT NULL,
  providerAccountId TEXT NOT NULL,
  refresh_token TEXT,
  access_token TEXT,
  expires_at INTEGER,
  token_type TEXT,
  scope TEXT,
  id_token TEXT,
  session_state TEXT,
  FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS Account_provider_providerAccountId_key ON Account(provider, providerAccountId);

CREATE TABLE IF NOT EXISTS Session (
  id TEXT PRIMARY KEY NOT NULL,
  sessionToken TEXT NOT NULL,
  userId TEXT NOT NULL,
  expires DATETIME NOT NULL,
  FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS Session_sessionToken_key ON Session(sessionToken);

CREATE TABLE IF NOT EXISTS VerificationToken (
  identifier TEXT NOT NULL,
  token TEXT NOT NULL,
  expires DATETIME NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS VerificationToken_token_key ON VerificationToken(token);
CREATE UNIQUE INDEX IF NOT EXISTS VerificationToken_identifier_token_key ON VerificationToken(identifier, token);

CREATE TABLE IF NOT EXISTS Test (
  id TEXT PRIMARY KEY NOT NULL,
  title TEXT NOT NULL,
  year INTEGER NOT NULL,
  month INTEGER NOT NULL,
  section TEXT NOT NULL,
  version TEXT,
  isFree BOOLEAN NOT NULL DEFAULT 1,
  createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Module (
  id TEXT PRIMARY KEY NOT NULL,
  testId TEXT NOT NULL,
  number INTEGER NOT NULL,
  timeLimit INTEGER NOT NULL DEFAULT 1920,
  FOREIGN KEY (testId) REFERENCES Test(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS Module_testId_idx ON Module(testId);
CREATE INDEX IF NOT EXISTS Module_testId_number_idx ON Module(testId, number);

CREATE TABLE IF NOT EXISTS Question (
  id TEXT PRIMARY KEY NOT NULL,
  moduleId TEXT NOT NULL,
  "order" INTEGER NOT NULL,
  stimulus TEXT,
  text TEXT NOT NULL,
  imageUrl TEXT,
  choices TEXT NOT NULL,
  correctAnswer TEXT NOT NULL,
  explanation TEXT,
  FOREIGN KEY (moduleId) REFERENCES Module(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS Question_moduleId_idx ON Question(moduleId);
CREATE INDEX IF NOT EXISTS Question_moduleId_order_idx ON Question(moduleId, "order");

CREATE TABLE IF NOT EXISTS Attempt (
  id TEXT PRIMARY KEY NOT NULL,
  userId TEXT,
  moduleId TEXT NOT NULL,
  claimToken TEXT,
  startedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finishedAt DATETIME,
  score INTEGER,
  totalQuestions INTEGER,
  timeSpent INTEGER,
  FOREIGN KEY (userId) REFERENCES User(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (moduleId) REFERENCES Module(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE INDEX IF NOT EXISTS Attempt_userId_idx ON Attempt(userId);
CREATE INDEX IF NOT EXISTS Attempt_moduleId_idx ON Attempt(moduleId);
CREATE INDEX IF NOT EXISTS Attempt_userId_moduleId_idx ON Attempt(userId, moduleId);
CREATE INDEX IF NOT EXISTS Attempt_finishedAt_idx ON Attempt(finishedAt);
CREATE INDEX IF NOT EXISTS Attempt_claimToken_idx ON Attempt(claimToken);

CREATE TABLE IF NOT EXISTS Answer (
  id TEXT PRIMARY KEY NOT NULL,
  attemptId TEXT NOT NULL,
  questionId TEXT NOT NULL,
  selected TEXT,
  isCorrect BOOLEAN NOT NULL,
  FOREIGN KEY (attemptId) REFERENCES Attempt(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (questionId) REFERENCES Question(id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS Answer_attemptId_questionId_key ON Answer(attemptId, questionId);
CREATE INDEX IF NOT EXISTS Answer_attemptId_idx ON Answer(attemptId);
CREATE INDEX IF NOT EXISTS Answer_questionId_idx ON Answer(questionId);
`;

console.info("[turso] applying schema…");
for (const stmt of SCHEMA_SQL.split(";")
  .map((s) => s.trim())
  .filter(Boolean)) {
  await remote.execute(stmt);
}

const tables = await remote.execute(
  "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
);
console.info(
  "[turso] tables:",
  tables.rows.map((r) => r.name).join(", ")
);

const localPath = path.join(process.cwd(), "prisma", "dev.db");
if (!existsSync(localPath)) {
  console.warn("[turso] no local prisma/dev.db — schema only");
  process.exit(0);
}

console.info("[turso] importing catalog from", localPath);
const local = new DatabaseSync(localPath);

async function copyTable(table, columns, batchSize = 80) {
  const rows = local.prepare(`SELECT ${columns.join(", ")} FROM ${table}`).all();
  console.info(`[turso] ${table}: ${rows.length} rows`);
  if (!rows.length) return;

  const placeholders = columns.map(() => "?").join(", ");
  const sql = `INSERT OR REPLACE INTO ${table} (${columns.join(", ")}) VALUES (${placeholders})`;

  for (let i = 0; i < rows.length; i += batchSize) {
    const chunk = rows.slice(i, i + batchSize);
    const stmts = chunk.map((row) => ({
      sql,
      args: columns.map((c) => {
        const key = c.replaceAll('"', "");
        const v = row[key];
        if (typeof v === "boolean") return v ? 1 : 0;
        return v ?? null;
      }),
    }));
    await remote.batch(stmts, "write");
    if ((i / batchSize) % 5 === 0 || i + batchSize >= rows.length) {
      console.info(
        `[turso] ${table}: ${Math.min(i + batchSize, rows.length)}/${rows.length}`
      );
    }
  }
}

await copyTable("Test", [
  "id",
  "title",
  "year",
  "month",
  "section",
  "version",
  "isFree",
  "createdAt",
]);
await copyTable("Module", ["id", "testId", "number", "timeLimit"]);
await copyTable("Question", [
  "id",
  "moduleId",
  '"order"',
  "stimulus",
  "text",
  "imageUrl",
  "choices",
  "correctAnswer",
  "explanation",
]);

const counts = await remote.execute(
  "SELECT (SELECT COUNT(*) FROM Test) AS tests, (SELECT COUNT(*) FROM Module) AS modules, (SELECT COUNT(*) FROM Question) AS questions"
);
console.info("[turso] catalog counts:", counts.rows[0]);
process.exit(0);
