const journeyKey = (testId: string) => `purplebook_test_journey_${testId}`;

export type TestJourney = {
  testId: string;
  module1AttemptId: string;
  module1ModuleId: string;
  updatedAt: number;
};

function writeJourney(storage: Storage, data: Omit<TestJourney, "updatedAt">) {
  const payload: TestJourney = { ...data, updatedAt: Date.now() };
  storage.setItem(journeyKey(data.testId), JSON.stringify(payload));
}

function readJourney(storage: Storage, testId: string): TestJourney | null {
  const raw = storage.getItem(journeyKey(testId));
  if (!raw) return null;
  return JSON.parse(raw) as TestJourney;
}

/** Persist Module 1 attempt across tabs/refreshes (localStorage) with sessionStorage mirror. */
export function saveModule1Journey(data: Omit<TestJourney, "updatedAt">): void {
  try {
    writeJourney(localStorage, data);
  } catch {
    /* ignore */
  }
  try {
    writeJourney(sessionStorage, data);
  } catch {
    /* ignore */
  }
}

export function readModule1Journey(testId: string): TestJourney | null {
  try {
    const fromLocal = readJourney(localStorage, testId);
    if (fromLocal?.module1AttemptId) return fromLocal;
  } catch {
    /* ignore */
  }
  try {
    return readJourney(sessionStorage, testId);
  } catch {
    return null;
  }
}

export function clearModule1Journey(testId: string): void {
  try {
    localStorage.removeItem(journeyKey(testId));
  } catch {
    /* ignore */
  }
  try {
    sessionStorage.removeItem(journeyKey(testId));
  } catch {
    /* ignore */
  }
}
