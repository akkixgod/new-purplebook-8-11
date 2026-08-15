#!/usr/bin/env python3
"""OCR 2025 August INT V1 page images and extract headers / question numbers."""

from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageOps, ImageFilter
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

ROOT = Path("public/mocks/2025-august-int-v1/pages")
OUT = Path("prisma/data/2025-august-int-v1/_ocr")
OUT.mkdir(parents=True, exist_ok=True)

WATERMARK = re.compile(
    r"@DSATPreps|https?://t\.me/dsatpreps|Mark for Review|\bABC\b|Hide|Highlights.?Notes|"
    r"Calculator|Reference|Directions|More",
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


def ocr(img: Image.Image, psm: int = 6) -> str:
    gray = ImageOps.grayscale(img)
    gray = ImageOps.autocontrast(gray)
    return clean(pytesseract.image_to_string(gray, config=f"--psm {psm}"))


def main() -> None:
    index = []
    for i in range(1, 99):
        png = ROOT / f"page-{i:02d}.png"
        img = Image.open(png)
        w, h = img.size

        header = img.crop((0, 0, w, int(h * 0.14)))
        qbox = img.crop((0, 0, int(min(220, w * 0.18)), int(h * 0.12)))
        # Split vs single-column
        if w > 1800:
            left = img.crop((int(w * 0.01), int(h * 0.12), int(w * 0.495), int(h * 0.98)))
            right = img.crop((int(w * 0.505), int(h * 0.12), int(w * 0.995), int(h * 0.98)))
            full = img.crop((int(w * 0.01), int(h * 0.10), int(w * 0.995), int(h * 0.98)))
        else:
            left = img.crop((int(w * 0.02), int(h * 0.08), int(w * 0.98), int(h * 0.55)))
            right = img.crop((int(w * 0.02), int(h * 0.50), int(w * 0.98), int(h * 0.98)))
            full = img.crop((int(w * 0.02), int(h * 0.06), int(w * 0.98), int(h * 0.98)))

        header_t = ocr(header, 6)
        qbox_t = ocr(qbox, 7)
        left_t = ocr(left, 6)
        right_t = ocr(right, 6)
        full_t = ocr(full, 6)

        rec = {
            "page": i,
            "width": w,
            "height": h,
            "header": header_t,
            "qbox": qbox_t,
            "left": left_t,
            "right": right_t,
            "full": full_t,
        }
        (OUT / f"page-{i:02d}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (OUT / f"page-{i:02d}.txt").write_text(
            f"===HEADER===\n{header_t}\n\n===QBOX===\n{qbox_t}\n\n===LEFT===\n{left_t}\n\n===RIGHT===\n{right_t}\n\n===FULL===\n{full_t}\n",
            encoding="utf-8",
        )
        qn = None
        m = re.search(r"\b(\d{1,2})\b", qbox_t)
        if m:
            qn = int(m.group(1))
        index.append(
            {
                "page": i,
                "w": w,
                "h": h,
                "q": qn,
                "header": header_t.replace("\n", " ")[:120],
            }
        )
        print(f"{i:02d} q={qn} {w}x{h} header={header_t.replace(chr(10), ' ')[:80]}")

    (OUT / "_index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    print("wrote", OUT / "_index.json")


if __name__ == "__main__":
    main()
