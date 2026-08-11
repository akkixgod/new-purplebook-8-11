#!/usr/bin/env python3
"""Batch OCR purplebook-test-10 page images (left/right panes)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

ROOT = Path("public/mocks/purplebook-test-10/pages")
OUT = Path("public/mocks/purplebook-test-10/ocr")
OUT.mkdir(parents=True, exist_ok=True)

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


def main() -> None:
    results = []
    for i in range(1, 99):
        png = ROOT / f"page-{i:02d}.png"
        img = Image.open(png)
        w, h = img.size
        left = img.crop((int(w * 0.08), int(h * 0.12), int(w * 0.48), int(h * 0.92)))
        right = img.crop((int(w * 0.48), int(h * 0.12), int(w * 0.92), int(h * 0.92)))
        full = img.crop((int(w * 0.08), int(h * 0.12), int(w * 0.92), int(h * 0.92)))

        cfg = "--psm 6"
        left_t = clean(pytesseract.image_to_string(left, config=cfg))
        right_t = clean(pytesseract.image_to_string(right, config=cfg))
        full_t = clean(pytesseract.image_to_string(full, config=cfg))

        rec = {"page": i, "left": left_t, "right": right_t, "full": full_t}
        (OUT / f"page-{i:02d}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (OUT / f"page-{i:02d}.txt").write_text(
            f"===LEFT===\n{left_t}\n\n===RIGHT===\n{right_t}\n\n===FULL===\n{full_t}\n",
            encoding="utf-8",
        )
        results.append(
            {
                "page": i,
                "left_chars": len(left_t),
                "right_chars": len(right_t),
                "full_chars": len(full_t),
            }
        )
        print(f"page {i:02d}: L={len(left_t)} R={len(right_t)} F={len(full_t)}")

    (OUT / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("done", len(results))


if __name__ == "__main__":
    main()
