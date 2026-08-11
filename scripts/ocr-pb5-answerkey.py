#!/usr/bin/env python3
"""
OCR the ElitePractice X5 (May Edition) answer-key page.

Goal: extract the M1/M2 Verbal (English) and M1/M2 Math answers accurately.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_crop(img: Image.Image, box: tuple[float, float, float, float]) -> str:
    w, h = img.size
    x0, y0, x1, y1 = box
    crop = img.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))

    # Preprocess for clearer digits/letters in the small answer-key grid.
    crop = crop.convert("L")
    crop = crop.resize((crop.size[0] * 3, crop.size[1] * 3))
    # Hard threshold helps Tesseract when backgrounds are light/washed.
    crop = crop.point(lambda p: 0 if p < 200 else 255)

    whitelist = "ABCDabcd0123456789()/.+-"
    config = f"--psm 6 -c tessedit_char_whitelist={whitelist}"
    txt = pytesseract.image_to_string(crop, config=config)
    txt = re.sub(r"\s+", " ", txt).strip()
    return txt


def main() -> None:
    img_path = Path("public/mocks/purplebook-test-5/pages/page-100.png")
    img = Image.open(img_path)

    # The answer-key page is laid out as 4 columns across the width:
    # M1 Verbal | M2 Verbal | M1 Math | M2 Math
    columns = [
        ("M1_Verbal", (0.00, 0.05, 0.25, 0.98)),
        ("M2_Verbal", (0.25, 0.05, 0.50, 0.98)),
        ("M1_Math", (0.50, 0.05, 0.75, 0.98)),
        ("M2_Math", (0.75, 0.05, 1.00, 0.98)),
    ]

    print("size", img.size)
    for name, box in columns:
        txt = ocr_crop(img, box)
        print(f"\n== {name} ==")
        print(txt)


if __name__ == "__main__":
    main()

