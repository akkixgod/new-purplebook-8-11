#!/usr/bin/env python3
"""Detect green-highlighted MC answers on 2025-august-us-v2 page PNGs."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

PAGES = Path("public/mocks/2025-august-us-v2/pages")
OUT = Path("prisma/data/2025-august-us-v2")
OUT.mkdir(parents=True, exist_ok=True)


def green_mask(a: np.ndarray) -> np.ndarray:
    r = a[:, :, 0].astype(np.int16)
    g = a[:, :, 1].astype(np.int16)
    b = a[:, :, 2].astype(np.int16)
    return (g > 130) & (g > r + 20) & (g > b + 10) & (r < 210) & (b < 200)


def choice_letter_near(im: Image.Image, cy: int, cx: int) -> str | None:
    """OCR-free: look left of green blob for A)/B)/C)/D) via dark ink clusters vs crop text."""
    # Fallback: parse from page text by y-order is better — here return None
    return None


def green_centers(path: Path) -> list[tuple[float, float, int]]:
    """Return list of (cx_frac, cy_frac, pixel_count) for green blobs."""
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    m = green_mask(a)
    if not m.any():
        return []
    h, w = m.shape
    # Connected components via crude flood on downsampled mask
    step = 4
    md = m[::step, ::step]
    visited = np.zeros_like(md, dtype=bool)
    blobs = []
    hs, ws = md.shape
    for y in range(hs):
        for x in range(ws):
            if not md[y, x] or visited[y, x]:
                continue
            stack = [(y, x)]
            visited[y, x] = True
            cells = []
            while stack:
                cy, cx = stack.pop()
                cells.append((cy, cx))
                for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < hs and 0 <= nx < ws and md[ny, nx] and not visited[ny, nx]:
                        visited[ny, nx] = True
                        stack.append((ny, nx))
            if len(cells) < 8:
                continue
            ys = [c[0] for c in cells]
            xs = [c[1] for c in cells]
            cy = (sum(ys) / len(ys)) * step
            cx = (sum(xs) / len(xs)) * step
            blobs.append((cx / w, cy / h, len(cells)))
    # Keep largest blobs (choice highlights), drop tiny watermark noise
    blobs.sort(key=lambda t: -t[2])
    return blobs[:6]


def parse_questions_from_txt(txt: str) -> list[dict]:
    txt = txt.replace("\r\n", "\n").replace("\ufeff", "")
    # Strip footer noise
    lines = []
    for line in txt.split("\n"):
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if "t.me/dsatpreps" in s.lower() or s.lower() == "@dsatpreps":
            continue
        if s.lower().startswith("exam questions"):
            continue
        if re.match(r"^section\s+\d", s, re.I):
            continue
        lines.append(s)
    body = "\n".join(lines)
    parts = re.split(r"(?m)^Question\s+(\d+)\s*$", body)
    # parts: preamble, num, content, num, content, ...
    qs = []
    for i in range(1, len(parts), 2):
        num = parts[i]
        content = parts[i + 1].strip()
        # Split choices
        m = re.search(r"(?m)^A\)\s*", content)
        if not m:
            qs.append({"n": int(num), "raw": content, "choices": None})
            continue
        stem = content[: m.start()].strip()
        choice_blob = content[m.start() :].strip()
        # Remove Module 2 header bleed
        choice_blob = re.split(r"(?m)^Section\s+\d|^Module\s+\d", choice_blob)[0].strip()
        choices = {}
        cm = list(re.finditer(r"(?m)^([A-D])\)\s*", choice_blob))
        for j, match in enumerate(cm):
            letter = match.group(1)
            start = match.end()
            end = cm[j + 1].start() if j + 1 < len(cm) else len(choice_blob)
            choices[letter] = re.sub(r"\s+", " ", choice_blob[start:end]).strip()
        # Prompt detection
        prompt_pats = [
            r"Which choice completes the text with the most logical and precise word or phrase\?",
            r"Which choice most logically completes the text\?",
            r"As used in the text, what does the (?:underlined )?word .+? most nearly mean\?",
            r"Which choice best (?:states|describes|describes the function|completes).+\?",
            r"Based on the text, .+\?",
            r"Which quotation .+\?",
            r"Which finding .+\?",
            r"Which choice best describes .+\?",
            r"The student wants .+\?",
            r"Which choice completes .+\?",
        ]
        text = None
        stimulus = stem
        for pat in prompt_pats:
            pm = re.search(pat, stem, re.I | re.S)
            if pm:
                text = re.sub(r"\s+", " ", pm.group(0)).strip()
                stimulus = stem[: pm.start()].strip()
                break
        if text is None:
            # last sentence as prompt heuristic
            bits = re.split(r"(?<=\?)\s*", stem)
            if len(bits) >= 2 and bits[-2].strip().endswith("?"):
                text = re.sub(r"\s+", " ", bits[-2]).strip()
                stimulus = " ".join(bits[:-2]).strip()
            else:
                text = re.sub(r"\s+", " ", stem).strip()
                stimulus = None
        stimulus = stimulus.replace("______blank", "______") if stimulus else None
        if stimulus:
            stimulus = re.sub(r"\s+", " ", stimulus).strip()
            if stimulus == "":
                stimulus = None
        qs.append(
            {
                "n": int(num),
                "stimulus": stimulus,
                "text": text,
                "choices": choices if choices else {"gridIn": True},
            }
        )
    return qs


def letter_from_y_frac(cy: float, choice_ys: list[tuple[str, float]]) -> str | None:
    if not choice_ys:
        return None
    best = min(choice_ys, key=lambda t: abs(t[1] - cy))
    if abs(best[1] - cy) > 0.08:
        return None
    return best[0]


def main() -> None:
    report = {}
    for i in range(1, 77):
        png = PAGES / f"page-{i:02d}.png"
        txtp = PAGES / f"page-{i:02d}.txt"
        if not png.exists():
            continue
        blobs = green_centers(png)
        qs = parse_questions_from_txt(txtp.read_text(encoding="utf-8", errors="replace")) if txtp.exists() else []
        # Map green blobs to left/right questions by x fraction
        left = [b for b in blobs if b[0] < 0.5]
        right = [b for b in blobs if b[0] >= 0.5]
        page_info = {"questions": qs, "greens": []}
        # For each side, pick largest green and guess letter by relative y among A-D block
        # Heuristic: within a question column, A/B/C/D are evenly spaced near bottom
        for side, side_blobs, qidx in (("L", left, 0), ("R", right, 1)):
            if not side_blobs or qidx >= len(qs):
                continue
            cx, cy, cnt = side_blobs[0]
            # Estimate letter from cy within typical choice band — read choice text order
            # Better approach: crop vertical strip and find which choice row has most green
            im = Image.open(png).convert("RGB")
            a = np.asarray(im)
            m = green_mask(a)
            h, w = m.shape
            x0, x1 = (0, w // 2) if side == "L" else (w // 2, w)
            # Find green y centroid
            region = m[:, x0:x1]
            if not region.any():
                continue
            ys = np.where(region.any(axis=1))[0]
            y_cent = float(ys.mean()) / h
            # Split choice area into 4 bands using A) positions from text length — use bottom 45% of page
            # Relative position of green within lower half:
            lo, hi = 0.45, 0.95
            t = (y_cent - lo) / (hi - lo)
            t = max(0.0, min(0.999, t))
            letter = "ABCD"[int(t * 4)]
            # Refine: among green rows, check density per quartile of choice block
            # Use actual green row cluster relative to all green in column — single highlight
            page_info["greens"].append(
                {
                    "side": side,
                    "q": qs[qidx]["n"] if qidx < len(qs) else None,
                    "y_frac": round(y_cent, 4),
                    "guess": letter,
                    "px": int(cnt),
                }
            )
        report[str(i)] = page_info
        guesses = ",".join(f"{g['q']}={g['guess']}" for g in page_info["greens"])
        print(f"page {i:02d}: qs={[q['n'] for q in qs]} greens={guesses}")

    (OUT / "_green_scan.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("wrote", OUT / "_green_scan.json")


if __name__ == "__main__":
    main()
