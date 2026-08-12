/** Map raw correct/total to a Digital SAT–style section scale (200–800).
 * Official College Board section scores are always multiples of 10.
 */
export function scaleSectionScore(correct: number, total: number): number {
  if (total <= 0) return 200;
  const safeCorrect = Math.min(Math.max(0, correct), total);
  const ratio = safeCorrect / total;
  const continuous = 200 + ratio * 600;
  // Snap to nearest official 10-point increment (e.g. 640, 650 — never 644).
  const roundedToTen = Math.round(continuous / 10) * 10;
  return Math.min(800, Math.max(200, roundedToTen));
}
