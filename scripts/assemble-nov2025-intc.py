#!/usr/bin/env python3
"""Assemble meta.json + questions.json for 2025 Nov Int-C."""

from __future__ import annotations

import json
from pathlib import Path

DATA = Path("prisma/data/2025-nov-int-c")


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def clean_module(mod: dict) -> dict:
    out = {}
    for k, v in mod.items():
        out[str(k)] = {
            "stimulus": v.get("stimulus"),
            "text": v["text"],
            "choices": v["choices"],
            "imageUrl": v.get("imageUrl"),
        }
    return out


def answers_list(obj: dict) -> list:
    if "answers" in obj:
        return obj["answers"]
    return [obj[str(i)] for i in range(1, len(obj) + 1)]


def main() -> None:
    rw1 = clean_module(load("_rw1.json"))
    rw2 = clean_module(load("_rw2.json"))
    m1 = clean_module(load("_math1.json"))
    m2 = clean_module(load("_math2.json"))
    a_rw1 = answers_list(load("_answers_rw1.json"))
    a_rw2 = answers_list(load("_answers_rw2.json"))
    a_m1 = answers_list(load("_answers_math1.json"))
    a_m2 = answers_list(load("_answers_math2.json"))

    assert len(rw1) == 27 and len(a_rw1) == 27
    assert len(rw2) == 27 and len(a_rw2) == 27
    assert len(m1) == 22 and len(a_m1) == 22
    assert len(m2) == 22 and len(a_m2) == 22

    questions = {"ENGLISH": {"1": rw1, "2": rw2}, "MATH": {"1": m1, "2": m2}}
    meta = {
        "slug": "2025-nov-int-c",
        "title": "2025 November Digital",
        "year": 2025,
        "month": 11,
        "version": "International Form C",
        "modules": {
            "ENGLISH": {
                "1": {"timeLimit": 1920, "answers": a_rw1},
                "2": {"timeLimit": 1920, "answers": a_rw2},
            },
            "MATH": {
                "1": {"timeLimit": 2100, "answers": a_m1},
                "2": {"timeLimit": 2100, "answers": a_m2},
            },
        },
        "notes": (
            "EliteXSAT PDF includes partial easy Module 2 routes; "
            "this seed uses Module 1 + hard Module 2 only. "
            "Source PDF has no answer-key pages — keys solved from items."
        ),
    }

    (DATA / "questions.json").write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (DATA / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("wrote questions.json + meta.json")
    print("ENGLISH M1", "".join(a_rw1))
    print("ENGLISH M2", "".join(a_rw2))
    print("MATH M1", a_m1)
    print("MATH M2", a_m2)


if __name__ == "__main__":
    main()
