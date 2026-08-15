#!/usr/bin/env python3
"""Crop highlighted MC answers for 2025-august-us-v3 pages."""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

PAGES = Path("public/mocks/2025-august-us-v3/pages")
OUT = Path("prisma/data/2025-august-us-v3")
CROPS = OUT / "_key_crops"
OUT.mkdir(parents=True, exist_ok=True)
CROPS.mkdir(parents=True, exist_ok=True)


def highlight_mask(a: np.ndarray) -> np.ndarray:
    """Blue/teal/green answer borders used in DSATPreps keys."""
    r = a[:, :, 0].astype(np.int16)
    g = a[:, :, 1].astype(np.int16)
    b = a[:, :, 2].astype(np.int16)
    green = (g > 130) & (g > r + 20) & (g > b + 10) & (r < 210)
    # teal/blue borders
    teal = (b > 120) & (g > 100) & (b > r + 15) & (g > r + 5) & (r < 180)
    return green | teal


def crops_for_page(path: Path) -> list[Image.Image]:
    im = Image.open(path).convert("RGB")
    a = np.asarray(im)
    m = highlight_mask(a)
    if not m.any():
        return []
    h, w = m.shape
    ys, xs = np.where(m)
    # cluster by y into bands
    order = np.argsort(ys)
    ys, xs = ys[order], xs[order]
    bands: list[list[tuple[int, int]]] = []
    cur: list[tuple[int, int]] = [(int(ys[0]), int(xs[0]))]
    for i in range(1, len(ys)):
        if ys[i] - cur[-1][0] > 40:
            bands.append(cur)
            cur = [(int(ys[i]), int(xs[i]))]
        else:
            cur.append((int(ys[i]), int(xs[i])))
    bands.append(cur)
    out = []
    for band in bands:
        by = [p[0] for p in band]
        bx = [p[1] for p in band]
        y0, y1 = min(by), max(by)
        x0, x1 = min(bx), max(bx)
        if (y1 - y0) < 18 or (x1 - x0) < 60:
            continue
        x0 = max(0, x0 - 40)
        crop = im.crop((x0, max(0, y0 - 4), min(w, x1 + 8), min(h, y1 + 4)))
        out.append(crop)
    return out[:2]


def main() -> None:
    meta = []
    for i in range(1, 104):
        png = PAGES / f"page-{i:02d}.png"
        if not png.exists():
            continue
        crops = crops_for_page(png)
        for j, crop in enumerate(crops):
            path = CROPS / f"p{i:02d}_{j}.png"
            crop.save(path)
            meta.append({"page": i, "i": j, "path": str(path).replace("\\", "/")})
            print(f"page {i:03d} crop {j} size={crop.size}")
    (OUT / "_key_crops_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    # contact sheet
    if not meta:
        print("no crops")
        return
    cols = 6
    cell_w, cell_h = 340, 70
    rows = (len(meta) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
    for idx, rec in enumerate(meta):
        r, c = divmod(idx, cols)
        x, y = c * cell_w, r * cell_h
        crop = Image.open(rec["path"]).convert("RGB")
        crop = crop.resize((320, 48))
        sheet.paste(crop, (x + 5, y + 16))
        draw.text((x + 2, y + 1), f"p{rec['page']:02d}", fill=(0, 0, 0), font=font)
    sheet.save(OUT / "_keys_contact.png")
    print("wrote", OUT / "_keys_contact.png", "crops", len(meta))


if __name__ == "__main__":
    main()
