#!/usr/bin/env python3
"""Crop figure regions from rendered mock pages into public/mocks/<slug>/figures/."""

from __future__ import annotations

from pathlib import Path

try:
    from PIL import Image
except ImportError:
    import subprocess, sys

    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image

ROOT = Path("public/mocks/2026-march-int-b")
PAGES = ROOT / "pages"
FIGS = ROOT / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# Crop boxes are (left, top, right, bottom) on the 2x rendered PNGs (1191 x 1684)
CROPS: dict[str, tuple[int, int, int, int]] = {
    # Math M1 Q1 — candle weight graph only
    "math1-q01-graph.png": (250, 430, 940, 900),
    # Math M1 Q21 — triangle FGH
    "math1-q21-triangle.png": (320, 620, 880, 1120),
    # Math M2 Q7 — choice A graph on page 26 (will also stitch page 27)
    "math2-q07-choice-a.png": (80, 1180, 700, 1620),
    # Math M2 Q15 — scatterplot
    "math2-q15-scatter.png": (280, 520, 920, 1080),
    # English tables/graphs
    "eng1-q10-table.png": (280, 120, 920, 520),
    "eng2-q11-table.png": (300, 80, 900, 480),
    "eng2-q13-graph.png": (220, 80, 980, 620),
}

# source page for each crop
SOURCES: dict[str, str] = {
    "math1-q01-graph.png": "page-20.png",
    "math1-q21-triangle.png": "page-24.png",
    "math2-q07-choice-a.png": "page-26.png",
    "math2-q15-scatter.png": "page-29.png",
    "eng1-q10-table.png": "page-04.png",
    "eng2-q11-table.png": "page-13.png",
    "eng2-q13-graph.png": "page-15.png",
}


def crop_one(name: str, box: tuple[int, int, int, int]) -> Path:
    src = PAGES / SOURCES[name]
    im = Image.open(src)
    w, h = im.size
    l, t, r, b = box
    l, t = max(0, l), max(0, t)
    r, b = min(w, r), min(h, b)
    out = FIGS / name
    im.crop((l, t, r, b)).save(out)
    print(f"wrote {out} ({r - l}x{b - t}) from {src.name}")
    return out


def crop_math2_q7_all() -> Path:
    """Build a vertical strip of choice graphs A–D for inequality Q7."""
    p26 = Image.open(PAGES / "page-26.png")
    p27 = Image.open(PAGES / "page-27.png")
    # A is bottom of page 26; B/C/D are on page 27 — rough full-width middle crops
    a = p26.crop((60, 1150, 720, 1640))
    # page 27 typically has B, C, D stacked — take a wide middle band and let layout show labels
    bcd = p27.crop((60, 80, 1100, 1500))
    # stitch A on top of BCD
    w = max(a.width, bcd.width)
    h = a.height + bcd.height + 12
    canvas = Image.new("RGB", (w, h), (255, 255, 255))
    canvas.paste(a, (0, 0))
    canvas.paste(bcd, (0, a.height + 12))
    out = FIGS / "math2-q07-choices.png"
    canvas.save(out)
    print(f"wrote {out} ({w}x{h})")
    return out


def main() -> None:
    for name, box in CROPS.items():
        if name == "math2-q07-choice-a.png":
            continue  # replaced by combined strip
        crop_one(name, box)
    crop_math2_q7_all()


if __name__ == "__main__":
    main()
