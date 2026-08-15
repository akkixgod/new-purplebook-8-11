#!/usr/bin/env python3
"""Extract green-highlighted answer keys by classifying cropped choice letters."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PAGES = Path("public/mocks/2025-august-us-v2/pages")
OUT = Path("prisma/data/2025-august-us-v2")
CROPS = OUT / "_green_crops"
OUT.mkdir(parents=True, exist_ok=True)
CROPS.mkdir(parents=True, exist_ok=True)


def green_mask(a: np.ndarray) -> np.ndarray:
    r = a[:, :, 0].astype(np.int16)
    g = a[:, :, 1].astype(np.int16)
    b = a[:, :, 2].astype(np.int16)
    return (g > 130) & (g > r + 20) & (g > b + 10) & (r < 210) & (b < 200)


def extract_prefix_ink(crop: Image.Image) -> np.ndarray:
    a = np.asarray(crop.convert("RGB"))
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    ink = (r + g + b) < 540
    w = ink.shape[1]
    left = ink[:, : min(w, 100)]
    ys = np.where(left.any(axis=1))[0]
    xs = np.where(left.any(axis=0))[0]
    if len(ys) == 0 or len(xs) == 0:
        return np.zeros((20, 20), dtype=bool)
    return left[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]


def render_letter(letter: str, size=(80, 56)) -> np.ndarray:
    im = Image.new("L", size, 255)
    d = ImageDraw.Draw(im)
    font = None
    for name in ("arial.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/calibri.ttf"):
        try:
            font = ImageFont.truetype(name, 40)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()
    d.text((6, 2), f"{letter})", fill=0, font=font)
    arr = np.asarray(im) < 128
    ys = np.where(arr.any(axis=1))[0]
    xs = np.where(arr.any(axis=0))[0]
    return arr[ys.min() : ys.max() + 1, xs.min() : xs.max() + 1]


def resize_bool(m: np.ndarray, th: int, tw: int) -> np.ndarray:
    im = Image.fromarray((m.astype(np.uint8) * 255))
    im = im.resize((tw, th), Image.NEAREST)
    return np.asarray(im) > 127


def iou(a: np.ndarray, b: np.ndarray) -> float:
    h = max(a.shape[0], b.shape[0])
    w = max(a.shape[1], b.shape[1])
    a2 = resize_bool(a, h, w)
    b2 = resize_bool(b, h, w)
    inter = (a2 & b2).sum()
    union = (a2 | b2).sum()
    return float(inter / union) if union else 0.0


TEMPLATES = {L: render_letter(L) for L in "ABCD"}


def classify_crop(crop: Image.Image) -> tuple[str, dict]:
    ink = extract_prefix_ink(crop)
    scores = {L: iou(ink, t) for L, t in TEMPLATES.items()}
    best = max(scores, key=scores.get)
    return best, scores


def green_crops_for_page(path: Path) -> list[tuple[str, Image.Image, float]]:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    m = green_mask(a)
    if not m.any():
        return []
    h, w = m.shape
    mid = w // 2
    out = []
    for side, x0, x1 in (("L", 0, mid), ("R", mid, w)):
        region = m[:, x0:x1]
        if not region.any():
            continue
        ys, xs = np.where(region)
        y0, y1 = int(ys.min()), int(ys.max())
        xx0, xx1 = int(xs.min() + x0), int(xs.max() + x0)
        # Keep only reasonably tall choice highlights (skip thin noise)
        if (y1 - y0) < 20 or (xx1 - xx0) < 80:
            continue
        xx0 = max(x0, xx0 - 50)
        crop = im.crop((xx0, max(0, y0 - 4), min(w, xx1 + 4), min(h, y1 + 4)))
        y_frac = ((y0 + y1) / 2) / h
        out.append((side, crop, y_frac))
    return out


def parse_qnums(txt: str) -> list[int]:
    return [int(x) for x in re.findall(r"(?m)^Question\s+(\d+)\s*$", txt)]


def main() -> None:
    keys_by_page: dict[str, list[dict]] = {}
    flat: dict[str, str] = {}

    for i in range(1, 77):
        png = PAGES / f"page-{i:02d}.png"
        txtp = PAGES / f"page-{i:02d}.txt"
        if not png.exists():
            continue
        qnums = parse_qnums(txtp.read_text(encoding="utf-8", errors="replace")) if txtp.exists() else []
        crops = green_crops_for_page(png)
        # Map L->first q, R->second q when two-up
        page_keys = []
        for side, crop, yf in crops:
            letter, scores = classify_crop(crop)
            q = None
            if side == "L" and len(qnums) >= 1:
                q = qnums[0]
            elif side == "R" and len(qnums) >= 2:
                q = qnums[1]
            elif len(qnums) == 1:
                q = qnums[0]
            crop_path = CROPS / f"p{i:02d}_{side}_Q{q or 'x'}.png"
            crop.save(crop_path)
            rec = {
                "page": i,
                "side": side,
                "q": q,
                "letter": letter,
                "scores": {k: round(v, 3) for k, v in scores.items()},
                "crop": str(crop_path).replace("\\", "/"),
            }
            page_keys.append(rec)
            if q is not None:
                # module context later; store as page-q for now
                flat[f"p{i:02d}-Q{q}"] = letter
            print(f"page {i:02d} {side} Q{q} -> {letter} {rec['scores']}")
        keys_by_page[str(i)] = page_keys

    (OUT / "_answer_keys_green.json").write_text(
        json.dumps({"byPage": keys_by_page, "flat": flat}, indent=2), encoding="utf-8"
    )
    print("wrote", OUT / "_answer_keys_green.json")


if __name__ == "__main__":
    main()
