/** Official SAT papers vs PurpleBook-branded mocks. */

export const PURPLEBOOK_GROUP = "purplebook";

export function getTestGroup(test: { title: string; year: number }): string {
  if (/^PurpleBook/i.test(test.title)) return PURPLEBOOK_GROUP;
  return String(test.year);
}

export function getTestGroupLabel(key: string): string {
  if (key === PURPLEBOOK_GROUP) return "PurpleBook tests";
  return key;
}

/** Years descending, then PurpleBook last. */
export function sortTestGroupKeys(keys: string[]): string[] {
  const years = keys.filter((k) => k !== PURPLEBOOK_GROUP).sort((a, b) => Number(b) - Number(a));
  const rest = keys.includes(PURPLEBOOK_GROUP) ? [PURPLEBOOK_GROUP] : [];
  return [...years, ...rest];
}

/** Sort cards within the active group for predictable ordering. */
export function sortTestsForDisplay<T extends { title: string; year: number; month: number; version: string | null }>(
  tests: T[]
): T[] {
  return [...tests].sort((a, b) => {
    const aPb = getTestGroup(a) === PURPLEBOOK_GROUP;
    const bPb = getTestGroup(b) === PURPLEBOOK_GROUP;
    if (aPb && bPb) {
      return a.title.localeCompare(b.title, undefined, { numeric: true });
    }
    if (a.year !== b.year) return b.year - a.year;
    if (a.month !== b.month) return b.month - a.month;
    return (a.version ?? "").localeCompare(b.version ?? "");
  });
}

export function buildTestGroups<T extends { title: string; year: number }>(
  tests: T[]
): { key: string; label: string; count: number }[] {
  const counts = new Map<string, number>();
  for (const t of tests) {
    const key = getTestGroup(t);
    counts.set(key, (counts.get(key) ?? 0) + 1);
  }
  return sortTestGroupKeys([...counts.keys()]).map((key) => ({
    key,
    label: getTestGroupLabel(key),
    count: counts.get(key) ?? 0,
  }));
}
