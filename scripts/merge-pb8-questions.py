#!/usr/bin/env python3
"""Merge purplebook-test-8 module JSON parts into questions.json."""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path("prisma/data/purplebook-test-8")


def load(name: str) -> dict:
    path = DATA / name
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    rw1 = load("_rw1.json")
    rw2 = load("_rw2.json")
    m1 = load("_math1.json")
    m2 = load("_math2.json")
    for label, d, n in (
        ("RW1", rw1, 27),
        ("RW2", rw2, 27),
        ("Math1", m1, 22),
        ("Math2", m2, 22),
    ):
        if len(d) != n:
            raise SystemExit(f"{label}: expected {n} questions, got {len(d)}")
        for i in range(1, n + 1):
            if str(i) not in d:
                raise SystemExit(f"{label}: missing Q{i}")
            q = d[str(i)]
            if not q.get("text"):
                raise SystemExit(f"{label} Q{i}: empty text")

    out = {
        "ENGLISH": {"1": rw1, "2": rw2},
        "MATH": {"1": m1, "2": m2},
    }
    path = DATA / "questions.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
