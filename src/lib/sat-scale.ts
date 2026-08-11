/** Map raw correct/total to a Digital SAT–style section scale (200–800). */
export function scaleSectionScore(correct: number, total: number): number {
  if (total <= 0) return 200;
  const ratio = Math.min(1, Math.max(0, correct / total));
  return Math.round(200 + ratio * 600);
}
