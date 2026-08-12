-- Remove duplicate answer rows (keep the earliest id) before uniqueness.
DELETE FROM "Answer"
WHERE EXISTS (
  SELECT 1 FROM "Answer" AS "a2"
  WHERE "a2"."attemptId" = "Answer"."attemptId"
    AND "a2"."questionId" = "Answer"."questionId"
    AND "a2"."id" < "Answer"."id"
);

CREATE UNIQUE INDEX "Answer_attemptId_questionId_key" ON "Answer"("attemptId", "questionId");
