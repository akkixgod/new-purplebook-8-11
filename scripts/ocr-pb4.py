#!/usr/bin/env python3
"""
Batch OCR purplebook-test-4 page images (left/right/full panes).

This PDF often has no extractable text, so we rely on OCR to transcribe
question content and answer keys.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


WATERMARK = re.compile(
    r"El[ijl]+an\s*Ahm[a-z]*|EliteXSAT|Azerba[ij]an|Made in|"
    r"INDEPENDENCE|28 MAY|AZERBAIJAN|1918|Mark for Review|\bABC\b",
    re.I,
)


def clean(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            lines.append("")
            continue
        if WATERMARK.search(s) and len(WATERMARK.sub("", s).strip()) < 8:
            continue
        s = WATERMARK.sub(" ", s)
        s = re.sub(r"\s{2,}", " ", s).strip()
        if s:
            lines.append(s)
    # collapse repeated empties
    out: list[str] = []
    blank = 0
    for ln in lines:
        if not ln:
            blank += 1
            if blank <= 1:
                out.append("")
        else:
            blank = 0
            out.append(ln)
    return "\n".join(out).strip()


def ocr_page(png: Path) -> dict:
    img = Image.open(png)
    w, h = img.size

    # Heuristic based on ElitePractice page layouts: crop left/right halves.
    left = img.crop((int(w * 0.08), int(h * 0.12), int(w * 0.48), int(h * 0.92)))
    right = img.crop((int(w * 0.48), int(h * 0.12), int(w * 0.92), int(h * 0.92)))
    full = img.crop((int(w * 0.08), int(h * 0.12), int(w * 0.92), int(h * 0.92)))

    cfg = "--psm 6"
    left_t = clean(pytesseract.image_to_string(left, config=cfg))
    right_t = clean(pytesseract.image_to_string(right, config=cfg))
    full_t = clean(pytesseract.image_to_string(full, config=cfg))

    return {
        "left": left_t,
        "right": right_t,
        "full": full_t,
        "left_chars": len(left_t),
        "right_chars": len(right_t),
        "full_chars": len(full_t),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=99)
    ap.add_argument("--root", default="public/mocks/purplebook-test-4/pages")
    ap.add_argument("--out", default="public/mocks/purplebook-test-4/ocr")
    args = ap.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    results = []
    for i in range(args.start, args.end + 1):
        png = root / f"page-{i:02d}.png"
        if not png.exists():
            print("skip missing", png)
            continue

        rec = ocr_page(png)
        (out / f"page-{i:02d}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (out / f"page-{i:02d}.txt").write_text(
            f"===LEFT===\n{rec['left']}\n\n===RIGHT===\n{rec['right']}\n\n===FULL===\n{rec['full']}\n",
            encoding="utf-8",
        )
        results.append(
            {"page": i, "left_chars": rec["left_chars"], "right_chars": rec["right_chars"], "full_chars": rec["full_chars"]}
        )
        print(f"OCR page {i:02d}: full_chars={rec['full_chars']}")

    (out / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("done", len(results), "pages")


if __name__ == "__main__":
    main()

