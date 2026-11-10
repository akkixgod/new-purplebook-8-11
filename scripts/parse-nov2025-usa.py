#!/usr/bin/env python3
"""Parse 2025 Nov US-A page texts into draft question JSON (single route)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("public/mocks/2025-nov-us-a/pages")
OUT = Path("prisma/data/2025-nov-us-a")
OUT.mkdir(parents=True, exist_ok=True)

MODULES = {
    ("ENGLISH", "1"): {"start": 1, "end": 10, "count": 27, "label": "RW M1"},
    ("ENGLISH", "2"): {"start": 11, "end": 21, "count": 27, "label": "RW M2"},
    ("MATH", "1"): {"start": 22, "end": 24, "count": 22, "label": "Math M1"},
    ("MATH", "2"): {"start": 25, "end": 27, "count": 22, "label": "Math M2"},
}

# US-A uses "1)" style numbering (sometimes with zero-width chars).
Q_SPLIT = re.compile(r"(?m)^[^\S\r\n]*(\d{1,2})\)\s*")
CHOICE_RE = re.compile(r"(?m)^[^\S\r\n]*([A-D])[\.\)]\s*(.*)$")
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
    "The measures",
    "Line ",
    "During ",
)


def clean_zw(text: str) -> str:
    return (
        text.replace("\u200b", "")
        .replace("\u200c", "")
        .replace("\u200d", "")
        .replace("\ufeff", "")
        .replace("\ue12c", "•")
    )


def load_pages(start: int, end: int) -> str:
    chunks = []
    for n in range(start, end + 1):
        p = ROOT / f"page-{n:02d}.txt"
        chunks.append(clean_zw(p.read_text(encoding="utf-8")))
    return "\n".join(chunks)


def strip_headers(text: str) -> str:
    text = re.sub(r"(?m)^Section\s+\d+,\s*Module\s+\d+:.*$", "", text)
    text = re.sub(r"(?m)^November US-A Math M[12].*$", "", text)
    return text


def split_questions(text: str) -> dict[int, str]:
    text = strip_headers(text)
    matches = list(Q_SPLIT.finditer(text))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        n = int(m.group(1))
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
    # US-A often puts passage first, then "Which choice..." at the end
    for i, ln in enumerate(lines):
        s = ln.strip()
        if any(s.startswith(h) for h in PROMPT_HINTS) or (
            s.endswith("?") and len(s) < 160
        ):
            # If this looks like the prompt near the end, stimulus is above
            if i > 0:
                text = " ".join(x.strip() for x in lines[i:] if x.strip())
                stimulus = "\n".join(lines[:i]).strip()
                return (stimulus or None), text
            # Prompt first (less common)
            prompt_lines = [s]
            j = i + 1
            while j < len(lines) and lines[j].strip() and len(lines[j].strip()) < 120:
                prompt_lines.append(lines[j].strip())
                j += 1
            text = " ".join(prompt_lines)
            rest = "\n".join(lines[j:]).strip()
            return (rest or None), text
    return None, stem


def main() -> None:
    draft: dict = {"ENGLISH": {}, "MATH": {}}
    summary = []
    for (section, mod), meta in MODULES.items():
        raw = load_pages(meta["start"], meta["end"])
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
            # Prefer passage-first layout for English: if stimulus empty but text long, swap heuristics already handled
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
