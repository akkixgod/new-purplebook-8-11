const journeyKey = (testId: string) => `purplebook_test_journey_${testId}`;

export type TestJourney = {
  testId: string;
  module1AttemptId: string;
  module1ModuleId: string;
  updatedAt: number;
};

export function saveModule1Journey(data: Omit<TestJourney, "updatedAt">): void {
  try {
    const payload: TestJourney = { ...data, updatedAt: Date.now() };
    sessionStorage.setItem(journeyKey(data.testId), JSON.stringify(payload));
  } catch {
    /* ignore */
  }
}

export function readModule1Journey(testId: string): TestJourney | null {
  try {
    const raw = sessionStorage.getItem(journeyKey(testId));
    if (!raw) return null;
    return JSON.parse(raw) as TestJourney;
  } catch {
    return null;
  }
}

export function clearModule1Journey(testId: string): void {
  try {
    sessionStorage.removeItem(journeyKey(testId));
  } catch {
    /* ignore */
  }
}
