#!/usr/bin/env python3
"""Parse 2025 Nov Int-A page texts into draft question JSON (hard M2 only)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path("public/mocks/2025-nov-int-a/pages")
OUT = Path("prisma/data/2025-nov-int-a")
OUT.mkdir(parents=True, exist_ok=True)

# Page ranges are 1-indexed inclusive starts from TOC links / section headers.
# We seed Module 1 + hard Module 2 only.
MODULES = {
    # RW M1 Q27 sits on page 14 above the M2-easy header — include page 14, then cut.
    ("ENGLISH", "1"): {"start": 1, "end": 14, "count": 27, "label": "RW M1", "cut_at": "Section: Section 1, Module 2"},
    ("ENGLISH", "2"): {"start": 29, "end": 44, "count": 27, "label": "RW M2 hard"},
    ("MATH", "1"): {"start": 45, "end": 53, "count": 22, "label": "Math M1"},
    ("MATH", "2"): {"start": 62, "end": 72, "count": 22, "label": "Math M2 hard"},
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
    # Drop TOC lines at top of page 1 if still present
    text = re.sub(
        r"^(?:\d+\.\s+Section\s+\d+,.*?\)\s*\n)+",
        "",
        text,
        flags=re.M,
    )
    return text


Q_SPLIT = re.compile(r"(?m)^(?P<n>\d{1,2})\.\s*$")


def split_questions(text: str) -> dict[int, str]:
    text = strip_section_headers(text)
    matches = list(Q_SPLIT.finditer(text))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        n = int(m.group("n"))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        # Prefer first occurrence of each number (avoid false splits)
        if n not in out:
            out[n] = body
    return out


CHOICE_RE = re.compile(r"(?m)^([A-D])\.\s*(.*)$")


def parse_choices(body: str) -> tuple[str, dict[str, str] | dict[str, bool]]:
    """Return (stem_block, choices). Detect grid-in when no A-D choices."""
    lines = body.splitlines()
    choice_idxs = [i for i, ln in enumerate(lines) if CHOICE_RE.match(ln.strip())]
    if not choice_idxs:
        # likely grid-in (math)
        return body.strip(), {"gridIn": True}

    # First A. starts choices; include multi-line choice text until next letter
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
    # Heuristic: if all choices empty-ish and math symbols leaked above, still OK
    if set(choices) != {"A", "B", "C", "D"}:
        return body.strip(), {"gridIn": True}
    return stem, choices


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


def split_prompt_stimulus(stem: str, section: str) -> tuple[str | None, str]:
    """Best-effort: first paragraph(s) that look like the question prompt → text; rest → stimulus."""
    stem = stem.strip()
    if not stem:
        return None, ""

    if section == "MATH":
        # Math: entire stem is usually the question text; figures via imageUrl later
        return None, stem

    lines = stem.splitlines()
    # Prompt often is the first non-empty line(s) before the passage
    # Common pattern: prompt line, then blank, then passage
    first = lines[0].strip() if lines else ""
    if any(first.startswith(h) for h in PROMPT_HINTS) or first.endswith("?"):
        # Keep consecutive prompt lines until a blank line
        prompt_lines = [first]
        i = 1
        while i < len(lines) and lines[i].strip():
            # Stop if this looks like start of a passage (long prose) after a short prompt
            if i >= 1 and len(first) < 120 and len(lines[i].strip()) > 80:
                break
            # Also stop at blank
            prompt_lines.append(lines[i].strip())
            i += 1
        # If we only took one short line, that's the prompt
        if len(prompt_lines) == 1 or (len(prompt_lines) <= 3 and all(len(p) < 160 for p in prompt_lines)):
            text = " ".join(prompt_lines).strip()
            rest = "\n".join(lines[len(prompt_lines) :]).strip()
            # skip leading blank
            while rest.startswith("\n"):
                rest = rest[1:]
            return (rest or None), text

    # Fallback: whole stem is text (no separate stimulus)
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
