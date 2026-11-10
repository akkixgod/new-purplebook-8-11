#!/usr/bin/env python3
"""Parse 2025 Nov Int-B page texts into draft question JSON (hard M2 only)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("public/mocks/2025-nov-int-b/pages")
OUT = Path("prisma/data/2025-nov-int-b")
OUT.mkdir(parents=True, exist_ok=True)

# TOC: RW M1; RW M2 easy (21, partial); RW M2 hard (27); Math M1; Math M2 easy (14); Math M2 hard (22)
MODULES = {
    ("ENGLISH", "1"): {
        "start": 1,
        "end": 15,
        "count": 27,
        "label": "RW M1",
        "cut_at": "Section: Section 1, Module 2",
    },
    ("ENGLISH", "2"): {"start": 27, "end": 42, "count": 27, "label": "RW M2 hard"},
    ("MATH", "1"): {"start": 42, "end": 52, "count": 22, "label": "Math M1"},
    ("MATH", "2"): {"start": 59, "end": 68, "count": 22, "label": "Math M2 hard"},
}


def load_pages(start: int, end: int, cut_at: str | None = None) -> str:
    chunks = []
    for n in range(start, end + 1):
        p = ROOT / f"page-{n:02d}.txt"
        chunks.append(p.read_text(encoding="utf-8"))
    text = "\n".join(chunks)
    if cut_at and cut_at in text:
        text = text.split(cut_at, 1)[0]
    return text


def strip_section_headers(text: str) -> str:
    text = re.sub(
        r"Section:\s*Section\s+\d+,\s*Module\s+\d+:[^\n]*\n[^\n]*\(.*?questions\)\n?",
        "\n",
        text,
        flags=re.I,
    )
    text = re.sub(r"^所有分组[\s\S]*?(?=^\d+\.\s*$)", "", text, count=1, flags=re.M)
    text = re.sub(
        r"^(?:\d+\.\s+Section\s+\d+,.*?\)\s*\n)+",
        "",
        text,
        flags=re.M,
    )
    return text


Q_SPLIT = re.compile(r"(?m)^(?P<n>\d{1,2})\.\s*$")
CHOICE_RE = re.compile(r"(?m)^([A-D])\.\s*(.*)$")

PROMPT_HINTS = (
    "Which choice",
    "As used in the text",
    "What is",
    "How many",
    "Based on",
    "The student wants",
    "Which quotation",
    "Which finding",
    "Which statement",
    "Which of the following",
    "If ",
    "In the ",
    "For ",
    "A ",
    "An ",
    "According to",
    "The table",
    "The graph",
    "The figure",
)


def split_questions(text: str) -> dict[int, str]:
    text = strip_section_headers(text)
    matches = list(Q_SPLIT.finditer(text))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        n = int(m.group("n"))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if n not in out:
            out[n] = body
    return out


def parse_choices(body: str) -> tuple[str, dict[str, str] | dict[str, bool]]:
    lines = body.splitlines()
    choice_idxs = [i for i, ln in enumerate(lines) if CHOICE_RE.match(ln.strip())]
    if not choice_idxs:
        return body.strip(), {"gridIn": True}

    first = choice_idxs[0]
    stem = "\n".join(lines[:first]).strip()
    choices: dict[str, str] = {}
    for j, idx in enumerate(choice_idxs):
        m = CHOICE_RE.match(lines[idx].strip())
        assert m
        letter = m.group(1)
        parts = [m.group(2).strip()]
        next_idx = choice_idxs[j + 1] if j + 1 < len(choice_idxs) else len(lines)
        for ln in lines[idx + 1 : next_idx]:
            if not ln.strip():
                continue
            parts.append(ln.strip())
        choices[letter] = " ".join(p for p in parts if p).strip()
    if set(choices) != {"A", "B", "C", "D"}:
        return body.strip(), {"gridIn": True}
    return stem, choices


def split_prompt_stimulus(stem: str, section: str) -> tuple[str | None, str]:
    stem = stem.strip()
    if not stem:
        return None, ""
    if section == "MATH":
        return None, stem

    lines = stem.splitlines()
    first = lines[0].strip() if lines else ""
    if any(first.startswith(h) for h in PROMPT_HINTS) or first.endswith("?"):
        prompt_lines = [first]
        i = 1
        while i < len(lines) and lines[i].strip():
            if i >= 1 and len(first) < 120 and len(lines[i].strip()) > 80:
                break
            prompt_lines.append(lines[i].strip())
            i += 1
        if len(prompt_lines) == 1 or (
            len(prompt_lines) <= 3 and all(len(p) < 160 for p in prompt_lines)
        ):
            text = " ".join(prompt_lines).strip()
            rest = "\n".join(lines[len(prompt_lines) :]).strip()
            return (rest or None), text
    return None, stem


def main() -> None:
    draft: dict = {"ENGLISH": {}, "MATH": {}}
    summary = []
    for (section, mod), meta in MODULES.items():
        raw = load_pages(meta["start"], meta["end"], meta.get("cut_at"))
        qs = split_questions(raw)
        mod_out: dict[str, dict] = {}
        missing = []
        for n in range(1, meta["count"] + 1):
            body = qs.get(n)
            if not body:
                missing.append(n)
                mod_out[str(n)] = {
                    "stimulus": None,
                    "text": f"MISSING Q{n}",
                    "choices": {"A": "", "B": "", "C": "", "D": ""},
                    "imageUrl": None,
                    "_raw": None,
                }
                continue
            stem, choices = parse_choices(body)
            stimulus, text = split_prompt_stimulus(stem, section)
            mod_out[str(n)] = {
                "stimulus": stimulus,
                "text": text,
                "choices": choices,
                "imageUrl": None,
                "_raw": body,
            }
        draft[section][mod] = mod_out
        summary.append(
            f"{meta['label']}: parsed {len(qs)} nums, missing={missing}, expected={meta['count']}"
        )

    (OUT / "_draft_parsed.json").write_text(
        json.dumps(draft, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("\n".join(summary))
    print("wrote", OUT / "_draft_parsed.json")


if __name__ == "__main__":
    main()
